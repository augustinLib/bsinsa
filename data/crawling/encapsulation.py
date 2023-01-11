from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time
from tqdm import tqdm
import random


class GetProductUrl():
    def __init__(self, page_link, type, max_page ,is_headless = False):
        self.page_link = page_link
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("no-sandbox")
        if is_headless == True:
            self.options.add_argument("headless")

        self.links_list = []
        self.type = type
        self.max_page = max_page + 1
        self.service = Service(ChromeDriverManager().install())


    def get_url(self):
        with webdriver.Chrome(service=self.service, options=self.options) as driver:
            driver.get(self.page_link)
            driver.implicitly_wait(5)
            error_num = 0

            for page_num in tqdm(range(1, self.max_page)):
                driver.execute_script(f"switchPage(document.f1,{page_num});")
                driver.implicitly_wait(5)
                for item_num in range(1,91):
                    try:
                        link= driver.find_element(
                        By.CSS_SELECTOR,
                        f"#searchList > li:nth-child({item_num}) > div.li_inner > div.article_info > p.list_info > a")
            
                        temp_link = link.get_attribute("href")
                        self.links_list.append(temp_link)
                    except:
                        print(f"{page_num}page {item_num}th error!")
                        error_num += 1
                        continue

                time.sleep(random.randint(2,6))

        print(f"{error_num} items omitted!")


    def export_link(self, path):
        links_df = pd.DataFrame(self.links_list, index=None)
        links_df.to_csv(f"{path}/{self.type}.csv")