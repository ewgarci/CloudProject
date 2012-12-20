import cgi
import webapp2

from google.appengine.ext import db

class Access(db.Model):
	token = db.StringProperty()
	secret = db.StringProperty()
	
	def store(self, t, s):
		self.token = t
		self.secret = s
		self.put()

