import sys
# sys.path.append("..")
import pywikibot
import json, urllib
import datetime

# TLDR: The main function, get_ores_assessment, takes in a list of article names and
# a language (English, Russian, or French). It then prints out each article's name,
# along with an automatically generated (machine learning oooohh) assessment of that
# article (Featured Article, Good Article, A-Class Article, B-Class Article, etc)
# This serves as one possible criterion by which users can sort articles.

# ORES Wiki: https://www.mediawiki.org/wiki/ORES
# ORES Documentation: https://ores.wikimedia.org/v3/

# Base ORES API URL
url = "http://ores.wmflabs.org/v3/scores/"
# url_example = "https://ores.wmflabs.org/v3/scores/enwiki/?models=wp10&revids=34854345"

# Note: We only use wp10 because this is what will give us the current article quality.
# We are not extremely concerned with draftquality

# Unfortunately, only three languages currently support automatic ORES wp10 assessment
# We hope that the impact of this function for sorting by article quality will increase
# as more languages begin to support ORES
ORES_SUPPORTED_WIKIS = {"en": "enwiki",
                    "ru": "ruwiki",
                    "fr": "frwiki"
}

# Create languages dictionary from "list_of_wiki_languages.txt"
def generate_language_dict():
    # with open("list_of_wiki_languages.txt", "r") as file:
    #     lines = file.read().split(",")
    #     for i in range(len(lines)):
    #         lines[i] = lines[i].strip()
    #         lines[i] = lines[i].strip("\'")
    #     dictionary = {lines[i+1]:lines[i] for i in range(0, len(lines), 2)}
    dictionary = {'Afrikaans': 'af', 'Alemannic': 'als', 'Anglo-Saxon': 'ang', 'Bavarian': 'bar', 'Danish': 'da', 'German': 'de', 'Deutsche Sprache': 'de', 'English language': 'en', 'English': 'en', 'Faroese': 'fo', 'North Frisian': 'frr', 'West Frisian': 'fy', 'Gothic': 'got', 'Icelandic': 'is', 'Ripuarian': 'ksh', 'Luxembourgish': 'lb', 'Limburgish': 'li', 'Low Saxon': 'nds', 'Dutch Low Saxon': 'nds-nl', 'Dutch': 'nl', 'Norwegian (Nynorsk)': 'nn', 'Norwegian (Bokm�l)': 'no', 'Pennsylvania German': 'pdc', 'Palatinate German': 'pfl', 'Scots': 'sco', 'Simple English': 'simple', 'Basic English': 'simple', 'Saterland Frisian': 'stq', 'Swedish': 'sv', 'West Flemish': 'vls', 'Yiddish': 'yi', 'Zeelandic': 'zea', 'Aragonese': 'an', 'Asturian': 'ast', 'Catalan': 'ca', 'Corsican': 'co', 'Emilian-Romagnol': 'eml', 'Idioma espa�ol': 'es', 'Spanish': 'es', 'Extremaduran': 'ext', 'French': 'fr', 'Franco-Proven�al': 'frp', 'Friulian': 'fur', 'Galician': 'gl', 'Italian': 'it', 'it': 'Lingua italiana', 'la': 'Lingua italiana', 'lad': 'Latin', 'lij': 'Ladino', 'Ligurian (Romance language)': 'lij', 'Lombard': 'lmo', 'Mirandese': 'mwl', 'Neapolitan': 'nap', 'Norman': 'nrm', 'Occitan': 'oc', 'Picard': 'pcd', 'Portuguese': 'pt', 'L�ngua portuguesa': 'pt', 'Piedmontese': 'pms', 'Romanian': 'ro', 'Aromanian': 'roa-rup', 'Romansh': 'rm', 'Tarantino': 'roa-tara', 'Sardinian': 'sc', 'Sicilian': 'scn', 'Venetian': 'vec', 'Walloon': 'wa', 'Belarusian': 'be', 'Belarusian (Tara�kievica)': 'be-tarask', 'Bulgarian': 'bg', 'Bosnian': 'bs', 'Czech': 'cs', 'Kashubian': 'csb', 'Old Church Slavonic': 'cu', 'Lower Sorbian': 'dsb', 'Croatian': 'hr', 'Upper Sorbian': 'hsb', 'Macedonian': 'mk', 'Polish': 'pl', 'Russian': 'ru', 'Rusyn': 'rue', 'Serbo-Croatian': 'sh', 'Slovenian': 'sl', 'Serbian': 'sr', 'Slovak': 'sk', 'Silesian': 'szl', 'Ukrainian': 'uk', 'Central Bicolano': 'bcl', 'Cebuano': 'ceb', 'Sinugboanon': 'ceb', 'Ilocano': 'ilo', 'Pagsasao nga Ilokano': 'ilo', 'Pangasinan': 'pag', 'Kapampangan': 'pam', 'Tagalog': 'tl', 'Wikang Tagalog': 'tl', 'Waray': 'war', 'Khmer': 'km', 'Vietnamese': 'vi', 'Japanese': 'ja', 'Acehnese': 'ace', 'Banyumasan': 'map-bms', 'Buginese': 'bug', 'Banjar': 'bjn', 'Chamorro': 'ch', 'Indonesian': 'id', 'Javanese': 'jv', 'Minangkabau': 'min', 'Malay': 'ms', 'Sundanese': 'su', 'Min Dong': 'cdo', 'Gan': 'gan', 'Hakka': 'hak', 'Wu': 'wuu', 'Chinese': 'zh', 'Classical Chinese': 'zh-classical', 'Min Nan': 'zh-min-nan', 'Cantonese': 'zh-yue', 'Azerbaijani': 'az', 'Southern Azerbaijani': 'azb', 'Bashkir': 'ba', 'Crimean Tatar': 'crh', 'Chuvash': 'cv', 'Gagauz': 'gag', 'Karakalpak': 'kaa', 'Kazakh': 'kk', 'Karachay-Balkar': 'krc', 'Kirghiz': 'ky', '': 'ky', 'Sakha': 'sah', 'Turkmen': 'tk', 'Turkish': 'tr', 'Tatar': 'tt', 'Tuvan': 'tyv', 'Uyghur': 'ug', 'Uzbek': 'uz', 'Arabic': 'ar', 'Hebrew': 'he', 'Amharic': 'am', 'Egyptian Arabic': 'arz', 'Maltese': 'mt', 'Aramaic': 'arc', 'Tigrinya': 'ti', 'Kurdish (Sorani)': 'ckb', 'Zazaki': 'diq', 'Persian': 'fa', 'Gilaki': 'glk', 'Northern Luri': 'lrc', 'Kurdish (Kurmanji)': 'ku', 'Mazandarani': 'mzn', 'Ossetian': 'os', 'Pashto': 'ps', 'Tajik': 'tg', 'Finnish': 'fi', 'Estonian': 'et', 'Northern Sami': 'se', 'Hill Mari': 'mrj', 'V�ro': 'fiu-vro', 'Komi': 'kv', 'Komi-Permyak': 'koi', 'Udmurt': 'udm', 'Meadow Mari': 'mhr', 'Vepsian': 'vep', 'Erzya': 'myv', 'Moksha': 'mdf', 'Assamese': 'as', 'Bishnupriya Manipuri': 'bpy', 'Bhojpuri': 'bh', 'Bengali': 'bn', 'Divehi': 'dv', 'Konkani': 'gom', 'Gujarati': 'gu', 'Hindi': 'hi', 'Fiji Hindi': 'hif', 'Marathi': 'mr', 'Kashmiri': 'ks', 'Nepali': 'ne', 'Doteli': 'dty', 'Odia': 'or', 'Eastern Punjabi': 'pa', 'Pali': 'pi', 'Western Punjabi': 'pnb', 'Romani': 'rmy', 'Maithili': 'mai', 'Sanskrit': 'sa', 'Sindhi': 'sd', 'Sinhalese': 'si', 'Urdu': 'ur', 'Esperanto': 'eo', 'Interlingua': 'ia', 'Interlingue': 'ie', 'Ido': 'io', 'Lojban': 'jbo', 'Novial': 'nov', 'Volap�k': 'vo', 'Korean': 'ko', 'Hungarian': 'hu', 'Lithuanian': 'lt', 'Latgalian': 'ltg', 'Latvian': 'lv', 'Samogitian': 'bat-smg', 'Basque': 'eu', 'Kannada': 'kn', 'Malayalam': 'ml', 'Tamil': 'ta', 'Telugu': 'te', 'Breton': 'br', 'Welsh': 'cy', 'Irish': 'ga', 'Scottish Gaelic': 'gd', 'Manx': 'gv', 'Cornish': 'kw', 'Armenian': 'hy', 'Tibetan': 'bo', 'Standard Tibetan': 'bo', 'Dzongkha': 'dz', 'Burmese': 'my', 'Newar': 'new', 'Greek': 'el', 'Pontic': 'pnt', 'Georgian': 'ka', 'Mingrelian': 'xmf', 'Lao': 'lo', 'Thai': 'th', 'Zhuang': 'za', 'Avar': 'av', 'Chechen': 'ce', 'Lezgian': 'lez', 'Lak': 'lbe', 'Malagasy': 'mg', 'Haitian': 'ht', 'Haitian Creole language': 'ht', 'Papiamentu': 'pap', 'Chavacano': 'cbk-zam', 'Albanian': 'sq', 'Kongo': 'kg', 'Kikuyu': 'ki', 'Lingala': 'ln', 'Luganda': 'lg', 'Northern Sotho': 'nso', 'Chichewa': 'ny', 'Kirundi': 'rn', 'Kinyarwanda': 'rw', 'Shona': 'sn', 'Swati': 'ss', 'Swahili': 'sw', 'Tswana': 'tn', 'Sesotho': 'st', 'Tsonga': 'ts', 'Tumbuka': 'tum', 'Venda': 've', 'Xhosa': 'xh', 'Zulu': 'zu', 'Yoruba': 'yo', 'Quechua': 'qu', 'Buryat': 'bxr', 'Mongolian': 'mn', 'Kalmyk': 'xal', 'Hawaiian': 'haw', 'Maori': 'mi', 'Samoan': 'sm', 'Tongan': 'to', 'Tahitian': 'ty', 'Nahuatl': 'nah', 'Oromo': 'om', 'Somali': 'so', 'Aymara': 'ay', 'Bislama': 'bi', 'Norfolk': 'pih', 'Sranan': 'srn', 'Tok Pisin': 'tpi', 'Guarani': 'gn', 'Navajo': 'nv', 'Abkhazian': 'ab', 'Kabardian': 'kbd', 'Kabyle': 'kab', 'Inupiak': 'ik', 'Inuktitut': 'iu', 'Greenlandic': 'kl', 'Hausa': 'ha', 'Tetum': 'tet', 'Nauruan': 'na', 'Fula': 'ff', 'Wolof': 'wo', 'Akan': 'ak', 'Ewe': 'ee', 'Twi': 'tw', 'Igbo': 'ig', 'Cheyenne': 'chy', 'Cree': 'cr', 'Cherokee': 'chr', 'Bambara': 'bm', 'Fijian': 'fj', 'Sango': 'sg', 'Afar': 'aa', 'Herero': 'hz', 'Hiri Motu': 'ho', 'Kanuri': 'kr', 'Muscogee': 'mus', 'Ndonga': 'ng', 'Kuanyama': 'kj', 'Adyghe': 'ady', 'Choctaw': 'cho', 'Marshallese': 'mh', 'Nuosu': 'ii', 'Moldovan': 'mo', 'Jamaican Patois': 'jam', 'Tulu': 'tcy', 'Livvi-Karelian': 'olo', 'Kabiye': 'kbp', 'Dinka': 'din', 'Atikamekw': 'atj'}

    return dictionary


