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
    tags = database.get_tags()
    html_code = flask.render_template('index.html', username=username,tags=tags)
    response = flask.make_response(html_code)
    return response


@app.route('/profile', methods=['GET'])
def profile():
    username = auth.authenticate()

    info = get_user()[0]
    print(info["uid"])

    year = info["dn"].split(" ")[3][:4]

    subs = database.get_subs(username)
    officerships = database.get_officerships(username)

    html_code = flask.render_template('profile.html', username=username,
            name=info["displayname"], year=year, subs=subs,
            officerships=officerships)
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


@app.route('/searchresults2', methods=['GET'])
def searchresults2():
    username = auth.authenticate()
    clubquery = '%' + flask.request.args.get('clubquery') + '%'
    tags = flask.request.args.getlist('tags')
    print("cq: ", clubquery)
    print("tags: ", tags)

    clubs = database.get_clubs(clubquery, tags)
    tags_dropdown = database.get_tags()
    subbed_clubs = database.get_subs(username)

    if clubs == "server":
        html_code = flask.render_template('error.html', error="server",
                                            username=username)
        response = flask.make_response(html_code)
        return response

    html_code = flask.render_template('searchresults2.html', results=clubs,
                                        username=username,tags=tags_dropdown,
                                        checked=tags)
    response = flask.make_response(html_code)
    return response


@app.route('/announce', methods=['GET'])
def announce():
    username = auth.authenticate()
    clubid = flask.request.args.get('clubid')
    clubname = database.get_clubname(clubid)[0]

    if database.verify_officer(username, clubid):
        html_code = flask.render_template('announce.html', username=username,
                                clubname=clubname, verified=True, clubid=clubid)
        # Returns list of clubids for which this user in an officer
        '''officer_clubids = database.get_officerships(username)
        clubnames, clubids = list(officer_clubids.keys()), list(officer_clubids.values())
        num_officerships = len(clubnames)
            # in html_code:
        officerships= zip(clubnames, clubids), num_officerships=num_officerships,
        '''
    else:
        html_code = flask.render_template('announce.html', username=username,
                                clubname=clubname, verified=False)
    response = flask.make_response(html_code)
    return response


@app.route("/add_officer", methods=['POST'])
def add_officer():
    auth.authenticate()
    newofficer = flask.request.form.get('newofficer')
    clubid = flask.request.form.get('clubid')

    result = database.add_officer(newofficer, clubid)
    print(result)    # success or failure
    return ''


@app.route('/get_info', methods=['GET'])
def get_info():
    username = auth.authenticate()
    clubid = flask.request.args.get('clubid')
    if clubid == "":
        print("AAAAAHHHHHHH NO CLUBID")
        return ["invalid clubid"]

    info = database.database_get_info(clubid)
    print(info)

    if info == "server":
        html_code = flask.render_template('error.html', error="server",
                                            username=username)
        response = flask.make_response(html_code)
        return response

    string = ""
    for item in info[0]:
        string += str(item) + "`"

    subbed = database.is_subbed(username, clubid)
    if subbed:
        string += "subscribed\n"
    else:
        string += "not subscribed\n"

    #print("about to return info: ")
    #print(string)
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


# subscribes user to club or unsubscribes from
@app.route('/subscribe', methods=['GET'])
def subscribe():
    username = auth.authenticate()
    clubid = flask.request.args.get('clubid')
    subscribe = flask.request.args.get('subscribe')

    if subscribe=="1":
        response = database.add_sub(username, clubid)
    else:
        response = database.remove_sub(username, clubid)

    if response:  # errored
        return "error"

    return "success"


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


@app.route('/send_announce')
def send_announce():
    clubid = flask.request.args.get('clubid')
    announcement = flask.request.args.get('announcement')
    announce_result = database.send_announcement(clubid, announcement)

    if announce_result == "success":
        return "success"

    return "error"




if __name__ == '__main__':
    app.run(debug=True, port=5002)
