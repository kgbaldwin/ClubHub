#!/usr/bin/env python

#-------------------------------------------------------------------
# clubhub.py
# Authors: Kevin Kim, Priya Naphade, Katie Baldwin, Lance Yoder
#-------------------------------------------------------------------

import os
import flask
import urllib
import database
import auth
from sendemail import send_email, append_address
# -------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='static/templates')
app.secret_key = os.environ['APP_SECRET_KEY']

# -------------------------------------------------------------------

@app.route('/logoutapp', methods=['GET'])
def logoutapp():
    return
    #return auth.logoutapp()


@app.route('/logoutcas', methods=['GET'])
def logoutcas():
    return #auth.logoutcas()


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    username = 'lyoder'#auth.authenticate()
    tags = database.get_tags()
    html_code = flask.render_template('index.html', username=username, tags=tags)
    response = flask.make_response(html_code)
    return response

@app.route('/about', methods=['GET'])
def about():
    username = 'lyoder'#auth.authenticate()
    html_code = flask.render_template('about.html', username=username)
    response = flask.make_response(html_code)
    return response

@app.route('/profile', methods=['GET'])
def profile():
    username = 'lyoder'#auth.authenticate()

    info = database.get_user(username)[0]

    ou = info["dn"].split(",")[1]
    if not ou.split(" ")[0] == "OU=Undergraduate":
        year = 'N/A'
    else:
        year = ou.split(" ")[3][:4]


    subs = database.get_subscriptions(username)
    officerships = database.get_officerships(username)
    sub_tags = database.get_tags()
    unsub_tags = database.get_user_sub_tags(username)

    if (subs == "server get_subscriptions") \
        or (officerships == "server get_officerships") \
        or (sub_tags == "server get_tags") \
        or (unsub_tags == "server get_user_sub_tags"):
            html_code = flask.render_template('error.html', error="server", username=username)

    html_code = flask.render_template('profile.html', username=username,
            name=info["displayname"], year=year, subs=subs,
            officerships=officerships, sub_tags=sub_tags,
            unsub_tags=unsub_tags)
    response = flask.make_response(html_code)
    return response


@app.route('/searchresults', methods=['GET'])
def searchresults():
    username = 'lyoder'#auth.authenticate()

    clubquery = flask.request.args.get('clubquery')
    if not clubquery:
        clubquery = ''
    clubquery = '%' + str(clubquery) + '%'
    if len(clubquery) == 2:
        clubquery = ""  # strip percent signs off empty queries

    tags = flask.request.args.getlist('tags')
    searchpersist = clubquery.lstrip('%').rstrip('%')

    for index in range(len(tags)):
        tags[index] = urllib.parse.unquote_plus(tags[index])

    clubs = database.get_clubs(clubquery, tags)
    tags_dropdown = database.get_tags()

    if clubs == "server get_clubs" or tags_dropdown == "server get_tags":
        html_code = flask.render_template('error.html', error="server",
                                            username=username)
        response = flask.make_response(html_code)
        return response

    html_code = flask.render_template('searchresults.html', results=clubs,
                            username=username,tags=tags_dropdown,
                            checked=tags, clubquery=searchpersist)
    response = flask.make_response(html_code)
    return response


@app.route('/announce_page', methods=['GET'])
def announce_page():
    username = 'lyoder'#auth.authenticate()
    clubid = flask.request.args.get('clubid')

    if not clubid or not clubid.isnumeric() or database.get_clubname(clubid)[0] == "Invalid Clubid":
        html_code = flask.render_template('announce.html', username=username,
                                verified=False)

    else:

        subscribers = database.get_club_subscribers(clubid)
        subscriber_emails = append_address(subscribers)

        clubname = database.get_clubname(clubid)
        if clubname:
            clubname = clubname[0]


        verified = database.verify_officer(username, clubid)

        if (clubname == "server get_clubname") or (clubname[0] == "Invalid Clubid") or (verified == "server verify_officer"):
            html_code = flask.render_template('error.html', error="server",
                                            username=username)
            response = flask.make_response(html_code)
            return response


        if verified:
            html_code = flask.render_template('announce.html',
                        username=username, clubname=clubname,verified=True,
                        clubid=clubid, subscriber_emails=subscriber_emails)

        else:
            html_code = flask.render_template('announce.html', username=username,
                                    clubname=clubname, verified=False)
    response = flask.make_response(html_code)
    return response


@app.route('/edit_club', methods=['GET'])
def edit_club():
    username = 'lyoder'#auth.authenticate()

    clubid = flask.request.args.get("clubid")
    if not clubid or not clubid.isnumeric() or database.get_clubname(clubid)[0] == "Invalid Clubid":
        html_code = flask.render_template('editclub.html', username=username,
                                verified=False)

    else:
        clubname = database.get_clubname(clubid)
        if clubname:
            clubname = clubname[0]

        officers = database.get_club_officers(clubid)

        verified = database.verify_officer(username, clubid)

        if (clubname == "server get_clubname")\
            or (clubname == "Invalid Clubid")\
            or (verified == "server verify_officer") \
            or (officers == "server get_club_officers"):
                html_code = flask.render_template('error.html', error="server",
                                                username=username)
                response = flask.make_response(html_code)
                return response

        if verified:
            html_code = flask.render_template('editclub.html', username=username,
                                    clubname=clubname, verified=True, clubid=clubid,
                                    curr_officers=officers)
        else:
            html_code = flask.render_template('editclub.html', username=username,
                                    clubname=clubname, verified=False)

    response = flask.make_response(html_code)
    return response



