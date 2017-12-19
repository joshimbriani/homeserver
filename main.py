# The main file is the file that manages the crontabs
# Also eventually runs a web server to listen on the app
import os
import re

import click
from crontab import CronTab

from utilities.misc import formatCron


@click.command()
@click.option('--verbose', is_flag=True, help="Will print verbose messages.")
@click.option('--list', is_flag=True, help="Lists all current jobs. Will quit when listing is complete.")
@click.option('--modules', '-m', type=click.STRING, multiple=True, default='', help='Modules to start cron with. Input as a comma delimited list.')
@click.option('--frequency', '-f', type=click.INT, help='Frequency to run the cron job (in minutes).')
def cli(verbose, list, modules, frequency):
    if list:
        cron = CronTab()
        # Get the cron jobs that start with homeserver*
        jobiterator = cron.find_command(re.compile(r'homeserver-\S+'))
        jobs = []
        for job in jobiterator:
            jobs.append(job)
        
        if len(jobs) == 0:
            click.echo("No jobs found")
        else:
            for job in jobs:
                click.echo(formatCron(job))
        return
    if modules:
        if not frequency:
            click.echo("You must list a frequency to run the given modules")
            return
        jobCommand = "python3 " + os.path.join(os.path.dirname(os.path.realpath(__file__)),'runner.py') + " " + generateParamString()
        job = cron.new(command=jobCommand)
        click.echo("You wanted to do {} every {} minutes.".format(modules, frequency))
        return

def generateParamString():
    return ""