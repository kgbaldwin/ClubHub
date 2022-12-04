#!/usr/bin/env python

#-------------------------------------------------------------------
# database.py
# Authors: Kevin Kim, Priya Naphade, Katie Baldwin, Lance Yoder
#-------------------------------------------------------------------

import psycopg2

database_url = "postgres://avgqxjcj:lg3PfhN5-G_5-KH1XleCGMAJgHkZfcN1@peanut.db.elephantsql.com/avgqxjcj"

# gets clubs corresponding matching the given phrase and/or tags
def get_clubs(clubquery, tags):

    args = [clubquery] + tags
    print("args: ", args)

    try:
        with psycopg2.connect(database_url) as conn:

            with conn.cursor() as cur:

                if tags:
                    script_tags = "select id from tags WHERE (tag=%s "
                    script_mission_goals = "select groupname, id from clubs where (mission ilike %s or goals ilike %s) and id not in (select id from tags where tag = %s "
                    for _ in tags[1:]:
                        script_tags += "or tag=%s "
                        script_mission_goals += "or tag=%s "
                    script_tags +=") group by id order by count(id) desc"
                    script_mission_goals += ") order by groupname"

                    
                    cur.execute(script_tags, tags)
                    tag_ids = []
                    row = cur.fetchone()
                    while row is not None:
                        tag_ids.append(row)
                        row = cur.fetchone()

                    script_namelike = "select groupname, id from clubs where groupname ilike %s "
                    script_namelike += "and id=%s"
                    clubs = []
                    for id in tag_ids:
                        cur.execute(script_namelike, [clubquery] + [id])
                        row = cur.fetchone()
                        while row is not None:
                            clubs.append(row)
                            row = cur.fetchone()

                    script_mission_goals_tag = "select groupname, id from clubs where (mission ilike %s or goals ilike %s) and (groupname not ilike %s) and id=%s"
                    for id in tag_ids:
                        cur.execute(script_mission_goals_tag, [clubquery] + [clubquery] + [clubquery] + [id])
                        row = cur.fetchone()
                        while row is not None:
                            clubs.append(row)
                            row = cur.fetchone()

                    cur.execute(script_mission_goals, [clubquery] + [clubquery] + tags)
                    row = cur.fetchone()
                    while row is not None:
                        clubs.append(row)
                        row = cur.fetchone()
                else:
                    script_namelike = "select groupname, id from clubs where groupname ilike %s"
                    
                    cur.execute(script_namelike, [clubquery])
                    clubs = []
                    row = cur.fetchone()
                    while row is not None:
                        clubs.append(row)
                        row = cur.fetchone()

                    script_mission_goals = "select groupname, id from clubs where (mission ilike %s or goals ilike %s) and groupname not ilike %s"
                    cur.execute(script_mission_goals, [clubquery] + [clubquery] + [clubquery])
                    row = cur.fetchone()
                    while row is not None:
                        clubs.append(row)
                        row = cur.fetchone()

                return clubs

    except Exception as ex:
        print(ex)
        return "server get_clubs"


# get club details of a selected club
def database_get_info(clubid):
    print("clubid:", clubid)
    try:
        with psycopg2.connect(database_url) as conn:

            with conn.cursor() as cur:

                script = "select groupname, mission, goals, groupemail, instagram, youtube, imlink from clubs WHERE id=%s"
                cur.execute(script, [clubid])

                row = cur.fetchone()

                info = []
                while row is not None:
                    info.append(row)
                    row = cur.fetchone()
                return info

    except Exception as ex:
        print(ex)
        return "server, get_info"


# get tags for displaying on search form
def get_tags():
    try:
        with psycopg2.connect(database_url) as conn:

            with conn.cursor() as cur:

                script = "select DISTINCT tag from tags order by tag asc"
                cur.execute(script)

                row = cur.fetchone()
                tags = []
                while row is not None:
                    tags.append(row)
                    row = cur.fetchone()

                return tags

    except Exception as ex:
        print(ex)
        return "server get_tags"


