from flask import Blueprint
import requests
from bs4 import BeautifulSoup
import json

screamscape = Blueprint('screamscape', __name__)

@screamscape.route('/')
def getScreamscape():
    r = requests.get('http://www.screamscape.com/')

    soup = BeautifulSoup(r.text, 'html.parser')

    tag = soup.find_all('b')[3].findNextSibling()
    tags = []

    while tag.name != "b":
        if tag.name == "a":
            tags.append([tag.string, "http://www.screamscape.com" + tag["href"][1:]])
        tag = tag.findNextSibling()
    
    return json.dumps(tags)