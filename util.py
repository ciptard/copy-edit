# -*- coding: utf-8 -*-

import os

def get_server_url():
    """ Return the current URL of the server """
    return "http://%s/" % os.environ['SERVER_NAME']
