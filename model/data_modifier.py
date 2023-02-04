### OLD 
import os
import pandas as pd

folder_path = 'data/data_sample/image'
imgs= []
for filename in os.listdir(folder_path):
    if os.path.isfile(os.path.join(folder_path, filename)):
        file_without_extension = os.path.splitext(filename)[0]
        imgs.append(int(file_without_extension))


df = pd.read_csv("data/data_sample/dataframe/total.csv")
rows_to_drop = df[~df['product_num'].isin(imgs)].index
df.drop(rows_to_drop, inplace=True)

# Drop the rows from the DataFrame
df.to_csv("data/data_sample/dataframe/total_modified.csv", index=False)

### NEW
