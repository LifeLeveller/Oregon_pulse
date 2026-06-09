# Oregon Pulse

A full stack data engineering project that scrapes and displays live Oregon news headlines, West Linn weather conditions, and local community events on a clean dashboard.

**Live demo:** https://oregon-pulse.vercel.app
**Backend API:** https://web-production-2d93c.up.railway.app

---

## What it does

- Scrapes Oregon news headlines from OregonLive RSS feeds
- Fetches live weather data for West Linn, Oregon via OpenWeatherMap API
- Scrapes local events from West Linn City and Lake Oswego city websites
- Stores all data in SQLite with deduplication so no duplicate rows ever appear
- Runs the entire pipeline automatically every hour via a scheduler
- Exposes all data via a FastAPI REST API
- Displays everything on a React dashboard

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
| Deployment | Railway (backend), Vercel (frontend) |

---

## Project structure

```
oregon-pulse/
├── backend/
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── news.py          # Oregon news via RSS
│   │   ├── weather.py       # West Linn weather via OpenWeatherMap
│   │   └── events.py        # Local events via web scraping
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── runner.py        # Runs all scrapers and saves to DB
│   │   └── scheduler.py     # Runs pipeline every 60 minutes
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py      # SQLite connection, schema, queries
│   │   └── oregon_pulse.db  # SQLite database
│   ├── main.py              # FastAPI app
│   └── .env                 # API keys (not committed)
├── server/
│   ├── index.js             # Node.js Express proxy server
│   ├── package.json
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── index.js     # Axios API calls
│   │   ├── components/
│   │   │   ├── WeatherCard.jsx
│   │   │   ├── NewsFeed.jsx
│   │   │   └── EventsList.jsx
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── vite.config.js
│   └── package.json
├── Procfile                 # Railway deployment config
├── runtime.txt              # Python version for Railway
├── requirements.txt         # Python dependencies
└── .gitignore
```

---

## Data engineering concepts covered

**ETL Pipeline**
Extract data from multiple sources (RSS feeds, REST APIs, HTML pages), transform it into a clean consistent structure, and load it into SQLite.

**Idempotent ingestion**
Using `INSERT OR IGNORE` with a `UNIQUE` constraint on the `link` column means running the pipeline multiple times never creates duplicate rows. This is a core data engineering pattern.

**Scheduled jobs**
APScheduler runs the pipeline every 60 minutes automatically, keeping data fresh without any manual intervention.

**Time series data**
Weather snapshots are stored as a time series. Every run saves a new row with a timestamp, allowing you to query temperature trends over time.

**Deduplication**
Each scraper filters out navigation links, short titles, and previously seen records before saving to the database.

---

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/api/headlines` | Latest Oregon news headlines |
| GET | `/api/weather` | Current West Linn weather |
| GET | `/api/events` | Local West Linn and Lake Oswego events |
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
    fetched_at TEXT
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
    fetched_at TEXT
);
```

---

## Local setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- OpenWeatherMap API key (free at openweathermap.org)

### Backend setup

```bash
# Clone the repo
git clone https://github.com/LifeLeveller/Oregon_pulse.git
cd Oregon_pulse

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Mac/Linux

# Install Python dependencies
pip install -r requirements.txt

# Create .env file
echo "OPENWEATHER_API_KEY=your_key_here" > backend/.env

# Initialize database and run pipeline
python backend/pipeline/runner.py

# Start FastAPI server
uvicorn backend.main:app --reload --port 8000
```

### Node server setup

```bash
cd server
npm install
echo "PORT=3001
FASTAPI_URL=http://localhost:8000" > .env
node index.js
```

### Frontend setup

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 in your browser.

---

## Deployment

### Backend on Railway

1. Push code to GitHub
2. Create new project on Railway from GitHub repo
3. Add environment variable: `OPENWEATHER_API_KEY`
4. Railway detects `Procfile` and deploys automatically
5. Generate a public domain under Settings > Networking

### Frontend on Vercel

1. Import GitHub repo on Vercel
2. Set root directory to `frontend`
3. Add environment variable: `VITE_API_URL=https://your-railway-url.up.railway.app/api`
4. Deploy

---

## Architecture

```
Browser
  └── Vercel (React frontend)
        └── /api/* requests
              └── Railway (FastAPI)
                    └── SQLite database
                          └── Python pipeline (runs every hour)
                                ├── OregonLive RSS feed
                                ├── OpenWeatherMap API
                                └── West Linn / Lake Oswego websites
```

---

## What I learned

- Building a real ETL pipeline from scratch with Python
- Scraping RSS feeds and HTML pages with feedparser and BeautifulSoup
- Designing a SQLite schema with deduplication patterns
- Building a REST API with FastAPI and automatic Swagger docs
- Setting up a Node.js Express proxy server
- Fetching and caching data in React with React Query
- Deploying a full stack app across Railway and Vercel
- Debugging CORS issues between services
- Managing environment variables across local and production environments

---

## Future improvements

- Filter news and events by Oregon city
- 5-day weather forecast widget
- Data refresh button on the dashboard
- Charts showing temperature trends over time
- More Oregon news sources
- Search bar to filter headlines
- PostgreSQL for production-grade persistence

---

## Built with

This project was built as a portfolio project to learn full stack data engineering concepts including ETL pipelines, REST APIs, React, and cloud deployment.
