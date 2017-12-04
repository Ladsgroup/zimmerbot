from flask import request, url_for, make_response
from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS
from zimmerbot import *

application = FlaskAPI(__name__)
CORS(application)

@application.route("/", methods=["GET", "POST"])
def get_links():
    if request.method == "GET":
        list_of_links = main("dog", "English", "popularity", "10")
    else:
        print(request)
        data = request.data
        list_of_links = main(data["query"], data["language"], data["filter"], data["limit"])
    return list_of_links

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    # app.debug = True
    application.run()
