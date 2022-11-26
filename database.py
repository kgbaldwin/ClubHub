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

                script1 = "select groupname, id from clubs WHERE groupname ILIKE %s "
                script2 = "select groupname, id from clubs WHERE groupname ILIKE %s "
                if tags:
                    script1 += "AND clubs.id=ANY(SELECT id from tags where tag=%s "
                    script2 += "AND clubs.id=ANY(SELECT id from tags where tag=%s "
                    for _ in tags[1:]:
                        script1 += "and tag=%s "
                        script2 += "or tag=%s "
                    script1 +=")"
                    script2 +=")"

                script = script1 + " union " + script2

                cur.execute(script, args + args)

                row = cur.fetchone()
                print(row)
                clubs = []
                while row is not None:
                    clubs.append(row)
                    row = cur.fetchone()
                    print(row)

                return clubs

    except Exception as ex:
        print(ex)
        return "server get_clubs"


# gets club details of a selected club
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


def get_tags():
    try:
        with psycopg2.connect(database_url) as conn:

            with conn.cursor() as cur:

                script = "select DISTINCT tag from tags"
                cur.execute(script)

                row = cur.fetchone()
                clubids = []
                while row is not None:
                    clubids.append(row)
                    row = cur.fetchone()

                return clubids

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

                # check for existence of row (may not be necessary)
                script = "delete from subscriptions where netid=%s and id=%s"
                cur.execute(script, [user, clubid])

    except Exception as ex:
        print(ex)
        return "server, remove_sub"


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

                return "success"

    except Exception as ex:
        print(ex)
        return "server, add_officer"


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


# return clubids and clubnames for clubs where netid is an officer
def get_officerships(netid):
    try:
        with psycopg2.connect(database_url) as conn:

            with conn.cursor() as cur:

                script = "select groupname, clubs.id from officers, clubs WHERE netid=%s AND clubs.id=officers.clubid"

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


# send an announcement
def send_announcement(clubid, announcement):
    try:
        with psycopg2.connect(database_url) as conn:

            with conn.cursor() as cur:

                script = "insert into announcements VALUES (%s, %s, CURRENT_TIMESTAMP)"

                cur.execute(script, [clubid, announcement])

                return "success"

    except Exception as ex:
        print(ex)
        return "server, send_announcements"