from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time
import argparse
import random

def define_argparse():
    p = argparse.ArgumentParser()

    p.add_argument("--url", required=True)
    p.add_argument("--pages", type=int)
    p.add_argument("--type", required=True)

    config = p.parse_args()
    return config



# https://www.musinsa.com/categories/item/001

config = define_argparse()

url = config.url
options = webdriver.ChromeOptions()
# 탭 간 이동 활성화
options.add_argument("no-sandbox")
options.add_argument("headless")

links = []
with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
    driver.get(url)
    driver.implicitly_wait(5)
    error_num = 0
    

    for page_num in range(1, config.pages):
        driver.execute_script(f"switchPage(document.f1,{page_num});")
        driver.implicitly_wait(5)
        for item_num in range(1,91):
            try:
                link= driver.find_element(
                By.CSS_SELECTOR,
                f"#searchList > li:nth-child({item_num}) > div.li_inner > div.article_info > p.list_info > a")
            
                temp_link = link.get_attribute("href")
                links.append(temp_link)
            except:
                print(f"{page_num}page {item_num}th error!")
                error_num += 1
                continue

        time.sleep(random.randint(2,6))
            
        

print(f"{error_num} items omitted!")
link_df= pd.DataFrame(links)
link_df.to_csv(f"./crawling/links/{config.type}.csv")
