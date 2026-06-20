# © 2026 Sriranjini Sridhar. All rights reserved.
# Oregon Pulse — github.com/LifeLeveller/Oregon_pulse
import requests
from datetime import datetime

NWS_ALERTS_URL = "https://api.weather.gov/alerts/active"

def fetch_oregon_alerts():
    headers = {"User-Agent": "OregonPulse (oregon-pulse.vercel.app)"}
    params = {"area": "OR"}

    try:
        response = requests.get(NWS_ALERTS_URL, headers=headers, params=params, timeout=10)
        data = response.json()

        alerts = []
        for feature in data.get("features", []):
            props = feature.get("properties", {})
            alerts.append({
                "event": props.get("event", ""),
                "headline": props.get("headline", ""),
                "severity": props.get("severity", "Unknown"),
                "urgency": props.get("urgency", "Unknown"),
                "area_desc": props.get("areaDesc", ""),
                "description": (props.get("description", "") or "")[:300],
                "effective": props.get("effective", ""),
                "expires": props.get("expires", ""),
                "fetched_at": str(datetime.now()),
            })

        print(f"Fetched {len(alerts)} active Oregon weather alerts")
        return alerts

    except Exception as e:
        print(f"Error fetching NWS alerts: {e}")
        return []


if __name__ == "__main__":
    results = fetch_oregon_alerts()
    for item in results[:5]:
        print(f"\n[{item['severity']}] {item['event']}: {item['headline']}")