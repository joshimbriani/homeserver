import datetime
import time
from datetime import datetime
import re

import click
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection

from utilities.misc import getCredentials


def run(argDict):
    ebayAppKey = getCredentials("ebayWatcher")["appID"]
    searchlist = []
    if "watchlist" in argDict:
        searchlist = argDict['watchlist']
    elif "watchlist" in getCredentials("ebayWatcher"):
        searchlist = getCredentials("ebayWatcher")["watchlist"]
    else:
        searchlist = [{"name": 'Decidueye GX'}]
    try:
        api = Connection(appid=ebayAppKey, config_file=None)
        for search in searchlist:
            response = api.execute('findItemsAdvanced', {'keywords': search['name']})
            for item in response.dict()['searchResult']['item']:
                price = float(item['sellingStatus']['convertedCurrentPrice']['value'])
                endTime = datetime.strptime(item['listingInfo']['endTime'], '%Y-%m-%dT%H:%M:%S.000Z')
                if price < search['price'] * 0.9 and (endTime-datetime.now()).seconds < 60*60*2 and not re.search("(World Champion|China|Chinese|Japan|Coin|Jumbo)", item['title'], re.IGNORECASE):
                    click.echo("The item {} is selling for ${} with {} minutes left. This is {}\% of the market value. The URL is {}.".format(
                        item['title'], float(item['sellingStatus']['convertedCurrentPrice']['value']), (endTime-datetime.now()).seconds / 60, 
                        float(item['sellingStatus']['convertedCurrentPrice']['value'])/search['price'], item['viewItemURL']))
                    
            time.sleep(2)

    except ConnectionError as e:
        print(e)
        print(e.response.dict())
