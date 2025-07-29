# scraper_reddit.py

import praw
import os

def get_reddit_posts(subreddit, limit=10):
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent="MarketSentimentBot/0.1"
    )
    posts = []
    for submission in reddit.subreddit(subreddit).hot(limit=limit):
        # return tuple (title, score) but score won't be used for scoring now
        posts.append((submission.title, submission.score))
    return posts
