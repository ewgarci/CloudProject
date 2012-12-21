import urlparse
import oauth2 as oauth
import simplejson
import cgitb
import io
import shelve
import sqlite3

#############
# db-writing#
#############
def dbwrite(id, token, secret):
    '''id is our fake user id, coudl just be a string like '1' 
       since we just storing a single user'''
    conn = sqlite3.connect('/home/ec2-user/CloudProject/user_access.db')
    c = conn.cursor()
    # clear any previous data, so we only track one user
    c.execute('''DELETE FROM user_access''')
    c.execute('INSERT INTO user_access VALUES (%s, %s, %s)' %(id, token, secret))
    c.close()


cgitb.enable()

consumer_key = 'yBIWSP9ujJvm3MkDuG15g'
consumer_secret = 'ce9AYrul1D1dZO66O00f7To2KKYuNiTjiT4452RDk'

request_token_url = 'http://twitter.com/oauth/request_token'
access_token_url = 'http://twitter.com/oauth/access_token'
authorize_url = 'http://twitter.com/oauth/authorize'

consumer = oauth.Consumer(consumer_key, consumer_secret)
client = oauth.Client(consumer)



# Step 1: Get a request token. This is a temporary token that is used for 
# having the user authorize an access token and to sign the request to obtain 
# said access token.

resp, content = client.request(request_token_url, "GET")
if resp['status'] != '200':
    raise Exception("Invalid response %s." % resp['status'])
	
request_token = dict(urlparse.parse_qsl(content))

# Step 2: Redirect to the provider. Since this is a CLI script we do not 
# redirect. In a web application you would redirect the user to the URL
# below.

print "Content-type: text/html\n\n"

print "<html>"
print "<head>"
print "<title>A web page that points a browser to a different page after 2 seconds</title>"
print '<meta http-equiv="refresh" content="2; URL='
print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])
print '">'
print "<meta name=\"keywords\" content=\"automatic redirection\">"
print "</head>"
print "<body>"
print "If your browser doesn't automatically go there within a few seconds, "
print "you may want to go to "
print "<a href="
print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])
print ">the destination</a>" 
print " manually."
print "</body>"
print "</html>"

#rq = shelve.open('my_shelf.dat')

# Add stuff to the shelve object
#rq['request token'] = request_token

# close it when you're done.
#rq.close()

#dbwrite("rq", request_token['oauth_token'], request_token['oauth_token_secret'])

