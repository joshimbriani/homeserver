from flask import Blueprint, request
from crontab import CronTab
from homeserver.utilities.cronCreator import CronCreator

from homeserver.models.jobs.job import Job

jobs = Blueprint('jobs', __name__)

@jobs.route('/', methods=['GET', 'POST'])
def getCreateJobs():
    if request.method == 'POST':
        if "name" not in request.form or "pythonFile" not in request.form or "description" not in request.form or "cronString" not in request.form or "active" not in request.form:
            return json.dumps({ "success": False, "error": "Missing argument" }), 400
        job = Job(name=request.form["name"], pythonFile=request.form["pythonFile"], description=request.form["description"], cronString=request.form["cronString"], active=request.form["active"] == "True")

        db.session.add(job)
        db.session.commit()
        
        cron = CronTab()
        c = CronCreator.create(c, job.description, job.pythonFile, job.cronString)
        c.enable(job.active)
        c.write()

        return json.dumps({"success": True, "id": job.id}), 201 
    else:
        active = request.args.get('active')
        queries = []

        if active:
            queries.append((Job.active == "True") == active)
        
        result = db.session.query(Job).filter(*queries)
        jobsSerial = []
        for job in result:
            jobsSerial.append(job.as_dict())
        return json.dumps(jobsSerial)

@jobs.route('/<jobid>', methods=['GET', 'PUT', 'DELETE'])
def getEditDeleteJob(jobid):
    try:
        jobid = int(jobid)
    except ValueError:
        return json.dumps({'error': "Can't convert id to int."}), 500

    job = Job.query.get(jobid)

    if request.method == 'PUT':
        if "name" in request.form:
            job.name = request.form["name"]
        if "pythonFile" in request.form:
            job.pythonFile = request.form["pythonFile"]
        if "description" in request.form:
            job.description = request.form["description"]
        if "cronString" in request.form:
            job.cronString = request.form["cronString"]
        if "active" in request.form:
            job.active = request.form["active"] == "True"

        db.session.add(job)
        db.session.commit()
        
        return json.dumps({"success": True, "job": job.as_dict()}), 200
    elif request.method == 'DELETE':
        db.session.delete(job)
        db.session.commit()

        return json.dumps({ "success": True }), 200 
    else:
        return json.dumps(job.as_dict()), 200
    