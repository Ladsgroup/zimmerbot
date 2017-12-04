from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from zimmerbot import *

application = FlaskAPI(__name__)

@application.route("/")
def get_links():

    results = {}
    data = request.data
    list_of_links = main(data.query, data.language, data.filter, data.limit)
    for i in range(len(list_of_links)):
        results[i] = list_of_links[i]

    resp = make_response([results])
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    # app.debug = True
    application.run()
