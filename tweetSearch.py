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
#from twsearch import searchTweets

def getTweets(query):
	#print "<p>Search Value is:", query
	#print "<p>"
	
	search = urllib.urlopen("http://search.twitter.com/search.json?q="+query)
	# dict is a dictionary created by parsing the search string
	#all tweets are in dict["result"], which is a list of dictionaries
	resultDict = simplejson.loads(search.read())

	results = []
	if resultDict and "results" in resultDict.keys():	
		for result in resultDict["results"]:
			results.append(result)
			#print "<p>"
			#print "*",result["text"].encode('utf-8'),"\n"

	return results
	
	#print searchTweets(query)

def getWebPgTweets(url):
	webpage = keyword_extract.getWebPg(url)
	keywords = keyword_extract.freqWords(webpage, 7)
	
	keywordTweets = dict()
	
	for keyword in keywords:
		tweets = getTweets(keyword)
        extractList = []
        for t in tweets:
            tempdic = dict()
            tempdic["text"] = t["text"]
            tempdic["from_user"] = t["from_user"]
            tempdic["from_user_name"] = t["from_user_name"]
            tempdic["profile_image_url"] = t["profile_image_url"]
            extractList.append(tempdic)

        keywordTweets[keyword] = extractList
	
	return json.dumps(keywordTweets)

# For webpage DEMO
cgitb.enable()

form = cgi.FieldStorage()

query = form.getvalue("urllink")

print "Content-type: text/html\n\n"
print getWebPgTweets(query)

