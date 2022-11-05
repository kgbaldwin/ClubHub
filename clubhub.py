#!/usr/bin/env python

#-------------------------------------------------------------------
# clubhub.py
# Authors: Kevin Kim, Priya Naphade, Katie Baldwin, Lance Yoder
#-------------------------------------------------------------------

import flask
import database
# import urllib.parse as up

# -------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='static/templates')

# -------------------------------------------------------------------


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

    # if tried to navigate to /searchresults without giving a query
    if flask.request.args.get('clubquery') == None:
        html_code = flask.render_template('error.html', error="query")
        response = flask.make_response(html_code)
        return response

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
        html_code = flask.render_template('error.html', error="server")
        response = flask.make_response(html_code)
        return response

    html_code = flask.render_template('searchresults2.html', results=clubs)
    response = flask.make_response(html_code)
    return response


@app.route('/get_info', methods=['GET'])
def get_info():
    print("entered get_info")
    clubid = flask.request.args.get('clubid')
    if clubid == "":
        print("AAAAAHHHHHHH NO CLUBID")
        return []
    info = database.database_get_info(clubid)
    print("after searching database")

    if info == "server":
        html_code = flask.render_template('error.html', error="server")
        response = flask.make_response(html_code)
        return response
    print("about to return info: ", info)
    return info


@app.errorhandler(404)
def page_not_found(e):
    html_code = flask.render_template('error.html', error="404")
    response = flask.make_response(html_code)
    return response


if __name__ == '__main__':
    app.run(debug=True)