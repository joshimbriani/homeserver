import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utilities.communication import Communication
from utilities.storage import getFileData, writeToFile
from utilities.misc import getCredentials
import importlib

def run(arguments):
    jsonData = getFileData("emailer", fileType="json")
    emailBody = """
        <html>
            <head></head>
            <body>
                <h1>Your hourly report</h1>
                {}
            </body>
        </html>
    """
    innerData = ""
    for module, data in jsonData.items():
        importModule = importlib.import_module("modules." + module)
        innerData += "<div><h2>{} module alerts</h2>".format(module)
        for item in data:
            innerData += importModule.emailTemplate(item)
        innerData += "</div>"
    emailBody = emailBody.format(innerData)
    if len(emailBody) > 164:
        commCreds = getCredentials("system")
        comm = Communication(
            commCreds["twilioSID"], commCreds["twilioAuth"], commCreds["sendGridToken"])
        comm.sendEmail("Hourly Report from Home Server", emailBody)
        writeToFile({}, "emailer", fileType="json")

if __name__ == "__main__":
    run()