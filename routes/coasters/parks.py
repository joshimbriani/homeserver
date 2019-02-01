from flask import Blueprint, request
from homeserver.models.coasters.journalEntry import CoasterJournalEntry
from homeserver.models.coasters.park import CoasterPark
import json
import os
from homeserver.database import db
from homeserver.utilities.constants import UPLOAD_FOLDER
import datetime

parks = Blueprint('parks', __name__)

@parks.route('/', methods=['GET', 'POST'])
def getAllParks():
    if request.method == 'POST':

        if "title" not in request.form or "content" not in request.form or "datetime" not in request.form or "park" not in request.form:
            return json.dumps({'error': "Request must contain title, content, datetime and park."}), 500

        park = CoasterPark.query.get(request.form['park']).one()

        journal = CoasterJournalEntry(title=request.form['title'], content=request.form['content'], datetime=datetime.datetime.strptime(request.form["datetime"], "%Y-%m-%dT%H:%M:%S%z"), park=park)
        db.session.add(journal)
        db.session.commit()

        upload = request.files["picture"]
        mimetype = request.files["picture"].content_type
        destination = "/".join([UPLOAD_FOLDER, "journalEntry", journal.id]) + "." + mimetype[6:]
        upload.save(destination)

        return json.dumps({"success": True, "id": journal.id}), 201
    else:
        nameContains = request.args.get('nameContains')
        abbrev = request.args.get('abbrev')
        limit = request.args.get('limit')
        one = request.args.get('one')
        queries = []

        try:
            if limit:
                limit = int(limit)
        except ValueError:
            return json.dumps({'error': "Can't convert id to int."}), 500
        if nameContains:
            queries.append(CoasterPark.name.startswith(nameContains))
        if abbrev:
            queries.append(CoasterPark.abbrev == abbrev)
        
        result = db.session.query(CoasterPark).filter(*queries)
        if limit:
            result.limit(limit)
        if one:
            return json.dumps(result[0].as_dict())
        parksSerial = []
        for park in result:
            parksSerial.append(park.as_dict())
        return json.dumps(parksSerial)

@parks.route('/<parkid>', methods=['GET', 'PUT'])
def getSpecPark(parkid):
    try:
        parkid = int(parkid)
    except ValueError:
        return json.dumps({'error': "Can't convert id to int."}), 500
    if request.method == 'PUT':
        pass
        journal = CoasterJournalEntry.query.get(journalid)
        
        if "title" in request.form:
            journal.title = request.form["title"]
        if "content" in request.form:
            journal.content = request.form["content"]
        if "datetime" in request.form:
            journal.datetime = datetime.datetime.strptime(request.form["datetime"], "%Y-%m-%dT%H:%M:%S%z")
        if "park" in request.form:
            park = CoasterPark.query.get(request.form['park']).one()
            journal.park = park
        
        if "picture" in request.files:
            upload = request.files["picture"]
            mimetype = request.files["picture"].content_type
            destination = "/".join([UPLOAD_FOLDER, "journalEntry", journal.id]) + "." + mimetype[6:]
            upload.save(destination)

        db.session.add(journal)
        db.session.commit()
        
        return json.dumps({"success": True, "goal": journal.as_dict()}), 200
    else:
        park = CoasterPark.query.get(parkid)
        if not park:
            return {'error': "No park found with that id"}, 404
        return json.dumps(park.as_dict())