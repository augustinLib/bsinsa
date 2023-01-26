import random
import pandas as pd

data = pd.read_csv('data/polyvore/processed_data/compatible_sets.csv')
data.head()

new_data = data.groupby('set_id').agg({'item_index': lambda x: list(x), 'categoryid': lambda x: list(x), 'type': lambda x: list(x)})
new_data['label'] = 1
new_data.reset_index(inplace=True)
new_data.head()

aligned_data = pd.DataFrame(columns=['set_id', 'item_index', 'categoryid', 'type', 'label'])
for i in range(len(new_data)):
    if new_data.iloc[i]['type'] == ['top', 'bottom']:
        aligned_data.at[i, 'set_id'] = new_data.iloc[i]['set_id']
        aligned_data.at[i, 'item_index'] = new_data.iloc[i]['item_index']
        aligned_data.at[i, 'categoryid'] = new_data.iloc[i]['categoryid']
        aligned_data.at[i, 'type'] = new_data.iloc[i]['type']
        aligned_data.at[i, 'label'] = new_data.iloc[i]['label']
    elif new_data.iloc[i]['type'] == ['bottom', 'top']:
        aligned_data.at[i, 'set_id'] = new_data.iloc[i]['set_id']
        aligned_data.at[i, 'item_index'] = new_data.iloc[i]['item_index'][::-1]
        aligned_data.at[i, 'categoryid'] = new_data.iloc[i]['categoryid'][::-1]
        aligned_data.at[i, 'type'] = new_data.iloc[i]['type'][::-1]
        aligned_data.at[i, 'label'] = new_data.iloc[i]['label']
    else:
        pass

# for each row in new_data, make a new data frame with the top and bottom items on the same row with separate column named with type
aligned_data.head()
sorted_data = pd.DataFrame(columns=['top_index', 'bottom_index', 'top_categoryid', 'bottom_categoryid', 'label'])
for i in range(len(aligned_data)):
    set_id = aligned_data.iloc[i]['set_id']
    top_index = aligned_data.iloc[i]['item_index'][0]
    bottom_index = aligned_data.iloc[i]['item_index'][1]
    top_categoryid = aligned_data.iloc[i]['categoryid'][0]
    bottom_categoryid = aligned_data.iloc[i]['categoryid'][1]
    label = aligned_data.iloc[i]['label']

    sorted_data.at[i, 'top_index'] = f'{set_id}_{top_index}'
    sorted_data.at[i, 'bottom_index'] = f'{set_id}_{bottom_index}'
    sorted_data.at[i, 'top_categoryid'] = top_categoryid
    sorted_data.at[i, 'bottom_categoryid'] = bottom_categoryid
    sorted_data.at[i, 'label'] = label

sorted_data.head()

# shuffle top
shuffled_index = list(range(len(sorted_data)))
random.shuffle(shuffled_index)

shuffled_data_top = pd.DataFrame(columns=['top_index', 'bottom_index', 'top_categoryid', 'bottom_categoryid', 'label'])
for i in range(0, len(sorted_data), 2):
    j = shuffled_index[i]
    set_id = aligned_data.iloc[i]['set_id']
    top_index = sorted_data.iloc[i]['top_index']
    top_categoryid = sorted_data.iloc[i]['top_categoryid']
    bottom_index = sorted_data.iloc[j]['bottom_index']
    bottom_categoryid = sorted_data.iloc[j]['bottom_categoryid']
    label = 0

    shuffled_data_top.at[i, 'top_index'] = top_index
    shuffled_data_top.at[i, 'bottom_index'] = bottom_index
    shuffled_data_top.at[i, 'top_categoryid'] = top_categoryid
    shuffled_data_top.at[i, 'bottom_categoryid'] = bottom_categoryid
    shuffled_data_top.at[i, 'label'] = label

# shuffle bottom
shuffled_index = list(range(len(sorted_data)))
random.shuffle(shuffled_index)

shuffled_data_bottom = pd.DataFrame(columns=['top_index', 'bottom_index', 'top_categoryid', 'bottom_categoryid', 'label'])
for i in range(0, len(sorted_data), 2):
    j = shuffled_index[i]
    set_id = aligned_data.iloc[i]['set_id']
    top_index = sorted_data.iloc[j]['top_index']
    top_categoryid = sorted_data.iloc[j]['top_categoryid']
    bottom_index = sorted_data.iloc[i]['bottom_index']
    bottom_categoryid = sorted_data.iloc[i]['bottom_categoryid']
    label = 0

    shuffled_data_bottom.at[i, 'top_index'] = top_index
    shuffled_data_bottom.at[i, 'bottom_index'] = bottom_index
    shuffled_data_bottom.at[i, 'top_categoryid'] = top_categoryid
    shuffled_data_bottom.at[i, 'bottom_categoryid'] = bottom_categoryid
    shuffled_data_bottom.at[i, 'label'] = label


# combine the shuffled data
combined_data = pd.concat([sorted_data, shuffled_data_top, shuffled_data_bottom], ignore_index=True)
combined_data.to_csv('data/polyvore/processed_data/combined_data.csv', index=False)
