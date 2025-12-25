import yfinance as yf
import json

def test_news():
    print("Fetching news for SPY...")
    spy = yf.Ticker("SPY")
    news = spy.news
    
    if news:
        print(f"Found {len(news)} news items.")
        print("First item structure:")
        print(json.dumps(news[0], indent=2))
    else:
        print("No news found via yfinance.")

if __name__ == "__main__":
    test_news()
