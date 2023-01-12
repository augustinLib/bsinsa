import pandas as pd

class Model:
  def __init__(self):
    self.data = pd.read_csv(".././data/data_sample/dataframe/total_modified.csv")
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

  def get_data(self, product_num):
    return self.data[self.data['product_num'] == product_num]

  def get_random_data(self, num):
    return self.data.sample(num)[['product_num', 'category', 'price']].to_json(orient='records')

  def get_random_data_by_category(self, category, num):
    return self.data[self.data['category'] == self.converter[category]].sample(num)[['product_num', 'product_name', 'price']].to_json(orient='records')

  def get_item(self, product_num):
    return self.data[self.data['product_num'] == product_num][['product_num', 'product_name', 'price']].to_json(orient='records')