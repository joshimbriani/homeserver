import feedparser
from datetime import datetime
from flask import Blueprint
import json

RSS_URLS = [
    'https://themeparkuniversity.com/feed/',
    'https://orlandoparkstop.com/feed/',
    'http://feeds.feedburner.com/NewsPlusNotes?format=xml',
    'https://attractionsmagazine.com/blog/feed/',
    'https://blog.touringplans.com/feed/'
    ]

articles = Blueprint('articles', __name__)

@articles.route('/')
def getArticles():
    posts = []
    for url in RSS_URLS:
        posts.extend(feedparser.parse(url).entries)

    posts.sort(key=lambda x: datetime.strptime(x.published, '%a, %d %b %Y %H:%M:%S %z'), reverse=True)

    returnedArticles = []
    for post in posts[:10]:
        returnedArticles.append([post.title, post.link, datetime.strptime(post.published, '%a, %d %b %Y %H:%M:%S %z').isoformat()])
    
    return json.dumps(returnedArticles)



