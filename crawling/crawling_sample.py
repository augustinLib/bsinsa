# 이건 셀레니욱
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# webdriver_manager : 각 브라우저 드라이버를 자동으로 설치
# ChromeDriverManager : 크롬 브라우저 자동으로 설치
from webdriver_manager.chrome import ChromeDriverManager

# find_by_xpath 이렇게 말고 저 By를 통해서 보다 직관적으로 구분할 수 있음
from selenium.webdriver.common.by import By
import pandas as pd
import time


# 무신사 url을 불러올거에요
url = "https://www.musinsa.com/app/goods/2861160?loc=goods_rank"
# option : 크롬드라이버 옵션
options = webdriver.ChromeOptions()
# 탭 간 이동 활성화
options.add_argument("no-sandbox")
# 아시죠? 그냥 창 안띄우고 잠수함모드
# options.add_argument("headless")

# 크롤링
# with문 안에 있는 코드를 실행할 때 자원을 땡겨와서, with문 안에 있는 코드가 끝나면 자원을 반납한다.
# 이슈 : webdriver manager가 특정 버전에서 m1에서 안됨!
# 그래서 제가 되는거 찾았으니깐 여러분은 안심하라구!!
with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
    # 크롬 드라이버로 하여금 url을 get하게 함
    driver.get(url)

    # 크롤링을 할때 2가지 방법의 대기가 있다.
    # 1. implicity_wait
    # 2. time.sleep(3)
    driver.implicitly_wait(5)
    num = 1,
    a = driver.find_elements(
                By.CSS_SELECTOR,
                f"#reviewListFragment > div:nth-child(1) > div.review-contents > div.review-contents__text"
            )

    print(a[0].text)