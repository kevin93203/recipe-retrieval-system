import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

with open("./icook_recipe/recipe_data.json", "r", encoding='utf-8') as f:
    DATA = json.load(f)


app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://10.54.12.187:5173",
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
async def search(query:str):
    # 使用列表推導式篩選字典，並進行錯誤處理
    filtered_data = [
        d for d in DATA
        if (d['name'] is not None and query in d['name']) or 
        (d['description'] is not None and query in d['description'])
    ]

    filtered_data = list({d['id']: d for d in filtered_data}.values())

    return filtered_data

@app.get("/api/recipe/{recipe_id}")
async def search(recipe_id:str):
    for d in DATA:
        if d['id'] is not None and d['id'] == recipe_id:
            return d
    return None