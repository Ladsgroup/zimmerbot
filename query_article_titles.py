import pywikibot
import requests
import json, urllib
import re
import sys
from language_dict import language_dict
import sqlite3
import random
import datetime


keyword_base_url = "w/api.php?action=query&format=json&list=search&srlimit=5&srsearch="

#To scrape the categories of articles that fall within the user's query
base_category_query_url = "w/api.php?action=query&clshow=!hidden&format=json&prop=categories&cllimit=5&cldir=ascending&titles="

#To scrape the most recent categry members from related categories to the user's query
#NOTE: currently capped at 20 related members max
base_related_query_url ="w/api.php?action=query&list=categorymembers&format=json&cmsort=timestamp&cmdir=desc&cmprop=type|title|timestamp&cmlimit=10&cmtitle="

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

#Returns a list of dictionaries of LANGUAGE articles from a search query SEARCH_ITEM
#The dictionaries contain the article's TITLE, PAGEID, WORDCOUNT, and SNIPPET
#Example:
#    Input: "Swift", "English"
#    Output:
#        [
#         {"title":"Swift", "pageid":455, "wordcount": 500, "snippet":"some description of Swift"},
#         {"title": "Taylor Swift", "pageid":280, "wordcount": 331, "snippet":"some description of Taylor Swift"},
#         {"title": "Reputation", "pageid":670, "wordcount": 899, "snippet":"some description of Repuation"}
#        ]
def query_articles(search_item, language_code):
    data = get_data(search_item, language_code)
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
    return result

#Returns a list of article names (strings) from querying for SEARCH_ITEM
#Example:
#    Input: "Swift", "English"
#    Output: ["Swift", "Taylor Swift", "Reputation"]
def get_article_names_from_query(article_dictionaries):
    result = []
    for d in article_dictionaries:
        result += [d["title"]]
    for title in result:
        print(title)
    return result

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

#Returns a list of dictionaries of LANGUAGE articles from a search query SEARCH_ITEM that are in CATEGORY
#The dictionaries contain the article's TITLE, PAGEID, WORDCOUNT, and SNIPPET
# def query_articles_in_category(search_item, language_code, category):
#     data = get_data(search_item, language_code)

#     #dictionary of categories mapping to dictionaries (i.e. {category : {article_id: article_title}})
#     articles_of_categories_dict = deserialize_dictionary("articles_of_categories.pickle")
#     result = []

#     if (category != None or category != ""): #Gets articles about SEARCH_ITEM that are in CATEGORY
#         if category in articles_of_categories_dict:
#             article_id_title_dict = articles_of_categories_dict[category]
#         else:
#             limit = 200 #Can change the limit

#             article_id_title_dict = get_articles_in_category(category, language_code, limit)

#             articles_of_categories_dict.update({category: article_id_title_dict})
#             serialize_dictionary(articles_of_categories_dict, "articles_of_categories.pickle")
#         for e in data["query"]["search"]:
#             if e["pageid"] in article_id_title_dict:
#                 e.pop("ns", None)
#                 e.pop("size", None)
#                 e.pop("timestamp", None)
#                 result += [e]
#     else: #Gets articles about SEARCH_ITEM (no CATEGORY specified)
#         for e in data["query"]["search"]:
#             #remove unwanted dictionary keys
#             e.pop("ns", None)
#             e.pop("size", None)
#             e.pop("timestamp", None)
#             result += [e]
#     if not result:
#         print("Please try another search query.")
#         if suggestion_exists(data):
#             print("Suggestion: " + get_search_suggestion(search_item, language_code))

#     return result


def query_related_articles_titles(search_item, language_code):
    print(111111111111111111111111111111111111111111111111111111111)
    data = get_data_related_articles(search_item, language_code, keyword_base_url)
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

    return get_article_categories_from_query(result_titles, language_code)

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
    print(2222222222222222222222222222222222222222222222222222222)

    for title in article_titles_list:
        print(33333333333333333333333333333333333333333333333333333333333)
        data = get_data_related_articles(title, language_code, base_category_query_url)

        #print(data["query"]["pages"])

        for page in data["query"]["pages"]:

            if "categories" not in data["query"]["pages"][page].keys():
                break

            for category in data["query"]["pages"][page]["categories"]:
                if category["title"] not in category_titles_list:
                    category_titles_list += [category["title"]]


    return get_articles_from_categories_catmem(category_titles_list, language_code)

