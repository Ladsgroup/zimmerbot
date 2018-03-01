import pywikibot
import requests
import json, urllib
import re
import sys
from language_dict import language_dict

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
def query_articles_in_category(search_item, language_code, category):
    data = get_data(search_item, language_code)
    result = []

    if (category != None or category != ""): #Gets articles about SEARCH_ITEM that are in CATEGORY
        article_id_title_dict = get_articles_in_category(category, language_code)
        for e in data["query"]["search"]:
            if e["pageid"] in article_id_title_dict:
                e.pop("ns", None)
                e.pop("size", None)
                e.pop("timestamp", None)
                result += [e]
    else: #Gets articles about SEARCH_ITEM (no CATEGORY specified)
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



############################
#QUERY CATEGORIES FUNCTIONS#
############################

#Returns a dictionary (key: article id, value: article title) of articles in CATEGORY
#Uses MediaWiki's API:Categorymembers
def get_articles_in_category(category, language_code):
    articles_in_category = get_category_members(category, language_code)
    article_id_title_dict = {}
    subcategories = []
    for e in articles_in_category["query"]["categorymembers"]:
        if (e["type"] == "subcat"):
            subcat_name = e["title"][9:]
            try:
                subcat_name.encode("ascii")
            except:
                continue
            subcategories += [subcat_name]
        elif (e["type"] == "page"):
            article_id_title_dict[e["pageid"]] = e["title"]
    print("CATEGORY: ", category)
    print ("ARTICLE LENGTH: ", len(article_id_title_dict))
    print ("SUBCAT LENGTH: ", len(subcategories))
    if (len(article_id_title_dict) >= 4) and len(subcategories) < len(article_id_title_dict):
        return article_id_title_dict
    else:
        if len(subcategories) >= 20: 
            truncated_list_of_subcategories = [subcategories[i] for i in range(0, len(subcategories), 10)]
        else: 
            truncated_list_of_subcategories = subcategories
        for subcat in truncated_list_of_subcategories:
            print("updated article length: ", len(article_id_title_dict))
            article_id_title_dict.update(get_articles_in_category(subcat, language_code))

    print ("=====returning=====")
    return article_id_title_dict

#Helper for get_articles_in_category(): returns a JSON object of categorymembers (articles in CATEGORY)
def get_category_members(category, language_code):
     with urllib.request.urlopen(build_category_members_url(category, language_code)) as url:
        data = json.loads(url.read().decode())
        return data

#Helper for get_category_members(): builds the url for the Categorymembers API
def build_category_members_url(category, language_code):
    #site = pywikibot.getSite(language_code)
    category = re.sub("\s", "%20", category)
    result = "https://" + language_code + ".wikipedia.org/w/api.php?format=json&action=query&list=categorymembers&cmprop=ids|title|type&cmlimit=500&cmtitle=Category:" + category 
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
    url = "http://en.wikipedia.org/w/api.php?format=json&action=query&list=allcategories&aclimit=500&acprefix=" + category
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





######################
#EXAMPLE / HOW TO USE#
######################

if __name__ == "__main__":

    #query_articles("ARTICLE NAME", "LANGUAGE")
    article_dictionaries = query_articles("tapas", language_dict["Spanish"])
    get_article_names_from_query(article_dictionaries)

    get_search_suggestion("asdf Einstein!", language_dict["English"])


