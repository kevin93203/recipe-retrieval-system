from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from search_engine import RecipeSearchEngine
from PIL import Image

# FastAPI 應用設置
app = FastAPI(title="食譜搜尋引擎 API")

# CORS 設置
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

# 初始化搜尋引擎
search_engine = RecipeSearchEngine("./icook_recipe/recipe_data.json")


@app.get("/")
async def root():
    return {
        "message": "食譜搜尋引擎 API",
        "version": "1.0.0",
        "endpoints": {
            "/api/search": "文字搜尋",
            "/api/ingredient-search": "食材搜尋",
            "/api/similar-ingredients/{ingredient}": "相似食材查詢",
            "/api/image-search": "圖片搜尋",
            "/api/recipe/{recipe_id}": "食譜詳情"
        }
    }



@app.get("/api/search")
async def text_search(query: str, top_k: int = 10):
    """文字搜尋 API"""
    return search_engine.text_search(query, top_k)


@app.get("/api/ingredient-search")
async def ingredient_search(ingredients: str, top_k: int = 10):
    """食材搜尋 API"""
    ingredient_list = ingredients.split(',')
    return search_engine.ingredient_based_search(ingredient_list, top_k)


@app.get("/api/similar-ingredients/{ingredient}")
async def get_similar_ingredients(ingredient: str, top_k: int = 5):
    """查詢相似食材 API"""
    return search_engine.get_similar_ingredients(ingredient, top_k)


@app.post("/api/image-search")
async def image_search(file: UploadFile = File(...), top_k: int = 10):
    """圖片搜尋 API"""
    image = Image.open(file.file)
    return search_engine.image_search(image, top_k)

@app.post("/api/multimodal-search")
async def multimodal_search(file: UploadFile = File(...), top_k: int = 10, text: str | None = None):
    image = Image.open(file.file)
    return search_engine.multimodal_search(image, text, top_k)


@app.get("/api/recipe/{recipe_id}")
async def get_recipe(recipe_id: str):
    """獲取特定食譜詳情"""
    for recipe in search_engine.data:
        if recipe['id'] == recipe_id:
            return recipe
    return None
