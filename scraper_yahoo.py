import feedparser

def get_yahoo_finance_headlines(ticker):
    url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
    feed = feedparser.parse(url)

    if feed.bozo:
        print(f"[Yahoo Finance] Failed to parse feed: {feed.bozo_exception}")
        return []

    headlines = [entry.title for entry in feed.entries]
    return headlines
