#!/usr/bin/python

import urllib
import simplejson
import sys
import yql
import re, string

def searchTweets(query):
    search = urllib.urlopen("http://search.twitter.com/search.json?q="+query)
    dict = simplejson.loads(search.read())
    yqlconsole = yql.Public()
    pattern = re.compile('[^a-zA-Z ]+')
    for tweet in dict["results"]:
        tweet = pattern.sub(' ', tweet["text"])
        yqlquery = ('SELECT * '
                    'FROM contentanalysis.analyze '
                    'WHERE text="%s"' 
                    'AND related_entities="false" '
                    'AND enable_categorizer="false" '
                    'AND max="1"' % tweet)

        yObj = yqlconsole.execute(yqlquery)
        for row in yObj.rows:
#            print row.get('entity').get('text').get('content')
            print row.get('entity')


if __name__ == '__main__':
    searchTweets(sys.argv[1])
