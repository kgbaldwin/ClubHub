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

                script = "select clubname, clubid from clubs WHERE clubname ILIKE %s "
                if tags:
                    script += "AND clubs.clubid=ANY(SELECT clubid from tags where tag=%s "
                    for tag in tags[1:]:
                        script += "or tag=%s "
                    script +=")"


                cur.execute(script, args)

                row = cur.fetchone()
                clubs = []
                while row is not None:
                    clubs.append(row)
                    row = cur.fetchone()

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

                script = "select clubname, description, meets, commitment, website, verified, stamp, imlink from clubs WHERE clubid=%s"

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

                script = "select clubname from subscriptions, clubs WHERE netid=%s AND clubs.clubid=subscriptions.clubid"

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
                script = "select * from subscriptions where netid=%s and clubid=%s"
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
                script = "delete from subscriptions where netid=%s and clubid=%s"
                cur.execute(script, [user, clubid])

    except Exception as ex:
        print(ex)
        return "server, remove_sub"

def is_subbed(netid, clubid):
    try:
        with psycopg2.connect(database_url) as conn:

            with conn.cursor() as cur:

                script = "select netid from subscriptions WHERE netid=%s AND clubid=%s"

                cur.execute(script, [netid, clubid])

                row = cur.fetchone()

                if row is None:
                    return False

                return True

    except Exception as ex:
        print(ex)
        return "server, is_subbed"

# return clubids and clubnames for clubs where netid is an officer
def get_officerships(netid):
    try:
        with psycopg2.connect(database_url) as conn:

            with conn.cursor() as cur:

                script = "select clubname, clubs.clubid from officers, clubs WHERE netid=%s AND clubs.clubid=officers.clubid"

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