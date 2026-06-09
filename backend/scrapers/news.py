import feedparser
import requests
from datetime import datetime

OREGON_RSS_FEEDS = [
    "https://www.oregonlive.com/arc/outboundfeeds/rss/?outputType=xml",
    "https://katu.com/feed/news",
]

def fetch_oregon_news():
    headlines = []

    for url in OREGON_RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:10]:
            headlines.append({
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "summary": entry.get("summary", ""),
                "source": feed.feed.get("title", url),
                "published_at": entry.get("published", str(datetime.now())),
                "fetched_at": str(datetime.now()),
            })

    print(f"Fetched {len(headlines)} headlines")
    return headlines

if __name__ == "__main__":
    results = fetch_oregon_news()
    for item in results[:3]:
        print(f"\n{item['source']}: {item['title']}")