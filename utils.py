def summarize_results(results):
    summary = {"positive": 0, "neutral": 0, "negative": 0}
    for r in results:
        summary[r["sentiment"]] += 1
    return summary

def print_report(source, results, summary):
    print(f"\n--- {source.upper()} Sentiment Summary ---")
    for key, val in summary.items():
        print(f"{key.capitalize()}: {val}")

    print(f"\n--- {source.upper()} Posts ---")
    for r in results:
        print(f"[{r['sentiment'].upper()}] {r['text']} (Score: {r['compound']:.2f})")
