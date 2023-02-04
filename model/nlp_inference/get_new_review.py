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



def get_review(item):
    
    options = webdriver.ChromeOptions()
    # 탭 간 이동 활성화
    options.add_argument("no-sandbox")
    options.add_argument("headless")
    
    try:
        with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
            url = f"https://www.musinsa.com/app/goods/{item}"
            driver.get(url)
            driver.implicitly_wait(5)
            review = driver.find_element(
                By.CSS_SELECTOR,
                f"#reviewListFragment > div:nth-child(1) > div.review-contents > div.review-contents__text"
            )

            result = review.text


    except:
        result = "디자인 맘에 들어서 샀는데, 기대했던대로 와서 만족합니다."
        
    
    return result
