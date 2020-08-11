from flask import Flask
from backend.validate import Validator

import redis
from rq import Queue

server = Flask(__name__)

r = redis.Redis()
q = Queue(connection=r)


def run_model(uid, sub_id):
    v = Validator(uid, sub_id)
    v.upload_result(v.validate())


@server.route("/", methods=['GET'])
def index():
    return "Backend Port : Pothole Detection System by Team BitFlip", 200

# will queue the uid, to be submitted to the model
@server.route("/api/submit_pic/<uid>/<sub_id>", methods=["GET"])
def submit_pic(uid,sub_id):
    if (uid != "") and (sub_id != ""):
        job = q.enqueue(run_model, uid, sub_id)
        return f"task added id : {job.id}", 200

    else:
        return "illformatted request", 200
