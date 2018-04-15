from zimmerbot import * 

def basic_functionality_test():

    methods = ["individual", "category", "related", "linked"]
    queries = ["people", "cat"]
    languages = ["en"]
    filter_methods = ["ores_quality", "popularity", "most_linked_to"]
    limits = [0, 10]
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
                                main(a, b, c, d, e, f)
                                print("works: ", a, b, c, d, e, f)
                                total += 1
                                functional += 1
                            except Exception as ex:
                                print(a, b, c, d, e, f, ex)

    print(str(functional), " out of ", str(total), " pass")

def language_test():
    
    #todo

    total = 0
    functional = 0

    print(str(functional), " out of ", str(total), " pass")

def fuzzing_input_test():
    
    #todo

    total = 0
    functional = 0

    print(str(functional), " out of ", str(total), " pass")



