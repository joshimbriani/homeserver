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
@click.option('--kill', '-k', is_flag=True, help="Kills all current homeserver jobs.")
@click.option('--modules', '-m', type=click.STRING, multiple=True, default='', help='Modules to start cron with. Input as a comma delimited list.')
@click.option('--frequency', '-f', type=click.INT, help='Frequency to run the cron job (in minutes).')
@click.option('--params', '-p', type=click.STRING, help='Params for modules.')
def cli(verbose, list, kill, modules, frequency, params):
    cron = CronTab(user='josh')
    if list:
        # Get the cron jobs that start with homeserver*
        jobs = getHSJobs()
        
        if len(jobs) == 0:
            click.echo("No jobs currently running.")
        else:
            for job in jobs:
                click.echo(formatCron(job))
        return
    if kill:
        killHSJobs()
        return
    if modules:
        if not frequency:
            click.echo("You must list a frequency to run the given modules")
            return
        
        jobs = getHSJobs()
        if len(jobs) != 0:
            click.echo("A homeserver job is already running.")
            kill = click.prompt("Kill the existing job? (Y/N)", type=str, default="N")
            if kill.upper() == "Y" or kill.upper() == "YES":
              for job in jobs:
                  cron.remove(job)
            else:
                click.echo("Will not add to existing jobs. Please delete them.")
                return  

        jobCommand = os.path.join(os.path.dirname(os.path.realpath(__file__)),"env", "bin", "python") + " " + os.path.join(os.path.dirname(os.path.realpath(__file__)),'runner.py') + " " + ",".join(modules) + " \"" + (params or "") + "\""
        job = cron.new(command=jobCommand)
        job.minute.every(frequency)
        cron.write()
        click.echo("Created a job doing {} every {} minutes.".format(", ".join(modules), frequency))
        return

def getHSJobs():
    cron = CronTab(user='josh')
    jobiterator = cron.find_command(re.compile(r'homeserver'))
    jobs = []
    for job in jobiterator:
        jobs.append(job)

    return jobs

def killHSJobs():
    cron = CronTab(user='josh')
    jobiterator = cron.find_command(re.compile(r'homeserver'))
    for job in jobiterator:
        cron.remove(job)
    cron.write()