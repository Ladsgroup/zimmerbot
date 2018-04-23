import pywikibot
import requests
import json, urllib
import re
import sys
from language_dict import language_dict

base_url = "w/api.php?action=query&format=json&formatversion=2&list=allcategories&acmin=1&acprefix="
#url_example = https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch=life%science%data

###############
#MAIN FUNCTION#
###############

#Returns a list of strings of LANGUAGE categories from a search query prefix
#Example:
#    Input: "cat", "English"
#    Output:
#        ["Cat's Eye", "Cat's Eye (manga)", "Cat's Eyes albums", 'Cat-Class Dallas-Fort Worth articles',
#           'Cat-Class Surrey articles', 'Cat-Class Systems articles', 'Cat-Class articles',
#           'Cat-Class mixed martial arts articles', 'Cat Butt albums', 'Cat Island, Bahamas']

def get_category_suggestions(prefix, language_code):
    data = get_data(prefix, language_code)
    categories = []
    for e in data["query"]["allcategories"]:
        categories.append(e["category"])
    categories_json  = {"categories": categories}
    if categories:
        return json.dumps(categories_json)
    return categories


##################
#HELPER FUNCTIONS#
##################

#Returns JSON data from the Wikipedia Web API for querying
def get_data(search_item, language_code):
    with urllib.request.urlopen(build_url(search_item, language_code)) as url:
        data = json.loads(url.read().decode())
        return data

#Builds the json request URL
def build_url(search_item, language_code):
    site = pywikibot.getSite(language_code)
    wiki_language_url = language_code + ".wikipedia.org/"

    url_search_extension = re.sub("\s", "%", search_item.strip())

    result = "https://" + wiki_language_url + base_url + url_search_extension
    return result


######################
#EXAMPLE / HOW TO USE#
######################

if __name__ == "__main__":
    print(get_category_suggestions("cat", language_dict["English"]))
