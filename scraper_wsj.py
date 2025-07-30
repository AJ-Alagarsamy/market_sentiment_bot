import requests
from bs4 import BeautifulSoup

def get_wsj_headlines(ticker):
    url = f"https://www.wsj.com/search?query={ticker}&mod=searchresults_viewallresults"
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
        for item in soup.select("article h3, article h2"):
            text = item.get_text(strip=True)
            if text and ticker.upper() in text.upper():
                headlines.append(text)
        return headlines[:10]
    except Exception as e:
        print(f"[WSJ] Failed to fetch headlines: {e}")
        return []
