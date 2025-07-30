from textblob import TextBlob

def analyze_sentiment(text):
    """
    Returns sentiment label: positive, neutral, or negative
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"

def compute_score(text):
    """
    Computes a buy/sell score on a scale 1-100 based on sentiment polarity.
    1 = Strong Sell (very negative), 50 = Neutral, 100 = Strong Buy (very positive)
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # range -1 to 1
    # Normalize polarity from [-1,1] to [1,100]
    score = int(((polarity + 1) / 2) * 99 + 1)
    return score
