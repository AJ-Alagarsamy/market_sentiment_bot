from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(texts):
    results = []
    for text in texts:
        score = analyzer.polarity_scores(text)
        results.append({
            "text": text,
            "compound": score['compound'],
            "sentiment": categorize_score(score['compound'])
        })
    return results

def categorize_score(score):
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    else:
        return "neutral"
