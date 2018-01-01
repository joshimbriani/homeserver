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
from utilities.communication import Communication
from utilities.storage import getFileData, writeToFile


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
                itemID = item['itemId']
                name = item['title']
                price = checkForMultipleCards(name, float(
                    item['sellingStatus']['convertedCurrentPrice']['value']))
                listingType = item['listingInfo']['listingType']
                endTime = datetime.strptime(
                    item['listingInfo']['endTime'], '%Y-%m-%dT%H:%M:%S.000Z')
                binPrice = None
                if "buyItNowPrice" in item['listingInfo']:
                    binPrice = float(item['listingInfo']
                                     ['buyItNowPrice']['value'])
                if itemDeservesNotification(0.85, price, search['price'], listingType, endTime, 60, name, binPrice):
                    
                    emailerdata = getFileData("emailer", fileType="json")
                    print(emailerdata)
                    if "ebayWatcher" in emailerdata:
                        inFile = False
                        for notification in emailerdata["ebayWatcher"]:
                            if notification["itemID"] == itemID:
                                inFile = True
                        if not inFile:
                            emailerdata["ebayWatcher"].append({"name": name, "price": price, "listingType": listingType, "itemID": itemID})
                    else:
                        emailerdata["ebayWatcher"] = [{"name": name, "price": price, "listingType": listingType, "itemID": itemID}]
                    writeToFile(emailerdata, "emailer", fileType="json")
                    
                    if endingWithinThreshold(endTime, 15) and listingType == "Auction":
                        commCreds = getCredentials("system")
                        comm = Communication(
                            commCreds["twilioSID"], commCreds["twilioAuth"], commCreds["sendGridToken"])
                        comm.sendText("The item {} is selling for ${} with {} minutes left. This is {}% of the market value. The URL is {}".format(
                            item['title'], price, (
                                endTime - datetime.now()).seconds / 60,
                            round(price / search['price'], 2) * 100, item['viewItemURL']))
                    if listingType == "FixedPrice" or listingType == "StoreInventory" and priceIsBelowMarket(0.6, price, search["price"]):
                        commCreds = getCredentials("system")
                        comm = Communication(
                            commCreds["twilioSID"], commCreds["twilioAuth"], commCreds["sendGridToken"])
                        comm.sendText("The item {} is selling for ${} with {} minutes left. This is {}% of the market value. The URL is {}".format(
                            item['title'], price, (
                                endTime - datetime.now()).seconds / 60,
                            round(price / search['price'], 2) * 100, item['viewItemURL']))
                    click.echo("The item {} is selling for ${} with {} minutes left. This is {}% of the market value. The URL is {}".format(
                        item['title'], price, (
                            endTime - datetime.now()).seconds / 60,
                        round(price / search['price'], 2) * 100, item['viewItemURL']))

            time.sleep(2)

    except ConnectionError as e:
        print(e)
        print(e.response.dict())


def getMarketPriceForCard(name):
    browser = webdriver.Chrome(getBrowserDriver("chrome"))
    browser.get(
        "https://shop.tcgplayer.com/productcatalog/product/show?newSearch=false&ProductType=All&IsProductNameExact=false&ProductName=" + name.replace(" ", "%20"))
    priceelements = browser.find_elements_by_class_name(
        "product__market-price")
    if len(priceelements) < 1:
        return 0.0
    price = priceelements[0].text.split("\n")[1]
    if price == "Unavailable":
        return 0.0
    else:
        return float(price[1:])


def priceIsBelowMarket(threshold, itemPrice, marketPrice):
    return itemPrice < marketPrice * threshold


def endingWithinThreshold(endTime, timeThreshold):
    return (endTime - datetime.now()).seconds < 60 * timeThreshold


def itemIsAuctionEndingSoonOrBIN(listingType, endTime, timeThreshold):
    isAuction = listingType == "Auction"
    isEndingSoon = endingWithinThreshold(endTime, timeThreshold)
    isBIN = (listingType == "FixedPrice" or listingType == "StoreInventory")
    return isAuction and isEndingSoon or isBIN


def itemIsNotExcluded(name):
    return not re.search("(" + "|".join(getCredentials("ebayWatcher")["termsToExclude"]) + ")", name, re.IGNORECASE)


def itemDeservesNotification(threshold, itemPrice, marketPrice, listingType, endTime, timeThreshold, name, binPrice=None):
    if listingType == "AuctionWithBIN" and binPrice and binPrice < marketPrice * threshold:
        return True
    else:
        return priceIsBelowMarket(threshold, itemPrice, marketPrice) and itemIsAuctionEndingSoonOrBIN(listingType, endTime, timeThreshold) and itemIsNotExcluded(name)


def checkForMultipleCards(name, price):
    matches = re.findall(r'(\d)x|x(\d)|(\d) x|x (\d)', name)
    if matches:
        for match in matches[0]:
            if match != "":
                return price / float(match)
    return price
