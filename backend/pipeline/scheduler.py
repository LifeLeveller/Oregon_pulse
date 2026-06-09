import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from apscheduler.schedulers.blocking import BlockingScheduler
from backend.pipeline.runner import run_pipeline

scheduler = BlockingScheduler()

# News and events every 60 minutes
scheduler.add_job(run_pipeline, "interval", minutes=60, id="pipeline")

print("Scheduler started. Pipeline runs every 60 minutes.")
print("Press Ctrl+C to stop.\n")

# Run once immediately on start
run_pipeline()

scheduler.start()