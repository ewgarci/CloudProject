#!/usr/bin/python

import urllib
import simplejson
import sys
from xml.dom.minidom import parseString
from string import rfind
from twsearch import searchTweets
import re, string
import yql

def findTitle(link):
    # get the topic from URL
    last_slash = rfind(link, '/')
    topic = link[last_slash+1:]

    # query the wikipedia API for the content
    out_link = ("http://en.wikipedia.org/w/api.php?"
                  "format=xml"
                  "&action=query"
                    "&titles=%s"
                    "&prop=revisions"
                    "&rvprop=content" % link)
#                    "&rvprop=content&rvparse" % link)

    retstr = urllib.urlopen(out_link.encode('utf-8'))
    dom = parseString(retstr.read())

    tag1 = dom.getElementsByTagName('page')[0]
    title = tag1.getAttribute('title')

    tag2 = dom.getElementsByTagName('rev')[0]
    pattern = re.compile('[^a-zA-Z ]+')
    wikicontent = tag2.firstChild.nodeValue
    wikicontent = pattern.sub('', wikicontent)

    yqlconsole = yql.Public()

    yqlquery = ('SELECT * '
                'FROM contentanalysis.analyze '
                'WHERE text="%s"' 
                'AND related_entities="false" '
                'AND show_metadata="true" '
                'AND enable_categorizer="false" '
                'AND max="50"' % wikicontent)

    yresult = yqlconsole.execute(yqlquery)
#    for row in yresult.rows:
#        for entity in row.get('entity'):
#            print entity

if __name__ == '__main__':
    findTitle(sys.argv[1])

