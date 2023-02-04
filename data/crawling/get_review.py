from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import pandas as pd
import time
import random
from urllib import request
import argparse
from tqdm import tqdm
import re

p = argparse.ArgumentParser()
p.add_argument(
        "--file_name",
        required=True,
        help="insert model name"
)

config = p.parse_args()


df = pd.read_csv(f"./data/crawling/data/dataframe/{config.file_name}_info.csv")
url_list = df["product_num"]

options = webdriver.ChromeOptions()
# 탭 간 이동 활성화
options.add_argument("no-sandbox")
options.add_argument("headless")


review_list = []
star_list = []
product_num_list = []


with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
    omitted_num = 0
    for num in tqdm(url_list):
        try:
            url = f"https://www.musinsa.com/app/goods/{num}"
            driver.get(url)
            driver.implicitly_wait(5)
            inside_bracket = re.compile('\((.*?)\)')

            style = driver.find_element(
                By.CSS_SELECTOR,
                "#estimate_style"
            )
            style_temp = inside_bracket.findall(style.text)[0]
            style_temp = style_temp.replace(",", "")
            style_num = int(style_temp)

            photo = driver.find_element(
                By.CSS_SELECTOR,
                "#estimate_photo"
            )
            photo_temp = inside_bracket.findall(photo.text)[0]
            photo_temp = photo_temp.replace(",", "")
            photo_num = int(photo_temp)

            goods = driver.find_element(
                By.CSS_SELECTOR,
                "#estimate_goods"
            )

            goods_temp = inside_bracket.findall(goods.text)[0]
            goods_temp = goods_temp.replace(",", "")
            goods_num = int(goods_temp)

            review_type_list = [style, photo, goods]
            time.sleep(random.uniform(0,2))
            # 각 리뷰 100개씩 없으면 패스
            if style_num < 100 or photo_num < 100 or goods_num < 100:
                omitted_num += 1

                continue
            

            sort = driver.find_element(
                By.CSS_SELECTOR,
                "#reviewSelectSort"
            )

            sort_select = Select(sort)


            # 각 리뷰 종류 클릭으로 이동 (각 리뷰 당 100개 추출)
            for review_type in review_type_list:
                if review_type != style:
                    review_type.click()
                time.sleep(random.uniform(0,1))
                #높은 평점 순으로 정렬
                sort_select.select_by_value("goods_est_desc")
                # 각 리뷰 별 높은 평점 순 50개 추출
                for page in range(1, 6):
                    time.sleep(random.uniform(0,1))
                    for i in range(1,11):

                        review = driver.find_element(
                            By.CSS_SELECTOR,
                            f"#reviewListFragment > div:nth-child({i}) > div.review-contents > div.review-contents__text"
                        )
                        review_txt = review.text
                        review_txt = review_txt.replace("\n", " ")

                        star_raw = driver.find_element(
                            By.CSS_SELECTOR,
                            f"#reviewListFragment > div:nth-child({i}) > div.review-list__rating-wrap > span > span > span"
                        )
                        star = star_raw.get_attribute("style")
                        star_temp = star.split(": ")[-1]
                        star_temp = star_temp.replace("%", "")
                        star_temp = star_temp.replace(";", "")
                        star_result = int(star_temp) / int(20)
                        product_num_list.append(num)
                        review_list.append(review_txt)
                        star_list.append(star_result)


                    time.sleep(random.uniform(0,1))
                    if page == 5:
                        continue
                    else:
                        new_page = page + 1
                        driver.execute_script(f"ReviewPage.goPage({new_page});")
                        time.sleep(random.uniform(0,1))


                #낮은 평점 순으로 정렬
                sort_select.select_by_value("goods_est_asc")
                # 각 리뷰 별 높은 평점 순 50개 추출
                for page in range(1, 6):
                    for i in range(1,11):
                        review = driver.find_element(
                            By.CSS_SELECTOR,
                            f"#reviewListFragment > div:nth-child({i}) > div.review-contents > div.review-contents__text"
                        )
                        review_txt = review.text
                        review_txt = review_txt.replace("\n", " ")

                        star_raw = driver.find_element(
                            By.CSS_SELECTOR,
                            f"#reviewListFragment > div:nth-child({i}) > div.review-list__rating-wrap > span > span > span"
                        )
                        star = star_raw.get_attribute("style")
                        star_temp = star.split(": ")[-1]
                        star_temp = star_temp.replace("%", "")
                        star_temp = star_temp.replace(";", "")
                        star_result = int(star_temp) / int(20)
                        product_num_list.append(num)
                        review_list.append(review_txt)
                        star_list.append(star_result)

                        time.sleep(random.uniform(0,1))


                    time.sleep(random.uniform(0,1))
                    if page == 5:
                        continue
                    else:
                        new_page = page + 1
                        driver.execute_script(f"ReviewPage.goPage({new_page});")
                        time.sleep(random.uniform(0,1))


                product_df = pd.DataFrame({"product_num" :product_num_list,
                                            "review" : review_list,
                                            "star" : star_list
                                            })
                product_df.to_csv(f"./data/crawling/data/review/{config.file_name}_review.csv")
        except:
            continue
        
    print(f"{omitted_num} omitted!")



