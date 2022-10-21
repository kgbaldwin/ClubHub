#!/usr/bin/env python

#-------------------------------------------------------------------
# clubhub.py
# Authors: Kevin Kim, Priya Naphade, Katie Baldwin, Lance Yoder
#-------------------------------------------------------------------

import time
import flask
import psycopg2
#import database
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
    #clubquery = flask.request.args.get('clubquery')
    clubquery = "PrincetOn Christian Fellowship"

    try:
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:

                script = """select description from clubs where clubname ILIKE %s"""
                cur.execute(script, [clubquery])

                retval = cur.fetchall()
                #print(retval)
                if not retval:
                    retval = "NONE FOUND"
                else:
                    retval = retval[0][0]
                print(retval)

    except Exception as ex:
        print(ex)

    html_code = flask.render_template('searchresults.html', results=retval)
    response = flask.make_response(html_code)
    return response




if __name__ == '__main__':
    searchresults()
    app.run(debug=True)