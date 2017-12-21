import click
from utilities.storage import writeToFile

def run(argDict):
    if "name" not in argDict:
        click.echo("Helloer takes a required name parameter.")
        return
    writeToFile([{"name": "Josh"}], "helloer", "json")
    click.echo("Hello " + argDict["name"])
    click.echo("Your install of HomeServer works!")