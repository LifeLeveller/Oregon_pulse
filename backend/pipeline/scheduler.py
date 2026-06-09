# © 2026 Sriranjini Sridhar. All rights reserved.
# Oregon Pulse — github.com/LifeLeveller/Oregon_pulse
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from apscheduler.schedulers.blocking import BlockingScheduler
from backend.pipeline.runner import run_pipeline

scheduler = BlockingScheduler()

scheduler.add_job(run_pipeline, "interval", minutes=60, id="pipeline")

print("Scheduler started. Pipeline runs every 60 minutes.")
print("Press Ctrl+C to stop.")

run_pipeline()

scheduler.start()
