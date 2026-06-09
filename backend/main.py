import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.db.database import query_headlines, query_weather, query_events, init_db
from backend.pipeline.runner import run_pipeline

app = FastAPI(title="Oregon Pulse API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return {"message": "Oregon Pulse API is running"}

@app.get("/api/headlines")
def get_headlines(limit: int = 20):
    try:
        data = query_headlines(limit)
        return {"count": len(data), "headlines": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/weather")
def get_weather():
    try:
        data = query_weather(limit=1)
        if not data:
            raise HTTPException(status_code=404, detail="No weather data found")
        return data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/events")
def get_events(limit: int = 20):
    try:
        data = query_events(limit)
        return {"count": len(data), "events": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/pipeline/run")
def trigger_pipeline():
    try:
        run_pipeline()
        return {"message": "Pipeline ran successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))