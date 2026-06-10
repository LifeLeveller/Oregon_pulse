# © 2026 Sriranjini Sridhar. All rights reserved.
# Oregon Pulse — github.com/LifeLeveller/Oregon_pulse
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"), override=False)

API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    from backend.config import OPENWEATHER_API_KEY
    API_KEY = OPENWEATHER_API_KEY

CITY_COORDINATES = {
    "Oregon": {"lat": 44.9429, "lon": -123.0351, "name": "Oregon (Salem)"},
    "West Linn": {"lat": 45.3651, "lon": -122.6465, "name": "West Linn"},
    "Portland": {"lat": 45.5051, "lon": -122.6750, "name": "Portland"},
    "Salem": {"lat": 44.9429, "lon": -123.0351, "name": "Salem"},
    "Eugene": {"lat": 44.0521, "lon": -123.0868, "name": "Eugene"},
    "Lake Oswego": {"lat": 45.4207, "lon": -122.7009, "name": "Lake Oswego"},
    "Bend": {"lat": 44.0582, "lon": -121.3153, "name": "Bend"},
    "Medford": {"lat": 42.3265, "lon": -122.8756, "name": "Medford"},
    "Ashland": {"lat": 42.1946, "lon": -122.7095, "name": "Ashland"},
    "Corvallis": {"lat": 44.5646, "lon": -123.2620, "name": "Corvallis"},
    "Hillsboro": {"lat": 45.5229, "lon": -122.9898, "name": "Hillsboro"},
    "Beaverton": {"lat": 45.4871, "lon": -122.8037, "name": "Beaverton"},
}

def fetch_weather(city="Oregon"):
    coords = CITY_COORDINATES.get(city, CITY_COORDINATES["Oregon"])

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": coords["lat"],
        "lon": coords["lon"],
        "appid": API_KEY,
        "units": "imperial",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if "main" not in data:
            print(f"Weather API error: {data}")
            return None

        weather = {
            "city": coords["name"],
            "temp_f": data["main"]["temp"],
            "feels_like_f": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
            "fetched_at": str(datetime.now()),
        }

        print(f"Weather in {weather['city']}: {weather['temp_f']}°F, {weather['description']}")
        return weather

    except Exception as e:
        print(f"Weather fetch failed: {e}")
        return None

if __name__ == "__main__":
    fetch_weather()