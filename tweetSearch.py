#!/usr/bin/python

import urllib
import simplejson
import sys
import cgitb
import cgi

from xml.dom.minidom import parseString
from string import rfind
from twsearch import searchTweets

def getTweets(query):
	print "<p>Search Value is:", query
	print "<p>"
	
	search = urllib.urlopen("http://search.twitter.com/search.json?q="+query)
	# dict is a dictionary created by parsing the search string
	#all tweets are in dict["result"], which is a list of dictionaries
	dict = simplejson.loads(search.read())
	
	for result in dict["results"]:
		print "<p>"
		print "*",result["text"].encode('utf-8'),"\n"
	
	#print searchTweets(query)

cgitb.enable()

form = cgi.FieldStorage()

query = form["search"].value

print "Content-type: text/html\n\n"
print "<html>"

getTweets(query)

print "</html>"