# get tags linked to a club
def get_club_tags(clubid):
    try:
        with psycopg2.connect(database_url) as conn:

            with conn.cursor() as cur:

                script = "select tag from tags WHERE id=%s order by tag asc"
                cur.execute(script, [clubid])

                row = cur.fetchone()
                tags = []
                while row is not None:
                    tags.append(row)
                    row = cur.fetchone()

                return tags

    except Exception as ex:
        print(ex)
        return "server get_tags"


# subscribes user to club
def add_sub(user, clubid):
    try:
        with psycopg2.connect(database_url) as conn:

            with conn.cursor() as cur:

                # check for existence of row (may not be necessary)
                script = "select * from subscriptions where netid=%s and id=%s"
                cur.execute(script, [user, clubid])

                if cur.rowcount == 0:
                    script = "insert into subscriptions values (%s, %s)"
                    cur.execute(script, [user, clubid])

    except Exception as ex:
        print(ex)
        return "server, add_sub"


# unsubscribes user from club
def remove_sub(user, clubid):
    try:
        with psycopg2.connect(database_url) as conn:

            with conn.cursor() as cur:

                script = "select * from subscriptions where netid=%s and id=%s"
                cur.execute(script, [user, clubid])
                row = cur.fetchone()
                if row is None:
                    print("NOT SUBBED!!!!")

                # check for existence of row (may not be necessary)
                script = "delete from subscriptions where netid=%s and id=%s"
                cur.execute(script, [user, clubid])
                print("remove_sub clubid: ", clubid)
    except Exception as ex:
        print(ex)
        return "server, remove_sub"


# subscribes user to tag
def add_sub_tag(user, tag):
    try:
        with psycopg2.connect(database_url) as conn:

            with conn.cursor() as cur:

                # check for existence of row (may not be necessary)
                script = "select id from tags where tag=%s"
                cur.execute(script, [tag])

                if cur.rowcount == 0:
                    print("no such tag: in database.add_sub_tag")
                    return "no such tag: in database.add_sub_tag"

                clubid = cur.fetchone()
                while clubid is not None:
                    add_sub(user, clubid)
                    clubid = cur.fetchone()

    except Exception as ex:
        print(ex)
        return "server, add_sub_tag"


# unsubscribes user from tag
def remove_sub_tag(user, tag):
    retval = None
    try:
        with psycopg2.connect(database_url) as conn:

            with conn.cursor() as cur:

                script = "select distinct tags.id from tags, subscriptions where tag=%s and netid=%s and tags.id=subscriptions.id"
                cur.execute(script, [tag] + [user])

                clubid = cur.fetchone()
                while clubid is not None:
                    if verify_officer(user, clubid):
                        retval = "isofficer"
                    else:
                        print("removing sub: ", user, clubid[0])
                        remove_sub(user, clubid)
                    clubid = cur.fetchone()

    except Exception as ex:
        print(ex)
        return "server, remove_sub_tag"

    return retval


# check if a user is subscribed to a club
def is_subbed(netid, clubid):
    try:
        with psycopg2.connect(database_url) as conn:

            with conn.cursor() as cur:

                script = "select netid from subscriptions WHERE netid=%s AND id=%s"

                cur.execute(script, [netid, clubid])

                row = cur.fetchone()

                if row is None:
                    return False

                return True

    except Exception as ex:
        print(ex)
        return "server, is_subbed"


def get_user_sub_tags(netid):
    try:
        with psycopg2.connect(database_url) as conn:

            with conn.cursor() as cur:

                script = "select distinct tag from tags WHERE id in (select id from subscriptions where netid=%s) order by tag asc"

                cur.execute(script, [netid])

                row = cur.fetchone()
                tags = []
                while row is not None:
                    tags.append(row)
                    row = cur.fetchone()
                print("TAGS IN GET: ", tags)

                return tags

    except Exception as ex:
        print(ex)
        return "server, get_user_sub_tags"


# gets all announcements from club with given clubid and returns
# them in sorted time order
def get_club_announcements(clubid):
    script = "SELECT announcement, stamp, officer FROM announcements "
    script += "WHERE clubid=%s ORDER BY stamp DESC"

    try:
        with psycopg2.connect(database_url) as conn:

            with conn.cursor() as cur:

                cur.execute(script, [clubid])
                rows = cur.fetchall()

                '''announcements = []
                for element in rows:
                    announcements.append(element[0])
                '''
                return rows

    except Exception as ex:
        print(ex)
        return "server, get_club_announcements"


