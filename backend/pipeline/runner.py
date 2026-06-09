# © 2026 Sriranjini Sridhar. All rights reserved.
# Oregon Pulse — github.com/LifeLeveller/Oregon_pulse
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from backend.scrapers.news import fetch_oregon_news
from backend.scrapers.events import fetch_events
from backend.scrapers.weather import fetch_weather
from backend.db.database import init_db, save_headlines, save_events, save_weather

def run_pipeline():
    print("\n--- Oregon Pulse Pipeline ---")
    print("Initializing database...")
    init_db()

    print("\nFetching news...")
    headlines = fetch_oregon_news()
    save_headlines(headlines)

    print("\nFetching weather...")
    weather = fetch_weather()
    if weather:
        save_weather(weather)

    print("\nFetching events...")
    events = fetch_events()
    save_events(events)

    print("\nPipeline complete.")

if __name__ == "__main__":
    run_pipeline()
