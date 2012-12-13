#!/usr/bin/python

import urllib
import simplejson
import sys

def searchTweets(query):
    # search is a string in json format returned by twitter search API
    search = urllib.urlopen("http://search.twitter.com/search.json?q="+query)
    # dict is a dictionary created by parsing the search string
    # all tweets are in dict["result"], which is a list of dictionaries
    dict = simplejson.loads(search.read())
    #for result in dict["results"]:
    #    print "*",result["text"],"\n"
    return dict["results"]


def getBuzz(text):
    return 123

if __name__ == '__main__':
    searchTweets(sys.argv[1])
