import json
import os

def formatCron(cron):
    return cron

def getCredentials(settingsFile):
    json_data=open(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),'settings', settingsFile + ".json")).read()
    data = json.loads(json_data)
    return data