#!/usr/bin/env python

#-------------------------------------------------------------------
# database.py
# Authors: Kevin Kim, Priya Naphade, Katie Baldwin, Lance Yoder
#-------------------------------------------------------------------

import os
import psycopg2
import urllib.parse as up
from req_lib import ReqLib
from psycopg2.pool import SimpleConnectionPool as simPool

up.uses_netloc.append("postgres")
url = up.urlparse(os.environ["DATABASE_URL"])

pool = simPool(1, 5, database=url.path[1:], user=url.username,
                            password=url.password, host=url.hostname,
                            port=url.port)

# gets clubs corresponding matching the given phrase and/or tags
def get_clubs(clubquery, tags):

    try:
        conn = pool.getconn()

        with conn.cursor() as cur:

            if tags:
                # get id's of clubs matching tags, ranked by number of matches
                script_get_tag_ids = "select id from tags WHERE (tag=%s "
                for _ in tags[1:]:
                    script_get_tag_ids += "or tag=%s "
                script_get_tag_ids +=") group by id order by count(id) desc, id"

                cur.execute(script_get_tag_ids, tags)
                tag_ids = []
                row = cur.fetchone()
                while row is not None:
                    tag_ids.append(row)
                    row = cur.fetchone()

                #########
                clubs = []
                if clubquery:
                    # get clubnames matching id's and name
                    script_namelike = "select groupname, id from clubs where groupname ilike %s and id=%s"
                    for id in tag_ids:
                        cur.execute(script_namelike, [clubquery] + [id])
                        row = cur.fetchone()
                        if row is not None:
                            clubs.append(row)

                    #print("clubs: ", clubs)
                    # get clubnames matching id's and (mis/goals), but NOT name
                    script_mission_goals_tag = "select groupname, id from clubs where (mission ilike %s or goals ilike %s) and (groupname not ilike %s) and id=%s"
                    for id in tag_ids:
                        cur.execute(script_mission_goals_tag, [clubquery] + [clubquery] + [clubquery] + [id])
                        row = cur.fetchone()
                        if row is not None:
                            clubs.append(row)

                    # get clubnames matching id's, but NOT name, mis/goals
                    script_tag = "select groupname, id from clubs where mission not ilike %s and goals not ilike %s and groupname not ilike %s and id=%s"
                    for id in tag_ids:
                        cur.execute(script_tag, [clubquery] + [clubquery] + [clubquery] + [id])
                        row = cur.fetchone()
                        if row is not None:
                            clubs.append(row)

                else:
                    # get clubnames matching id's
                    script_tag = "select groupname, id from clubs where id=%s"
                    for id in tag_ids:
                        cur.execute(script_tag, [id])
                        row = cur.fetchone()
                        if row is not None:
                            clubs.append(row)

            else:
                if clubquery:
                    script_namelike = "select groupname, id from clubs where groupname ilike %s order by groupname"

                    cur.execute(script_namelike, [clubquery])
                    clubs = []
                    row = cur.fetchone()
                    while row is not None:
                        clubs.append(row)
                        row = cur.fetchone()

                    script_mission_goals = "select groupname, id from clubs where (mission ilike %s or goals ilike %s) and groupname not ilike %s order by groupname"
                    cur.execute(script_mission_goals, [clubquery] + [clubquery] + [clubquery])
                    row = cur.fetchone()
                    while row is not None:
                        clubs.append(row)
                        row = cur.fetchone()
                else:
                    script_namelike = "select groupname, id from clubs order by groupname"

                    cur.execute(script_namelike)
                    clubs = []
                    row = cur.fetchone()
                    while row is not None:
                        clubs.append(row)
                        row = cur.fetchone()

            return clubs

    except Exception as ex:
        print("__________database.py:", ex)
        return "server get_clubs"
    finally:
        pool.putconn(conn)


# get club details of a selected club
def database_get_info(clubid):

    try:
        print('inside try, database_get_info')
        conn = pool.getconn()
        print('retrieving cursor')
        with conn.cursor() as cur:
            print("about to execute SQL script")
            script = "select groupname, mission, goals, groupemail, instagram, youtube, imlink from clubs WHERE id=%s"
            cur.execute(script, [clubid])
            print("executed script")

            row = cur.fetchone()
            print("fetched one row")
            info = []
            while row is not None:
                info.append(row)
                row = cur.fetchone()
            return info

    except psycopg2.OperationalError as ex:
        print("__________database.py get clubs: ", ex)

        return "server, get_info"
    finally:
        pool.putconn(conn)
    ############ catch general exception?


# get tags for displaying on search form
def get_tags():
    try:
        conn = pool.getconn()

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
        print("__________database.py get tags:", ex)
        return "server get_tags"

    finally:
        pool.putconn(conn)


# get tags linked to a club
def get_club_tags(clubid):
    try:
        conn = pool.getconn()
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
        print("__________database.py get club tags:", ex)
        return "server get_tags"

    finally:
        pool.putconn(conn)


# subscribes user to club
def add_sub(user, clubid):
    try:
        conn = pool.getconn()
        with conn.cursor() as cur:

            # check for existence of row (may not be necessary)
            script = "select * from subscriptions where netid=%s and id=%s"
            cur.execute(script, [user, clubid])

            if cur.rowcount == 0:
                script = "insert into subscriptions values (%s, %s)"
                cur.execute(script, [user, clubid])

    except Exception as ex:
        print("__________database.py add sub:", ex)
        return "server, add_sub"

    finally:
        pool.putconn(conn)


# unsubscribes user from club
def remove_sub(user, clubid):
    try:
        conn = pool.getconn()
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
        print("__________database.py remove sub:", ex)
        return "server, remove_sub"

    finally:
        pool.putconn(conn)


