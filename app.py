from flask import Flask, request, jsonify
from datafetchers.fetch_all import fetch_all
import datetime
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from flask_mongoengine import MongoEngine
from flask_cors import CORS, cross_origin
import config

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


app.config["MONGODB_HOST"] = config.DB_URI
db = MongoEngine(app)

class Hour(db.Document):
    time = db.DateTimeField(default=datetime.datetime.utcnow)
    data = db.DictField()

def scrape_info_to_db():
    print("SAVING")
    Hour(data=fetch_all()).save()

scheduler = BackgroundScheduler()
scheduler.add_job(func=scrape_info_to_db, trigger="interval", next_run_time=datetime.datetime.now(), hours=1)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())


@app.route("/api/current", methods=["GET"])
@cross_origin()
def get():
    result = Hour.objects.order_by("-time").first()
    print(len(Hour.objects))
    return {"time": result.time, "id": str(result.id), "data": result.data}

@app.route("/api/metadata", methods=["GET"])
@cross_origin()
def meta_data():
    return {"numberOfRecords": len(Hour.objects)}


@app.route("/api/range", methods=["GET"])
@cross_origin()
def list():
    start = int(request.args.get('start'))
    finnish = int(request.args.get('finnish'))
    try:
        result_list = Hour.objects.order_by("-time")[start - 1: finnish]
    except(IndexError):
        return {"error": "invalid incesies"}, 400
    return jsonify([{"time": result.time, "id": str(result.id), "data": result.data} for result in result_list])


if __name__ == "__main__":
    app.run()