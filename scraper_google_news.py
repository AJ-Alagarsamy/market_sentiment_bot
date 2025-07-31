import feedparser

def get_google_news_headlines(ticker, limit=200):
    print(f"Fetching Google News headlines for {ticker} via RSS...")
    rss_url = f"https://news.google.com/rss/search?q={ticker}+when:7d&hl=en-US&gl=US&ceid=US:en"

    feed = feedparser.parse(rss_url)
    if not feed.entries:
        print("[Google News] No headlines found in RSS feed.")
        return []

    headlines = []
    for entry in feed.entries[:limit]:
        title = entry.title
        if title:
            headlines.append(title)

    return headlines
