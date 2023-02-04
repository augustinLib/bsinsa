import pandas as pd
import json
import pickle
import numpy as np
from pymongo import MongoClient

class Model:
  def __init__(self):
    self.data = pd.read_csv(".././data/data_sample/dataframe/total_modified.csv")
    # self.rec_data = np.load(".././data/data_sample/dist_mtx.npy")
    self.converter = {
      'hood': "후드",
      'knit': "니트",
      'long': "롱슬리브",                                
      'polo': "폴로",
      'shirt': "셔츠",
      'short': "반팔",
      'sleeveless': "슬리브리스",
      'sweat': "스웨터",            
      'cotton': "면바지",
      'denim': "데님",
      'jogger': "조거",
      'jumper': "점퍼",
      'leggings': "레깅스",
      'shorts': "반바지",
      'slacks': "슬랙스",
      'etc': "바지"
      }
    self.client = MongoClient('mongodb://localhost:27017', 5555)
    self.db = self.client['conference']

  def get_data(self, product_num):

    return self.data[self.data['product_num'] == product_num]

  def get_random_data(self, num):
    return self.data.sample(num)[['product_num', 'category', 'price']].to_json(orient='records')

  def get_random_data_by_category(self, category, num):
    return self.data[self.data['category'] == self.converter[category]].sample(num, replace=True)[['product_num', 'product_name', 'price']].to_json(orient='records')

  def get_item(self, product_num):
    return self.data[self.data['product_num'] == product_num][['product_num', 'product_name', 'price', 'category']].to_json(orient='records')

  def get_initial_item(self):
    to_return = {}
    for key, _ in self.converter.items():
      to_return[key] = self.data[self.data['category'] == self.converter[key]].sample(6)['product_num'].to_json(orient='records')
    return json.dumps(to_return)

  def get_similar_items(self, userId):
    likes = self.db.users.find({'userId': userId})
    # likes에서 다 담아와서 sampling 하고 dist_mtx에서 처리해서 내보내기
    liked_items = [doc[key] for key in self.converter.keys() for doc in likes]
    return liked_items[0]