#### ------------- Back-end Information Delivery ----------------- ####


@app.route('/get_info', methods=['GET'])
def get_info():
    username = 'lyoder'#auth.authenticate()
    clubid = flask.request.args.get('clubid')
    if not clubid:
        return page_not_found('lacking_info')

    info = database.database_get_info(clubid)

    if info == "server get_info":
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


@app.route("/get_club_announcements", methods=['GET'])
def get_club_announcements():
    clubid = flask.request.args.get('clubid')
    if not clubid:
        return page_not_found('_')
    # announcements is a list of tuples [(announcement, stamp, officer,), (ann2, stamp2, officer2,), etc]
    announcements = database.get_club_announcements(clubid)

    if announcements == "server get_club_announcements":
        return "announcements error"

    response = ""

    for announcement in announcements:
        response += announcement[0]
        response += '`'
        response += announcement[1].strftime("%m/%d/%Y, %H:%M")
        response += '`'
        response += announcement[2]
        response += '`'

    return response


# subscribes user to club or unsubscribes from
@app.route('/subscribe', methods=['GET'])
def subscribe():
    username = 'lyoder'#auth.authenticate()
    clubid = flask.request.args.get('clubid')
    subscribe = flask.request.args.get('subscribe')
    if not clubid or not subscribe:
        return page_not_found('lacking_info')

    if subscribe=="1":
        response = database.add_sub(username, clubid)
    elif subscribe=="0":
        if not database.verify_officer(username, clubid):
            response = database.remove_sub(username, clubid)
        else:
            return "cannot unsubscribe officer"

    if response:  # errored
        return "error"

    return "success"


# subscribes user to tag or unsubscribes from tag
@app.route('/subscribe_tag', methods=['GET'])
def subscribe_tag():
    username = 'lyoder'#auth.authenticate()
    tag = flask.request.args.get('tag')
    subscribe_tag = flask.request.args.get('subscribe_tag')
    if not tag or not subscribe_tag:
        return page_not_found('lacking_info')

    if subscribe_tag=="1":
        response = database.add_sub_tag(username, tag)
    else:
        response = database.remove_sub_tag(username, tag)

    if response:  # errored
        if response=="isofficer":
            return "success_isofficer"
        return "error"

    return "success"



@app.route("/add_officer", methods=['GET'])
def add_officer():
    #auth.authenticate()

    newofficer = flask.request.args.get('newofficer')
    clubid = flask.request.args.get('clubid')
    if not clubid or not newofficer:
        return page_not_found('lacking_info')

    if not database.get_user(newofficer) or not newofficer.isalnum():
        return "invalid netid"

    success = database.add_officer(newofficer, clubid)
    return success


@app.route("/remove_officer", methods=['GET'])
def remove_officer():
    username = 'lyoder'#auth.authenticate()

    clubid = flask.request.args.get('clubid')
    if not clubid:
        return page_not_found('lacking_info')

    success = database.remove_officer(username, clubid)
    return success


@app.route("/edit_club_info", methods=['POST'])
def edit_club_info():
    #auth.authenticate()

    data = flask.request.json

    clubid = data['clubid']
    if not clubid:
        return page_not_found('lacking_info')

    mission = data['mission']
    goals = data['goals']
    imlink = data['imlink']
    email = data['email']
    instagram = data['instagram']
    youtube = data['youtube']

    success = database.update_club_info(clubid=clubid, mission=mission, goals=goals,
        imlink=imlink, email=email, instagram=instagram,
        youtube=youtube)

    return success


@app.route('/send_announce', methods=['POST'])
def send_announce():
    username = 'lyoder'#auth.authenticate()

    # Get data embedded in the post request body
    data = flask.request.json
    clubid = data['clubid']
    announcement = data['announcement']

    # update database
    announce_result = database.send_announcement(clubid, announcement, username)
    # send email to subscribers
    subscribers = database.get_club_subscribers(clubid)
    clubname = database.get_clubname(clubid)[0]
    subscriber_emails = append_address(subscribers)
    email_result = send_email(subscriber_emails, clubname, announcement)
    if announce_result == "success" and email_result == "success":
       return "success"

    return "error"


@app.errorhandler(404)
def page_not_found(e):
    try:
        username = 'lyoder'#auth.authenticate()
    except:
        username = "False"
    if e == "lacking_info":
        error = "lacking_info"
    else: error = "404"
    html_code = flask.render_template('error.html', error=error,
                                        username=username)
    response = flask.make_response(html_code)
    return response


if __name__ == '__main__':
    app.run(debug=True, port=5002)
