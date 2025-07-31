import requests
from bs4 import BeautifulSoup

def get_finviz_headlines(ticker):
    url = f"https://finviz.com/quote.ashx?t={ticker}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        news_table = soup.find("table", class_="fullview-news-outer")
        rows = news_table.find_all("tr")

        headlines = [row.a.get_text(strip=True) for row in rows if row.a]
        return headlines[:55]  # limit to 55
    except Exception as e:
        print(f"[Finviz] Failed to fetch headlines: {e}")
        return []
