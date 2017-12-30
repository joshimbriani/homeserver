import json
import os

def formatCron(cron):
    cronsplit = str(cron).split(" ")
    if len(cronsplit[0]) > 1:
        frequency = cronsplit[0][2:]
    else:
        frequency = "1"
    runInfo = cronsplit[7:]
    return "Modules: " + runInfo[0] + " with arguments: " + runInfo[1] + " running every " + frequency + " minutes."

def getCredentials(settingsFile):
    json_data=open(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),'settings', settingsFile + ".json")).read()
    data = json.loads(json_data)
    return data

def getBrowserDriver(browser):
    if browser == "chrome":
        return os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),'assets', "browserdrivers", "chromedriver")