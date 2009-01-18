#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Ankit Solanki.
#
# Licensed under the MIT License, see the README file.

"""
An online application that is helps with copy-editing your blog posts.
"""

__author__ = 'Ankit Solanki'


from wsgiref.handlers import CGIHandler
from google.appengine.ext import webapp

from handlers import *

_DEBUG = True
_APP_NAME = 'copy-editor'

def main():

    application = webapp.WSGIApplication([
            ('/', WelcomePage),
            ('/home', HomePage),
            (r'/post/(.*)/', ShowPost),
            ('/create', CreatePost),
            ('/save', SavePost),
            ('/save_comment', SaveComment),
            ('/add_reviewer', AddReviewer),
        ], debug=_DEBUG)
    CGIHandler().run(application)

if __name__ == '__main__':
    main()
