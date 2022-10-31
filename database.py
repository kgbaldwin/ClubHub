#!/usr/bin/env python

#-------------------------------------------------------------------
# database.py
# Authors: Kevin Kim, Priya Naphade, Katie Baldwin, Lance Yoder
#-------------------------------------------------------------------

import flask
import psycopg2

database_url = "postgres://avgqxjcj:lg3PfhN5-G_5-KH1XleCGMAJgHkZfcN1@peanut.db.elephantsql.com/avgqxjcj"

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
                        print("added a tag: ", tag)
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

def database_get_info(clubid):

    print("clubid:", clubid)

    try:
        with psycopg2.connect(database_url) as conn:

            with conn.cursor() as cur:

                script = "select clubname, description, meets, commitment, website, verified, lastupdated, imlink from clubs WHERE clubid=%s"

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