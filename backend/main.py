import json
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Union
import torch
import torch.nn.functional as F
import clip
from PIL import Image
from io import BytesIO

# 載入食譜資料
with open("./icook_recipe/recipe_data.json", "r", encoding='utf-8') as f:
    DATA = json.load(f)


class RecipeSearchEngine:
    def __init__(self, model_name: str = "ViT-B/32"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        self.model, self.preprocess = clip.load(model_name, device=self.device)
        self.recipe_embeddings = self._compute_recipe_embeddings()

    def _compute_recipe_embeddings(self) -> torch.Tensor:
        # 準備所有食譜的文本
        all_texts = []
        for recipe in DATA:
            # 只保留最重要的信息
            name = recipe.get('name', '').strip()
            # 取前三個主要食材
            main_ingredients = []
            for ing in recipe.get('ingredients', [])[:3]:
                ing_name = ing.get('name', '')
                if ing_name:
                    main_ingredients.append(ing_name)
            # 取前三個標籤
            main_tags = []
            for tag in recipe.get('hashtags', [])[:3]:
                if tag:
                    main_tags.append(tag)

            # 組合文本
            text = f"{name} {' '.join(main_ingredients)} {' '.join(main_tags)}"
            all_texts.append(text)

        all_features = []

        for i in range(0, len(all_texts)):
            text = all_texts[i]

            # text to vector by clip (如果text長度太長就截斷)
            text_tokens = clip.tokenize(text, truncate=True).to(self.device)
            with torch.no_grad():
                features = self.model.encode_text(text_tokens)
                features = F.normalize(features, dim=1)
                all_features.append(features)
 

        # 檢查是否有有效的特徵
        if not all_features:
            raise RuntimeError("無法生成任何有效的特徵")

        # 合併所有特徵
        return torch.cat(all_features, dim=0)

    def _process_image(self, image_data: Union[bytes, Image.Image]) -> torch.Tensor:
        if isinstance(image_data, bytes):
            image = Image.open(BytesIO(image_data))
        else:
            image = image_data

        image_input = self.preprocess(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            image_features = self.model.encode_image(image_input)
            image_features = F.normalize(image_features, dim=1)
        return image_features

    def search_by_text_clip(self, query: str, top_k: int = 10) -> List[Dict]:
        text_tokens = clip.tokenize([query]).to(self.device)
        with torch.no_grad():
            text_features = self.model.encode_text(text_tokens)
            text_features = F.normalize(text_features, dim=1)

        similarity = torch.cosine_similarity(
            text_features, self.recipe_embeddings)
        top_indices = similarity.topk(
            min(top_k, len(DATA))).indices.cpu().numpy()

        return [
            {**DATA[idx], 'similarity_score': float(similarity[idx])}
            for idx in top_indices
        ]

    def search_by_image(self, image_data: Union[bytes, Image.Image], top_k: int = 10) -> List[Dict]:
        image_features = self._process_image(image_data)
        similarity = torch.cosine_similarity(
            image_features, self.recipe_embeddings)
        top_indices = similarity.topk(
            min(top_k, len(DATA))).indices.cpu().numpy()

        return [
            {**DATA[idx], 'similarity_score': float(similarity[idx])}
            for idx in top_indices
        ]


app = FastAPI()

# 初始化搜索引擎
print("Initializing search engine...")
search_engine = RecipeSearchEngine()
print("Search engine initialized successfully!")

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/search")
async def search(query: str):
    # 使用列表推導式篩選字典，並進行錯誤處理
    filtered_data = [
        d for d in DATA
        if (d['name'] is not None and query in d['name']) or
        (d['description'] is not None and query in d['description'])
    ]

    filtered_data = list({d['id']: d for d in filtered_data}.values())

    return filtered_data


@app.get("/api/recipe/{recipe_id}")
async def recipe(recipe_id: str):
    for d in DATA:
        if d['id'] is not None and d['id'] == recipe_id:
            return d
    return None


@app.post("/api/search/clip")
async def search_using_clip(
    query: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    if file:
        contents = await file.read()
        results = search_engine.search_by_image(contents)
    elif query:
        results = search_engine.search_by_text_clip(query)
    else:
        return {"error": "Need to provide either query text or image"}

    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)