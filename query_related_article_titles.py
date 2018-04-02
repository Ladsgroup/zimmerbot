import pywikibot
import requests
import json, urllib
import re
import sys
from language_dict import language_dict

keyword_base_url = "w/api.php?action=query&format=json&list=search&srlimit=10&srsearch="

#To scrape the categories of articles that fall within the user's query
base_category_query_url = "w/api.php?action=query&format=json&prop=categories&cllimit=20&cldir=ascending&titles="

#To scrape the most recent categry members from related categories to the user's query
#NOTE: currently capped at 20 related members max
base_related_query_url ="w/api.php?action=query&list=categorymembers&cmsort=timestamp&cmdir=desc&cmprop=type|id|title|timestamp&cmlimit=20&cmtitle="

#Example of a query for the categories of Albert Einstein
#"api.php?action=query&prop=categories&titles=Albert%20Einstein"

#"w/api.php?action=query&format=json&list=search&srlimit=500&srsearch="
#url_example = https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch=life%science%data

#Create languages dictionary from "list_of_wiki_languages.txt"
# def generate_language_dict():
#     with open("list_of_wiki_languages.txt", "r") as file:
#         lines = file.read().split(",")
#         for i in range(len(lines)):
#             #lines[i] = re.sub("\s","",lines[i])
#             lines[i] = lines[i].strip()
#             lines[i] = lines[i].strip("\'")
#         dictionary = {lines[i+1]:lines[i] for i in range(0, len(lines), 2)}
#     return dictionary

###############
#MAIN FUNCTION#
###############

#Returns a list of article names (strings) from querying for SEARCH_ITEM
#Returns a list of titles of LANGUAGE articles from a search query SEARCH_ITEM
#Example:
#    Input: "Swift", "English"
#    Output:
#        [
#         Swift", "Taylor Swift", "Reputation"
#        ]
def query_related_articles_titles(search_item, language_code):
    data = get_data(search_item, language_code, keyword_base_url)
    result = []
    for e in data["query"]["search"]:
        #remove unwanted dictionary keys
        e.pop("ns", None)
        e.pop("size", None)
        e.pop("timestamp", None)
        result += [e]

    if not result:
        print("Please try another search query.")
        if suggestion_exists(data):
            print("Suggestion: " + get_search_suggestion(search_item, language_code))

    result_titles = []

    for article in result:
        result_titles += [article["title"]]

    return result_titles

#Returns the categories of a list of pages
#Example:
#    Input: ["Abraham"], "English"
#    Output:
#        [
#         "Category:Abraham", "Category:Angelic visionaries", "Category:Biblical patriarchs",
#         "Category:Christian saints from the  Old Testament", "Category:Founders of religions", "Category:Lech-Lecha",
#         "Category:Prophets of Islam", "Category:Prophets of the Hebrew Bible", "Category:Use dmy dates from April 2012",
#         "Category:Vayeira"
#        ]
def get_article_categories_from_query(article_titles_list, language_code):
    category_titles_list = []

    for title in article_titles_list:
        data = get_data_related_articles(title, language_code, base_category_query_url)

        #print(data["query"]["pages"])

        for page in data["query"]["pages"]:

            if "categories" not in data["query"]["pages"][page].keys():
                break

            for category in data["query"]["pages"][page]["categories"]:
                if category["title"] not in category_titles_list:
                    category_titles_list += [category["title"]]


    return category_titles_list

#return a list of recent article page titles for each category from a list of categories
#Example:
#    Input: ["Presidents"], "English"
#    Output: ["President", "President of the Continental Congress", "President of the Senate"]
def get_articles_from_categories(category_titles_list, language_code):

    related_article_titles = []
    for category in category_results:
        data = get_data(category, language_code, base_related_query_url)

        for member in data["query"]["categorymembers"]:
            if member["type"] == "page":
                dummy_dict = {"title" : member["title"]}
                related_article_titles += [dummy_dict]

    return related_article_titles

# Returns the Page objects from a query
def get_articles_from_names(article_names, language_code):
    articles = {}
    site = pywikibot.getSite(language_code)
    for article_name in article_names:
        articles[article_name] = pywikibot.Page(site, article_name)
    return articles



#Returns the search replacement suggestion for the user's search
#Example:
#    Input: "asdf Einstein!"
#    Output: "asif Einstein"
#    Input: "Albert Einstein"
#     Output: None
def get_search_suggestion(search_item, language_code):
    data = get_data(search_item, language_code)
    if suggestion_exists(data):
        return data["query"]["searchinfo"]["suggestion"]
    else:
        return None


##################
#HELPER FUNCTIONS#
##################

#Returns JSON data from the Wikipedia Web API for querying
#changed to accept different API urls
def get_data(search_item, language_code, base_url):
    with urllib.request.urlopen(build_url(search_item, language_code, base_url)) as url:
        data = json.loads(url.read().decode())
        return data

def get_data_related_articles(search_item, language_code, base_url):
    with urllib.request.urlopen(build_url_related_articles(search_item, language_code, base_url)) as url:
        data = json.loads(url.read().decode())
        return data

#Builds the json request URL
def build_url(search_item, language_code, base_url):
    site = pywikibot.getSite(language_code)
    wiki_language_url = language_code + ".wikipedia.org/"

    url_search_extension = re.sub("\s", "%", search_item.strip())

    result = "https://" + wiki_language_url + base_url + url_search_extension
    return result

def build_url_related_articles(search_item, language_code, base_url):
    site = pywikibot.getSite(language_code)
    wiki_language_url = language_code + ".wikipedia.org/"

    url_search_extension = re.sub("\s", "%20", search_item.strip())

    result = "https://" + wiki_language_url + base_url + url_search_extension
    return result

#returns True/False depending if there is a search replacement suggestion for the user's search
def suggestion_exists(json_data):
    return "suggestion" in json_data["query"]["searchinfo"]



######################
#EXAMPLE / HOW TO USE#
######################

if __name__ == "__main__":

    # query_articles("ARTICLE NAME", "LANGUAGE")
    #article_dictionaries = query_articles("tapas", language_dict["Spanish"])
    #get_article_names_from_query(article_dictionaries)

    #get_search_suggestion("asdf Einstein!", language_dict["English"])

    titles = query_related_articles_titles("Donald Trump", language_dict["English"])

    categories = get_article_categories_from_query(titles, language_dict["English"])

    for _ in categories:
        print(_)
