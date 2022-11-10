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
        return "server"


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
        return "server"

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
        return "server"