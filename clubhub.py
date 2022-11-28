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
from sendemail import send_email

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
                                        checked=tags, clubquery=clubquery)
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

    tags = database.get_club_tags(clubid)
    for tag in tags:
        string += str(tag) + "#"
    string += "`"

    subbed = database.is_subbed(username, clubid)
    if subbed:
        string += "subscribed`"
    else:
        string += "not subscribed`"



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


@app.route('/edit_club', methods=['GET'])
def edit_club():
    username = auth.authenticate()

    clubid = flask.request.args.get("clubid")
    clubname = database.get_clubname(clubid)[0]
    print(clubid)

    if database.verify_officer(username, clubid):
        html_code = flask.render_template('editclub.html', username=username,
                                clubname=clubname, verified=True, clubid=clubid)
    else:
        html_code = flask.render_template('editclub.html', username=username,
                                clubname=clubname, verified=False)

    response = flask.make_response(html_code)
    return response


@app.route("/edit_club_field")
def edit_club_field():
    # email instagram youtube mission goals
    fieldname = flask.request.args.get("fieldname")
    newvalue = flask.request.args.get("newvalue")
    print("editing")




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
        return "error subscribe"

    return "success subscribe"


# subscribes user to tag or unsubscribes from tag
@app.route('/subscribe_tag', methods=['GET'])
def subscribe_tag():
    username = auth.authenticate()
    tag = flask.request.args.get('tag')
    subscribe_tag = flask.request.args.get('subscribe_tag')

    if subscribe_tag=="1":
        response = database.add_sub_tag(username, tag)
    else:
        response = database.remove_sub_tag(username, tag)

    if response:  # errored
        return "error subscribe tags"

    return "success subscribe tags"


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


@app.route('/send_announce', methods=['POST'])
def send_announce():
    clubid = flask.request.args.get('clubid')
    announcement = flask.request.args.get('announcement')
    announce_result = database.send_announcement(clubid, announcement)

    subscribers = database.get_subscribers(clubid)
    clubname = database.get_clubname(clubid)

    send_email(to=subscribers, clubname=clubname, content=announcement)

    if announce_result == "success":
        return "success"

    return "error"




if __name__ == '__main__':
    app.run(debug=True, port=5002)
