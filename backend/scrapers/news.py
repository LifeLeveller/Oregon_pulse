# © 2026 Sriranjini Sridhar. All rights reserved.
# Oregon Pulse — github.com/LifeLeveller/Oregon_pulse
import feedparser
from datetime import datetime

CITY_FEEDS = {
    "Oregon": [
        "https://www.oregonlive.com/arc/outboundfeeds/rss/?outputType=xml",
        "https://www.opb.org/rss/",
    ],
    "Portland": [
        "https://www.portlandmercury.com/portland/Rss.xml",
    ],
    "Salem": [
        "https://www.salemreporter.com/feed",
    ],
    "Eugene": [
        "https://www.eugeneweekly.com/feed",
    ],
    "West Linn": [
        "https://westlinntidings.com/feed",
    ],
    "Lake Oswego": [
        "https://lakeoswegoreview.com/feed",
    ],
}

def fetch_city_news(city, urls):
    headlines = []

    for url in urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]:
                title = entry.get("title", "")
                summary = entry.get("summary", "")

                headlines.append({
                    "title": title,
                    "link": entry.get("link", ""),
                    "summary": summary,
                    "source": feed.feed.get("title", url),
                    "city": city,
                    "published_at": entry.get("published", str(datetime.now())),
                    "fetched_at": str(datetime.now()),
                })
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    return headlines


def fetch_oregon_news():
    headlines = []

    for city, urls in CITY_FEEDS.items():
        city_headlines = fetch_city_news(city, urls)
        headlines += city_headlines
        print(f"{city}: {len(city_headlines)} headlines")

    print(f"Fetched {len(headlines)} headlines total")
    return headlines


if __name__ == "__main__":
    results = fetch_oregon_news()
    for item in results[:5]:
        print(f"\n{item['city']} — {item['source']}: {item['title'][:60]}")