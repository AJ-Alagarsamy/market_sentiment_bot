import requests
from bs4 import BeautifulSoup

def get_cnbc_headlines(ticker):
    url = f"https://www.cnbc.com/quotes/{ticker}?tab=news"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[CNBC] Failed to fetch headlines: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    headlines = []

    # CNBC often uses 'LatestNews-container' for news lists
    for link in soup.find_all("a", class_="LatestNews-headline"):
        title = link.get_text(strip=True)
        if title:
            headlines.append(title)

    return headlines