###############
#MAIN FUNCTION#
###############

# Returns the ORES automatic article quality assessment for the given article_name and language_code
def get_ores_assessment(article_names, language_code):
    if language_code not in ORES_SUPPORTED_WIKIS:
        print("Sorry, automatic ORES article quality assessment is not available in " + language_code)
        sys.exit(0)
    else:
        built_url, rev_ids, = build_ores_url(article_names, language_code)
        with urllib.request.urlopen(built_url) as url:
            data = json.loads(url.read().decode())
            all_assessments = get_article_assessments(data)
            for i in range(len(article_names)):
                print("Article Name: " + article_names[i])
                print("ORES Assessment: " + all_assessments[rev_ids[i]])
            return all_assessments

##################
#HELPER FUNCTIONS#
##################

# Builds the JSON request URL
def build_ores_url(article_names, language_code):
    # Get Wikipedia's revision id for the articles' most recent revision (aka the current version)
    site = pywikibot.getSite(language_code)
    rev_ids = []
    for article_name in article_names:
        page = pywikibot.Page(site, article_name)
        rev_id = page.latest_revision.hist_entry().revid
        rev_ids.append(str(rev_id))
    # The context is essentially the same as the language (only three languages/contexts are supported at this time)
    context = ORES_SUPPORTED_WIKIS[language_code]

    result = url + context + "/?models=wp10&revids=" + "|".join(rev_ids)

    return result, rev_ids


