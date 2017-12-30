import datetime
import re
import time
from datetime import datetime

import click
import requests
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection

from selenium import webdriver
from utilities.misc import getCredentials, getBrowserDriver


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
            if "price" not in search:
                search["price"] = getMarketPriceForCard(search["name"])
            response = api.execute('findItemsAdvanced', {
                                   'keywords': search['name']})
            for item in response.dict()['searchResult']['item']:
                price = float(item['sellingStatus']
                              ['convertedCurrentPrice']['value'])
                endTime = datetime.strptime(
                    item['listingInfo']['endTime'], '%Y-%m-%dT%H:%M:%S.000Z')
                if price < search['price'] * 1.0 and (endTime - datetime.now()).seconds < 60 * 60 * 1 and not re.search("(World Champion|China|Chinese|Japan|Coin|Jumbo|playmat|oversize|pin|code|ptcgo)", item['title'], re.IGNORECASE):
                    click.echo("The item {} is selling for ${} with {} minutes left. This is {}% of the market value. The URL is {}.".format(
                        item['title'], float(item['sellingStatus']['convertedCurrentPrice']['value']), (
                            endTime - datetime.now()).seconds / 60,
                        round(float(item['sellingStatus']['convertedCurrentPrice']['value']) / search['price'],2)*100, item['viewItemURL']))

            time.sleep(2)

    except ConnectionError as e:
        print(e)
        print(e.response.dict())


def getMarketPriceForCard(name):
    browser = webdriver.Chrome(getBrowserDriver("chrome"))
    browser.get(
        "https://shop.tcgplayer.com/productcatalog/product/show?newSearch=false&ProductType=All&IsProductNameExact=false&ProductName=" + name.replace(" ", "%20"))
    priceelements = browser.find_elements_by_class_name("product__market-price")
    if len(priceelements) < 1:
        return 0.0
    price = priceelements[0].text.split("\n")[1]
    if price == "Unavailable":
        return 0.0
    else:
        return float(price[1:])
