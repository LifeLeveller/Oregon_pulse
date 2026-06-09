# © 2026 Sriranjini Sridhar. All rights reserved.
# Oregon Pulse — github.com/LifeLeveller/Oregon_pulse
import requests
from bs4 import BeautifulSoup
from datetime import datetime

SOURCES = [
    {
        "name": "West Linn City",
        "url": "https://www.westlinnoregon.gov/calendar",
    },
    {
        "name": "Lake Oswego Events",
        "url": "https://www.ci.oswego.or.us/calendar",
    },
    {
        "name": "Oregon Live Events",
        "url": "https://www.oregonlive.com/events/",
    },
]

def scrape_page(url, source_name):
    events = []
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        selectors = [
            ".calendar-item", ".views-row", "article",
            ".event-item", ".event-card", ".tribe-event",
            "li.views-row", ".field-content"
        ]

        items = []
        for selector in selectors:
            items = soup.select(selector)
            if len(items) > 2:
                break

        if not items:
            items = soup.find_all(["article", "li"], limit=15)

        for item in items[:10]:
            title_tag = item.find(["h2", "h3", "h4", "a"])
            if not title_tag:
                continue

            title = title_tag.get_text(strip=True)

            if len(title) < 5:
                continue

            skip_words = ["home", "about", "contact", "menu", "search", "login", "sign"]
            if any(word in title.lower() for word in skip_words):
                continue

            link_tag = item.find("a", href=True)
            link = ""
            if link_tag:
                href = link_tag["href"]
                if href.startswith("http"):
                    link = href
                elif href.startswith("/"):
                    base = "/".join(url.split("/")[:3])
                    link = base + href

            date_tag = item.find(
                class_=lambda x: x and any(
                    word in x.lower() for word in ["date", "time", "when"]
                )
            )
            date = date_tag.get_text(strip=True) if date_tag else ""

            events.append({
                "title": title,
                "link": link,
                "source": source_name,
                "date": date,
                "description": "",
                "fetched_at": str(datetime.now()),
            })

    except Exception as e:
        print(f"Error scraping {source_name}: {e}")

    return events


def fetch_events():
    events = []

    for source in SOURCES:
        results = scrape_page(source["url"], source["name"])
        events += results
        print(f"{source['name']}: {len(results)} events")

    seen = set()
    unique = []
    for e in events:
        if e["title"] not in seen:
            seen.add(e["title"])
            unique.append(e)

    print(f"Fetched {len(unique)} unique events total")
    return unique


if __name__ == "__main__":
    results = fetch_events()
    for item in results:
        print(f"\n{item['source']}: {item['title']}")
        if item["date"]:
            print(f"  Date: {item['date']}")
