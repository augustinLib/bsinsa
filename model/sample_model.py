import pandas as pd

class Model:
  def __init__(self):
    self.data = pd.read_csv(".././data/data_sample/dataframe/total.csv")

  def get_data(self, product_num):
    return self.data[self.data['product_num'] == product_num]

  def get_random_data(self, num):
    return self.data['product_num'].sample(num).to_json(orient='records')
