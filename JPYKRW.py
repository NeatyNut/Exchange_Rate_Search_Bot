import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_currency():
    index_url = "https://finance.naver.com/marketindex/"

    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    response = requests.get(jpykrw_url, headers=headers)
    now = str(datetime.now())
    date = now[:10]
    time = now[11:19]

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        selector_price = "#content > div.DetailInfo_article__gnpKe > div.DetailInfo_info__CL557.DetailInfo_widePadding__cyDJ6 > div.DetailInfo_infoPrice__IwFL1.DetailInfo_widePadding__cyDJ6 > strong"
        selector_updown = "#content > div.DetailInfo_article__gnpKe > div.DetailInfo_info__CL557.DetailInfo_widePadding__cyDJ6 > div.DetailInfo_infoPrice__IwFL1.DetailInfo_widePadding__cyDJ6 > div > span:nth-child(1) > span"
        selector_percent = "#content > div.DetailInfo_article__gnpKe > div.DetailInfo_info__CL557.DetailInfo_widePadding__cyDJ6 > div.DetailInfo_infoPrice__IwFL1.DetailInfo_widePadding__cyDJ6 > div > span:nth-child(2)"

        price = soup.select_one(selector_price)
        price = price.text.strip().replace("KRW","")
        updown = soup.select_one(selector_updown)
        if "RISING" in str(updown):
            updown = "▲ " + updown.text.strip()
        else:
            updown = "▼ " + updown.text.strip()

        percent = soup.select_one(selector_percent)
        percent = percent.text.strip().replace("<!-- -->","")
        
        return date, time, price, updown, percent

    else:
        return get_currency()