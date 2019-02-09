import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utilities.cronCreator import CronCreator
from app import db, app
from homeserver.models.coasters.waitTimes import CoasterWaitTime
from homeserver.models.coasters.ride import CoasterRide
from homeserver.models.coasters.park import CoasterPark

import pyarks
import arrow
import requests
from datetime import datetime

def getParkName(name):
    if name == "The Incredible Hulk Coaster":
        return "Incredible Hulk"
    elif name == "Hollywood Rip Ride Rockit":
        return "Hollywood Rip, Ride, Rockit"
    else:
        return name

def run():
    with app.app_context():
        usf = pyarks.getPark('USF')
        ioa = pyarks.getPark('IOA')

        scheduleTodayUSF = usf.getOpenCloseTime()[0]
        earlyEntryUSF = scheduleTodayUSF['earlyEntryTime']
        openUSF = scheduleTodayUSF['openTime']
        closeUSF = scheduleTodayUSF['closeTime']

        scheduleTodayIOA = ioa.getOpenCloseTime()[0]
        earlyEntryIOA = scheduleTodayIOA['earlyEntryTime']
        openIOA = scheduleTodayIOA['openTime']
        closeIOA = scheduleTodayIOA['closeTime']
        weather = requests.get('http://api.openweathermap.org/data/2.5/weather?id=4167147&appid=2dfb662eba418c99bb6a79afa3cbfe09')
        if weather.status_code != 200:
            print("Weather get failed. Try again later")
            exit()

        weather = weather.json()
        weatherfeature = weather['weather'][0]['main']
        temp = ((weather['main']['temp'] - 273.15) * (9/5) + 32)
        humidity = weather['main']['humidity']
        windspeed = weather['wind']['speed']

        now = arrow.now()
        date = datetime.now()

        if now <= closeUSF and now >= earlyEntryUSF:
            for ride in usf.rides:
                if not ride.closed:
                    earlyEntry = 0
                    if now > earlyEntryUSF and now < openUSF:
                        earlyEntry = 1
                    p = CoasterPark.query.filter_by(abbrev='USF').first()
                    print("Park Name: '", p.name, "'")
                    print("Ride Name: '", ride.name, "'")
                    c = CoasterRide.query.filter_by(name=getParkName(ride.name.replace('®', '')), park=p.id).first()
                    print("Ride Name: '", c.name, "'")
                    w = CoasterWaitTime(park=p.id, ride=c.id, waitTime=ride.waitTime, datetime=date, earlyEntry=earlyEntry, weather=weatherfeature, temp=int(temp), windspeed=int(windspeed), humidity=int(humidity))
                    db.session.add(w)
                print(ride.name, ' ', ride.waitTime)

        if now <= closeIOA and now >= earlyEntryIOA:
            for ride in ioa.rides:
                if not ride.closed:
                    earlyEntry = False
                    if now > earlyEntryIOA and now < openIOA:
                        earlyEntry = True
                    p = CoasterPark.query.filter_by(abbrev='IOA').first()
                    c = CoasterRide.query.filter_by(name=getParkName(ride.name.replace('®', '')), park=p.id).first()
                    w = CoasterWaitTime(park=p.id, ride=c.id, waitTime=ride.waitTime, datetime=date, earlyEntry=earlyEntry, weather=weatherfeature, temp=int(temp), windspeed=int(windspeed), humidity=int(humidity))
                    db.session.add(w)
                print(ride.name, ' ', ride.waitTime)

        db.session.commit()

if __name__ == "__main__":
    
    run()