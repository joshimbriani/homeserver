from crontab import CronTab
import os

class CronCreator:
    
    @staticmethod
    def create(cron, description, pythonFile, cronString):
        topLevelDir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
        executablePath = os.path.join(topLevelDir, "env", "bin", "python")
        pythonFilePath = os.path.join(topLevelDir, "modules", pythonFile)
        command = executablePath + " " + pythonFilePath 
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
            li = []
            for i in crons:
                li.append(i)
            if len(li) > 0:
                myCron = li[0]

        elif formatString:
            crons = cron.find_time(formatString)
            li = []
            for i in crons:
                li.append(i)
            if len(li) > 0:
                myCron = li[0]

        if myCron:
            return myCron
        
        return None

    @staticmethod
    def edit(cron, currentFile=None, currentCronString=None, description=None, pythonFile=None, cronString=None):
        if not currentFile and not currentCronString:
            return None
        
        myCron = None
        
        if currentFile:
            crons = cron.find_command(currentFile)
            li = []
            for i in crons:
                li.append(i)
            if len(li) > 0:
                myCron = li[0]

        elif currentCronString:
            crons = cron.find_time(currentCronString)
            li = []
            for i in crons:
                li.append(i)
            if len(li) > 0:
                myCron = li[0]

        if myCron:
            if pythonFile:
                topLevelDir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
                executablePath = os.path.join(topLevelDir, "env", "bin", "python")
                pythonFilePath = os.path.join(topLevelDir, "modules", pythonFile)
                command = executablePath + " " + pythonFilePath 
                myCron.set_command(command)

            if description:
                myCron.set_comment(description)

            if cronString:
                print("Cron string ", cronString)
                myCron.setall(cronString)

            cron.write()

    @staticmethod
    def delete(cron, pythonFile=None, formatString=None):
        job = CronCreator.get(cron, pythonFile=pythonFile, formatString=formatString)

        if job:
            cron.remove(job)

            cron.write()