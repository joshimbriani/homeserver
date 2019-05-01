from croniter import croniter
from datetime import datetime

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
            pass

            # And run it
            module.run()

            

        pass


if __name__ == "__main__":
    check_tasks()
