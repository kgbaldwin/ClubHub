import psycopg2

database_url = "postgres://avgqxjcj:lg3PfhN5-G_5-KH1XleCGMAJgHkZfcN1@peanut.db.elephantsql.com/avgqxjcj"

try:
    with psycopg2.connect(database_url) as conn:

        with conn.cursor() as cur:

            '''allTags = set()

            script = "select distinct category from clubsall"
            cur.execute(script)

            row = cur.fetchone()

            while row is not None:
                tags = row[0].split(",")

                for element in tags:
                    allTags.add(element)
                row = cur.fetchone()

            allTags.discard('')


            # insert
            for tag in allTags:

                script = "select id from clubsall where category ilike %s"
                cur.execute(script, ['%' + tag + '%'])

                rows = cur.fetchall()
                #print(rows)

                for row in rows:
                    script = "insert into tagsall values(%s, %s)"

                    cur.execute(script, [tag, row[0]])

                #print("_____________")
                '''


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
