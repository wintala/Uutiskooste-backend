from apscheduler.schedulers.blocking import BlockingScheduler
from main import Hour
from datafetchers.fetch_all import fetch_all

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=30)
def scrape_info_to_db():
    print("SAVING")
    Hour(data=fetch_all()).save()

sched.start()