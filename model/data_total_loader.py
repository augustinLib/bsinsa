import pandas as pd

def category_appender(path: str, category: str):
  data = pd.read_csv(path)
  data['category'] = category
  data.to_csv(path)

### OLD
category_appender("data/data_sample/dataframe/bottom_cotton_info.csv", "면바지")
category_appender("data/data_sample/dataframe/bottom_denim_info.csv", "데님")
category_appender("data/data_sample/dataframe/bottom_etc_info.csv", "바지")
category_appender("data/data_sample/dataframe/bottom_jogger_info.csv", "조거")
category_appender("data/data_sample/dataframe/bottom_jumpper_info.csv", "점퍼")
category_appender("data/data_sample/dataframe/bottom_leggings_info.csv", "레깅스")
category_appender("data/data_sample/dataframe/bottom_short_info.csv", "반바지")
category_appender("data/data_sample/dataframe/bottom_slacks_info.csv", "슬랙스")
category_appender("data/data_sample/dataframe/top_hood_info.csv", "후드")
category_appender("data/data_sample/dataframe/top_knit_info.csv", "니트")
category_appender("data/data_sample/dataframe/top_long_info.csv", "롱슬리브")
category_appender("data/data_sample/dataframe/top_polo_info.csv", "폴로")
category_appender("data/data_sample/dataframe/top_shirts_info.csv", "셔츠")
category_appender("data/data_sample/dataframe/top_short_info.csv", "반팔")
category_appender("data/data_sample/dataframe/top_sleeveless_info.csv", "슬리브리스")
category_appender("data/data_sample/dataframe/top_sweatshirt_info.csv", "스웨터")

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
axis=0)

df.to_csv("data/data_sample/dataframe/total.csv")

### NEW 

import pandas as pd

def category_appender(path: str, category: str):
  data = pd.read_csv(path)
  data['category'] = category
  data.to_csv(path)

category_appender("data/crawling/data/dataframe/bottom_cotton_info.csv", "면바지")
category_appender("data/crawling/data/dataframe/bottom_denim_info.csv", "데님")
category_appender("data/crawling/data/dataframe/bottom_etc_info.csv", "바지")
category_appender("data/crawling/data/dataframe/bottom_jogger_info.csv", "조거")
category_appender("data/crawling/data/dataframe/bottom_jumpper_info.csv", "점퍼")
category_appender("data/crawling/data/dataframe/bottom_leggings_info.csv", "레깅스")
category_appender("data/crawling/data/dataframe/bottom_short_info.csv", "반바지")
category_appender("data/crawling/data/dataframe/bottom_slacks_info.csv", "슬랙스")
category_appender("data/crawling/data/dataframe/top_hood_info.csv", "후드")
category_appender("data/crawling/data/dataframe/top_knit_info.csv", "니트")
category_appender("data/crawling/data/dataframe/top_long_info.csv", "롱슬리브")
category_appender("data/crawling/data/dataframe/top_polo_info.csv", "폴로")
category_appender("data/crawling/data/dataframe/top_shirts_info.csv", "셔츠")
category_appender("data/crawling/data/dataframe/top_short_info.csv", "반팔")
category_appender("data/crawling/data/dataframe/top_sleeveless_info.csv", "슬리브리스")
category_appender("data/crawling/data/dataframe/top_sweatshirt_info.csv", "스웨터")

df = pd.concat([pd.read_csv("data/crawling/data/dataframe/bottom_cotton_info.csv"),
pd.read_csv("data/crawling/data/dataframe/bottom_denim_info.csv"),
pd.read_csv("data/crawling/data/dataframe/bottom_etc_info.csv"),
pd.read_csv("data/crawling/data/dataframe/bottom_jogger_info.csv"),
pd.read_csv("data/crawling/data/dataframe/bottom_jumpper_info.csv"),
pd.read_csv("data/crawling/data/dataframe/bottom_leggings_info.csv"),
pd.read_csv("data/crawling/data/dataframe/bottom_short_info.csv"),
pd.read_csv("data/crawling/data/dataframe/bottom_slacks_info.csv"),
pd.read_csv("data/crawling/data/dataframe/top_hood_info.csv"),
pd.read_csv("data/crawling/data/dataframe/top_knit_info.csv"),
pd.read_csv("data/crawling/data/dataframe/top_long_info.csv"),
pd.read_csv("data/crawling/data/dataframe/top_polo_info.csv"),
pd.read_csv("data/crawling/data/dataframe/top_shirts_info.csv"),
pd.read_csv("data/crawling/data/dataframe/top_short_info.csv"),
pd.read_csv("data/crawling/data/dataframe/top_sleeveless_info.csv"),
pd.read_csv("data/crawling/data/dataframe/top_sweatshirt_info.csv")],
axis=0)


df.to_csv("data/data_sample/dataframe/total_final.csv")