# -*- coding: utf-8 -*-

from google.appengine.ext import db
from google.appengine.api import users

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
    reviewers = db.ListProperty(users.User)
    updated = db.DateTimeProperty(auto_now_add = True)

    def formattedd_time(self):
        return self.updated.strftime("%Y-%m-%d")


class ReviewComment(db.Model):
    """
    Models a review comment.
    """
    author = db.UserProperty(required = True)
    
    # No HTML is allowed for ReviewComments
    body = db.TextProperty(required = True)
    
    published = db.DateTimeProperty(auto_now_add = True)
    post = db.ReferenceProperty(Post, collection_name='review_comments')


def posts_to_review(user):
    """
    Return a list of posts that are pending review by the input user.
    This method seems to be horribly inefficient, but it works for now.
    """
    other_posts = db.GqlQuery("SELECT * from Post where author != :1", user)
    return [post for post in other_posts if user in post.reviewers]
