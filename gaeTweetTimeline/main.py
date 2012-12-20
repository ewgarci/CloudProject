# functionality:
#   1) log in a user using the Twitter OAuth API
#   2) extract the user's home_timeline.

import oauth
import simplejson
from access import Access

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util


class MainHandler(webapp.RequestHandler):

    def getNewsfeed(self, client):
        user_acs=Access.all()
        for ua in user_acs:
            ACCESS_TOKEN = ua.token
            ACCESS_SECRET = ua.secret

        timeline_url = "http://api.twitter.com/1/statuses/home_timeline.json"
        results = client.make_request(url=timeline_url.encode('utf-8'), 
                                      additional_params={"count":100}, 
                                      token=ACCESS_TOKEN, 
                                      secret=ACCESS_SECRET)

        twdict = simplejson.loads(results.content)
        return twdict

    def get(self, mode=""):
        # key for the app
        CONSUMER_KEY = "fgPzVQVDu8pUn8tsz8ixog" 
        CONSUMER_SECRET = "MMEEaWtsEIY2CzYs8CXcgX981zext7y4kDv1Hvjfw"  
       
        # This is where the user is sent to after they have
        # authenticated with Twitter. 
        callback_url = "%s/verify" % self.request.host_url
        
        client = oauth.TwitterClient(CONSUMER_KEY, CONSUMER_SECRET, 
            callback_url)
        
        if mode == "login":
            return self.redirect(client.get_authorization_url())

        elif mode == "verify":
            auth_token = self.request.get("oauth_token")
            auth_verifier = self.request.get("oauth_verifier")
            user_info = client.get_user_info(auth_token, auth_verifier=auth_verifier)
            ACCESS_TOKEN = user_info.get("token")
            ACCESS_SECRET = user_info.get("secret")
            # WARNING: only keeps one user's access key!
            db.delete(Access.all())
            user_access = Access()
            user_access.store(ACCESS_TOKEN, ACCESS_SECRET)
            self.response.out.write("<a href='/timeline'>Go to my news feed</a>")

        elif mode == "timeline":
            twdict = self.getNewsfeed(client)
            tweets = ""
#            self.response.out.write(twdict)
            for k,v in twdict[0]["user"].items():
                print k
#            for tweet in twdict:
#                tweets += tweet["text"] + "    "
#                self.response.out.write("{text: '%s'}" % tweet["text"])
#                self.response.out.write("<br /><br />")

        elif mode == "query":
            keyword = self.request.get("kw")
            twdict = self.getNewsfeed(client)
            tweets = []
            for tweet in twdict:
                if keyword in tweet["text"]:
                # re.compile(r'\b({0})\b'.format(keyword), flags=re.IGNORECASE).search
                    tweets += '{"text": "%s", "from_user": "%s", "from_user_name": "%s", "profile_image_url": "%s"}' \
                            % (tweet["text"], tweet["user"]["name"], tweet["user"]["screen_name"], tweet["user"]["profile_image_url_https"])
            self.response.out.write(tweets)

        else:
            self.response.out.write("<a href='/login'>Login via Twitter</a>")
      

app = webapp.WSGIApplication([('/(.*)', MainHandler)])

