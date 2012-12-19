#!/usr/bin/python

import urllib
import simplejson
import sys
import cgitb
import cgi
import keyword_extract
import simplejson, json

from xml.dom.minidom import parseString
from string import rfind
from twsearch import searchTweets

def getTweets(query):
	#print "<p>Search Value is:", query
	#print "<p>"
	
	search = urllib.urlopen("http://search.twitter.com/search.json?q="+query)
	# dict is a dictionary created by parsing the search string
	#all tweets are in dict["result"], which is a list of dictionaries
	dict = simplejson.loads(search.read())
	
	results = []
	for result in dict["results"]:
		results.append(result["text"].encode('utf-8'))
		#print "<p>"
		#print "*",result["text"].encode('utf-8'),"\n"

	return results
	
	#print searchTweets(query)

def getWebPgTweets(url):
	webpage = keyword_extract.getWebPg(url)
	keywords = keyword_extract.freqWords(webpage, 15)
	
	keywordTweets = dict()
	
	for keyword in keywords:
		tweets = getTweets(keyword)
		keywordTweets[keyword] = tweets
	
	return json.dumps(keywordTweets)

# For webpage DEMO
cgitb.enable()

form = cgi.FieldStorage()

query = form.getvalue("urllink")

print getWebPgTweets(query)

