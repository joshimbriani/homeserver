import importlib
from datetime import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..')))

from homeserver.database import db
from homeserver.app import app
from homeserver.models.jobs.job import Job

from croniter import croniter
from homeserver.utilities.communication import Communication
from homeserver.utilities.misc import getBrowserDriver, getCredentials
from homeserver.errors.network_error import NetworkError

def run_tasks():
    # Get all jobs that are active in the database
    jobs = db.session.query(Job).filter(Job.active == True)

    # Iterate through the list of current cron jobs
    for job in jobs:
        # Get the previous scheduled runtime
        cron_str = croniter(job.cronString, datetime.now())
        last_runtime = cron_str.get_prev(datetime)

        # If the runtime is after our last recorded runtime
        if last_runtime > job.lastRun:
            # Import the module
            module = importlib.import_module(job.pythonFile[:-3])

            # And run it
            try:
                module.run({"name": "josh"})
            except NetworkError:
                commCreds = getCredentials("system")
                comm = Communication(commCreds["twilioSID"], commCreds["twilioAuth"], commCreds["sendGridToken"])
                comm.sendEmail("Failing module", "The module %s is failing with a network error. Please fix it when you can!" % job.name)

if __name__ == "__main__":
    with app.app_context():
        run_tasks()
