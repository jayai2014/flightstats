# -*- coding: utf-8 -*-
"""
Created on Sun May 15 14:37:26 2016

@author: Jay
"""

from flask import Flask
app = Flask(__name__, static_folder='.', static_url_path='')

@app.route("/")
def index():
    return app.send_static_file('index.html')

@app.errorhandler(404)
def page_not_found(e):
    
    """Return a custom 404 error."""
    return app.send_static_file('404.html')


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500


if __name__ == "__main__":
    app.run()