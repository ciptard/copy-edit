# -*- coding: utf-8 -*-

from google.appengine.ext import db

class Post(db.Model):
    """
    This class models a single blog post. Pretty basic stuff.
    """
    # Title and body are the only two major fields we have
    title = db.StringProperty(required = True)
    body = db.TextProperty(required = True)

    # HTML is auto-generated from the body
    html = db.TextProperty()

    # meta-fields
    author = db.UserProperty(required = True)
    updated = db.DateTimeProperty(auto_now_add = True)
