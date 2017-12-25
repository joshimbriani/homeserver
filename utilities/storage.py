import json
import os
import sqlite3

import click

# Storage.py allows modules to have access to local storage
# Databases and text Files

def writeToFile(data, module, fileType="txt"):
    if fileType != "txt" and fileType != "json" and fileType != "csv":
        click.echo("Unsupported file type. HomeServer supports \"txt\", \"json\" and \"csv\"")
    # Open file
    if fileType == "txt" or fileType == "csv":
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", module + "." + fileType), 'a+') as f:
            f.write(data)
            if fileType == "csv":
                f.write("\n")
    if fileType == "json":
        fileContents = ""
        open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", module + ".json"), "a+")
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", module + ".json"), "r+") as f:
            fileContents = f.read()
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", module + ".json"), "w") as f:
            result = []
            if fileContents:
                result = json.loads(fileContents)
            result += data
            f.write(json.dumps(result))

    return

def writeToDB(data, module, table, dataFormat="json", createStatment=None):
    if dataFormat != "json" and dataFormat != "csv" and dataFormat != "obj":
        click.echo("writeToDB only supports data in the json, csv and Python object formats")
    conn = sqlite3.connect(module + ".db")
    c = conn.cursor()
    if createStatment:
        # Execute create statement to create DB before we insert data
        # Create statement should be of form "(name text, temp int)" etc.
        c.execute("CREATE table " + table + " " + createStatment)
        return

    # INSERT INTO table DATA ('', '')

    # if json
    if dataFormat != "csv":
        if dataFormat == "json"
            # Convert json string to obj
            data = json.loads(data)
        
        # Save the schema to a text file when we create. Then have a function that takes an object and returns the proper
        # insert string with correct nulls if the obj doesn't have a schema field on it. 
        getInsertStringFromObject(data)

def getInsertStringFromObject(obj):
    
    return ""
