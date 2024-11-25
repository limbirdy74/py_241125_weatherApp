import requests
from bs4 import BeautifulSoup

stockName = input("주식명 :")
html = requests.get(f"https://search.daum.net/search?nil_suggest=btn&w=tot&DA=SBC&q={stockName}+주가")
soup = BeautifulSoup(html.text, "html.parser")

# print(soup.prettify())

stockNowPrice =  soup.find("span",{"class":"num_stock"}).text.strip()
print(f"{stockName} 현재주가는 {stockNowPrice}원 입니다.")