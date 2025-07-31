import praw
import os
# Initialize Reddit client (make sure your praw.ini or environment variables are set)
reddit = praw.Reddit(
    client_id="bto-wdvgCtYcSiM4hw1KKg",
    client_secret="9ARNN0jHXRitVgn7IX4FWJvP1murhQ",
    user_agent="MarketSentimentBot by /u/OkraSuspicious8725"
)

def get_reddit_posts(subreddit, limit=2500, ticker=None):
    """
    Fetch top 'limit' hot posts from the subreddit that mention the ticker.
    Only posts containing ticker or $ticker (case-insensitive) are included.
    
    Returns list of tuples: (title, score)
    """
    posts = []
    ticker_lower = ticker.lower() if ticker else None
    subreddit_obj = reddit.subreddit(subreddit)
    
    for submission in subreddit_obj.hot(limit=limit * 3):  # fetch extra posts to filter later
        title = submission.title
        title_lower = title.lower()
        selftext = submission.selftext.lower() if submission.selftext else ""
        
        # Check if ticker appears in title or body
        if ticker_lower and (ticker_lower in title_lower or f"${ticker_lower}" in title_lower or
                             ticker_lower in selftext or f"${ticker_lower}" in selftext):
            posts.append((title, submission.score))
            if len(posts) >= limit:
                break

    return posts
