#!/usr/bin/env python

#-------------------------------------------------------------------
# clubhub.py
# Authors: Kevin Kim, Priya Naphade, Katie Baldwin, Lance Yoder
#-------------------------------------------------------------------

import flask
import psycopg2
import urllib.parse as up


database_url = "postgres://avgqxjcj:lg3PfhN5-G_5-KH1XleCGMAJgHkZfcN1@peanut.db.elephantsql.com/avgqxjcj"


#-------------------------------------------------------------------

app = flask.Flask(__name__)



#-------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    html_code = flask.render_template('index.html')
    response = flask.make_response(html_code)
    return response


@app.route('/searchform', methods=['GET'])
def searchform():
    html_code = flask.render_template('searchform.html')
    response = flask.make_response(html_code)
    return response


@app.route('/searchresults', methods=['GET'])
def searchresults():
    clubquery = '%' + flask.request.args.get('clubquery') + '%'
    tags = flask.request.args.getlist('tags')
    print("cq: ", clubquery)
    print("tags: ", tags)
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

                #script = "select clubname from clubs where clubname ILIKE %s AND clubs.clubid=ANY(SELECT clubid from tags where tag=%s or tag=%s)"
                #print("script: ", script)
                cur.execute(script, args)

                retval = cur.fetchall()
                print("retval:", retval)

    except Exception as ex:
        print(ex)

    html_code = flask.render_template('searchresults.html', results=retval)
    response = flask.make_response(html_code)
    return response

@app.errorhandler(404)
def page_not_found(e):
    html_code = flask.render_template('404.html')
    response = flask.make_response(html_code)
    return response

if __name__ == '__main__':
    #searchresults()
    app.run(debug=True)