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
from sendemail import send_email, append_address
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

    info = get_user(username)[0]

    year = info["dn"].split(" ")[3][:4]

    subs = database.get_subs(username)
    officerships = database.get_officerships(username)
    tags = database.get_tags()

    html_code = flask.render_template('profile.html', username=username,
            name=info["displayname"], year=year, subs=subs,
            officerships=officerships, tags = tags)
    response = flask.make_response(html_code)
    return response

@app.route('/profile_edit', methods=['GET'])
def profile_edit():
    username = auth.authenticate()

    info = get_user(username)[0]

    year = info["dn"].split(" ")[3][:4]

    subs = database.get_subs(username)
    officerships = database.get_officerships(username)
    tags = database.get_tags()

    html_code = flask.render_template('profile-edit.html', username=username,
            name=info["displayname"], year=year, subs=subs,
            officerships=officerships, tags = tags)
    response = flask.make_response(html_code)
    return response


@app.route('/searchform', methods=['GET'])
def searchform():
    username = auth.authenticate()
    tags = database.get_tags()

    html_code = flask.render_template('searchform.html',
                                    username=username, tags=tags)
    #print("tags: ", tags)
    response = flask.make_response(html_code)
    return response


@app.route('/searchresults2', methods=['GET'])
def searchresults2():
    username = auth.authenticate()
    clubquery = '%' + flask.request.args.get('clubquery') + '%'
    tags = flask.request.args.getlist('tags')
    searchpersist = clubquery.lstrip('%').rstrip('%')
    #print("cq: ", clubquery)
    #print("tags: ", tags)

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
                                        checked=tags, clubquery=searchpersist)
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

    else:
        html_code = flask.render_template('announce.html', username=username,
                                clubname=clubname, verified=False)
    response = flask.make_response(html_code)
    return response


@app.route('/get_info', methods=['GET'])
def get_info():
    username = auth.authenticate()
    clubid = flask.request.args.get('clubid')
    if clubid == "":
        print("no clubid")
        return ["invalid clubid"]

    info = database.database_get_info(clubid)

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
        string += str(tag[0]) + "#"
    string += "`"

    subbed = database.is_subbed(username, clubid)
    if subbed:
        string += "subscribed`"
    else:
        string += "not subscribed`"

    return string


@app.route('/edit_club', methods=['GET'])
def edit_club():
    username = auth.authenticate()

    clubid = flask.request.args.get("clubid")
    clubname = database.get_clubname(clubid)[0]

    if database.verify_officer(username, clubid):
        html_code = flask.render_template('editclub.html', username=username,
                                clubname=clubname, verified=True, clubid=clubid)
    else:
        html_code = flask.render_template('editclub.html', username=username,
                                clubname=clubname, verified=False)

    response = flask.make_response(html_code)
    return response


@app.route("/add_officer", methods=['GET'])
def add_officer():
    auth.authenticate()

    newofficer = flask.request.args.get('newofficer')
    clubid = flask.request.args.get('clubid')

    if not get_user(newofficer):
        print("invalid netid")
        return "invalid netid"

    database.add_officer(newofficer, clubid)
    return ''


@app.route("/edit_club_info", methods=['POST'])
def edit_club_info():
    print("edit club info")
    auth.authenticate()
    clubid = flask.request.form.get("clubid")
    print("clubid///: ", clubid)
    mission = flask.request.form.get('clubmission')
    goals = flask.request.form.get('clubgoals')
    imlink = flask.request.form.get('clubimlink')
    email = flask.request.form.get('clubemail')
    instagram = flask.request.form.get('clubinstagram')
    youtube = flask.request.form.get('clubyoutube')

    database.update_club_info(clubid=clubid, mission=mission, goals=goals,
        imlink=imlink, email=email, instagram=instagram,
        youtube=youtube)

    return ''

################
# getting user infos from netid
#######################
@app.route('/get_user', methods=['GET'])
def get_user(username):
    req_lib = ReqLib()

    reqBasic = req_lib.getJSON(
        req_lib.configs.USERS_BASIC,
        uid=username,
    )
    #print("req2: ", reqBasic)

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


# subscribes user to tag or unsubscribes from tag
@app.route('/subscribe_tag', methods=['GET'])
def subscribe_tag():
    username = auth.authenticate()
    tag = flask.request.args.get('tag')
    subscribe_tag = flask.request.args.get('subscribe_tag')
    print("subscribe_tag = ",subscribe_tag)
    print("tag: ", tag)
    if subscribe_tag=="1":
        response = database.add_sub_tag(username, tag)
    else:
        response = database.remove_sub_tag(username, tag)

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
    #print("req2: ", reqBasic)

    return reqBasic


@app.route('/send_announce', methods=['POST'])
def send_announce():

    clubid = flask.request.args.get('clubid')
    announcement = flask.request.args.get('announcement')

    # update database
    announce_result = database.send_announcement(clubid, announcement)

    # send email to subscribers
    subscribers = database.get_subscribers(clubid)
    clubname = database.get_clubname(clubid)[0]
    subscriber_emails = append_address(subscribers)
    email_result = send_email(subscriber_emails, clubname, announcement)

    if announce_result == "success" and email_result == "success":
       return "success"

    return "error"


@app.route("/get_club_announcements", methods=['GET'])
def get_club_announcements():
    clubid = flask.request.args.get('clubid')
    announcements = database.get_club_announcements(clubid)
    response = ""

    for announcement in announcements:
        response += announcement
        response += '`'

    return response


@app.errorhandler(404)
def page_not_found(e):
    username = auth.authenticate()
    html_code = flask.render_template('error.html', error="404",
                                        username=username)
    response = flask.make_response(html_code)
    return response


if __name__ == '__main__':
    app.run(debug=True, port=5002)
