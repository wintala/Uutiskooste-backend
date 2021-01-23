from apscheduler.schedulers.blocking import BlockingScheduler
from app import Hour
from datetime import datetime
from datafetchers.fetch_all import fetch_all
import requests

sched = BlockingScheduler()

@sched.scheduled_job('interval', hours=1, next_run_time=datetime.now())
def scrape_info_to_db():
    #print("SAVING")
    Hour(data=fetch_all()).save()

@sched.scheduled_job('interval', minutes=20)
def prevent_free_tier_sleeping():
    requests.get("http://top5uutiset.herokuapp.com/api/metadata")


sched.start()