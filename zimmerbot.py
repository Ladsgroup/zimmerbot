from query_article_titles import *
from page_popularity import *
from linked_pages import *
from ores_assessment import *
import sys

# MAIN FUNCTION

def main(query, language, filter_method, limit):
    # # Process script arguments
    # query = input("Search query: ")
    # language_code = language_dict[input("Language: ").capitalize()]
    # filter_method = input("Filter Method: ")
    # # For now, we only support limiting by number of articles, not total package size
    # limit = min(int(input("Limit: ")), 500)
    language_dict = generate_language_dict()
    language_code = language_dict[language.capitalize()]
    limit = min(int(limit), 500)

    # Get the query results
    article_dictionaries = query_articles(query, language_code)[:limit]
    # Turn the query results into a list of article titles
    article_names = get_article_names_from_query(article_dictionaries)
    # Get the hashed page objects from the article names
    articles = get_articles_from_names(article_names, language_code) # {"title: page_object"}
    # Initialize empty dictionary of article ratings hashed by article name/title
    article_ratings = {} # {"title: numerical_article_score"}

    if filter_method == "ores_quality":
        article_rating_results = get_ores_assessment(article_names, language_code)
        # Assign a numerical score based on qualitative assessment
        scaled_article_rating_results = scale_article_assessments(article_rating_results)
        for i in range(len(article_names)):
            article_ratings[article_names[i]] = scaled_article_rating_results[i]
    elif filter_method == "popularity":
        for article in articles:
            article_ratings[article] = get_page_view(article, language_code)
    elif filter_method == "most_linked_to":
        for article in articles:
            article_ratings[article] = count_backlinks(article, language_code)
    else:
        print("Invalid filter method. Please choose popularity, most_linked_to, or ores_quality")
        sys.exit(0)

    sorted_articles = sorted(articles.items(), key=lambda x: article_ratings[x[0]], reverse=True)

    return print_results(sorted_articles, article_ratings)

def print_results(sorted_articles, article_ratings):
    results = []
    for i in range(len(sorted_articles)):
        results.append(sorted_articles[i][1].full_url())
    return results

if __name__ == "__main__":
    language_dict = generate_language_dict()
    main()
