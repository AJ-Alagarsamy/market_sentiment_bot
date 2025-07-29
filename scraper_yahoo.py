# scraper_yahoo.py

import requests
from bs4 import BeautifulSoup

def get_yahoo_finance_headlines(ticker="AAPL"):
    url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    headlines = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, features="xml")
        items = soup.find_all("item")
        for item in items:
            title = item.title.text.strip()
            if title:
                headlines.append(title)
    return headlines
