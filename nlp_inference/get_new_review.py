from bs4 import BeautifulSoup as BS
import requests as req




url = "https://www.musinsa.com/app/goods/2886235"
res = req.get(url)
soup = BS(res.text, 'html.parser')

arr = soup.find("#reviewListFragment > div:nth-child(1) > div.review-contents > div.review-contents__text")
print(arr)