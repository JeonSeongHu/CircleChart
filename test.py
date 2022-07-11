from bs4 import BeautifulSoup
import requests


html = requests.get("https://circlechart.kr/page_chart/onoff.circle?nationGbn=T&serviceGbn=ALL&targetTime=27&hitYear=2022&termGbn=week&yearTime=3")
soup = BeautifulSoup(html.text, 'html.parser')
print(soup)