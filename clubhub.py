#!/usr/bin/env python

#-------------------------------------------------------------------
# clubhub.py
# Authors: Kevin Kim, Priya Naphade, Katie Baldwin, Lance Yoder
#-------------------------------------------------------------------

import os
import flask
import database
import auth
from req_lib import ReqLib

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


@app.route('/profile', methods=['GET'])
def profile():
    username = auth.authenticate()

    info = get_user()[0]
    print(info["uid"])

    year = info["dn"].split(" ")[3][:4]

    subs=database.get_subs(username)
    print(subs)

    html_code = flask.render_template('profile.html', username=username,
            name=info["displayname"], year=year, subs=subs)
    response = flask.make_response(html_code)
    return response


@app.route('/searchform', methods=['GET'])
def searchform():
    username = auth.authenticate()
    tags = database.get_tags()

    html_code = flask.render_template('searchform.html',
                                    username=username, tags=tags)
    print("tags: ", tags)
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

    string = ""
    print(info[0])
    for item in info[0]:
        print(item)
        string += str(item) + "\n"

    print("about to return info: ")
    print(string)
    return string


@app.errorhandler(404)
def page_not_found(e):
    username = auth.authenticate()
    html_code = flask.render_template('error.html', error="404",
                                        username=username)
    response = flask.make_response(html_code)
    return response


################
# getting user infos from netid
#######################
@app.route('/get_user', methods=['GET'])
def get_user():
    req_lib = ReqLib()

    username = auth.authenticate()

    reqBasic = req_lib.getJSON(
        req_lib.configs.USERS_BASIC,
        uid=username,
    )
    print("req2: ", reqBasic)

    return reqBasic

@app.route('/register_club', methods=['GET'])
def register_club():
    req_lib = ReqLib()

    username = auth.authenticate()

    reqBasic = req_lib.getJSON(
        req_lib.configs.USERS_BASIC,
        uid=username,
    )
    print("req2: ", reqBasic)

    return reqBasic





if __name__ == '__main__':
    app.run(debug=True, port=5002)
