# -*- coding: utf-8 -*-

import os
import logging

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import login_required
from google.appengine.ext import db

from lib.pymarkdown import Markdown

from models import Post, ReviewComment
import models

class BaseRequestHandler(webapp.RequestHandler):
    """
    Supplies a common template generation function.
    When you call generate(), we augment the template variables supplied with
    the current user in the 'user' variable and the current webapp request
    in the 'request' variable.
    """
    def generate(self, template_name, template_values={}):
        values = {
            'request': self.request,
            'user': users.GetCurrentUser(),
            'login_url': users.CreateLoginURL(self.request.uri),
            'logout_url': users.CreateLogoutURL('http://' + self.request.host + '/'),
            'debug': self.request.get('deb'),
            'application_name': 'copy-editor',
        }
        values.update(template_values)
        directory = os.path.dirname(__file__)
        path = os.path.join(directory, os.path.join('templates', template_name))
        logging.debug("BaseRequestHandler :: generate() :: rendering template %s" % path)
        self.response.out.write(template.render(path, values, debug=True))

class HomePage(BaseRequestHandler):
    """
    This Handler defines the home page of copy-editor.
    """
    @login_required
    def get(self):
        user = users.GetCurrentUser()
        my_posts = db.GqlQuery("SELECT * FROM Post where author = :1", user)
        posts_to_review = models.posts_to_review(user)
        template_vars = {
            'posts': my_posts,
            'to_review': posts_to_review,
            'page_title': 'Home'
            }
        self.generate('home.html', template_vars)

class CreatePost(BaseRequestHandler):
    """
    This Handler defines the create-post page of copy-editor.
    """
    @login_required
    def get(self):
        self.generate('create.html', {'page_title': 'Create Post'})
        
class SavePost(BaseRequestHandler):
    """
    This class handles the creation of a post.
    """
    def post(self):
        user = users.get_current_user()
        
        title = self.request.get('title')
        body = db.Text(self.request.get('body'))

        post = Post(title=title, body=body, author=user)
        post.html = Markdown(post.body)
        post.put()

        self.redirect('/home')


class SaveComment(BaseRequestHandler):
    """
    This class handles the creation of a review-comment.
    """
    def post(self):
        user = users.get_current_user()
        
        body = db.Text(self.request.get('body'))
        post_id = db.Text(self.request.get('post_id'))
        
        post = Post.get_by_id(int(post_id))

        review_comment = ReviewComment(body=body, post=post, author=user)
        review_comment.put()

        self.redirect('/post/%s/' % post_id)


class AddReviewer(BaseRequestHandler):
    """
    This class handles adding a reviewer to an post.
    """
    def post(self):
        user = users.get_current_user()
        
        post_id = db.Text(self.request.get('post_id'))
        email_address = self.request.get('email_address')
        
        post = Post.get_by_id(int(post_id))
        reviewer = users.User(email_address)
        if post.reviewers:
            post.reviewers.append(reviewer)
        else:
            post.reviewers = [reviewer]

        post.put()

        self.redirect('/post/%s/' % post_id)
        
class WelcomePage(BaseRequestHandler):
    """
    Shows welcome message to the user if he’s not logged-in
    """
    def get(self):
        user = users.GetCurrentUser()
        if not user:
            self.generate('welcome.html', {'page_title': 'Welcome'})
        else:
            self.redirect('/home')


class ShowPost(BaseRequestHandler):
    """
    Handler to show render a single post. Also shows the feedback form.
    """
    @login_required
    def get(self, id):
        user = users.GetCurrentUser()
        post = Post.get_by_id(int(id))
        if post.author == user or user in post.reviewers:
            self.generate('post.html', {'post': post, 'page_title': 'Post', 'user': user})
        else:
            self.generate('error.html', {
                'error_message': 'You don’t have permission to view that post',
                'page_title': 'Error'})
