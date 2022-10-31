#!/usr/bin/env python

#-------------------------------------------------------------------
# clubhub.py
# Authors: Kevin Kim, Priya Naphade, Katie Baldwin, Lance Yoder
#-------------------------------------------------------------------

import flask
import psycopg2
import database
import urllib.parse as up

#-------------------------------------------------------------------

app = flask.Flask(__name__)

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
    clubquery = '%' + flask.request.args.get('clubquery') + '%'
    tags = flask.request.args.getlist('tags')
    print("cq: ", clubquery)
    print("tags: ", tags)

    clubs = database.get_clubs(clubquery, tags)

    if clubs == "server":
        print("hello there")
        html_code = flask.render_template('error.html', error="server")
        response = flask.make_response(html_code)
        return response

    html_code = flask.render_template('searchresults.html', results=clubs)
    response = flask.make_response(html_code)
    return response


@app.route('/searchresults2', methods=['GET'])
def searchresults2():
    clubquery = '%' + flask.request.args.get('clubquery') + '%'
    tags = flask.request.args.getlist('tags')
    print("cq: ", clubquery)
    print("tags: ", tags)

    clubs = database.get_clubs(clubquery, tags)

    if clubs == "server":
        print("hello there")
        html_code = flask.render_template('error.html', error="server")
        response = flask.make_response(html_code)
        return response

    html_code = flask.render_template('searchresults2.html', results=clubs)
    response = flask.make_response(html_code)
    return response

@app.errorhandler(404)
def page_not_found(e):
    html_code = flask.render_template('error.html', error="404")
    response = flask.make_response(html_code)
    return response

if __name__ == '__main__':
    #searchresults()
    app.run(debug=True)