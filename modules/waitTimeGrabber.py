import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from utilities.cronCreator import CronCreator
from app import db
from homeserver.models.coasters.waitTimes import CoasterWaitTime
from homeserver.models.coasters.ride import CoasterRide
from homeserver.models.coasters.park import CoasterPark

import pyarks
import arrow
import requests

def rideToID(rideName):
    ID = 0
    #if rideName == ""

    return ID

def run():
    usf = pyarks.getPark('USF')
    ioa = pyarks.getPark('IOA')

    print(usf.getOpenCloseTime())
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

    if now <= closeUSF and now >= earlyEntryUSF:
        for ride in usf.rides:
            if not ride.closed:
                earlyEntry = 0
                if now > earlyEntryUSF and now < openUSF:
                    earlyEntry = 1
                db.session.execute("INSERT INTO coasterwaittimes(waitTime, weather, temp, datetime, humidity, windspeed, park, ride, earlyentry) VALUES ('" + now.isoformat() + "', '" + str(ride.name.encode('unicode_escape').decode('utf-8').replace("'", "''")) + "', " + str(ride.waitTime) + " , 'USF', " + str(int(earlyEntry)) + ", '" + str(weatherfeature) + "', " + str(int(temp)) + ", " + str(int(humidity)) + ", " + str(int(windspeed)) + ")")
            print(ride.name, ' ', ride.waitTime)

    if now <= closeIOA and now >= earlyEntryIOA:
        for ride in ioa.rides:
            if not ride.closed:
                earlyEntry = False
                if now > earlyEntryIOA and now < openIOA:
                    earlyEntry = True
                db.session.execute("INSERT INTO coasterwaittimes(waitTime, weather, temp, datetime, humidity, windspeed, park, ride) VALUES (" + str(ride.waitTime) + ", '" + str(weatherfeature) + "', " + str(int(temp)) + ", '" + now.isoformat() + "', " + str(int(humidity)) + ", " + str(int(windspeed)) + ", " + str() + str(ride.name.encode('unicode_escape').decode('utf-8').replace("'", "''")) + "', " + " , 'IOA', " + str(int(earlyEntry)) + ", '" +  + "', " +  + ", " +  + ")")
            print(ride.name, ' ', ride.waitTime)

    db.session.commit()

    return "Wait Time"

if __name__ == "__main__":
    
    run()