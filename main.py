# main.py
from dotenv import load_dotenv
load_dotenv()
from scraper_reddit import get_reddit_posts
from analyzer import analyze_sentiment
from scraper_yahoo import get_yahoo_finance_headlines  # your Yahoo headlines scraper
from colorama import Fore, Style

def calculate_actionable_score(sentiments):
    positive = sentiments.count("positive")
    negative = sentiments.count("negative")
    total = positive + negative

    if total == 0:
        return 50  # neutral if only neutral posts

    raw_score = (positive - negative) / total
    scaled_score = int(round((raw_score + 1) / 2 * 100))  # scale -1..1 to 0..100

    return scaled_score

def run_sentiment_bot(ticker="AAPL"):
    subreddits = [
        "stocks", "wallstreetbets", "finance", "economics",
        "financenews", "investing", "Stockmarket", "trading"
    ]
    print(f"\n--- Market Sentiment for {ticker.upper()} ---")

    all_sentiments = []

    # Process each subreddit
    for subreddit in subreddits:
        print(f"\nFetching Reddit posts from r/{subreddit}...")
        reddit_posts = get_reddit_posts(subreddit=subreddit, limit=10)
        reddit_sentiments = [analyze_sentiment(post[0]) for post in reddit_posts]
        all_sentiments.extend(reddit_sentiments)

        score = calculate_actionable_score(reddit_sentiments)
        label, color = label_score(score)

        print(f"\n--- r/{subreddit} Sentiment Summary ---")
        print(f"Positive: {reddit_sentiments.count('positive')}")
        print(f"Neutral: {reddit_sentiments.count('neutral')}")
        print(f"Negative: {reddit_sentiments.count('negative')}")
        print(f"Actionable Sentiment Score: {color}{score}/100 ({label}){Style.RESET_ALL}")

        print(f"\n--- r/{subreddit} Posts ---")
        for post, sentiment in zip(reddit_posts, reddit_sentiments):
            title, _ = post
            s_color = sentiment_color(sentiment)
            print(f"- {title} [{s_color}{sentiment}{Style.RESET_ALL}]")

    # Cumulative Reddit sentiment
    print("\n\n=== CUMULATIVE SENTIMENT ACROSS ALL SUBREDDITS ===")
    cum_score = calculate_actionable_score(all_sentiments)
    cum_label, cum_color = label_score(cum_score)
    print(f"Total posts analyzed: {len(all_sentiments)}")
    print(f"Cumulative Actionable Sentiment Score: {cum_color}{cum_score}/100 ({cum_label}){Style.RESET_ALL}")

    # Yahoo Finance headlines
    print(f"\n\nFetching Yahoo Finance headlines for {ticker}...")
    yahoo_headlines = get_yahoo_finance_headlines(ticker)
    yahoo_sentiments = [analyze_sentiment(headline) for headline in yahoo_headlines]
    yahoo_score = calculate_actionable_score(yahoo_sentiments)
    yahoo_label, yahoo_color = label_score(yahoo_score)

    print(f"\n--- YAHOO FINANCE HEADLINES Sentiment Summary ---")
    print(f"Positive: {yahoo_sentiments.count('positive')}")
    print(f"Neutral: {yahoo_sentiments.count('neutral')}")
    print(f"Negative: {yahoo_sentiments.count('negative')}")
    print(f"Yahoo Finance Actionable Sentiment Score: {yahoo_color}{yahoo_score}/100 ({yahoo_label}){Style.RESET_ALL}")

    print(f"\n--- YAHOO FINANCE HEADLINES ---")
    for headline, sentiment in zip(yahoo_headlines, yahoo_sentiments):
        s_color = sentiment_color(sentiment)
        print(f"- {headline} [{s_color}{sentiment}{Style.RESET_ALL}]")

def label_score(score):
    if score >= 70:
        return "BUY", Fore.GREEN
    elif score <= 30:
        return "SELL", Fore.RED
    else:
        return "HOLD", Fore.YELLOW

def sentiment_color(sentiment):
    if sentiment == "positive":
        return Fore.GREEN
    elif sentiment == "negative":
        return Fore.RED
    else:
        return Fore.YELLOW

if __name__ == "__main__":
    ticker = input("Enter a stock ticker (default: AAPL): ").strip().upper() or "AAPL"
    run_sentiment_bot(ticker)
