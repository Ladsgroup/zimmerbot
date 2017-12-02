import sys
sys.path.append("C:/users/celena/pywikibot/core")
import pywikibot
import requests
import json, urllib
import re

base_url = "w/api.php?action=query&format=json&list=search&"
#url_example = https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srlimit=10&srsearch=life%science%data

#Create languages dictionary from "list_of_wiki_languages.txt"
def generate_language_dict():
	with open("list_of_wiki_languages.txt", "r") as file:
		lines = file.read().split(",")
		for i in range(len(lines)):
			#lines[i] = re.sub("\s","",lines[i])
			lines[i] = lines[i].strip()
			lines[i] = lines[i].strip("\'")
		dictionary = {lines[i+1]:lines[i] for i in range(0, len(lines), 2)}
	return dictionary

language_dict = generate_language_dict()


###############
#MAIN FUNCTION#
###############

#Returns a list of dictionaries of LANGUAGE articles from a search query SEARCH_ITEM
#The dictionaries contain the article's TITLE, PAGEID, WORDCOUNT, and SNIPPET
#Example: 
#	Input: "Swift", "English"
#	Output:
#		[
#	 	{"title":"Swift", "pageid":455, "wordcount": 500, "snippet":"some description of Swift"},
#	 	{"title": "Taylor Swift", "pageid":280, "wordcount": 331, "snippet":"some description of Taylor Swift"},
#	 	{"title": "Reputation", "pageid":670, "wordcount": 899, "snippet":"some description of Repuation"}
#		]
def query_articles(search_item, language, cap):
	data = get_data(search_item, language, cap)
	result = []
	for e in data["query"]["search"]:
		#remove unwanted dictionary keys
		e.pop("ns", None) 
		e.pop("size", None)
		e.pop("timestamp", None)
		result += [e]
	return result

#Returns a list of article names (strings) from querying for SEARCH_ITEM
#Example: 
#	Input: "Swift", "English"
#	Output: ["Swift", "Taylor Swift", "Reputation"]
def get_article_names_from_query(search_item, language, cap):
	article_dictionaries = query_articles(search_item, language, cap)
	result = []
	for d in article_dictionaries:
		result += [d["title"]]
	return(result)

#Returns the search replacement suggestion for the user's search
#Example: 
#	Input: "asdf Einstein!"
#	Output: "asif Einstein"
#	Input: "Albert Einstein"
# 	Output: None
def get_search_suggestion(search_item, language, cap):
	data = get_data(search_item, language, cap)
	if suggestion_exists(data):
		return data["query"]["searchinfo"]["suggestion"]
	else:
		return None


##################
#HELPER FUNCTIONS#
##################

#Returns JSON data from the Wikipedia Web API for querying
def get_data(search_item, language, cap):
	with urllib.request.urlopen(build_url(search_item, language, cap)) as url:
		data = json.loads(url.read().decode())
		return data

#Builds the json request URL
def build_url(search_item, language, cap):
	language_code = language_dict[language]
	site = pywikibot.getSite(language_code) 
	wiki_language_url = language_code + ".wikipedia.org/"

	url_search_extension = "srsearch=" + re.sub("\s", "%", search_item.strip())

	url_article_cap_extension = "srlimit=" + str(cap)

	result = "https://" + wiki_language_url + base_url + "&" + url_search_extension + "&" + url_article_cap_extension
	return result

#returns True/False depending if there is a search replacement suggestion for the user's search
def suggestion_exists(json_data):
	return "suggestion" in json_data["query"]["searchinfo"]



######################
#EXAMPLE / HOW TO USE#
######################

#query_articles("ARTICLE NAME", "LANGUAGE")
print(get_article_names_from_query("Albert Einstein", "English", 15))