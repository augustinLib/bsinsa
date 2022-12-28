from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time
import random
from urllib import request
import argparse

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


with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
    omitted_num = 0
    for url in url_list:
        try:
            driver.get(url)
            driver.implicitly_wait(5)

        except:
            omitted_num +=1
            continue

        product_num = url.split("/")[-1]
        product_num_list.append(product_num)


        main_category = driver.find_element(
                By.CSS_SELECTOR,
                "#page_product_detail > div.right_area.page_detail_product > div.right_contents.section_product_summary > div.product_info > p > a:nth-child(1)")
        main_category_list.append(main_category.text)


        sub_category = driver.find_element(
                By.CSS_SELECTOR,
                "#page_product_detail > div.right_area.page_detail_product > div.right_contents.section_product_summary > div.product_info > p > a:nth-child(2)")
        sub_category_list.append(sub_category.text)
        

        product_name =  driver.find_element(
                By.CSS_SELECTOR,
                "#page_product_detail > div.right_area.page_detail_product > div.right_contents.section_product_summary > span > em")
        product_name_list.append(product_name.text)


        brand = driver.find_element(
                By.CSS_SELECTOR,
                "#product_order_info > div.explan_product.product_info_section > ul > li:nth-child(1) > p.product_article_contents > strong > a")
        brand_list.append(brand.text)


        year_sold = driver.find_element(
                By.CSS_SELECTOR,
                "#sales_1y_qty")
        year_sold_list.append(year_sold.text)


        like = driver.find_element(
                By.CSS_SELECTOR,
                f"#product-top-like > p.product_article_contents.goods_like_{product_num} > span")
        like_list.append(like.text)


        rate = driver.find_element(
                By.CSS_SELECTOR,
                "#product_order_info > div.explan_product.product_info_section > ul > li:nth-child(6) > p.product_article_contents > a > span.prd-score__rating")
        rate_list.append(rate.text)
        
        price = driver.find_element(
                By.CSS_SELECTOR,
                "#goods_price > del")
        price_list.append(price.text)

        image_url = driver.find_element(
                By.CSS_SELECTOR,
                "#detail_bigimg > div > img").get_attribute("src")
            
        
        request.urlretrieve(image_url, f"./crawling/data/image/{product_num}.jpg")
        time.sleep(random.randint(2,6))

    
    product_df = pd.DataFrame([product_num_list,
                            main_category_list,
                            sub_category_list,
                            product_name_list,
                            brand_list,
                            year_sold_list,
                            like_list,
                            rate_list,
                            price_list])
    
    product_df.to_csv(f"./crawling/data/dataframe/{config.file_name}_info.csv")