import pandas as pd

df = pd.concat([pd.read_csv("data/data_sample/dataframe/bottom_cotton_info.csv"),
pd.read_csv("data/data_sample/dataframe/bottom_denim_info.csv"),
pd.read_csv("data/data_sample/dataframe/bottom_etc_info.csv"),
pd.read_csv("data/data_sample/dataframe/bottom_jogger_info.csv"),
pd.read_csv("data/data_sample/dataframe/bottom_jumpper_info.csv"),
pd.read_csv("data/data_sample/dataframe/bottom_leggings_info.csv"),
pd.read_csv("data/data_sample/dataframe/bottom_short_info.csv"),
pd.read_csv("data/data_sample/dataframe/bottom_slacks_info.csv"),
pd.read_csv("data/data_sample/dataframe/top_hood_info.csv"),
pd.read_csv("data/data_sample/dataframe/top_knit_info.csv"),
pd.read_csv("data/data_sample/dataframe/top_long_info.csv"),
pd.read_csv("data/data_sample/dataframe/top_polo_info.csv"),
pd.read_csv("data/data_sample/dataframe/top_shirts_info.csv"),
pd.read_csv("data/data_sample/dataframe/top_short_info.csv"),
pd.read_csv("data/data_sample/dataframe/top_sleeveless_info.csv"),
pd.read_csv("data/data_sample/dataframe/top_sweatshirt_info.csv")],
axis=0).iloc[:, 1:]

df.to_csv("data/data_sample/dataframe/total.csv")