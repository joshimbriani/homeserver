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
                listingType = item['listingInfo']['listingType']
                endTime = datetime.strptime(
                    item['listingInfo']['endTime'], '%Y-%m-%dT%H:%M:%S.000Z')
                name = item['title']
                binPrice = None
                if "buyItNowPrice" in item['listingInfo']:
                    binPrice = float(item['listingInfo']['buyItNowPrice']['value'])
                if itemDeservesNotification(0.9, price, search['price'], listingType, endTime, 1, name, binPrice):
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

def priceIsBelowMarket(threshold, itemPrice, marketPrice):
    return itemPrice < marketPrice * threshold

def itemIsAuctionEndingSoonOrBIN(listingType, endTime, timeThreshold):
    isAuction = listingType == "Auction"
    isEndingSoon = (endTime - datetime.now()).seconds < 60 * 60 * timeThreshold
    isBIN = (listingType == "FixedPrice" or listingType == "StoreInventory")
    return isAuction and isEndingSoon or isBIN

def itemIsNotExcluded(name):
    return not re.search("(" + "|".join(getCredentials("ebayWatcher")["termsToExclude"]) + ")", name, re.IGNORECASE) 

def itemDeservesNotification(threshold, itemPrice, marketPrice, listingType, endTime, timeThreshold, name, binPrice=None):
    if listingType == "AuctionWithBIN" and binPrice and binPrice < marketPrice * threshold:
        return True
    else:
        return priceIsBelowMarket(threshold, itemPrice, marketPrice) and itemIsAuctionEndingSoonOrBIN(listingType, endTime, timeThreshold) and itemIsNotExcluded(name)