import urlparse
import oauth2 as oauth
import simplejson
import urllib
import cgitb
import re
import cgi
import sqlite3
import keyword_extract

consumer_key = 'fgPzVQVDu8pUn8tsz8ixog'
consumer_secret = 'MMEEaWtsEIY2CzYs8CXcgX981zext7y4kDv1Hvjfw'

consumer = oauth.Consumer(consumer_key, consumer_secret)

request_token_url = 'http://twitter.com/oauth/request_token'
access_token_url = 'http://twitter.com/oauth/access_token'
authorize_url = 'http://twitter.com/oauth/authorize'



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

def getWebPgTweets2(keyword):
      
	tweets = getTweets(keyword)
	extractList = []
	for t in tweets:
		tempdic = dict()
		tempdic["text"] = t["text"]
		tempdic["from_user"] = t["from_user"]
		tempdic["from_user_name"] = t["from_user_name"]
		tempdic["profile_image_url"] = t["profile_image_url"]
		extractList.append(tempdic)
	#print extractList
	#print ""
	return extractList


def getWebPgTweets(url, no_keywords):
	webpage = keyword_extract.getWebPg(url)
	keywords = keyword_extract.freqWords(webpage, no_keywords)
	
	#print keywords

	token = oauth.Token("1008218550-g8WKidpCiwoxbyf2OsG6auJmI6oUdo2sI5grEUc".encode('utf-8'), "pYZdeU79HLOElzI3lcYloGSMsOvsK6MiuMtYjFaknU".encode('utf-8'))
	client = oauth.Client(consumer, token)
	timeline_url = "http://api.twitter.com/1/statuses/home_timeline.json?count=500"
	response, data = client.request(timeline_url.encode('utf-8'))
	tweets = simplejson.loads(data)

	
	kt = dict()
	for keyword in keywords:
		tweetsFiltered = []
		for tweet in tweets:
			if keyword.lower() in tweet["text"].lower():
				#re.compile(r'\b({0})\b'.format(keyword), flags=re.IGNORECASE).search
				tempdic = dict()
				tempdic["text"] = tweet["text"]
				tempdic["from_user"] = tweet["user"]["name"]
				tempdic["from_user_name"] = tweet["user"]["screen_name"]
				tempdic["profile_image_url"] = tweet["user"]["profile_image_url_https"]
				tweetsFiltered.append(tempdic)
		if tweetsFiltered:
			kt[keyword] = tweetsFiltered
		else:
			#tweetsFiltered.append(getWebPgTweets2(keyword))
			kt[keyword] = getWebPgTweets2(keyword)

	return simplejson.dumps(kt)
	
cgitb.enable()

form = cgi.FieldStorage()

query = form.getvalue("urllink")
keywords = form.getvalue("keywords")
no_of_kw = int(keywords)

print "Content-type: text/html\n\n"
print getWebPgTweets(query, no_of_kw)

#print getWebPgTweets("http://en.wikipedia.org/wiki/Sarah_Palin", 5)


###################################
# The table is in user_access.db. #
# it has three fields:            #
# id | token | secret             #
###################################

#############
# db-writing#
#############
def dbwrite(id, token, secret):
    '''id is our fake user id, coudl just be a string like '1' 
       since we just storing a single user'''
    conn = sqlite3.connect('user_access.db')
    c = conn.cursor()
    # clear any previous data, so we only track one user
    c.execute('''DELETE FROM user_access''')
    c.execute('INSERT INTO user_access VALUES (%s, %s, %s)' %(id, token, secret))
    c.commit()
    c.close()
    conn.close()

##############
# db-reading #
##############
def dbread():
    conn = sqlite3.connect('user_access.db')
    c = conn.cursor()
    c.execute('SELECT * FROM user_access')
    user = c.fetchone()
    c.close()
    conn.close()
    return user

