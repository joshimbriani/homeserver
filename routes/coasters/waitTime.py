
import json
from flask import Blueprint, request

#from homeserver.app import db
from homeserver.models.coasters.waitTimes import CoasterWaitTime

waittime = Blueprint('waittime', __name__)

@waittime.route('/')
def getAllWaitTimes():
    return "wait time"

@waittime.route('/<int:parkid>', methods=['GET'])
def getWaitTimePark(parkid):
    if request.method == 'GET':
        #subquery = db.session.query(db.func.max(CoasterWaitTime.datetime)).group_by().subquery()
        waitTimes = CoasterWaitTime.query.filter_by(park=parkid).order_by("datetime desc").distinct(CoasterWaitTime.ride).all()
        
        waitTimesSerial = []
        for time in waitTimes:
            waitTimesSerial.append(time.as_dict())
        
        return json.dumps({ "park": parkid, "waittimes": waitTimesSerial })

@waittime.route('/<int:parkid>/<int:rideid>', methods=['GET'])
def getWaitTimeParkRide(parkid, rideid):
    if request.method == 'GET':
        limit = request.args.get('limit')
        
        try:
            if limit:
                limit = int(limit)
        except ValueError:
            return json.dumps({'error': "Can't convert limit to int."}), 500
        
        waitTimes = CoasterWaitTime.query.filter_by(ride=rideid, park=parkid).order_by("datetime desc").limit(limit).all()

        waitTimesSerial = []
        for time in waitTimes:
            waitTimesSerial.append(time.as_dict())

        return json.dumps(waitTimesSerial), 200