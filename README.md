# Oregon Pulse

A full stack data engineering project that scrapes and displays live Oregon news headlines, weather conditions, local community events, weather alerts, and active wildfire detections on a clean dashboard. Filter by 6 Oregon cities with live weather updates per city.

**Live demo:** https://oregon-pulse.vercel.app
**Backend API:** https://web-production-2d93c.up.railway.app

© 2026 Sriranjini Sridhar. All rights reserved.

---

## What it does

- Scrapes city-specific Oregon news headlines from 6 dedicated local RSS feeds
- Fetches live weather data for any selected Oregon city via OpenWeatherMap API
- Surfaces live weather alerts (Red Flag Warnings, Extreme Heat Watches, and other active NWS alerts) for Oregon via the National Weather Service API
- Displays active wildfire detections across Oregon via NASA's FIRMS satellite system
- Scrapes local events from West Linn City and Lake Oswego city websites
- Filters news, weather and events by Oregon city via a city selector
- Stores all data in SQLite with deduplication so no duplicate rows ever appear
- Runs the entire pipeline automatically every 6 hours via GitHub Actions
- Exposes all data via a FastAPI REST API
- Displays everything on a React dashboard with an Oregon landscape banner and an urgent alert banner when active warnings exist

---

## Tech stack

| Layer | Technology |
|---|---|
| Scraping | Python, BeautifulSoup, feedparser, requests |
| Pipeline | APScheduler, python-dotenv |
| Database | SQLite |
| Backend API | FastAPI, Uvicorn |
| Proxy server | Node.js, Express |
| Frontend | React, Vite, React Query, Axios |
| External data sources | OpenWeatherMap, National Weather Service (NOAA), NASA FIRMS |
| CI/CD | GitHub Actions |
| Deployment | Railway (backend), Vercel (frontend) |

---

## Project structure

```
Oregon_pulse/
├── backend/
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── news.py          # City-specific Oregon news via RSS feeds
│   │   ├── weather.py       # Live weather per city via OpenWeatherMap
│   │   ├── events.py        # Local events via web scraping
│   │   ├── alerts.py        # Live weather alerts via National Weather Service API
│   │   └── wildfires.py     # Active fire detections via NASA FIRMS
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── runner.py        # Runs all scrapers and saves to DB
│   │   └── scheduler.py     # Runs pipeline every 60 minutes locally
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py      # SQLite connection, schema, queries
│   │   └── oregon_pulse.db  # SQLite database
│   ├── config.py            # Fallback config for deployment (API key safety net)
│   ├── main.py              # FastAPI app
│   └── .env                 # API keys (not committed)
├── server/
│   ├── index.js             # Node.js Express proxy server
│   ├── package.json
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── index.js     # Axios API calls with city parameter
│   │   ├── components/
│   │   │   ├── WeatherCard.jsx
│   │   │   ├── NewsFeed.jsx
│   │   │   ├── EventsList.jsx
│   │   │   ├── CityFilter.jsx
│   │   │   ├── AlertBanner.jsx     # Urgent NWS alert banner
│   │   │   └── WildfireWidget.jsx  # Active wildfire detections card
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── vite.config.js
│   └── package.json
├── .github/
│   └── workflows/
│       └── pipeline.yml     # GitHub Actions scheduled pipeline
├── Procfile                 # Railway deployment config
├── runtime.txt              # Python version for Railway
├── railway.toml             # Railway build config
├── requirements.txt         # Python dependencies
└── .gitignore
```

---

## Supported cities

| City | News Source | Weather | Events |
|---|---|---|---|
| All Oregon | OregonLive, OPB | Yes | All |
| Portland | Portland Mercury | Yes | No |
| Salem | Salem Reporter | Yes | No |
| Eugene | Eugene Weekly | Yes | No |
| West Linn | West Linn Tidings | Yes | Yes |
| Lake Oswego | Lake Oswego Review | Yes | Yes |

Weather alerts and wildfire detections cover the entire state of Oregon regardless of the selected city filter, since both are statewide public safety data sources.

---

## Public safety data sources

**Weather alerts** are pulled from `api.weather.gov`, the National Weather Service's free public API. No API key is required since this is fully open government data. Active alerts (Red Flag Warnings, Extreme Heat Watches, Severe Thunderstorm Warnings, and others) are filtered to Oregon and surfaced in an urgent banner at the top of the dashboard whenever any are active.

**Wildfire detections** are pulled from NASA's FIRMS (Fire Information for Resource Management System), the same near real-time satellite detection system used by the USDA Forest Service and emergency managers. Detections use VIIRS satellite thermal imaging filtered to a bounding box covering Oregon, with a confidence threshold applied so only nominal and high confidence detections are shown. Requires a free FIRMS MAP_KEY.

---

## Data engineering concepts covered

**ETL Pipeline**
Extract data from multiple sources (RSS feeds, REST APIs, HTML pages, government open-data APIs), transform it into a clean consistent structure, and load it into SQLite.

**Idempotent ingestion**
Using `INSERT OR IGNORE` with a `UNIQUE` constraint on the `link` column means running the pipeline multiple times never creates duplicate rows. This is a core data engineering pattern.

**City-based data tagging**
Each headline is tagged with its source city at ingest time based on which RSS feed it came from. This enables fast city-based filtering at query time without scanning full article content.

**Time-sensitive data handling**
Weather alerts and wildfire detections are point-in-time data rather than accumulating history, so each pipeline run clears and replaces these tables rather than appending, ensuring the dashboard only ever shows currently active alerts and detections.

**Geospatial filtering**
Wildfire detections are filtered using a latitude/longitude bounding box covering Oregon's borders, a common geospatial data engineering pattern for scoping satellite or sensor data to a region.

