import yfinance as yf
from datetime import datetime

def get_stock_data(ticker: str) -> dict | None:
    """Fetch current stock price and metadata using yfinance."""
    try:
        stock = yf.Ticker(ticker)
        # Attempt real-time price
        price = None
        if hasattr(stock, 'fast_info') and hasattr(stock.fast_info, 'last_price'):
            price = stock.fast_info.last_price
        if price is None:
            info = stock.info
            price = info.get('regularMarketPrice')
        if price is None:
            hist = stock.history(period='1d')
            if not hist.empty:
                price = hist['Close'].iloc[-1]
        if price is None:
            return None
        return {
            'price': float(price),
            'currency': stock.info.get('currency', 'USD'),
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source': 'yfinance'
        }
    except Exception as e:
        print(f"[sentiment_model] Error fetching data for {ticker}: {e}")
        return None


def get_trade_recommendation(ticker: str, sentiment_score: int) -> dict:
    """
    Generate a trading recommendation based on sentiment score.
    Returns dict with keys:
      - label
      - expected_return
      - confidence
      - message
      - current_price
      - target_price
      - stop_loss
      - timestamp
      - data_source
    """
    # Define sentiment-to-metrics mapping
    mapping = [
        ('Strong Buy', 80, 7.0, 90),
        ('Buy',        60, 4.0, 75),
        ('Hold',       50, 0.0, 50),
        ('Sell',       45, -4.0, 70),
        ('Strong Sell',0, -7.0, 90),
    ]
    # Select profile
    label = None
    expected_return = 0.0
    confidence = 50
    for lbl, min_score, exp_ret, conf in mapping:
        if sentiment_score >= min_score:
            label = lbl
            expected_return = exp_ret
            confidence = conf
            break
    if label is None:
        label, expected_return, confidence = 'Hold', 0.0, 50

    # Fetch stock data
    stock_data = get_stock_data(ticker)
    if not stock_data:
        return {
            'label': 'Data Error',
            'expected_return': None,
            'confidence': None,
            'message': f"Could not retrieve price data for {ticker}",
            'current_price': None,
            'target_price': None,
            'stop_loss': None,
            'timestamp': None,
            'data_source': None
        }
    price = stock_data['price']
    currency = stock_data['currency']
    ts = stock_data['time']
    src = stock_data['source']

    # Compute targets
    target_price = None
    stop_loss = None
    if label in ['Strong Buy', 'Buy']:
        target_price = round(price * (1 + expected_return/100), 2)
        stop_loss = round(price * (1 - 0.02), 2)
    elif label == 'Strong Sell':
        target_price = round(price * (1 + expected_return/100), 2)

    # Form message
    if label in ['Strong Buy', 'Buy']:
        message = f"{label}: buy {ticker} at {currency}{price:.2f}, target {currency}{target_price:.2f} (+{expected_return:.1f}%), stop-loss {currency}{stop_loss:.2f}."
    elif label == 'Hold':
        message = f"Hold: neutral sentiment for {ticker}, current price {currency}{price:.2f}."
    elif label == 'Sell':
        message = f"Sell: consider reducing exposure to {ticker} at {currency}{price:.2f}."
    else:  # Strong Sell
        message = f"Strong Sell: sell {ticker} at {currency}{price:.2f}, target downside to {currency}{target_price:.2f} ({expected_return:.1f}%)."

    return {
        'label': label,
        'expected_return': expected_return,
        'confidence': confidence,
        'message': message,
        'current_price': round(price, 2),
        'target_price': target_price,
        'stop_loss': stop_loss,
        'timestamp': ts,
        'data_source': src
    }
