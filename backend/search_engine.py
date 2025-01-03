import json
from typing import List, Dict
import numpy as np
from gensim.models import Word2Vec
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from sentence_transformers import SentenceTransformer
import jieba
from collections import defaultdict
import requests
import io
from chromadb import PersistentClient

class RecipeSearchEngine:
    def __init__(self, data_path: str, image_vector_reload = False):
        # 載入食譜資料
        with open(data_path, "r", encoding='utf-8') as f:
            data = json.load(f)
            # 過濾重複的id
            self.data = list({d['id']: d for d in data}.values())

        # 初始化模型
        self.sentence_model = SentenceTransformer(
            'paraphrase-multilingual-MiniLM-L12-v2')
        self.clip_model = CLIPModel.from_pretrained(
            "openai/clip-vit-base-patch32")
        self.clip_processor = CLIPProcessor.from_pretrained(
            "./model")
        
        # 初始化 ChromaDB，啟用持久化存儲
        self.client = PersistentClient()
        self.collection = self.client.get_or_create_collection("recipe_image_vectors")

        # 初始化食材向量化
        self.ingredient_tokenizer = jieba.Tokenizer()
        # 加入常見的食材單位到停用詞
        self.units = {'克', '公克', 'g', '條', '片', '個', '顆', '些', '適量',
                      '份', '兩', '斤', '匙', '湯匙', '茶匙', '杯', 'ml', '毫升', '公升', '把'}

        # 預處理所有食譜文字
        self.preprocess_recipe_texts()

        # 預處理所有圖片
        if image_vector_reload: self.precompute_image_vectors()
     
        # 初始化食材向量化
        self.initialize_ingredients()
    
    def _fetch_image(self, url: str) -> io.BytesIO:
        """
            从给定的URL下载图片并显示。

            参数:
            url (str): 图片的URL地址
         """
        response = requests.get(url)
        return io.BytesIO(response.content)


    def preprocess_recipe_texts(self):
        """預處理所有食譜文字,建立文本嵌入"""
        texts = []
        # 確保所有必要欄位都有值
        for recipe in self.data:
            # 處理可能為 None 的欄位
            recipe['name'] = recipe.get('name', '') or ''
            recipe['description'] = recipe.get('description', '') or ''
            recipe['hashtags'] = recipe.get('hashtags', []) or []

            # 組合食譜名稱、描述和標籤
            text_parts = [
                recipe['name'],
                recipe['description']
            ]
            text_parts.extend(recipe['hashtags'])

            texts.append(' '.join(text_parts))

        # 使用 sentence-transformer 產生文本嵌入
        self.text_embeddings = self.sentence_model.encode(texts)
    
    def precompute_image_vectors(self):
        """將所有圖片轉為向量並存儲到 ChromaDB"""
        for recipe in self.data:
            if recipe.get("image"):
                try:
                    image = Image.open(self._fetch_image(recipe["image"]))
                    inputs = self.clip_processor(images=image, return_tensors="pt")
                    image_features = self.clip_model.get_image_features(**inputs).detach().numpy()
                    
                    # 將向量存儲到 ChromaDB 中
                    self.collection.add(
                        ids=[recipe["id"]],
                        embeddings=image_features.tolist(),
                        metadatas=[{"name": recipe["name"], "description": recipe["description"]}]
                    )
                except Exception as e:
                    print(f"Error processing image for recipe {recipe['id']}: {e}")

    def clean_ingredient_name(self, name: str) -> str:
        """清理食材名稱，移除單位詞"""
        if not name:
            return ""
        tokens = list(self.ingredient_tokenizer.cut(name))
        return "".join([t for t in tokens if t not in self.units])

    def initialize_ingredients(self):
        """初始化並訓練食材的Word2Vec模型"""
        # 收集所有食材列表
        all_ingredients = []
        self.ingredient_to_recipes = defaultdict(list)
        self.recipe_ingredients = {}  # 儲存每個食譜的原始食材資訊

        for recipe in self.data:
            if 'ingredients' in recipe and recipe['ingredients']:
                # 儲存原始食材資訊
                self.recipe_ingredients[recipe['id']] = recipe['ingredients']

                # 處理食材名稱
                recipe_ingredients = []
                for ing in recipe['ingredients']:
                    if ing.get('name'):
                        clean_name = self.clean_ingredient_name(ing['name'])
                        if clean_name:
                            tokens = list(
                                self.ingredient_tokenizer.cut(clean_name))
                            recipe_ingredients.extend(tokens)
                            # 建立食材到食譜的映射
                            for token in tokens:
                                self.ingredient_to_recipes[token].append({
                                    'recipe_id': recipe['id'],
                                    'amount': ing.get('amount', '適量')
                                })

                if recipe_ingredients:
                    all_ingredients.append(recipe_ingredients)

        # 訓練Word2Vec模型
        self.ingredient_model = Word2Vec(
            sentences=all_ingredients,
            vector_size=100,
            window=5,
            min_count=1,
            workers=4
        )

        # 預計算所有食譜的食材向量
        self.recipe_ingredient_vectors = {}
        for recipe in self.data:
            if 'ingredients' in recipe and recipe['ingredients']:
                vectors = []
                for ing in recipe['ingredients']:
                    if ing.get('name'):
                        clean_name = self.clean_ingredient_name(ing['name'])
                        if clean_name:
                            tokens = list(
                                self.ingredient_tokenizer.cut(clean_name))
                            # 取每個食材詞的平均向量
                            token_vectors = []
                            for token in tokens:
                                if token in self.ingredient_model.wv:
                                    token_vectors.append(
                                        self.ingredient_model.wv[token])
                            if token_vectors:
                                vectors.append(np.mean(token_vectors, axis=0))

                if vectors:
                    self.recipe_ingredient_vectors[recipe['id']] = np.mean(
                        vectors, axis=0)

    def get_similar_ingredients(self, ingredient: str, top_k: int = 5) -> List[Dict]:
        """找出相似的食材，並返回使用這些食材的食譜"""
        clean_ing = self.clean_ingredient_name(ingredient)
        tokens = list(self.ingredient_tokenizer.cut(clean_ing))
        similar_ingredients = []

        for token in tokens:
            if token in self.ingredient_model.wv:
                # 找出相似的食材詞
                similar = self.ingredient_model.wv.most_similar(
                    token, topn=top_k)
                for word, score in similar:
                    # 找出使用該食材的食譜
                    # 只取前5個食譜
                    recipe_refs = self.ingredient_to_recipes[word][:5]
                    recipes = []
                    for ref in recipe_refs:
                        recipe = next(
                            (r for r in self.data if r['id'] == ref['recipe_id']), None)
                        if recipe:
                            recipes.append({
                                'id': recipe['id'],
                                'name': recipe['name'],
                                'amount': ref['amount']
                            })

                    similar_ingredients.append({
                        'ingredient': word,
                        'similarity': float(score),
                        'recipes': recipes
                    })

        return similar_ingredients

    def ingredient_based_search(self, ingredients: List[str], top_k: int = 10) -> List[dict]:
        """基於食材相似度的搜尋"""
        query_vectors = []

        # 計算查詢食材的平均向量
        for ing in ingredients:
            clean_ing = self.clean_ingredient_name(ing)
            tokens = list(self.ingredient_tokenizer.cut(clean_ing))
            token_vectors = []
            for token in tokens:
                if token in self.ingredient_model.wv:
                    token_vectors.append(self.ingredient_model.wv[token])
            if token_vectors:
                query_vectors.append(np.mean(token_vectors, axis=0))

        if not query_vectors:
            return []

        query_vector = np.mean(query_vectors, axis=0)

        # 計算與所有食譜的相似度
        similarities = []
        for recipe_id, recipe_vector in self.recipe_ingredient_vectors.items():
            similarity = float(np.dot(query_vector, recipe_vector) /
                               (np.linalg.norm(query_vector) * np.linalg.norm(recipe_vector)))
            # 取得該食譜的完整資訊
            recipe = next(r for r in self.data if r['id'] == recipe_id)
            # 計算食材匹配度
            matching_ingredients = []
            for ing in recipe.get('ingredients', []):
                if any(q_ing in ing.get('name', '') for q_ing in ingredients):
                    matching_ingredients.append(ing)

            similarities.append({
                **recipe,
                'similarity': similarity,
                'matching_ingredients': matching_ingredients,
                'total_ingredients': len(recipe.get('ingredients', []))
            })

        # 排序並返回結果
        similarities.sort(key=lambda x: (
            len(x['matching_ingredients']), x['similarity']), reverse=True)
        return similarities[:top_k]

    def text_search(self, query: str, top_k: int = 10) -> List[dict]:
        """基於文字相似度的搜尋"""
        if not query:
            return []

        # 對查詢文字進行編碼
        query_embedding = self.sentence_model.encode([query])[0]

        # 計算相似度
        similarities = np.dot(self.text_embeddings, query_embedding)
        top_indices = np.argsort(similarities)[-top_k:][::-1]

        # 回傳最相關的食譜
        results = []
        for idx in top_indices:
            recipe = self.data[idx].copy()
            recipe['similarity_score'] = float(similarities[idx])
            # 標註匹配到的部分
            recipe['matched_parts'] = []

            # 確保所有字串比較都是安全的
            recipe_name = str(recipe.get('name', ''))
            recipe_description = str(recipe.get('description', ''))
            recipe_hashtags = list(recipe.get('hashtags', []))

            if query in recipe_name:
                recipe['matched_parts'].append('name')
            if query in recipe_description:
                recipe['matched_parts'].append('description')
            if any(query in str(tag) for tag in recipe_hashtags):
                recipe['matched_parts'].append('hashtags')

            # 確保回傳的資料格式正確
            result = {
                'id': recipe.get('id', ''),
                'name': recipe_name,
                'description': recipe_description,
                'image': recipe.get('image', ''),
                'duration': recipe.get('duration', ''),
                'servings': recipe.get('servings', ''),
                'hashtags': recipe_hashtags,
                'ingredients': recipe.get('ingredients', []),
                'steps': recipe.get('steps', []),
                'similarity_score': recipe['similarity_score'],
                'matched_parts': recipe['matched_parts']
            }
            results.append(result)

        return results

    def image_search(self, image: Image.Image, top_k: int = 10) -> List[dict]:
        """基於圖片相似度的搜尋"""
        # 處理輸入圖片
        inputs = self.clip_processor(images=image, return_tensors="pt")
        image_features = self.clip_model.get_image_features(**inputs).detach().numpy()

        # 使用 ChromaDB 搜尋相似向量
        results = self.collection.query(
            query_embeddings=image_features.tolist(),
            n_results=top_k
        )

        ids = results.get("ids")[0]
        distances = results.get("distances")[0]
        id_distance = {id:distance for id, distance in zip(ids, distances)}

        search_results = []
        for recipe in self.data:
            if recipe["id"] in ids:
                search_results.append({**recipe,"distance":id_distance[recipe["id"]]})
        
        search_results = sorted(search_results, key=lambda x : x["distance"])

        return search_results