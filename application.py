from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS
from zimmerbot import *
from test_suite import *
from category_autocomplete import *


application = FlaskAPI(__name__)
CORS(application)

@application.route("/", methods=["GET", "POST"])
def get_links():
    if request.method == "GET":
        list_of_links = main("related", "dog", "en", "popularity", 10, "exclude")
    else:
        data = request.data
        if data["filter"] == "ores_quality" and data["language"] not in ["en", "ru", "fr"]:
            return ["ORES is not supported in this language"], status.HTTP_202_ACCEPTED
        list_of_links = main(data["method"], data["query"], data["language"], data["filter"], int(data["limit"]), data["stub"])
        if not list_of_links:
            return ["No search results found for this query"], status.HTTP_202_ACCEPTED
    return list_of_links

@application.route("/category-autocomplete", methods=["GET", "POST"])
def get_categories():
    data = request.data
    if data["language"] not in ["en", "ru", "fr"]:
        return ["ORES is not supported in this language"], status.HTTP_202_ACCEPTED
    list_of_categories = get_category_suggestions(data["prefix"], data["language"])
    if not list_of_categories:
        return ["No search results found for this query"], status.HTTP_202_ACCEPTED
    return list_of_categories

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    #app.debug = True

    #app.run(host='127.0.0.1', port=80)
    application.run()
