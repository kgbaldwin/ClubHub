#!/usr/bin/env python

#-------------------------------------------------------------------
# clubhub.py
# Authors: Kevin Kim, Priya Naphade, Katie Baldwin, Lance Yoder
#-------------------------------------------------------------------

import time
import flask
#import database

#-------------------------------------------------------------------

app = flask.Flask(__name__)

#-------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    html_code = flask.render_template('index.html')
    response = flask.make_response(html_code)
    return response


@app.route('/searchform', methods=['GET'])
def searchform():
    html_code = flask.render_template('searchform.html')
    response = flask.make_response(html_code)
    return response


@app.route('/searchresults', methods=['GET'])
def searchresults():
    html_code = flask.render_template('searchresults.html')
    response = flask.make_response(html_code)
    return response



if __name__ == '__main__':
    app.run(debug=True)