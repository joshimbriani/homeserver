from flask import Blueprint, request
from homeserver.models.coasters.journalEntry import CoasterJournalEntry
from homeserver.models.coasters.park import CoasterPark
import json
import os
from homeserver.database import db
from homeserver.utilities.constants import UPLOAD_FOLDER
import datetime

tripjournals = Blueprint('tripjournals', __name__)

@tripjournals.route('/', methods=['GET', 'POST'])
def getAllJournals():
    if request.method == 'POST':
        if "title" not in request.form or "content" not in request.form or "datetime" not in request.form or "park" not in request.form:
            return json.dumps({'error': "Request must contain title, content, datetime and park."}), 500

        park = CoasterPark.query.get(request.form['park'])

        journal = CoasterJournalEntry(title=request.form['title'], content=request.form['content'], datetime=datetime.datetime.strptime(request.form["datetime"], "%Y-%m-%dT%H:%M:%S.%fZ"))
        journal.park = park.id
        db.session.add(journal)
        db.session.commit()

        upload = request.files["picture"]
        mimetype = request.files["picture"].content_type
        destination = "/".join([UPLOAD_FOLDER, "themeparks/journalEntry", str(journal.id)]) + "." + mimetype[6:]
        upload.save(destination)

        return json.dumps({"success": True, "id": journal.id}), 201
    else:
        limit = request.args.get('limit')
        journals = CoasterJournalEntry.query

        try:
            if limit:
                limit = int(limit)
        except ValueError:
            return json.dumps({'error': "Can't convert id to int."}), 500
        if limit:
            journals.limit(limit)
        journalsSerial = []
        for journal in journals:
            journalsSerial.append(journal.as_dict())
        return json.dumps(journalsSerial)

@tripjournals.route('/<int:journalid>', methods=['GET', 'PUT', 'DELETE'])
def getSpecJournal(journalid):
    try:
        journalid = int(journalid)
    except ValueError:
        return json.dumps({'error': "Can't convert id to int."}), 500
    if request.method == 'PUT':
        journal = CoasterJournalEntry.query.get(journalid)
        
        if "title" in request.form:
            journal.title = request.form["title"]
        if "content" in request.form:
            journal.content = request.form["content"]
        if "datetime" in request.form:
            journal.datetime = datetime.datetime.strptime(request.form["datetime"], "%Y-%m-%dT%H:%M:%S.%fZ")
        if "park" in request.form:
            park = CoasterPark.query.get(request.form['park'])
            journal.park = park.id
        
        if "picture" in request.files:
            upload = request.files["picture"]
            mimetype = request.files["picture"].content_type
            destination = "/".join([UPLOAD_FOLDER, "themeparks/journalEntry", str(journal.id)]) + "." + mimetype[6:]
            upload.save(destination)

        db.session.add(journal)
        db.session.commit()
        
        return json.dumps({"success": True, "journal": journal.as_dict()}), 200
    elif request.method == 'DELETE':
        journal = CoasterJournalEntry.query.get(journalid)
        db.session.delete(journal)
        db.session.commit()

        return json.dumps({ "success": True }), 200 
    else:
        journal = CoasterJournalEntry.query.get(journalid)
        if not journal:
            return {'error': "No journal found with that id"}, 404
        return json.dumps(journal.as_dict())