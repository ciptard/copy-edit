# -*- coding: utf-8 -*-

import os
import logging

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import login_required
from google.appengine.ext import db

from lib.pymarkdown import Markdown

from models import Post

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
        posts = db.GqlQuery("SELECT * FROM Post where author = :1", user)
        template_vars = {
            'posts': posts
            }
        self.generate('home.html', template_vars)

class CreatePost(BaseRequestHandler):
    """
    This Handler defines the create-post page of copy-editor.
    """
    @login_required
    def get(self):
        self.generate('create.html')
        
class SavePost(BaseRequestHandler):
    """
    This Handler defines the create-post page of copy-editor.
    """
    def post(self):
        user = users.get_current_user()
        
        title = self.request.get('title')
        body = db.Text(self.request.get('body'))

        post = Post(title=title, body=body, author=user)
        post.html = Markdown(post.body)
        post.put()

        self.redirect('/home')
        
class WelcomePage(BaseRequestHandler):
    """
    Shows welcome message to the user if he’s not logged-in
    """
    def get(self):
        user = users.GetCurrentUser()
        if not user:
            self.generate('welcome.html')
        else:
            self.redirect('/home')

class ShowPost(BaseRequestHandler):
    """
    Handler to show render a single post. Also shows the feedback form.
    """
    @login_required
    def get(self, id):
        post = Post.get_by_id(int(id))
        self.generate('post.html', {'post': post})
