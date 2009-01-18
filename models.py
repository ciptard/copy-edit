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
    reviewers = db.StringListProperty()
    updated = db.DateTimeProperty(auto_now_add = True)

class ReviewComment(db.Model):
    """
    Models a review comment.
    """
    author = db.UserProperty(required = True)
    
    # No HTML is allowed for ReviewComments
    body = db.TextProperty(required = True)
    
    published = db.DateTimeProperty(auto_now_add = True)
    post = db.ReferenceProperty(Post, collection_name='review_comments')