#return a list of recent article page titles for each category from a list of categories
#Example:
#    Input: ["Presidents"], "English"
#    Output: ["President", "President of the Continental Congress", "President of the Senate"]
def get_articles_from_categories_catmem(category_titles_list, language_code):
    print("ya ya yeet")
    related_article_titles = []
    for category in category_titles_list:
        print(44444444444444444444444)
        data = get_data_related_articles(category, language_code, base_related_query_url)

        for member in data["query"]["categorymembers"]:
            print(55555555555555555555555555555555)
            if member["type"] == "page":
                dummy_dict = {"title" : member["title"]}
                related_article_titles += [dummy_dict]


    now = datetime.datetime.now()
    random.seed(now.day)
    random.shuffle(related_article_titles)
    print(66666666666666666666666666666)
    return related_article_titles

def get_articles_from_categories_keyword(category_titles_list, language_code):

    result = []
    for category in category_titles_list:
        data = get_data(category[10:], language_code, keyword_base_url)

        for e in data["query"]["search"]:
            e.pop("ns", None)
            e.pop("size", None)
            e.pop("timestamp", None)
            e.pop("snippet", None)
            e.pop("wordcount", None)
            result += [e]

    now = datetime.datetime.now()
    random.seed(now.day)
    random.shuffle(related_article_titles)
    return result

##################
#HELPER FUNCTIONS#
##################

#Returns JSON data from the Wikipedia Web API for querying article titles
def get_data(search_item, language_code):
    with urllib.request.urlopen(build_url(search_item, language_code)) as url:
        data = json.loads(url.read().decode())
        return data

#Builds the json request URL for querying article titles
def build_url(search_item, language_code):
    #site = pywikibot.getSite(language_code)
    search_item = re.sub("\s", "%", search_item.strip())
    result = "https://" + language_code + ".wikipedia.org/w/api.php?action=query&format=json&list=search&srlimit=500&srsearch=" + search_item
    return result

#returns True/False depending if there is a search replacement suggestion for the user's search
def suggestion_exists(json_data):
    return "suggestion" in json_data["query"]["searchinfo"]

#Saves DICTIONARY to a json file called FILENAME
def dictionary_to_json_file(dictionary, filename):
    f = open(filename, "w")
    f.write(json.dumps(dictionary))
    f.close()

#Returns the dictionary stored in the JSON file called FILENAME
def json_file_to_dictionary(filename):
    f = open(filename, "r")
    dictionary = json.load(f)
    return dictionary

#serializes DICTIONARY to FILENAME
def serialize_dictionary(dictionary, filename):
    with open(filename, "wb") as f:
        pickle.dump(dictionary, f, pickle.HIGHEST_PROTOCOL)

#Returns the deserialized dictionary in FILENAME
def deserialize_dictionary(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)


############################
#QUERY CATEGORIES FUNCTIONS#
############################

#Returns a dictionary (key: article id, value: article title) of LIMIT number of articles in CATEGORY
#(randomly prunes the dictionary returned by get_articles_in_category if initially len(dictionary) > LIMIT)
def get_limit_number_of_articles_in_category(category, language_code, limit):
    articles_in_category = get_articles_in_category(category, language_code, limit)
    if len(articles_in_category) > limit:
        for key in random.sample(articles_in_category.keys(), len(articles_in_category) - limit):
            articles_in_category.pop(key) # removes articles from the dictionary randomly
    return articles_in_category


#Returns a dictionary of articles in CATEGORY
#Uses MediaWiki's API:Categorymembers
#Input: "Swift", "English"
#    Output:
#        [
#         {"title":"Swift", "pageid":455},
#         {"title": "Taylor Swift", "pageid":280},
#         {"title": "Reputation", "pageid":670}
#        ]
def get_articles_in_category(category, language_code, limit):
    category_members = get_category_members(category, language_code, limit)
    article_id_title_dict = {}
    subcategories = []
    for e in category_members["query"]["categorymembers"]:
        if (e["type"] == "subcat"):
            subcat_name = e["title"][9:]
            try:
                subcat_name.encode("ascii")
            except:
                continue
            subcategories += [subcat_name]
        elif (e["type"] == "page"):
            article_id_title_dict[e["pageid"]] = e["title"]
            article_id_title_dict["title"] = e["title"]
            article_id_title_dict["pageid"] = e["pageid"]
            if len(article_id_title_dict) >= limit:
                return article_id_title_dict

    # print("CATEGORY: ", category)
    # print ("ARTICLE LENGTH: ", len(article_id_title_dict))
    # print ("SUBCAT LENGTH: ", len(subcategories))

    if len(article_id_title_dict) >= limit:
        return article_id_title_dict
    else:
        for subcat in subcategories:
            #print("updated article length: ", len(article_id_title_dict))
            remaining_limit = limit - len(article_id_title_dict)
            article_id_title_dict.update(get_articles_in_category(subcat, language_code, remaining_limit))

    return article_id_title_dict

