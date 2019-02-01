from crontab import CronTab
import os

class CronCreator:
    
    @staticmethod
    def create(cron, description, pythonFile, cronString):
        topLevelDir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
        executablePath = os.path.join(topLevelDir, "env", "bin", "python")
        command = executablePath + " " + pythonFile 
        job = cron.new(command=command, comment=description)
        job.setall(cronString)
        return job

    @staticmethod
    def get(cron, pythonFile=None, formatString=None):
        if not pythonFile and not formatString:
            return None
        
        myCron = None
        if pythonFile:
            crons = cron.find_command(pythonFile)
            if len(crons) > 0:
                myCron = crons[0]

        elif formatString:
            crons = cron.find_time(formatString)
            if len(crons) > 0:
                myCron = crons[0]

        if myCron:
            return myCron
        
        return None

    @staticmethod
    def edit(cron, currentFile=None, currentCronString=None, description=None, pythonFile=None, cronString=None):
        if not currentFile and not currentCronString:
            return None
        
        if pythonFile:
            crons = cron.find_command(currentFile)
            if len(crons) > 0:
                myCron = crons[0]

        elif formatString:
            crons = cron.find_time(currentCronString)
            if len(crons) > 0:
                myCron = crons[0]

        if myCron:
            if pythonFile:
                topLevelDir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
                executablePath = os.path.join(topLevelDir, "env", "bin", "python")
                command = executablePath + " " + pythonFile 
                myCron.set_command(command)

            if description:
                myCron.set_comment(description)

            if cronString:
                myCron.setall(cronString)