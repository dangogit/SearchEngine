import re

import nltk
import spacy
from math import log


import search_engine
from reader import ReadFile
from urllib.parse import urlparse




def parse_hashtag(text):
    if '_' in text:
        pattern = re.compile(r"[a-z]+|\d+|[][a-z]+(?![a-z])-[_]")
    else:
        pattern = re.compile(r"[A-Z][a-z]+|\d+|[a-z]+(?![a-z])")
    splitted = pattern.findall(text[1:])
    splitted.append('#' + "".join(splitted))
    mylist = [x.lower() for x in splitted]
    string = ' '.join(mylist)
    return string


def check_num_in_string(text):
    flag=False
    for letter in text:
        if letter.isdigit():
            flag=True
    return True











if __name__ == '__main__':
    #search_engine.main()
    #newReader= ReadFile(r"C:\Users\dorle\Data")
    #newReader.Read_Files()

    URL="https://www.programiz.com/python-programming/dictionary"

    test=parse_hastag_new("#StayAtHome2020")
    print(test)

    text="CongressWoman Alexandria Ocasio-Cortez has announced Google as a crime syndicate"

    nlp=spacy.load("en_core_web_sm")

    doc=nlp(text)

    for entity in doc.ents:
        print(entity.text)

    def parse_URL(URL):
        parsed = urlparse(URL, allow_fragments=True)
        parsed_url = []
        parsed_url.append(parsed.scheme)
        netloc = parsed.netloc
        if "www" in netloc:
            netloc = netloc.replace("www.", "")
            parsed_url.append("www")
        parsed_url.append(netloc)
        path = parsed.path
        path = re.split(', |_|-|!|\+|=|/', path)
        query = parsed.query
        query = re.split(', |_|-|!|\+|=|/', query)
        for word in path:
            if (word != ""):
                parsed_url.append(word)
        for word in query:
            if (word != ""):
                parsed_url.append(word)
        string = ' '.join(parsed_url)
        return string


    parse_hastag_new("StayAtHome")

    string=parse_URL(URL)
    print(string)







