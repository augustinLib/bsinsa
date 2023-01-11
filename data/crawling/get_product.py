from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time
import random
from urllib import request
import argparse
from tqdm import tqdm


p = argparse.ArgumentParser()
p.add_argument(
        "--file_name",
        required=True,
        help="insert model name"
)

config = p.parse_args()


df = pd.read_csv(f"./crawling/links/{config.file_name}.csv")
url_list = df.iloc[:,1]
options = webdriver.ChromeOptions()
# 탭 간 이동 활성화
options.add_argument("no-sandbox")
options.add_argument("headless")



product_num_list = []
main_category_list = []
sub_category_list = []
product_name_list = []
brand_list = []
year_sold_list = []
like_list = []
rate_list = []
price_list = []
tag_list = []


with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
    omitted_num = 0
    for url in tqdm(url_list):
        try:
                driver.get(url)
                driver.implicitly_wait(5)
                product_num = url.split("/")[-1]
                


                # main_category = driver.find_element(
                #         By.CSS_SELECTOR,
                #         "#page_product_detail > div.right_area.page_detail_product > div.right_contents.section_product_summary > div.product_info > p > a:nth-child(1)")
                # main_category_list.append(main_category.text)


                # sub_category = driver.find_element(
                #         By.CSS_SELECTOR,
                #         "#page_product_detail > div.right_area.page_detail_product > div.right_contents.section_product_summary > div.product_info > p > a:nth-child(2)")
                # sub_category_list.append(sub_category.text)


                product_name =  driver.find_element(
                        By.CSS_SELECTOR,
                        "#page_product_detail > div.right_area.page_detail_product > div.right_contents.section_product_summary > span > em")
                


                brand = driver.find_element(
                        By.CSS_SELECTOR,
                        "#product_order_info > div.explan_product.product_info_section > ul > li:nth-child(1) > p.product_article_contents > strong > a")
                


                year_sold = driver.find_element(
                        By.CSS_SELECTOR,
                        "#sales_1y_qty")
                if len(year_sold.text) == 0:
                        omitted_num +=1
                        continue


                like = driver.find_element(
                        By.CSS_SELECTOR,
                        f"#product-top-like > p.product_article_contents.goods_like_{product_num} > span")
                if len(like.text) == 0:
                        omitted_num +=1
                        continue


                rate = driver.find_element(
                        By.CSS_SELECTOR,
                        "#product_order_info > div.explan_product.product_info_section > ul > li:nth-child(6) > p.product_article_contents > a > span.prd-score__rating")
                if len(rate.text) == 0:
                        omitted_num +=1
                        continue

                price = driver.find_element(
                        By.CSS_SELECTOR,
                        "#goods_price")
                


                image_url = driver.find_element(
                        By.CSS_SELECTOR,
                        "#detail_bigimg > div > img").get_attribute("src")
                
                tags = driver.find_elements(
                    By.CSS_SELECTOR,
                    "#product_order_info > div.explan_product.product_info_section > ul > li.article-tag-list.list a"
                )
                
                temp_tag_list = []
                for tag in tags:
                    temp_tag_list.append(tag.text[1:])

                tag_str = ",".join(temp_tag_list)
                if len(tag_str) == 0:
                        omitted_num +=1
                        continue
                


        except:
            omitted_num +=1
            continue


        product_num_list.append(product_num)
        product_name_list.append(product_name.text)
        brand_list.append(brand.text)
        year_sold_list.append(year_sold.text)
        like_list.append(like.text)
        rate_list.append(rate.text)
        price_list.append(price.text)
        tag_list.append(tag_str)
        request.urlretrieve(image_url, f"./crawling/data/image/{product_num}.jpg")
        time.sleep(random.uniform(0,1))

        product_df = pd.DataFrame({"product_num" :product_num_list,
                            #main_category_list,
                            #sub_category_list,
                            "product_name" : product_name_list,
                            "brand" : brand_list,
                            "year_sold" : year_sold_list,
                            "like" : like_list,
                            "rate" : rate_list,
                            "price" : price_list,
                            "tag" : tag_list
                            })
    
        product_df.to_csv(f"./crawling/data/dataframe/{config.file_name}_info.csv")
        

    print()
    print(f"{config.file_name} : {omitted_num} omitted!")
