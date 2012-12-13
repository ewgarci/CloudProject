#!/usr/bin/python

import urllib
import simplejson
import sys
from xml.dom.minidom import parseString
from string import rfind
from twsearch import searchTweets

def findTitle(link):
    #print "-----src: "+prevlinks[-1]+"-----"
    #print "des: "+des_title+"\nprev: "
    #print prevlinks

    last_slash = rfind(link, '/')
    topic = link[last_slash+1:]

    print searchTweets(topic)
    return topic



if __name__ == '__main__':
    findTitle(sys.argv[1])

