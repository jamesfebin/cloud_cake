import feedparser
import time
import MySQLdb
import re
from BeautifulSoup import BeautifulSoup
import HTMLParser
import datetime
import urllib, cStringIO
import MySQLdb.cursors
import requests
import json

server='YOUR_SERVER_ADDRESS'
database='YOUR_DATABASE_NAME'
username='YOUR_USER_NAME'
password='YOUR_PASSWORD'


def writeToDatabase(data):
    try :
        client = MySQLdb.connect(server,username,password,database,cursorclass=MySQLdb.cursors.DictCursor)
        client.set_character_set('utf8')
        cursor = client.cursor()
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        cursor.execute("SELECT * FROM news WHERE link=%s",(data['link'],))
        data['published'] = time.time()
        if cursor.rowcount == 0:
            cursor.execute("INSERT INTO news (title,link,summary,published,image,category) VALUES (%s,%s,%s,%s,%s,%s)",(data['title'],data['link'],data['summary'],data['published'],data['image'],data['category']))
        client.commit()
    except Exception as e:
        print(e)


def cleanhtml(raw_html):
    cleanr =re.compile('<.*?>')
    cleantext = re.sub(cleanr,'', raw_html)
    return cleantext

sources = [{'category':'business','url':'http://www.business-standard.com/rss/home_page_top_stories.rss'},{'category':'tech','url':'http://feeds.feedburner.com/TechCrunch/'},{'category':'entertainment','url':'http://feeds.feedburner.com/thr/news'}]

for source in sources:
    feedData=feedparser.parse(source['url'])
    for entry in feedData.entries:
        try:
            link = ''
            published = 0
            summary= ''
            title = ''
            image = ''
            if 'link' in entry:
                link = entry.link
            if 'enclosures' in entry:
                enclosures = entry.enclosures
            for enclosure in enclosures:
                    if "image" in enclosure['type'] and 'href' in enclosure:
                        image = enclosure['href']
                        break
            if 'title' in entry:
                title = entry.title.encode('ascii','ignore')
            if 'summary' in entry:
                 summary=entry.summary.encode('ascii','ignore')
            elif 'description' in entry:
                 summary=entry.description.encode('ascii','ignore')
            if summary != '':
                soup = BeautifulSoup(summary)
                urls = soup.findAll("img")
                for urlTag in urls:
                    image = urlTag['src']
                    break
            data={'link':link,'summary':summary,'title':title,'image':image,'category':source['category']}
            writeToDatabase(data)
        except Exception as e:
            print(e)

