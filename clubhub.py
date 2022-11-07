#!/usr/bin/env python

#-------------------------------------------------------------------
# clubhub.py
# Authors: Kevin Kim, Priya Naphade, Katie Baldwin, Lance Yoder
#-------------------------------------------------------------------

import os
import flask
import database
import auth
# import urllib.parse as up

# -------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='static/templates')
os.environ['APP_SECRET_KEY'] = "hello" # not very secret???
app.secret_key = os.environ['APP_SECRET_KEY']

# -------------------------------------------------------------------

@app.route('/logoutapp', methods=['GET'])
def logoutapp():
    return auth.logoutapp()


@app.route('/logoutcas', methods=['GET'])
def logoutcas():
    return auth.logoutcas()


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    username = auth.authenticate()
    html_code = flask.render_template('index.html', username=username)
    response = flask.make_response(html_code)
    return response


@app.route('/searchform', methods=['GET'])
def searchform():
    username = auth.authenticate()
    html_code = flask.render_template('searchform.html',
                                    username=username)
    response = flask.make_response(html_code)
    return response


@app.route('/searchresults', methods=['GET'])
def searchresults():

    username = auth.authenticate()

    # if tried to navigate to /searchresults without giving a query
    if flask.request.args.get('clubquery') == None:
        html_code = flask.render_template('error.html', error="query",
                                            username=username)
        response = flask.make_response(html_code)
        return response

    clubquery = '%' + flask.request.args.get('clubquery') + '%'
    tags = flask.request.args.getlist('tags')
    print("cq: ", clubquery)
    print("tags: ", tags)

    clubs = database.get_clubs(clubquery, tags)

    if clubs == "server":
        print("hello there")
        html_code = flask.render_template('error.html', error="server",
                                            username=username)
        response = flask.make_response(html_code)
        return response

    html_code = flask.render_template('searchresults.html', results=clubs,
                                        username=username)
    response = flask.make_response(html_code)
    return response


@app.route('/searchresults2', methods=['GET'])
def searchresults2():
    username = auth.authenticate()
    clubquery = '%' + flask.request.args.get('clubquery') + '%'
    tags = flask.request.args.getlist('tags')
    print("cq: ", clubquery)
    print("tags: ", tags)

    clubs = database.get_clubs(clubquery, tags)

    if clubs == "server":
        html_code = flask.render_template('error.html', error="server",
                                            username=username)
        response = flask.make_response(html_code)
        return response

    html_code = flask.render_template('searchresults2.html', results=clubs,
                                        username=username)
    response = flask.make_response(html_code)
    return response


@app.route('/get_info', methods=['GET'])
def get_info():
    username = auth.authenticate()
    clubid = flask.request.args.get('clubid')
    if clubid == "":
        print("AAAAAHHHHHHH NO CLUBID")
        return ["invalid clubid"]
    info = database.database_get_info(clubid)
    if info == "server":
        html_code = flask.render_template('error.html', error="server",
                                            username=username)
        response = flask.make_response(html_code)
        return response
    print("about to return info: ", info)
    print(info[0][1])
    return info



@app.errorhandler(404)
def page_not_found(e):
    username = auth.authenticate()
    html_code = flask.render_template('error.html', error="404",
                                        username=username)
    response = flask.make_response(html_code)
    return response

#get attributes
"""
@app.route('/get_name', methods=['GET'])
def get_name():
    clubid = flask.request.args.get('clubid')
    if clubid == "":
        return ["invalid clubid"]
    name = database.database_get_info(clubid)[0][0]
    return name

@app.route('/get_desc', methods=['GET'])
def get_desc():
    clubid = flask.request.args.get('clubid')
    if clubid == "":
        return ["invalid clubid"]
    desc = database.database_get_info(clubid)[0][1]
    return desc

@app.route('/get_meets', methods=['GET'])
def get_meets():
    clubid = flask.request.args.get('clubid')
    if clubid == "":
        return ["invalid clubid"]
    meets = database.database_get_info(clubid)[0][2]
    return meets

@app.route('/get_commit', methods=['GET'])
def get_commit():
    clubid = flask.request.args.get('clubid')
    if clubid == "":
        return ["invalid clubid"]
    commit = database.database_get_info(clubid)[0][3]
    return commit

@app.route('/get_website', methods=['GET'])
def get_website():
    clubid = flask.request.args.get('clubid')
    if clubid == "":
        return ["invalid clubid"]
    website = database.database_get_info(clubid)[0][4]
    print("website:", website)
    return website

@app.route('/get_verified', methods=['GET'])
def get_verified():
    clubid = flask.request.args.get('clubid')
    if clubid == "":
        return ["invalid clubid"]
    verified = database.database_get_info(clubid)[0][5]
    return verified

@app.route('/get_lastup', methods=['GET'])
def get_lastup():
    clubid = flask.request.args.get('clubid')
    if clubid == "":
        return ["invalid clubid"]
    lastup = database.database_get_info(clubid)[0][6]
    return lastup
@app.route('/get_imlink', methods=['GET'])
def get_imlink():
    clubid = flask.request.args.get('clubid')
    if clubid == "":
        return ["invalid clubid"]
    imlink = database.database_get_info(clubid)[0][7]
    return imlink
"""


if __name__ == '__main__':
    app.run(debug=True)