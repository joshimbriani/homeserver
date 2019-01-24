from flask import Blueprint, request
from models.coasters.goals import CoasterGoal
import json

coastergoals = Blueprint('coastergoals', __name__)

@coastergoals.route('/', methods=['GET', 'POST'])
def getAllGoals():
    if request.method == 'POST':
        return ""
    else:
        goals = CoasterGoal.query.all()
        return json.dumps(goals)

@coastergoals.route('/<goalid>', methods=['GET', 'PUT'])
def getSpecGoal(goalid):
    try:
        goalid = int(goalid)
    except ValueError:
        return {'error': "Can't convert id to int."}, 500
    if request.method == 'PUT':
        return ""
    else:
        goal = CoasterGoal.query.get(goalid)
        if not goal:
            return {'error': "No goal found with that id"}, 404
        return json.dumps(goal)