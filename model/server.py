from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sample_model import Model

app = FastAPI()
model = Model()

origins = ["http://localhost:3000", "http://127.0.0.1:3000", "http://172.30.1.61:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/home-data")
async def home():
    return model.get_random_data(3)

@app.get("/product-data/{product_category}")
async def product(product_category: str):
    return model.get_random_data_by_category(product_category, 11)

@app.get("/item/{product_num}")
async def item(product_num: int):
    return model.get_item(product_num)