###### -------------- Profile Information -------------------- ######

# get all clubs that single user is subscribed to
def get_subs(netid):
    try:
        with psycopg2.connect(database_url) as conn:

            with conn.cursor() as cur:

                script = "select groupname, clubs.id from subscriptions, clubs WHERE netid=%s AND clubs.id=subscriptions.id"
                cur.execute(script, [netid])

                row = cur.fetchone()
                clubids = []
                while row is not None:
                    clubids.append(row)
                    row = cur.fetchone()

                return clubids

    except Exception as ex:
        print(ex)
        return "server, get_subs"


# return clubids and clubnames for clubs where netid is an officer
def get_officerships(netid):
    try:
        with psycopg2.connect(database_url) as conn:

            with conn.cursor() as cur:

                script = "select groupname, clubs.id from officers, clubs"
                script += " WHERE netid=%s AND clubs.id=officers.clubid"

                cur.execute(script, [netid])

                row = cur.fetchone()
                clubids = {}
                while row is not None:
                    clubids[row[0]] = row[1]
                    row = cur.fetchone()

                return clubids

    except Exception as ex:
        print(ex)
        return "server, get_officerships"



###### ---------------- Club Edit information ------------------ #####

# verifies that given netid is an officer of given clubid
def verify_officer(netid, clubid):
    try:
        with psycopg2.connect(database_url) as conn:

            with conn.cursor() as cur:

                script = "select * from officers where netid=%s and clubid=%s"

                cur.execute(script, [netid, clubid])

                if len(cur.fetchall()) > 0:
                    return True
                return False

    except Exception as ex:
        print(ex)
        return "server, verify_officer"


### not working ?? ###
def add_officer(netid, clubid):
    try:
        with psycopg2.connect(database_url) as conn:

            with conn.cursor() as cur:

                script = "insert into officers values (%s, %s)"

                cur.execute(script, [netid, clubid])

                add_sub(netid, clubid)

                return "success"

    except Exception as ex:
        print(ex)
        return "server, add_officer"


# send an announcement to a given club
def send_announcement(clubid, announcement, officer):
    try:

        # update the database of announcements
        with psycopg2.connect(database_url) as conn:

            with conn.cursor() as cur:

                script = "insert into announcements VALUES (%s, %s, CURRENT_TIMESTAMP, %s)"

                cur.execute(script, [clubid, announcement, officer])

        return "success"


    except Exception as ex:
        print(ex)
        return "server, send_announcements"


# get all subscribers for a club
def get_subscribers(clubid):
    try:
        with psycopg2.connect(database_url) as conn:

            with conn.cursor() as cur:

                script = "select netid from subscriptions where id=%s"
                cur.execute(script, [clubid])

                row = cur.fetchone()
                subscribers = []
                while row is not None:
                    subscribers.append(row[0])
                    row = cur.fetchone()

                return subscribers


    except Exception as ex:
        print(ex)
        return "server, get_subscribers"


# updates club info in database
def update_club_info(clubid, instagram=None, youtube=None, email=None,
            mission=None, goals=None, imlink=None):

    print("entering update_club_info in database")

    script = "UPDATE clubs SET "
    script += "instagram=%s, youtube=%s, groupemail=%s, "
    script += "mission=%s, goals=%s, imlink=%s "
    script += "WHERE id=%s"
    args = [instagram, youtube, email, mission, goals, imlink]

    try:
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(script, args+[clubid])

    except Exception as ex:
        print(ex)
        return "server, update_club_info"


# get clubname from clubid
def get_clubname(clubid):
    try:
        with psycopg2.connect(database_url) as conn:

            with conn.cursor() as cur:

                script = "select MAX(id) from clubs"
                cur.execute(script)
                num = cur.fetchone()[0]

                if int(clubid) > num or int(clubid) < 0:
                    return ("Invalid Clubid",)

                script = "select groupname from clubs where id=%s"
                cur.execute(script, [clubid])

                return cur.fetchone()

    except Exception as ex:
        print(ex)
        return "server, get_clubname"