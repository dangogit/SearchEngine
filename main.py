import re

import nltk
import spacy


import search_engine
from parser_module import Parse
from reader import ReadFile
from urllib.parse import urlparse
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer



if __name__ == '__main__':
    #search_engine.main()
    #newReader= ReadFile(r"C:\Users\dorle\Data")
    #newReader.Read_Files()
    #testing:
   # print(re.sub('[0-9\[\]/"{},.:-]+', '', "COVID-19:"))
    p = Parse()
    #text = p.parse_all_text("CongressWoman Alexandria Ocasio-Cortez has announced Google as a crime syndicate Google")
    #print(text)

    porter = PorterStemmer()
    lancaster = LancasterStemmer()

    print("Porter Stemmer")
    print(porter.stem("cats"))
    print(porter.stem("trouble"))
    print(porter.stem("troubling"))
    print(porter.stem("troubled"))
    print("Lancaster Stemmer")
    print(lancaster.stem("cats"))
    print(lancaster.stem("trouble"))
    print(lancaster.stem("troubling"))
    print(lancaster.stem("troubled"))

