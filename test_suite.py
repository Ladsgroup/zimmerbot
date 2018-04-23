from zimmerbot import * 
import time

def basic_functionality_test():

    methods = ["individual", "category", "related", "linked"]
    queries = ["people", "cat"]
    languages = ["en"]
    filter_methods = ["ores_quality", "popularity", "most_linked_to"]
    limits = [0, 10]
    stubs = ["include", "exclude"]

    total = 0
    functional = 0

    #querying by category
    valid_categories = ["people", "sports", "animals"] 
    invalid_categories = ["cat"]

    #querying by linked articles
    valid_articles = ["Anne Frank", "cat", "people"]
    invalid_articles = ["Tilden Park"]

    for a in methods:
        for b in queries:
            for c in languages:
                for d in filter_methods:
                    for e in limits:
                        for f in stubs:
                            try:
                                start = time.time()
                                lst = main(a, b, c, d, e, f)
                                end = time.time()
                                total += 1
                                if len(lst) == e:
                                    functional += 1
                                    print(end - start, "pass: ", a, b, c, d, e, f)
                                elif (a == "category") and (b in invalid_categories) and (len(lst) == 0):
                                    #A category search for an invalid category should return an empty list []
                                    functional += 1
                                    print(end - start, "pass: ", a, b, c, d, e, f)
                                elif (a == "linked") and (b in invalid_articles) and (len(lst) == 0):
                                    #A linked article search for an invalid list should return an empty list []
                                    functional += 1
                                    print(end - start, "pass: ", a, b, c, d, e, f)
                                else:
                                    print(end - start, "fail_func: ", a, b, c, d, e, f)
                            except Exception as ex:
                                total += 1
                                print(time.time() - start, "fail_ex: ", a, b, c, d, e, f, ex)

    print(str(functional), " out of ", str(total), " pass")

def language_test():
    
    #todo

    total = 0
    functional = 0

    print(str(functional), " out of ", str(total), " pass")

def fuzzing_input_test():
    
    methods = ["individual", "category", "related", "linked"]
    queries = ["jwekae", "13vdf2"]
    languages = ["en"]
    filter_methods = ["ores_quality", "popularity", "most_linked_to"]
    limits = [10]
    stubs = ["include", "exclude"]

    total = 0
    functional = 0

    for a in methods:
        for b in queries:
            for c in languages:
                for d in filter_methods:
                    for e in limits:
                        for f in stubs:
                            try:
                                start = time.time()
                                lst = main(a, b, c, d, e, f)
                                end = time.time()
                                total += 1
                                if len(lst) == e:
                                    functional += 1
                                    print(end - start, "pass: ", a, b, c, d, e, f)
                                else:
                                    print(end - start, "fail_func: ", a, b, c, d, e, f)
                            except Exception as ex:
                                total += 1
                                print(time.time() - start, "fail_ex: ", a, b, c, d, e, f, ex)


    print(str(functional), " out of ", str(total), " pass")

if __name__ == "__main__":
    
    basic_functionality_test()
    #fuzzing_input_test()