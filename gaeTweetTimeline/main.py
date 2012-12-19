# functionality:
#   1) log in a user using the Twitter OAuth API
#   2) extract the user's home_timeline.

import oauth
import simplejson

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util


class MainHandler(webapp.RequestHandler):
      
    def get(self, mode=""):

        # key for the app
        CONSUMER_KEY = "fgPzVQVDu8pUn8tsz8ixog" 
        CONSUMER_SECRET = "MMEEaWtsEIY2CzYs8CXcgX981zext7y4kDv1Hvjfw"  
        
        # This is where the user is sent to after they have
        # authenticated with Twitter. 
        callback_url = "%s/timeline" % self.request.host_url
        
        client = oauth.TwitterClient(CONSUMER_KEY, CONSUMER_SECRET, 
            callback_url)
        
        if mode == "login":
            return self.redirect(client.get_authorization_url())
          
        elif mode == "timeline":
            auth_token = self.request.get("oauth_token")
            auth_verifier = self.request.get("oauth_verifier")
            user_info = client.get_user_info(auth_token, auth_verifier=auth_verifier)
            ACCESS_TOKEN = user_info.get("token")
            ACCESS_SECRET = user_info.get("secret")

            timeline_url = "http://api.twitter.com/1/statuses/home_timeline.json"
            results = client.make_request(url=timeline_url.encode('utf-8'), 
                                          additional_params={"count":100}, 
                                          token=ACCESS_TOKEN, 
                                          secret=ACCESS_SECRET)

            tweets = ""
            twdict = simplejson.loads(results.content)
            for tweet in twdict:
                tweets += tweet["text"] + "    "
                self.response.out.write(tweet["text"])
                self.response.out.write("<br /><br />")

        else:
            self.response.out.write("<a href='/login'>Login via Twitter</a>")
      

app = webapp.WSGIApplication([('/(.*)', MainHandler)])

