import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import click
from utilities.communication import Communication
from utilities.misc import getCredentials
from errors.network_error import NetworkError

def run(argDict):
    if "name" not in argDict:
        click.echo("Helloer takes a required name parameter.")
        return
    commCreds = getCredentials("system")
    comm = Communication(commCreds["twilioSID"], commCreds["twilioAuth"], commCreds["sendGridToken"])
    comm.sendEmail("Hello Josh", "send email")
    click.echo("Hello " + argDict["name"])
    click.echo("Your install of HomeServer works!")

if __name__ == "__main__":
    run()