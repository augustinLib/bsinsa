var = {
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


def cleanser(json_train, name):
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
            item_dict = {'set_id': set_of_items['set_id'], 'item_id': item['index'], 'categoryid': item['categoryid'],
                         'price': item['price'], 'likes': item['likes'], 'name': item['name']}
            if item["categoryid"] in top_categories:
                top_items.append(item_dict)
                total_items.append(item_dict)
            if item["categoryid"] in bottom_categories:
                bottom_items.append(item_dict)
                total_items.append(item_dict)

    compatible_sets = []
    for set_of_items in train_items:
        for item in set_of_items['items']:
            item_dict = {'set_id': set_of_items['set_id'], 'item_index': item['index'], 'categoryid': item['categoryid']}

            if item["categoryid"] in top_categories:
                item_dict['type'] = 'top'
                compatible_sets.append(item_dict)
            if item["categoryid"] in bottom_categories:
                item_dict['type'] = 'bottom'
                compatible_sets.append(item_dict)

    # df = pd.DataFrame(compatible_sets).sort_values('set_id', ascending=False).to_csv(
    # 'data/polyvore/compatible_sets.csv', index=False)
    df = pd.DataFrame(compatible_sets).sort_values('set_id', ascending=False)

    return df


json_train = json.load(open('data/polyvore/metadata/train_no_dup.json'))
json_val = json.load(open('data/polyvore/metadata/valid_no_dup.json'))
json_test = json.load(open('data/polyvore/metadata/test_no_dup.json'))

df_train = cleanser(json_train, 'train')
df_val = cleanser(json_val, 'val')
df_test = cleanser(json_test, 'test')

df = pd.concat([df_train, df_val, df_test])
df.to_csv('data/polyvore/processed_data/compatible_sets.csv', index=False)
