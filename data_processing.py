import psycopg2
import urllib.parse as up
import os

url = up.urlparse(os.environ["DATABASE_URL"])

try:
    with psycopg2.connect(database=url.path[1:], user=url.username, password=url.password,
                            host=url.hostname, port=url.port) as conn:

        with conn.cursor() as cur:

            ### -------- extract tags ---------
            allTags = set()

            script = "select distinct category from clubsall"
            cur.execute(script)

            row = cur.fetchone()

            while row is not None:
                tags = row[0].split(",")

                for element in tags:
                    allTags.add(element)
                row = cur.fetchone()

            allTags.discard('')


            # insert tags into new "tags" table
            for tag in allTags:

                script = "select id from clubsall where category ilike %s"
                cur.execute(script, ['%' + tag + '%'])

                rows = cur.fetchall()

                for row in rows:
                    script = "insert into tagsall values(%s, %s)"

                    cur.execute(script, [tag, row[0]])


            ### ----------- fill officers table ----------------
            script = "select distinct groupname from clubs"
            cur.execute(script)
            rows = cur.fetchall()
            for row in rows:
                script = "insert into officers (netid, clubid) "
                script += "select netid, id from clubs, bigdataok "
                script += "where bigdataok.groupname=clubs.groupname "
                script += "and clubs.groupname=%s"

                cur.execute(script, [row])


except:
    print("failed :(")
