from flask import Blueprint, request
from homeserver.models.coasters.goals import CoasterGoal
import json
import os
from homeserver.database import db
from homeserver.utilities.constants import UPLOAD_FOLDER

coastergoals = Blueprint('coastergoals', __name__)

@coastergoals.route('/', methods=['GET', 'POST'])
def getAllGoals():
    if request.method == 'POST':
        if "title" not in request.form or "description" not in request.form:
            return json.dumps({'error': "Request must contain name and description."}), 500
        
        upload = request.files["picture"]
        mimetype = request.files["picture"].content_type
        destination = "/".join([UPLOAD_FOLDER, request.form['title']]) + "." + mimetype[6:]
        upload.save(destination)

        goal = CoasterGoal(title=request.form['title'], description=request.form['description'], progress=int(request.form["progress"]), status=int(request.form["status"]))
        db.session.add(goal)
        db.session.commit()

        return json.dumps({"success": True, "id": goal.id}), 201
    else:
        status = request.args.get('status')
        limit = request.args.get('limit')
        goals = CoasterGoal.query

        try:
            status = int(status)
            limit = int(limit)
        except ValueError:
            return json.dumps({'error': "Can't convert id to int."}), 500
        if status:
            goals.filter_by(status=status)
        if limit:
            goals.limit(limit)
        goalsSerial = []
        for goal in goals:
            goalsSerial.append(goal.as_dict())
        return json.dumps(goalsSerial)

@coastergoals.route('/<goalid>', methods=['GET', 'PUT'])
def getSpecGoal(goalid):
    try:
        goalid = int(goalid)
    except ValueError:
        return json.dumps({'error': "Can't convert id to int."}), 500
    if request.method == 'PUT':
        goal = CoasterGoal.query.get(goalid)
        if "title" in request.form:
            goal.title = request.form["title"]
        if "description" in request.form:
            goal.description = request.form["description"]
        if "progress" in request.form:
            goal.progress = int(request.form["progress"])
        if "status" in request.form:
            goal.status = int(request.form["status"])
        
        if "picture" in request.files:
            upload = request.files["picture"]
            mimetype = request.files["picture"].content_type
            destination = "/".join([UPLOAD_FOLDER, goal.title]) + "." + mimetype[6:]
            upload.save(destination)
        
        return json.dumps({"success": True, "goal": goal.as_dict()}), 200
    else:
        goal = CoasterGoal.query.get(goalid)
        if not goal:
            return {'error': "No goal found with that id"}, 404
        return json.dumps(goal.as_dict())