**Scheduled jobs**
GitHub Actions runs the pipeline every 6 hours automatically, keeping data fresh without any manual intervention. APScheduler handles local scheduling during development.

**Time series data**
Weather snapshots are stored as a time series. Every run saves a new row with a timestamp, allowing you to query temperature trends over time.

**Deduplication**
Each scraper filters out navigation links, short titles, and previously seen records before saving to the database.

**Graceful degradation**
The wildfire widget and alert banner are both designed to handle the zero-result case cleanly (most days have no active fires or alerts), rather than treating an empty result as an error state.

---

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/api/headlines?city=Portland` | News headlines filtered by city |
| GET | `/api/weather?city=Portland` | Live weather for selected city |
| GET | `/api/events?city=West Linn` | Local events filtered by city |
| GET | `/api/alerts` | Active NWS weather alerts for Oregon |
| GET | `/api/wildfires` | Active wildfire detections in Oregon |
| POST | `/api/pipeline/run` | Manually trigger the pipeline |

Interactive API docs available at `/docs` (FastAPI Swagger UI).

---

## Database schema

```sql
CREATE TABLE headlines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    link TEXT UNIQUE,
    summary TEXT,
    source TEXT,
    published_at TEXT,
    fetched_at TEXT,
    city TEXT DEFAULT 'Oregon'
);

CREATE TABLE weather_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    temp_f REAL,
    feels_like_f REAL,
    humidity INTEGER,
    description TEXT,
    wind_speed REAL,
    fetched_at TEXT
);

CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    link TEXT UNIQUE,
    source TEXT,
    date TEXT,
    description TEXT,
    fetched_at TEXT,
    city TEXT DEFAULT 'Oregon'
);

CREATE TABLE weather_alerts (
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

CREATE TABLE wildfires (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    latitude REAL,
    longitude REAL,
    brightness REAL,
    confidence TEXT,
    acq_date TEXT,
    acq_time TEXT,
    fetched_at TEXT
);
```

---

## Local setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- OpenWeatherMap API key (free at openweathermap.org)
- NASA FIRMS MAP_KEY (free at firms.modaps.eosdis.nasa.gov/api/map_key)

### Quick start

A `start.sh` script starts all three services at once:

```bash
./start.sh
```

Open http://localhost:5173 in your browser.

### Manual setup

**Backend:**

```bash
git clone https://github.com/LifeLeveller/Oregon_pulse.git
cd Oregon_pulse

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

echo "OPENWEATHER_API_KEY=your_key_here
FIRMS_MAP_KEY=your_key_here" > backend/.env

python backend/pipeline/runner.py
uvicorn backend.main:app --reload --port 8000
```

**Node server:**

```bash
cd server
npm install
echo "PORT=3001
FASTAPI_URL=http://localhost:8000" > .env
node index.js
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

---

## Deployment

### Backend on Railway

1. Push code to GitHub
2. Create new project on Railway from GitHub repo
3. Add environment variables: `OPENWEATHER_API_KEY`, `FIRMS_MAP_KEY`
4. Railway detects `Procfile` and deploys automatically
5. Generate a public domain under Settings > Networking

A fallback config (`backend/config.py`) is included as a safety net in case Railway's environment variable injection is unreliable, since this was observed during development on the free tier.

### Frontend on Vercel

1. Import GitHub repo on Vercel
2. Set root directory to `frontend`
3. Add environment variable: `VITE_API_URL=https://your-railway-url.up.railway.app/api`
4. Deploy

### Scheduled pipeline via GitHub Actions

Add `OPENWEATHER_API_KEY` and `FIRMS_MAP_KEY` to your GitHub repo secrets under Settings > Secrets > Actions. The pipeline runs every 6 hours automatically and commits the updated database back to the repo.

---

## Architecture

```
Browser
  └── Vercel (React frontend)
        └── /api/* requests with ?city= filter
              └── Railway (FastAPI)
                    └── SQLite database (city-tagged records)
                          └── Python pipeline (runs every 6 hours via GitHub Actions)
                                ├── City-specific RSS feeds (6 Oregon cities)
                                ├── OpenWeatherMap API (live per city)
                                ├── National Weather Service API (statewide alerts)
                                ├── NASA FIRMS (statewide wildfire detections)
                                └── West Linn / Lake Oswego city websites
```

---

## What I learned

- Building a real ETL pipeline from scratch with Python
- Scraping RSS feeds and HTML pages with feedparser and BeautifulSoup
- Designing a SQLite schema with city tagging and deduplication patterns
- Building a REST API with FastAPI including query parameter filtering
- Setting up a Node.js Express proxy server
- Fetching and caching data in React with React Query
- Deploying a full stack app across Railway and Vercel
- Debugging CORS issues between services on different domains
- Managing environment variables across local, Railway, and Vercel
- Productionalising a project teaches more than any tutorial
- GitHub Actions for automated scheduled data pipelines
- Real production debugging: environment variables not injecting, RSS feeds going down, database records with wrong tags
- Integrating with official government open-data APIs (NOAA/NWS, NASA FIRMS) rather than only commercial ones
- Geospatial filtering with bounding boxes for satellite-derived data
- Designing UI for urgent, time-sensitive content (a banner that only appears when something matters) versus regular static content
- Handling zero-result states gracefully rather than treating them as errors

---

## Future improvements

- 5-day weather forecast widget
- Data refresh button on the dashboard
- Charts showing temperature trends over time using weather snapshots
- Map visualization for wildfire detections instead of a list
- Search bar to filter headlines
- PostgreSQL for production-grade persistence
- More Oregon cities and news sources

---

## Built with

This project was built as a portfolio project by Sriranjini Sridhar to learn full stack data engineering concepts including ETL pipelines, REST APIs, React, cloud deployment, and integration with public government data sources.