# subscribes user to tag
def add_sub_tag(user, tag):
    try:
        conn = pool.getconn()

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
        print("__________database.py add sub tag:", ex)
        return "server, add_sub_tag"


# unsubscribes user from tag
def remove_sub_tag(user, tag):
    retval = None
    try:
        conn = pool.getconn()
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
        print("__________database.py remove sub tag:", ex)
        return "server, remove_sub_tag"

    finally:
        pool.putconn(conn)

    return retval


# check if a user is subscribed to a club
def is_subbed(netid, clubid):
    try:
        conn = pool.getconn()
        with conn.cursor() as cur:

            script = "select netid from subscriptions WHERE netid=%s AND id=%s"

            cur.execute(script, [netid, clubid])

            row = cur.fetchone()

            if row is None:
                return False

            return True

    except Exception as ex:
        print("__________database.py is subbed:", ex)
        return "server, is_subbed"

    finally:
        pool.putconn(conn)


def get_user_sub_tags(netid):
    try:
        conn = pool.getconn()
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
        print("__________database.py get user sub tags: ", ex)
        return "server, get_user_sub_tags"

    finally:
        pool.putconn(conn)


# gets all announcements from club with given clubid and returns
# them in sorted time order
def get_club_announcements(clubid):
    script = "SELECT announcement, stamp, officer FROM announcements "
    script += "WHERE clubid=%s ORDER BY stamp DESC"

    try:
        conn = pool.getconn()
        with conn.cursor() as cur:

            cur.execute(script, [clubid])
            rows = cur.fetchall()

            return rows

    except Exception as ex:
        print("__________database.py get club announcements: ", ex)
        return "server, get_club_announcements"

    finally:
        pool.putconn(conn)


###### -------------- Profile Information -------------------- ######

# get all clubs that single user is subscribed to
def get_subs(netid):
    try:
        conn = pool.getconn()
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
        print("__________database.py get subs: ", ex)
        return "server, get_subs"
    
    finally:
        pool.putconn(conn)


# return clubids and clubnames for clubs where netid is an officer
def get_officerships(netid):
    try:
        conn = pool.getconn()
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
        print("__________database.py get officerships: ", ex)
        return "server, get_officerships"

    finally:
        pool.putconn(conn)

# return clubids and clubnames for clubs where netid is an officer
def get_club_officers(clubid):
    try:
        conn = pool.getconn()
        with conn.cursor() as cur:

            script = "select netid from officers WHERE clubid=%s"

            cur.execute(script, [clubid])

            row = cur.fetchone()
            names = []
            while row is not None:
                print("row: ", row)
                user = get_user(row)[0]
                print(user)
                print(user['displayname'])
                names.append((user['displayname'], row[0]))
                row = cur.fetchone()

            return names


    except Exception as ex:
        print("__________database.py get club officers: ", ex)
        return "server, get_club_officers"

    finally:
        pool.putconn(conn)



###### ---------------- Club Edit information ------------------ #####

# verifies that given netid is an officer of given clubid
def verify_officer(netid, clubid):
    try:
        conn = pool.getconn()
        with conn.cursor() as cur:

            script = "select * from officers where netid=%s and clubid=%s"

            cur.execute(script, [netid, clubid])

            if len(cur.fetchall()) > 0:
                return True
            return False

    except Exception as ex:
        print("__________database.py verify officer: ", ex)
        return "server, verify_officer"
        
    finally:
        pool.putconn(conn)


def add_officer(netid, clubid):
    try:
        conn = pool.getconn()
        with conn.cursor() as cur:

            script = "insert into officers values (%s, %s)"

            cur.execute(script, [netid, clubid])

            add_sub(netid, clubid)

            return "success"

    except Exception as ex:
        print("__________database.py add officer: ", ex)
        return "server, add_officer"

    finally:
        pool.putconn(conn)


def remove_officer(netid, clubid):
    print("in remove_officer")
    try:
        conn = pool.getconn()
        with conn.cursor() as cur:

            script = "delete from officers where netid=%s and clubid=%s"

            cur.execute(script, [netid, clubid])

            return "success"

    except Exception as ex:
        print("__________database.py reomve officer: ", ex)
        return "server, remove_officer"

    finally:
        pool.putconn(conn)


# send an announcement to a given club
def send_announcement(clubid, announcement, officer):
    try:

        # update the database of announcements
        conn = pool.getconn()
        with conn.cursor() as cur:

            script = "insert into announcements VALUES (%s, %s, CURRENT_TIMESTAMP, %s)"

            cur.execute(script, [clubid, announcement, officer])

            return "success"


    except Exception as ex:
        print("__________database.py send announcement: ", ex)
        return "server, send_announcements"

    finally:
        pool.putconn(conn)


# get all subscribers for a club
def get_subscribers(clubid):
    try:
        conn = pool.getconn()
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
        print("__________database.py get subscribers: ", ex)
        return "server, get_subscribers"

    finally:
        pool.putconn(conn)


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
        conn = pool.getconn()
        with conn.cursor() as cur:
            cur.execute(script, args+[clubid])

    except Exception as ex:
        print("__________database.py update club info: ", ex)
        return "server, update_club_info"

    finally:
        pool.putconn(conn)


# get clubname from clubid
def get_clubname(clubid):
    try:
        conn = pool.getconn()
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
        print("__________database.py get clubname: ", ex)
        return "server, get_clubname"

    finally:
        pool.putconn(conn)

################
# getting user infos from netid
#######################
def get_user(username):

    req_lib = ReqLib()

    reqBasic = req_lib.getJSON(
        req_lib.configs.USERS_BASIC,
        uid=username,
    )
    print("get user????")
    return reqBasic
