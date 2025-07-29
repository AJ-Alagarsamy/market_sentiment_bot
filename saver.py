# main.py

from scraper_reddit import get_reddit_posts
from analyzer import analyze_sentiment
from bs4 import BeautifulSoup
import requests

SUBREDDITS = [
    "stocks",
    "wallstreetbets",
    "finance",
    "economics",
    "financenews",
    "investing",
    "StockMarket",
    "trading",
]

def run_sentiment_bot(ticker="AAPL"):
    print(f"\n=== Market Sentiment for {ticker.upper()} ===")

    all_reddit_sentiments = []

    # 1. Loop through subreddits and fetch Reddit posts
    for subreddit in SUBREDDITS:
        print(f"\nFetching Reddit posts from r/{subreddit}...")
        reddit_posts = get_reddit_posts(subreddit=subreddit, limit=20)
        sentiments = [analyze_sentiment(post) for post in reddit_posts]

        all_reddit_sentiments.extend(sentiments)

        print(f"\n--- r/{subreddit} Sentiment Summary ---")
        summarize_sentiment(sentiments)

        print(f"\n--- r/{subreddit} Posts ---")
        for post in reddit_posts:
            print(f"- {post}")

    # 2. Fetch Yahoo Finance headlines
    print(f"\nFetching Yahoo Finance headlines for {ticker.upper()}...")
    yahoo_headlines = get_yahoo_finance_headlines(ticker)
    yahoo_sentiments = [analyze_sentiment(h) for h in yahoo_headlines]

    # 3. Summarize Yahoo Finance
    print(f"\n--- Yahoo Finance Sentiment Summary ---")
    summarize_sentiment(yahoo_sentiments)

    print(f"\n--- Yahoo Headlines ---")
    for headline in yahoo_headlines:
        print(f"- {headline}")

    # 4. Final Summary (all subreddits combined)
    print(f"\n=== Overall Reddit Sentiment Summary ===")
    summarize_sentiment(all_reddit_sentiments)

def summarize_sentiment(sentiments):
    positive = sum(1 for s in sentiments if s == "positive")
    neutral = sum(1 for s in sentiments if s == "neutral")
    negative = sum(1 for s in sentiments if s == "negative")
    print(f"Positive: {positive}")
    print(f"Neutral: {neutral}")
    print(f"Negative: {negative}")

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
    else:
        print("Failed to fetch Yahoo Finance headlines.")
    return headlines

if __name__ == "__main__":
    ticker = input("Enter a stock ticker (default: AAPL): ").strip().upper() or "AAPL"
    run_sentiment_bot(ticker)