# Returns the ORES automatic article assessment (see following link for table of assessments:
# https://www.mediawiki.org/wiki/ORES#/media/File:Article_quality_and_importance.wp10bot.enwiki.png)
def get_article_assessments(data):
    print(data)
    scores = {}
    # first index 0 is the wiki (enwiki, ruwiki, or frwiki)
    # second index 0 is the rev_id
    scores_json = list(data.values())[0]["scores"]
    for article in scores_json:
        score = scores_json[article]["wp10"]["score"]
        scores[article] = score["prediction"]
    return scores

def scale_article_assessments(article_rating_results):
    article_rating_rules = {
        "FA" : 5,
        "FL" : 5,
        "GA" : 4,
        "A" : 4,
        "B" : 3,
        "C" : 2,
        "Start" : 1,
        "Stub" : 0,

        "AdQ" : 6,
        "BA" : 5,
        "A" : 4,
        "B" : 3,
        "BD" : 2,
        "E" : 1,

        "ХС" : 7,
        "ИС" : 6,
        "ДС" : 5,
        "IV" : 4,
        "III" : 3,
        "II" : 2,
        "I" : 1

    }
    for i in range(len(article_rating_results)):
        letter_grade = article_rating_results[i]
        article_rating_results[i] = article_rating_rules[letter_grade]
    return article_rating_results

######################
#EXAMPLE / HOW TO USE#
######################

if __name__ == "__main__":
    language_dict = generate_language_dict()

    get_ores_assessment(["Mediterranean", "Rhode Island", "Car"], language_dict["Russian"])

# Performance notes:
# After an article has been queried, it seems that it is cached automatically, so if it is queried again,
# the process is much faster.
