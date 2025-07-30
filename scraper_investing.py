import requests
from bs4 import BeautifulSoup

def get_investing_headlines(ticker, limit=10):
    """
    Fetch recent news headlines from Investing.com for a given ticker.
    Returns a list of headline strings.
    """
    base_url = f"https://www.investing.com/equities/{ticker.lower()}-news"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # News headlines are inside <article> tags with class "js-article-item"
        articles = soup.select("article.js-article-item")[:limit]
        headlines = []
        for article in articles:
            headline_tag = article.find("a", class_="title")
            if headline_tag and headline_tag.text.strip():
                headlines.append(headline_tag.text.strip())
        
        return headlines
    except Exception as e:
        print(f"[Investing.com] Failed to fetch headlines: {e}")
        return []
