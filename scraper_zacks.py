import requests
from bs4 import BeautifulSoup

def get_zacks_headlines(ticker, limit=10):
    url = f"https://www.zacks.com/stock/quote/{ticker}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # News might be under div with id 'news' or class 'news-list' - inspect page
        news_section = soup.find("div", id="news") or soup.find("div", class_="news-list")

        if not news_section:
            return []

        headlines = []
        for item in news_section.find_all("li"):
            a = item.find("a")
            if a and a.get_text(strip=True):
                headlines.append(a.get_text(strip=True))
            if len(headlines) >= limit:
                break

        return headlines

    except requests.RequestException as e:
        print(f"[Zacks] Failed to fetch headlines: {e}")
        return []
