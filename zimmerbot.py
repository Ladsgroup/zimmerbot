from query_article_titles import *
from page_popularity import *
from linked_pages import *
from ores_assessment import *
import sys
import multiprocessing as mp
import time

def exclude_helper(article_names, scaled_ores_rating_results):
    ans = []
    for name in article_names:
        if name in scaled_ores_rating_results:
            ans += [name]
    return ans

def popularity_helper(article_keys, language_code, article_ratings):
    for k in article_keys:
            pageview = get_page_view(k, language_code)
            if pageview != -1:
                article_ratings[k] = pageview
            else:
                articles.pop(k)
    return article_ratings

# MAIN FUNCTION

def main(method, query, language_code, filter_method, limit, stub="include"):
    # Process script arguments
    # For now, we only support limiting by number of articles, not total package size
    
    # limit = max(min(int(limit), 500), 1)

    # article_dictionaries is a list of dictionaries
    start = time.time()
    if method == "individual":
        article_dictionaries = query_articles(query, language_code)[:limit+20]
    elif method == "category":
        article_dictionaries = get_articles_in_category(query, language_code, limit)[:limit+20]
    elif method == "related":
        article_dictionaries = query_related_articles_titles(query, language_code)[:limit+20]
    elif method == "linked":
        article_dictionaries = query_linked_articles(query, language_code)
        if article_dictionaries == None:
            print(query + " is not a valid Wikipedia article")
            article_dictionaries = []
            sys.exit(0)
        else:
            article_dictionaries = article_dictionaries[:limit+20]
    else:
        print("Invalid search method. Please choose individual_articles, categories, related_articles, linked_to_articles")
        sys.exit(0)
    end = time.time()
    print("TIMER1 ", end - start)
    # list of strings
    start1 = time.time()
    #pool_orig = mp.Pool(processes=10)
    pool_orig = Pool(4)
    article_names = pool_orig.map(get_article_names_from_query, article_dictionaries)
    #article_names = pool_orig.apply(get_article_names_from_query, args=(article_dictionaries,))
    #article_names = get_article_names_from_query(article_dictionaries)

    if filter_method == "ores_quality" or stub == "exclude":
        ores_rating_results = get_ores_assessment(article_names, language_code)
        # Assign a numerical score based on qualitative assessment
        scaled_ores_rating_results = scale_article_assessments(ores_rating_results)
        if stub == "exclude":
            scaled_ores_rating_results = {name : score for name, score in scaled_ores_rating_results.items() if score != 0}
            pool = mp.Pool(processes=4)
            article_names = pool.apply(exclude_helper, args=(article_names, scaled_ores_rating_results))

    # Dictionary of page objects with article names as keys
    articles = get_articles_from_names(article_names, language_code) # {"name: page_object"}
    end1 = time.time()
    print("TIMER2 ", end1 - start1)
    # Initialize empty dictionary of article ratings hashed by article name/title
    article_ratings = {} # {"title: numerical_article_score"}
    start2 = time.time()
    if filter_method == "ores_quality":
            article_ratings = scaled_ores_rating_results
    elif filter_method == "popularity":
        article_keys = list(articles.keys())
        pool2 = mp.Pool(processes=4)
        article_ratings = pool2.apply(popularity_helper, args=(article_keys, language_code, article_ratings))
    elif filter_method == "most_linked_to":
        for article in articles:
            article_ratings[article] = count_backlinks(article, language_code)
    else:
        print("Invalid filter method. Please choose popularity, most_linked_to, or ores_quality")
        sys.exit(0)

    sorted_articles = sorted(articles.items(), key=lambda x: article_ratings[x[0]], reverse=True)
    end2 = time.time()
    print("TIMER3 ", end2 - start2)
    return process_results(sorted_articles[:limit])

def process_results(sorted_articles):
    results = []
    for i in range(len(sorted_articles)):
        results.append(sorted_articles[i][1].full_url())
    return results

if __name__ == "__main__":
    # query = input("Please enter your query: ")
    # language = language_dict[input("Please enter a language: ").capitalize()]
    # filter_method = input("Please enter the filtering method: ")
    # limit = input("Enter a limit no more than 500: ")
    #print(main("category", "query", "language", "filter_method", number, "include"))
    lst = main("individual", "science", "en", "popularity", 10, "exclude")
    #print("TIMER ",)
    print("----", lst)
    print("LENGTH: ", len(lst))
    
