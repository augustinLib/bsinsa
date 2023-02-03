import os
import shutil
import pandas as pd
import matplotlib.pyplot as plt

# Read the data
df = pd.read_csv('data/polyvore/processed_data/compatible_sets.csv')
# check df duplicates

# Item directory is like images/set_id/item_id.jpg
# plot some images
plt.figure(figsize=(10, 10))
for i in range(9):
    plt.subplot(3, 3, i+1)
    path = os.path.join('data/polyvore/images', str(df.iloc[i]['set_id']), str(df.iloc[i]['item_index']) + '.jpg')
    plt.imshow(plt.imread(path))
    # img = plt.imread(os.path.join('data/polyvore/images', df.iloc[i]['set_id'], df.iloc[i]['item_index'] + '.jpg'))
    plt.axis('off')
plt.show()

# Item directory is like images/set_id/item_id.jpg
# extract images in the csv and copy it to a new directory

def copy_images(df, src_dir, dst_dir):
    print(len(df))
    count = 0
    for i in range(len(df)):
        src = os.path.join(src_dir, str(df.iloc[i]['set_id']), str(df.iloc[i]['item_index']) + '.jpg')
        dst = os.path.join(dst_dir, str(df.iloc[i]['set_id']), str(df.iloc[i]['item_index']) + '.jpg')
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
        count += 1
    print(count)

copy_images(df, 'data/polyvore/images_', 'data/polyvore/images2')

# count how many items are in the data/polyvore/images2 directory

def count_images(dir):
    count = 0
    for path, subdirs, files in os.walk(dir):
        for name in files:
            count += 1
    return count

count_images('data/polyvore/images')
