import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sample_model import Model
from pymongo import MongoClient
from bson.json_util import dumps
from nlp_inference.inference_class import *
from nlp_inference.get_new_review import *

app = FastAPI()
model = Model()
nlp_model = NLPInference() 
# origins = ["http://localhost:3000", "http://127.0.0.1:3000", "http://172.30.1.25:3000"]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
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

@app.get("/test-data")
async def test():
    return model.test_mongo()

@app.get("/initial-data")
async def initial():
    return model.get_initial_item()
    
client = MongoClient('mongodb://localhost:27017', 5555)
db = client['conference']
@app.get('/mongo')
async def get_users_in_mongo():
    items = db['item']
    return json.loads(dumps(items.find().limit(20)))

@app.get('/get-similar/{userId}')
async def get_similar(userId):
    return json.loads(dumps(model.get_similar_items(userId)))

@app.get('/tag-label/{product_num}')
async def get_tag_label(product_num):
    review = get_review(product_num)
    return json.loads(dumps(nlp_model.predict(review)))
