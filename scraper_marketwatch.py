import requests
from bs4 import BeautifulSoup

def get_marketwatch_headlines(ticker):
    url = f"https://www.marketwatch.com/investing/stock/{ticker.lower()}"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        headlines = []
        for item in soup.select("h3.article__headline, div.article__summary"):
            text = item.get_text(strip=True)
            if text and ticker.upper() in text.upper():
                headlines.append(text)
        return headlines[:10]
    except Exception as e:
        print(f"[MarketWatch] Failed to fetch headlines: {e}")
        return []
