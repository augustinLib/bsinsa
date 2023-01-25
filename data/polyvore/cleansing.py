{
    "name": "Name of the outfit", 
    "views": "Number of views of the outfit",
    "items": [
        {
            "index": "Index of the fashion item in this outfit on Polyvore",
            "name": "Description of the fashion item",
            "price": "Price of the fashion item (usually in US dollars)",
            "likes": "Number of likes of the item",
            "image": "Image url of the item",
            "categoryid": "Category ID of the item"
        }, 
        ...
    ], 
    "image": "Outfit image url",
    "likes": "Number of likes of the outfit",
    "date": "Upload date of the outfit",
    "set_url": "Outfit url",
    "set_id": "Outfit ID",
    "desc": "Outfit description"
}


import json
import pandas as pd

json_train = json.load(open('data/polyvore/metadata/train_no_dup.json'))
len(json_train)
json_train[0].keys()
json_train['items'][0].keys() 


top_categories = [4454, 4495, 4496, 273, 4498, 19, 4497, 21, 342, 272, 341]
bottom_categories = [288, 280, 255, 4452, 4459, 237, 238, 239, 240, 241, 29, 278, 279, 310, 27, 253, 287]

train_items = []
for set_of_items in json_train:
  item_categories = []
  for item in set_of_items['items']:
    item_categories.append(item["categoryid"])
  if set(item_categories) & set(top_categories): 
    if set(item_categories) & set(bottom_categories):
      train_items.append(set_of_items)

top_items = []
bottom_items = []
total_items = []
for set_of_items in train_items:
  for item in set_of_items['items']:
    item_dict = {}
    item_dict['set_id'] = set_of_items['set_id']
    item_dict['item_id'] = item['index']
    item_dict['categoryid'] = item['categoryid']
    item_dict['price'] = item['price']
    item_dict['likes'] = item['likes']
    item_dict['name'] = item['name']
    if item["categoryid"] in top_categories:
      top_items.append(item_dict)
      total_items.append(item_dict)
    if item["categoryid"] in bottom_categories:
      bottom_items.append(item_dict)
      total_items.append(item_dict)

compatible_sets = []
for set_of_items in train_items:
  for item in set_of_items['items']:
    item_dict = {}
    item_dict['set_id'] = set_of_items['set_id']
    item_dict['item_index'] = item['index']
    item_dict['categoryid'] = item['categoryid']
    
    if item["categoryid"] in top_categories:
      item_dict['type'] = 'top'
      compatible_sets.append(item_dict)
    if item["categoryid"] in bottom_categories:
      item_dict['type'] = 'bottom'
      compatible_sets.append(item_dict)

pd.DataFrame(total_items).sort_values('set_id', ascending=False).to_csv('data/polyvore/total_items.csv', index=False)
pd.DataFrame(compatible_sets).sort_values('set_id', ascending=False).to_csv('data/polyvore/compatible_sets.csv', index=False)
