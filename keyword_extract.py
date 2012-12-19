#! /usr/bin/python

import sys
import nltk
from nltk import FreqDist, WordPunctTokenizer
from nltk.corpus import stopwords
import urllib, urllib2
from nltk.util import clean_html
import re

def freqWords(string,count):
#  Based on: http://graus.nu/blog/simple-keyword-extraction-in-python/ 
	wordList=[]
	stopset = set(stopwords.words('english'))
	words = WordPunctTokenizer().tokenize(string)
	wordsCleaned = [word.lower() for word in words if word.lower() not in stopset and len(word) > 2 ]
	fdist = FreqDist(wordsCleaned).keys()
	if len(wordsCleaned) < count:
		count = len(wordsCleaned)-1
	if count > 0:
		for j in range(1,len(wordsCleaned)-1):
			if (count <= len(wordList)):
				break
			word = fdist[j-1:j]
			if len(word) > 0 and not word[0].isdigit():
				wordList.append(word[0])
	return wordList

def getWebPg(link):
	# Get url in file format
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	f = opener.open(link)

	# Read in url and store page
	page = f.read()
	f.close()

	# Parse out text (clean html tags)
	page = clean_html(page)

	match = re.search('^\s*References\s*$', page, re.MULTILINE)
	if match:
		endPage = match.start()
		page = page[:endPage]

	#print page

	#page = page.decode('utf-8');

	return page

pg = getWebPg("http://en.wikipedia.org/wiki/Usa");
print freqWords(pg, 20)
''' Demos the script, stand-alone from command link
if (len(sys.argv) != 2):
	print "Will return 15 keywords from a URL link"
	print "usage: " + sys.argv[0] + " URL"
	sys.exit()

# Get webpage
print "Retreiving webpage " + sys.argv[1]
wikiPage = getWebPg(sys.argv[1]);

# Get keywords
print "The keywords of this page is:"
print freqWords(wikiPage, 15)
'''
