"""
models.py

App Engine datastore models

"""


from google.appengine.ext import db


class PostModel(db.Model):
    """New Post Model"""
    title = db.StringProperty(required = True)
    prose = db.TextProperty(required = True)
    when = db.DateTimeProperty(auto_now_add = True)
    author = db.UserProperty(required = True)

