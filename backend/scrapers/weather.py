# © 2026 Sriranjini Sridhar. All rights reserved.
# Oregon Pulse — github.com/LifeLeveller/Oregon_pulse
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

API_KEY = os.getenv("OPENWEATHER_API_KEY")

WEST_LINN_LAT = 45.3651
WEST_LINN_LON = -122.6465

def fetch_weather():
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": WEST_LINN_LAT,
        "lon": WEST_LINN_LON,
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
            "city": data["name"],
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
