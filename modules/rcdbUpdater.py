import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..')))

print(sys.path)

import json
import re
import time
import os

import requests
from bs4 import BeautifulSoup
from sqlalchemy.sql.expression import func

from homeserver.models.coasters.ride import CoasterRide
from homeserver.app import db, app

def run():
    def scrapeEntity(i):
        isCoaster = "Unknown"
        info = "Unknown"
        name = "Unknown"
        parkid = "Unknown"
        status = "Unknown"
        statusDate = "Unknown"
        openDate = "Unknown"
        rideType = "Unknown"
        woodOrSteel = "Unknown"
        configuration = "Unknown"
        make = "Unknown"
        modelCategory = "Unknown"
        modelLayout = "Unknown"
        trainArrangement = "Unknown"
        trainManufacturer = "Unknown"
        request = requests.get("http://rcdb.com/" + str(i) + ".htm")
        assert request.status_code == 200

        isCoaster = re.search(r'Tracks', request.text) != None
        isPark = re.search(r'Operating Roller Coasters', request.text) != None
        isPark = isPark or re.search(r'Defunct Roller Coasters', request.text) != None
        isPark = isPark or re.search(r'SBNO Roller Coasters', request.text) != None
        isPark = isPark or re.search(r'Roller Coasters Under Construction', request.text) != None
        isPark = isPark or re.search(r'Roller Coasters In Storage', request.text) != None
        isManufacturer = re.search(r'Models', request.text) != None
        soup = BeautifulSoup(request.text, "lxml")
        
        if isCoaster:
            # Scrape the coaster
            info = soup.find_all("div")[6].find_all("section")

            name = info[0].h1.string
            # print("Name is", name)
    
            if len(info[0].find_all('a', class_="picture")) > 0:
                parkid = int(info[0].find_all('a')[1]['href'][1:-4])
            else:
                parkid = int(info[0].find_all('a')[0]['href'][1:-4])
            # print("Park ID is", parkid)

            r = re.compile(r'Operating|SBNO|Removed')
            for content in info[0].div.div.contents:
                    if content.string:
                        m = re.search(r'(Operating)|(SBNO)|(Removed)', content.string)
                        if m:
                            status = m.group(0)
            # print("Status is", status)

            if status == 'Operating':
                statusDate = "Unknown"
                for content in info[0].div.div.contents:
                    if content.string:
                        m = re.search(r'((\d+/\d+/)*\d{4})', content.string)
                        if m:
                            statusDate = m.group(0)
            elif status == "SBNO":
                statusDate = "Unknown"
                for content in info[0].div.div.contents:
                    if content.string:
                        m = re.search(r'since ((\d+/\d+/)*\d{4})', content.string)
                        if m:
                            statusDate = m.group(1)
                        m = re.search(r'during ((\d+/\d+/)*\d{4})', content.string)
                        if m:
                            statusDate = m.group(1)
            else: 
                statusDate = "Unknown"
                openDate = "Unknown"
                for content in info[0].div.div.contents:
                    if content.string:
                        m = re.search(r'((\d+/\d+/)*\d{4})* to (((\d+/\d+/)*\d{4})|(\?))', content.string)
                        if m:
                            openDate = m.group(1)
                            if m.group(6) != "?":
                                statusDate = m.group(3)
                            else:
                                statusDate = "Unknown"
                # print("Open Date is", openDate)
            # print("Date is", statusDate)

            rideType = info[0].div.div.find_all('a', text=re.compile(r'Roller Coaster|Mountain Coaster|Powered Coaster'))[0].string
            # print("The rideType is", rideType)

            woodOrSteel = info[0].div.div.find_all('a', text=re.compile(r'Roller Coaster|Mountain Coaster|Powered Coaster'))[0].find_next('a').text
            # print("This coaster is made of", woodOrSteel)

            configuration = info[0].div.div.find_all('a', text=re.compile(r'Roller Coaster|Mountain Coaster|Powered Coaster'))[0].find_next('a').find_next('a').text
            # print("The configuration is", configuration)

            makeList = info[0].find_all(text=re.compile("Make"))
            if len(makeList) > 0:
                make = makeList[0].find_next().string
            # print("The make is", make)

            modelList = info[0].find_all(text=re.compile("Model"))
            if len(modelList) > 0:
                modelCategory = modelList[0].find_next().string
                modelLayout = modelCategory.find_next().string

            if modelLayout == "Unknown":
                layoutList = info[0].find_all(text=re.compile("Track layout"))
                if len(layoutList) > 0:
                    modelLayout = layoutList[0].find_next().string
            # print("The model is", modelCategory, modelLayout)

            tracksInfo = soup.find("table", id="statTable")

            tracks = []
            numTracks = len(tracksInfo.tbody.tr.find_all('td'))
            # print("The number of tracks was", numTracks)

            tracksStats = tracksInfo.find_all('tr')

            for j in range(numTracks):
                stats = {}

                for statPair in tracksStats:
                    if statPair.th.string.lower() != "elements":
                        stats[statPair.th.string.lower()] = statPair.find_all('td')[j].string
                    else:
                        elements = []
                        for element in statPair.find_all('td')[j].find_all('a'):
                            elements.append(element.string)
                        stats["elements"] = elements
                tracks.append(stats)

            trainsSection = soup.find('h3', text="Trains")
            if trainsSection:
                trainsSection = trainsSection.parent
                for trainDetail in trainsSection.table.find_all('tr'):
                    if trainDetail.find_all('td')[0].string[:-1].lower() == "arrangement":
                        trainArrangement = trainDetail.find_all('td')[1].string
                    elif trainDetail.find_all('td')[0].string[:-1].lower() == "built by":
                        trainManufacturer = trainDetail.find_all('td')[1].string
                
                # print("Trains were arranged like", trainArrangement)
                # print("Trains were built by", trainManufacturer)

            details = {}

            detailsSection = soup.find('h3', text="Details")
            if detailsSection:
                detailsSection = detailsSection.parent
                for detail in detailsSection.table.find_all('tr'):
                    if detail.find_all('td')[0].string[:-1].lower() == "relocations":
                        relos = []
                        reloCounter = 0
                        while reloCounter < len(detail.find_all('td')[1].contents):
                            relos.append(int(detail.find_all('td')[1].contents[reloCounter+2]["href"][1:-4]))
                            reloCounter += 4
                        details["relocations"] = relos
                    elif detail.find_all('td')[0].string[:-1].lower() == "former status":
                        status = []
                        statusCounter = 0
                        while statusCounter < len(detail.find_all('td')[1].contents):
                            indStatus = {}
                            indStatus["status"] = detail.find_all('td')[1].contents[statusCounter].string
                            if detail.find_all('td')[1].contents[statusCounter+1].string:
                                m = re.search(r'((\d+/\d+/)*\d{4})* to (((\d+/\d+/)*\d{4})|(\?))', detail.find_all('td')[1].contents[statusCounter+1].string)
                                if m:
                                    indStatus["start"] = m.group(1)
                                    if m.group(6) != "?":
                                        indStatus["end"] = m.group(3)
                                    else:
                                        indStatus["end"] = "Unknown"
                                else:
                                    m = re.search(r'during ((\d+/\d+/)*\d{4})', detail.find_all('td')[1].contents[statusCounter+1].string)
                                    if m:
                                        indStatus["start"] = m.group(1)
                                        indStatus["end"] = m.group(1)
                            status.append(indStatus)
                            statusCounter += 3 
                        details["former status"] = status
                    else:
                        details[detail.find_all('td')[0].string[:-1].lower()] = detail.find_all('td')[1].string
                
            coaster = {}
            coaster["type"] = "coaster"
            coaster["name"] = name
            coaster["rcdbid"] = i
            coaster["parkid"] = parkid
            coaster["status"] = status
            coaster["statusDate"] = statusDate
            coaster["openDate"] = openDate
            coaster["rideType"] = rideType
            coaster["coasterType"] = woodOrSteel
            coaster["configuration"] = configuration
            coaster["make"] = make
            coaster["modelCategory"] = modelCategory
            coaster["modelLayout"] = modelLayout
            coaster["numTracks"] = numTracks
            coaster["tracks"] = tracks
            coaster["trainArrangement"] = trainArrangement
            coaster["trainManufacturer"] = trainManufacturer
            coaster["details"] = details

            return ["c", coaster]
        
        elif isPark:
            # Scrape the park
            info = soup.find_all("div")[6].find_all("section")[0]

            name = info.h1.string
            # print("Name is", name)

            address = " "
            for item in info.div.div.div.contents[1:]:
                if item and item.string:
                    if address[-1] != " " and item.string[0] != ",":
                        address += " "
                    address += item.string
            address = address.strip()
            # print("Address is", address)

            r = re.compile(r'Operating|SBNO|Defunct')
            for content in info.div.div.contents:
                    if content.string:
                        m = re.search(r'(Operating)|(SBNO)|(Defunct)', content.string)
                        if m:
                            status = m.group(0)
            # print("Status is", status)

            if status == 'Operating':
                statusDate = "Unknown"
                for content in info.div.div.contents:
                    if content.string:
                        m = re.search(r'((\d+/\d+/)*\d{4})', content.string)
                        if m:
                            statusDate = m.group(0)
                            break
            elif status == "SBNO":
                statusDate = "Unknown"
                for content in info.div.div.contents:
                    if content.string:
                        m = re.search(r'since ((\d+/\d+/)*\d{4})', content.string)
                        if m:
                            statusDate = m.group(1)
                            break
                        m = re.search(r'during ((\d+/\d+/)*\d{4})', content.string)
                        if m:
                            statusDate = m.group(1)
                            break
            else: 
                statusDate = "Unknown"
                openDate = "Unknown"
                for content in info.div.div.contents:
                    if content.string:
                        m = re.search(r'((\d+/\d+/)*\d{4})* to (((\d+/\d+/)*\d{4})|(\?))', content.string)
                        if m:
                            openDate = m.group(1)
                            if m.group(6) != "?":
                                statusDate = m.group(3)
                                break
                            else:
                                statusDate = "Unknown"
                                break
                # print("Open Date is", openDate)
            # print("Date is", statusDate)

            if not openDate:
                openDate = "Unknown"

            park = {}
            park["name"] = name
            park["rcdbId"] = i
            park["address"] = address
            park["status"] = status
            park["statusDate"] = statusDate
            park["openDate"] = openDate

            return ["p", park]

    home = requests.get("http://rcdb.com/")

    # Make sure we get a good response from the site 
    assert home.status_code == 200

    # ID 2193 is a ride with no open/close dates 
    # ID 8 is a ride with defined open/close dates
    # ID 589 is an SBNO ride

    # Will want to eventually connect to our DB(?)/JSON file(?) and get the lower bound
    # We'll set it manually for now
    #startpoint = 11200
    with app.app_context():
        startpoint = db.session.query(db.func.max(CoasterRide.id)).scalar() + 1
        print(startpoint)
        return
    #startpoint = None

    # Get the latest coaster/park from the site - this is the upper limit to our search
    # Temporarily set to 10 for testing
    #endpoint = max(list(map(int, re.findall(r'/(\d+).htm', home.text))))
    #endpoint = 11300
    endpoint = None

    scrapeList = [15233, 14980, 12041, 15500, 16269, 12557, 16282, 16923, 14494, 16803, 15141, 17062, 16040, 15658, 15403, 16305, 15666, 15539, 16181, 15479, 16826, 16187, 16828, 15547, 16700, 15679, 14912, 15680, 16063, 15684, 16838, 16582, 15176, 14539, 15948, 16974, 13903, 16594, 16853, 16471, 16729, 16221, 14429, 15327, 14048, 14946, 16739, 16229, 10213, 15593, 16362, 14955, 16749, 15982, 15087, 16494, 12017, 16508, 13681, 14964, 14065, 15222, 10610, 12412, 15997]
    #scrapeList = None

    # Since RCDB is really unreliable, we can't assume that it'll stay up
    # So instead of waiting until the full scrape is done to output to a json
    # We output whatever our batch size is.
    batchSize = 100

    # Create the folder for the scrapes
    try:
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    except OSError:
        print ("Creation of the directory failed")

    items = {}
    items["coasters"] = []
    items["parks"] = []

    if startpoint and endpoint:
        for i in range(startpoint, endpoint+1):
            entity = scrapeEntity(i)
            if entity[0] == 'c':
                items["coasters"].append(entity)
            if entity[0] == 'p':
                items["parks"].append(entity)
            
            if i % batchSize == 0 or i == endpoint:
                filename = "data/scrape" + str(i - batchSize) + "-" + str(i) + ".json"
                with open(filename, "w") as writeJSON:
                    json.dump(items, writeJSON, ensure_ascii=False)
                    
                    items = {}
                    items["coasters"] = []
                    items["parks"] = []
            
            time.sleep(3.5)
            print("Processed", i, "of", endpoint)

    elif scrapeList:
        counter = 0
        batchCount = 0
        for i, rcdbid in enumerate(scrapeList):
            entity = scrapeEntity(rcdbid)
            print("Processed", i + 1, "of", len(scrapeList), ". The park id is ", str(rcdbid))

            if entity[0] == 'c':
                items["coasters"].append(entity)
            if entity[0] == 'p':
                items["parks"].append(entity)
            
            counter += 1
            if counter >= batchSize or i == len(scrapeList) - 1:
                filename = "data/scrapebatch" + str(batchCount) + ".json"
                with open(filename, "w") as writeJSON:
                    json.dump(items, writeJSON, ensure_ascii=False)
                    
                    items = {}
                    items["coasters"] = []
                    items["parks"] = []
                    batchCount += 1
                    counter = 0
            
            time.sleep(3.5)

    # Initially, we're just going to save the park name as the string rcdb id.
    # After we scrape everything, we go back trhough the db and replace all entries with our id

    parks = []
    coasters = []

    #with open('scrape1-5000.json') as json_file:
    #    data = json.load(json_file)
    #    for coaster in data['coasters']:
    #        coasters.append(coaster)
    #    for park in data['parks']:
    #        parks.append(park)

    #with open('scrape5000-10000.json') as json_file:
    #    data = json.load(json_file)
    #    for coaster in data['coasters']:
    #        coasters.append(coaster)
    #    for park in data['parks']:
    #        parks.append(park)

    #client = MongoClient()
    #db = client.tpsn
    #parksCollection = db.parks
    #coastersCollection = db.coasters

    #for park in parks:
    #    parksCollection.insert_one(park)

    #for coaster in coasters:
    #    park = parksCollection.find_one({"rcdbId": coaster["parkId"]})
    #    coaster["park"] = park["_id"]
    #    coastersCollection.insert_one(coaster)

if __name__ == "__main__":
    run()