from homeserver.models.coasters.park import CoasterPark
from homeserver.models.coasters.ride import CoasterRide
from homeserver.models.coasters.coasterTrack import CoasterTrack
from homeserver.database import db
from homeserver.app import app

from sqlalchemy.orm.exc import NoResultFound

import json
import re

coasters = []
parks = []

with open('data/combined.json') as data:
    data = json.load(data)
    for coaster in data["coasters"]:
        coasters.append(coaster)
    for park in data["parks"]:
        parks.append(park)

with app.app_context():
    for park in parks:
        status = park["status"]
        if status == "Defunct":
            status = 2
        elif status == "SBNO":
            status = 3
        else:
            status = 1
        #pk = CoasterPark(name=park["name"], rcdbID=park["rcdbId"], status=status, address=park["address"], openDate=park["openDate"], statusDate=park["statusDate"])
        
        #db.session.add(pk)

    db.session.commit()

    badParks = set()

    for coaster in coasters:
        status = coaster["status"]
        if status == "Defunct":
            status = 2
        else:
            status = 1

        try:
            park = CoasterPark.query.filter_by(rcdbID=coaster["parkid"]).one()
            cstr = CoasterRide(park=park.id, name=coaster["name"], rcdbID=coaster["rcdbid"], ridden=False, coasterOrRide=True, statusDate=coaster["statusDate"], openDate=coaster["openDate"], status=status)
            db.session.add(cstr)
        except NoResultFound:
            badParks.add(coaster["parkid"])
            print("No result found for ", coaster["parkid"])

    for coaster in coasters:
        for track in coaster["tracks"]:
            cstr = CoasterRide.query.filter_by(rcdbID=coaster["rcdbid"]).one()
            t = CoasterTrack(modelLayout=coaster["modelLayout"], configuration=coaster["configuration"], modelCategory=coaster["modelCategory"], make=coaster["make"], coasterType=coaster["coasterType"], coaster=cstr.id)
            
            length = db.Column(db.Integer)
            speed = db.Column(db.Integer)
            elements = db.Column(db.String(500), unique=False)
            duration = db.Column(db.String(10), unique=False)
            verticalAngle = db.Column(db.Integer)
            drop = db.Column(db.Integer)
            
            if "inversions" in track and track["inversions"] and len(track["inversions"]) > 0:
                t.inversions = int(re.sub('[^0-9]', '', str(track["inversions"])))

            if "height" in track and track["height"] and len(track["height"]) > 0:
                t.height = int(re.sub('[^0-9]', '', str(track["height"])))

            if "length" in track and track["length"] and len(track["length"]) > 0:
                t.length = int(re.sub('[^0-9]', '', str(track["length"])))
            
            if "speed" in track and track["speed"] and len(track["speed"]) > 0:
                t.speed = int(re.sub('[^0-9]', '', str(track["speed"])))

            if "elements" in track:
                t.elements = ", ".join(track["elements"])

            if "duration" in track:
                t.duration = track["duration"]

            if "vertical angle" in track and track["vertical angle"] and len(track["vertical angle"]) > 0:
                t.verticalAngle = int(re.sub('[^0-9]', '', str(track["vertical angle"])))

            if "drop" in track and track["drop"] and len(track["drop"]) > 0:
                t.drop = int(re.sub('[^0-9]', '', str(track["drop"])))

            db.session.add(t)

    db.session.commit()

print(badParks)