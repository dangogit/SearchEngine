import re

import nltk
import spacy


import search_engine
from reader import ReadFile
from urllib.parse import urlparse


if __name__ == '__main__':
    #search_engine.main()
    #newReader= ReadFile(r"C:\Users\dorle\Data")
    #newReader.Read_Files()

    URL="https://www.programiz.com/python-programming/dictionary"

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




    string=parse_URL(URL)
    print(string)


