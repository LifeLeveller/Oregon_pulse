# © 2026 Sriranjini Sridhar. All rights reserved.
# Oregon Pulse — github.com/LifeLeveller/Oregon_pulse
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "oregon_pulse.db")
OREGON_CITIES = [
    "Portland", "Salem", "Eugene", "West Linn", "Lake Oswego",
    "Bend", "Medford", "Ashland", "Corvallis", "Gresham",
    "Hillsboro", "Beaverton", "Tigard", "Tualatin", "Wilsonville"
]

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS headlines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            link TEXT UNIQUE,
            summary TEXT,
            source TEXT,
            published_at TEXT,
            fetched_at TEXT
        );

        CREATE TABLE IF NOT EXISTS weather_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            temp_f REAL,
            feels_like_f REAL,
            humidity INTEGER,
            description TEXT,
            wind_speed REAL,
            fetched_at TEXT
        );

        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            link TEXT UNIQUE,
            source TEXT,
            date TEXT,
            description TEXT,
            fetched_at TEXT
        );

        CREATE TABLE IF NOT EXISTS weather_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT,
            headline TEXT,
            severity TEXT,
            urgency TEXT,
            area_desc TEXT UNIQUE,
            description TEXT,
            effective TEXT,
            expires TEXT,
            fetched_at TEXT
        );
        CREATE TABLE IF NOT EXISTS wildfires (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            latitude REAL,
            longitude REAL,
            brightness REAL,
            confidence TEXT,
            acq_date TEXT,
            acq_time TEXT,
            fetched_at TEXT
        );
    """)

    conn.commit()
    conn.close()
    print("Database initialized at", DB_PATH)

def save_headlines(headlines):
    conn = get_connection()
    cursor = conn.cursor()
    saved = 0

    for item in headlines:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO headlines
                (title, link, summary, source, published_at, fetched_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                item["title"], item["link"], item["summary"],
                item["source"], item["published_at"], item["fetched_at"]
            ))
            if cursor.rowcount > 0:
                saved += 1
        except Exception as e:
            print(f"Error saving headline: {e}")

    conn.commit()
    conn.close()
    print(f"Saved {saved} new headlines")

def save_weather(weather):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO weather_snapshots
        (city, temp_f, feels_like_f, humidity, description, wind_speed, fetched_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        weather["city"], weather["temp_f"], weather["feels_like_f"],
        weather["humidity"], weather["description"],
        weather["wind_speed"], weather["fetched_at"]
    ))

    conn.commit()
    conn.close()
    print(f"Saved weather snapshot for {weather['city']}")

def save_events(events):
    conn = get_connection()
    cursor = conn.cursor()
    saved = 0

    for item in events:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO events
                (title, link, source, date, description, fetched_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                item["title"], item["link"], item["source"],
                item["date"], item["description"], item["fetched_at"]
            ))
            if cursor.rowcount > 0:
                saved += 1
        except Exception as e:
            print(f"Error saving event: {e}")

    conn.commit()
    conn.close()
    print(f"Saved {saved} new events")

def query_headlines(limit=20, city=None):
    conn = get_connection()
    cursor = conn.cursor()

    if city and city != "Oregon":
        cursor.execute(
            "SELECT * FROM headlines WHERE city = ? ORDER BY fetched_at DESC LIMIT ?",
            (city, limit)
        )
        rows = cursor.fetchall()
    else:
        # For All Oregon show top 3 from each city
        cities = ["Oregon", "Portland", "Salem", "Eugene", "West Linn", "Lake Oswego"]
        rows = []
        for c in cities:
            cursor.execute(
                "SELECT * FROM headlines WHERE city = ? ORDER BY fetched_at DESC LIMIT 3",
                (c,)
            )
            rows += cursor.fetchall()

    conn.close()
    return [dict(row) for row in rows]

def query_weather(limit=1):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weather_snapshots ORDER BY fetched_at DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def query_events(limit=20):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events ORDER BY fetched_at DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def detect_city(text):
    if not text:
        return "Oregon"
    text_lower = text.lower()
    for city in OREGON_CITIES:
        if city.lower() in text_lower:
            return city
    return "Oregon"

def save_headlines(headlines):
    conn = get_connection()
    cursor = conn.cursor()
    saved = 0

    for item in headlines:
        # Use city from scraper if provided, otherwise detect it
        city = item.get("city") or detect_city(item.get("title", "") + " " + item.get("summary", ""))
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO headlines
                (title, link, summary, source, published_at, fetched_at, city)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                item["title"], item["link"], item["summary"],
                item["source"], item["published_at"], item["fetched_at"], city
            ))
            if cursor.rowcount > 0:
                saved += 1
        except Exception as e:
            print(f"Error saving headline: {e}")

    conn.commit()
    conn.close()
    print(f"Saved {saved} new headlines")

def save_events(events):
    conn = get_connection()
    cursor = conn.cursor()
    saved = 0

    for item in events:
        city = detect_city(item.get("title", "") + " " + item.get("source", ""))
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO events
                (title, link, source, date, description, fetched_at, city)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                item["title"], item["link"], item["source"],
                item["date"], item["description"], item["fetched_at"], city
            ))
            if cursor.rowcount > 0:
                saved += 1
        except Exception as e:
            print(f"Error saving event: {e}")

    conn.commit()
    conn.close()
    print(f"Saved {saved} new events")

def query_events(limit=20, city=None):
    conn = get_connection()
    cursor = conn.cursor()
    if city and city != "Oregon":
        cursor.execute(
            "SELECT * FROM events WHERE city = ? ORDER BY fetched_at DESC LIMIT ?",
            (city, limit)
        )
    else:
        cursor.execute(
            "SELECT * FROM events ORDER BY fetched_at DESC LIMIT ?",
            (limit,)
        )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def save_alerts(alerts):
    conn = get_connection()
    cursor = conn.cursor()

    # Clear old alerts since these are time-sensitive and shouldn't accumulate
    cursor.execute("DELETE FROM weather_alerts")

    saved = 0
    for item in alerts:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO weather_alerts
                (event, headline, severity, urgency, area_desc, description, effective, expires, fetched_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item["event"], item["headline"], item["severity"], item["urgency"],
                item["area_desc"], item["description"], item["effective"],
                item["expires"], item["fetched_at"]
            ))
            if cursor.rowcount > 0:
                saved += 1
        except Exception as e:
            print(f"Error saving alert: {e}")

    conn.commit()
    conn.close()
    print(f"Saved {saved} active weather alerts")


def query_alerts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weather_alerts ORDER BY severity DESC, effective DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def save_wildfires(fires):
    conn = get_connection()
    cursor = conn.cursor()

    # Clear old fire data since these are point-in-time detections
    cursor.execute("DELETE FROM wildfires")

    saved = 0
    for item in fires:
        try:
            cursor.execute("""
                INSERT INTO wildfires
                (latitude, longitude, brightness, confidence, acq_date, acq_time, fetched_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                item["latitude"], item["longitude"], item["brightness"],
                item["confidence"], item["acq_date"], item["acq_time"], item["fetched_at"]
            ))
            saved += 1
        except Exception as e:
            print(f"Error saving wildfire: {e}")

    conn.commit()
    conn.close()
    print(f"Saved {saved} active fire detections")


def query_wildfires():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM wildfires ORDER BY brightness DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

if __name__ == "__main__":
    init_db()
