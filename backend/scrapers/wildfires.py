# © 2026 Sriranjini Sridhar. All rights reserved.
# Oregon Pulse — github.com/LifeLeveller/Oregon_pulse
import requests
import csv
import os
from io import StringIO
from datetime import datetime
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"), override=False)

FIRMS_MAP_KEY = os.getenv("FIRMS_MAP_KEY", "").strip().strip('"').strip("'")

# Oregon bounding box: west, south, east, north
OREGON_BBOX = "-124.6,41.9,-116.4,46.3"

def fetch_oregon_wildfires():
    if not FIRMS_MAP_KEY:
        print("No FIRMS_MAP_KEY found, skipping wildfire fetch")
        return []

    url = (
        f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/"
        f"{FIRMS_MAP_KEY}/VIIRS_SNPP_NRT/{OREGON_BBOX}/1"
    )

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        reader = csv.DictReader(StringIO(response.text))
        fires = []

        for row in reader:
            try:
                confidence = row.get("confidence", "")
                # VIIRS confidence is l/n/h (low/nominal/high)
                if confidence.lower() not in ("n", "h"):
                    continue

                fires.append({
                    "latitude": float(row["latitude"]),
                    "longitude": float(row["longitude"]),
                    "brightness": float(row.get("bright_ti4", 0)),
                    "confidence": confidence,
                    "acq_date": row.get("acq_date", ""),
                    "acq_time": row.get("acq_time", ""),
                    "fetched_at": str(datetime.now()),
                })
            except (ValueError, KeyError):
                continue

        print(f"Fetched {len(fires)} active fire detections in Oregon")
        return fires

    except Exception as e:
        print(f"Error fetching FIRMS wildfire data: {e}")
        return []


if __name__ == "__main__":
    results = fetch_oregon_wildfires()
    for item in results[:5]:
        print(f"\nFire at ({item['latitude']}, {item['longitude']}) — confidence: {item['confidence']}, date: {item['acq_date']}")