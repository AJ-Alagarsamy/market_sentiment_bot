import snscrape.modules.twitter as sntwitter

def get_twitter_posts(ticker, limit=20):
    query = f"{ticker} lang:en"
    tweets = []

    scraper = sntwitter.TwitterSearchScraper(query)
    
    # Patch the _request method of this scraper instance to disable SSL verification
    original_request = scraper._request

    def patched_request(method, *args, **kwargs):
        kwargs['verify'] = False
        return original_request(method, *args, **kwargs)

    scraper._request = patched_request

    for i, tweet in enumerate(scraper.get_items()):
        if i >= limit:
            break
        tweets.append(tweet.content)

    return tweets
