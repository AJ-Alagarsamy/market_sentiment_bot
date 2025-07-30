import requests
from bs4 import BeautifulSoup

def get_seeking_alpha_headlines(ticker):
    url = f"https://seekingalpha.com/symbol/{ticker}/news"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        articles = soup.select("li[data-test-id='post-list-item'] a[data-test-id='post-list-title']")
        headlines = [a.get_text(strip=True) for a in articles]
        return headlines[:10]
    except Exception as e:
        print(f"[Seeking Alpha] Failed to fetch headlines: {e}")
        return []