#Helper for get_articles_in_category(): returns a JSON object of categorymembers (articles in CATEGORY)
def get_category_members(category, language_code, limit):
     with urllib.request.urlopen(build_category_members_url(category, language_code, limit)) as url:
        data = json.loads(url.read().decode())
        return data

#Helper for get_category_members(): builds the url for the Categorymembers API
def build_category_members_url(category, language_code, limit):
    #site = pywikibot.getSite(language_code)
    category = re.sub("\s", "%20", category)

    result = "https://" + language_code + ".wikipedia.org/w/api.php?format=json&action=query&list=categorymembers&cmprop=ids|title|type&cmlimit=" + str(limit) + "&cmtitle=Category:" + category

    return result


#Returns a list of categories starting with prefix CATEGORY
#Uses MediaWiki's API:Allcategories
def query_categories(category, language_code):
    result = []
    categories_data = get_categories(category, language_code)
    for e in categories_data["query"]["allcategories"]:
        result.extend(e.values())
    return result

#Helper for query_categories(): returns a JSON object of categories with prefix CATEGORY
def get_categories(category, language_code):
    category = re.sub("\s", "%20", category)
    url = "https://" + language_code + ".wikipedia.org/w/api.php?format=json&action=query&list=allcategories&aclimit=500&acprefix=" + category
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())
        return data

#Returns a list of subcategories of CATEGORY
def get_sub_categories(category, language_code):
    subcategories, stack = [], []
    stack.append(category)
    print(category)
    while stack and len(subcategories) < 50: #if stack is empty
        curr_category = stack.pop()
        try:
            curr_category.encode("ascii")
        except:
            continue
        subcategories += [curr_category]
        print (curr_category)
        category_members = get_category_members(curr_category, language_code) #returns a JSON of the data
        for member in category_members["query"]["categorymembers"]:
            if member["type"] == "subcat":
                stack.append(member["title"][9:]) #[9:] to remove the leading "Category:" in the category name
    return subcategories

def get_data_related_articles(search_item, language_code, base_url):
    with urllib.request.urlopen(build_url_related_articles(search_item, language_code, base_url)) as url:
        data = json.loads(url.read().decode())
        return data

def build_url_related_articles(search_item, language_code, base_url):
    site = pywikibot.getSite(language_code)
    wiki_language_url = language_code + ".wikipedia.org/"

    url_search_extension = re.sub("\s", "%20", search_item.strip())

    result = "https://" + wiki_language_url + base_url + url_search_extension

    return result
#######################
#QUERY LINKED ARTICLES#
#######################

#NOTE: QUERY must be a valid Wikipedia article title
def query_linked_articles(article_title, language_code):
    result = []
    limited_data = get_linked_articles(article_title, language_code, None)
    if "-1" in limited_data["query"]["pages"]: #Note: -1 denotes an invalid pageID
        print (article_title + " is not a valid Wikipedia article")
        return None
    all_links = (list(limited_data["query"]["pages"].values())[0])["links"] #extracting just the list of links from the data
    while "continue" in limited_data.keys(): #obtaining all links (iterating through requests of 500)
        limited_data = get_linked_articles(article_title, language_code, limited_data["continue"]["plcontinue"])
        links_in_limited_data = (list(limited_data["query"]["pages"].values())[0] )["links"]
        all_links += links_in_limited_data #updating all_links

    for e in all_links:
        if e["ns"] == 0: #if element is an article (and not a category, template, help page, etc.)
            result += [{"title" : e["title"]}]
    return result

def get_linked_articles(article_title, language_code, continue_key):
    article_title = re.sub("\s", "%20", article_title)
    if continue_key == None:
        url = "https://" + language_code + ".wikipedia.org/w/api.php?action=query&format=json&prop=links&titles=" + article_title + "&redirects=1&pllimit=500"
    else:
        continue_key = re.sub("\|", "%7C", continue_key)
        url = "https://" + language_code + ".wikipedia.org/w/api.php?action=query&format=json&prop=links&titles=" + article_title + "&redirects=1&pllimit=500&plcontinue=" + continue_key
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())
        return data




######################
#EXAMPLE / HOW TO USE#
######################

if __name__ == "__main__":
    #dictionary = deserialize_dictionary("articles_of_categories.pickle")
    #print(dictionary)
    #serialize_dictionary({}, "articles_of_categories.pickle")

    articles = get_limit_number_of_articles_in_category("sports", language_dict["English"], 2)
    print("number of articles received: ", len(articles))
    print(articles)
    #query_articles("ARTICLE NAME", "LANGUAGE")
    # article_dictionaries = query_articles("tapas", language_dict["Spanish"])
    # get_article_names_from_query(article_dictionaries)

    # get_search_suggestion("asdf Einstein!", language_dict["English"])
