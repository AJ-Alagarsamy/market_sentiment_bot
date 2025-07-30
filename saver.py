from dotenv import load_dotenv
load_dotenv()

from scraper_reddit import get_reddit_posts
from scraper_yahoo import get_yahoo_finance_headlines
from scraper_finviz import get_finviz_headlines
from scraper_cnbc import get_cnbc_headlines
from scraper_google_news import get_google_news_headlines
from analyzer import analyze_sentiment, compute_score
from colorama import Fore, Style, init

init(autoreset=True)

SUBREDDITS = [
    "stocks",
    "wallstreetbets",
    "finance",
    "economics",
    "financenews",
    "investing",
    "stockmarket",
]

def summarize_sentiment(sentiments):
    positive = sum(1 for s in sentiments if s == "positive")
    neutral = sum(1 for s in sentiments if s == "neutral")
    negative = sum(1 for s in sentiments if s == "negative")
    print(f"Positive: {positive}")
    print(f"Neutral: {neutral}")
    print(f"Negative: {negative}")

def color_sentiment(sentiment):
    if sentiment == "positive":
        return Fore.GREEN + sentiment.capitalize() + Style.RESET_ALL
    elif sentiment == "negative":
        return Fore.RED + sentiment.capitalize() + Style.RESET_ALL
    else:
        return Fore.YELLOW + sentiment.capitalize() + Style.RESET_ALL

def run_sentiment_bot(ticker="AAPL"):
    print(f"\n--- Market Sentiment for {ticker.upper()} ---\n")

    all_reddit_posts = []
    all_reddit_sentiments = []

    # Reddit
    for subreddit in SUBREDDITS:
        print(f"\nFetching Reddit posts from r/{subreddit} that mention '{ticker}'...")
        reddit_posts = get_reddit_posts(subreddit=subreddit, limit=10, ticker=ticker)
        reddit_sentiments = [analyze_sentiment(post[0]) for post in reddit_posts]

        print(f"\n--- r/{subreddit} Sentiment Summary ---")
        summarize_sentiment(reddit_sentiments)

        print(f"\n--- r/{subreddit} Posts ---")
        for (title, score), sentiment in zip(reddit_posts, reddit_sentiments):
            print(f"- {title} (Upvotes: {score}) - Sentiment: {color_sentiment(sentiment)}")

        all_reddit_posts.extend([post[0] for post in reddit_posts])
        all_reddit_sentiments.extend(reddit_sentiments)

    combined_reddit_text = " ".join(all_reddit_posts) if all_reddit_posts else ""
    reddit_score = compute_score(combined_reddit_text) if combined_reddit_text else 50

    print(f"\n--- Cumulative Reddit Sentiment for '{ticker}' ---")
    summarize_sentiment(all_reddit_sentiments)
    print(f"Reddit Buy/Sell Score (1=Sell, 100=Buy): {reddit_score}\n")

    # Yahoo
    print("Fetching Yahoo Finance headlines...")
    yahoo_headlines = get_yahoo_finance_headlines(ticker)
    yahoo_sentiments = [analyze_sentiment(headline) for headline in yahoo_headlines]

    print(f"\nYahoo Finance headlines for {ticker}:")
    for headline, sentiment in zip(yahoo_headlines, yahoo_sentiments):
        print(f"- {headline} - Sentiment: {color_sentiment(sentiment)}")

    combined_yahoo_text = " ".join(yahoo_headlines) if yahoo_headlines else ""
    yahoo_score = compute_score(combined_yahoo_text) if combined_yahoo_text else 50
    print(f"Yahoo Finance Buy/Sell Score (1=Sell, 100=Buy): {yahoo_score}\n")

    # Finviz
    print("Fetching Finviz headlines...")
    finviz_headlines = get_finviz_headlines(ticker)
    finviz_sentiments = [analyze_sentiment(headline) for headline in finviz_headlines]

    print(f"\nFinviz headlines for {ticker}:")
    for headline, sentiment in zip(finviz_headlines, finviz_sentiments):
        print(f"- {headline} - Sentiment: {color_sentiment(sentiment)}")

    combined_finviz_text = " ".join(finviz_headlines) if finviz_headlines else ""
    finviz_score = compute_score(combined_finviz_text) if combined_finviz_text else 50
    print(f"Finviz Buy/Sell Score (1=Sell, 100=Buy): {finviz_score}\n")

    # CNBC
    print("Fetching CNBC headlines...")
    cnbc_headlines = get_cnbc_headlines(ticker)
    cnbc_sentiments = [analyze_sentiment(headline) for headline in cnbc_headlines]

    print(f"\nCNBC headlines for {ticker}:")
    for headline, sentiment in zip(cnbc_headlines, cnbc_sentiments):
        print(f"- {headline} - Sentiment: {color_sentiment(sentiment)}")

    combined_cnbc_text = " ".join(cnbc_headlines) if cnbc_headlines else ""
    cnbc_score = compute_score(combined_cnbc_text) if combined_cnbc_text else 50
    print(f"CNBC Buy/Sell Score (1=Sell, 100=Buy): {cnbc_score}\n")

    # Google News
    print("Fetching Google News headlines...")
    google_headlines = get_google_news_headlines(ticker)
    google_sentiments = [analyze_sentiment(headline) for headline in google_headlines]

    print(f"\nGoogle News headlines for {ticker}:")
    for headline, sentiment in zip(google_headlines, google_sentiments):
        print(f"- {headline} - Sentiment: {color_sentiment(sentiment)}")

    combined_google_text = " ".join(google_headlines) if google_headlines else ""
    google_score = compute_score(combined_google_text) if combined_google_text else 50
    print(f"Google News Buy/Sell Score (1=Sell, 100=Buy): {google_score}\n")

    # Overall
    overall_score = int(
        (reddit_score + yahoo_score + finviz_score + cnbc_score + google_score) / 5
    )
    print(f"Overall Market Sentiment Score (1=Sell, 100=Buy): {overall_score}\n")

if __name__ == "__main__":
    ticker = input("Enter a stock ticker (default: AAPL): ").strip().upper() or "AAPL"
    run_sentiment_bot(ticker)
