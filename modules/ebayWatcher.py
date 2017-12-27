import datetime

import click
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection

from utilities.misc import getCredentials

def run(argDict):
    ebayAppKey = getCredentials("ebayWatcher")["appID"]
    try:
        api = Connection(appid=ebayAppKey, config_file=None)
        response = api.execute('findItemsAdvanced', {'keywords': 'legos'})

        assert(response.reply.ack == 'Success')
        assert(type(response.reply.timestamp) == datetime.datetime)
        assert(type(response.reply.searchResult.item) == list)

        click.echo(response.reply.searchResult.item)

        item = response.reply.searchResult.item[0]
        assert(type(item.listingInfo.endTime) == datetime.datetime)
        assert(type(response.dict()) == dict)

    except ConnectionError as e:
        print(e)
        print(e.response.dict())
