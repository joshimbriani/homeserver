import requests
from bs4 import BeautifulSoup

r = requests.get('http://www.screamscape.com/')

soup = BeautifulSoup(r.text, 'html.parser')

tag = soup.find_all('b')[2].findNextSibling()
while tag.name != "b":
    if tag.name == "a":
        print(tag)
    tag = tag.findNextSibling()