import click
from utilities.communication import Communication
from utilities.misc import getCredentials

def run(argDict):
    if "name" not in argDict:
        click.echo("Helloer takes a required name parameter.")
        return
    commCreds = getCredentials("system")
    comm = Communication(commCreds["twilioSID"], commCreds["twilioAuth"], commCreds["sendGridToken"])
    comm.sendEmail("Hello Josh", "send email")
    click.echo("Hello " + argDict["name"])
    click.echo("Your install of HomeServer works!")