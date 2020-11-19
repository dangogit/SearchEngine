import re

import nltk
import spacy


import search_engine
from parser_module import Parse
from reader import ReadFile
from urllib.parse import urlparse
import pandas as pd

if __name__ == '__main__':
    search_engine.main()
    #newReader= ReadFile(r"C:\Users\dorle\Data")
    #newReader.Read_Files()
    #testing:
   # print(re.sub('[0-9\[\]/"{},.:-]+', '', "COVID-19:"))
    df = pd.read_json("posting_file.json", lines=True)
    df.columns = ['1', '2', '3', '4', '5', '6']
    print(df.sort_values(by=['1', '2'], ascending=True))
    df = pd.DataFrame([['1','aa'],['2','bb']], columns=['f','s'])
    df2 = pd.DataFrame([['0','cc'],['3','dd']], columns=['f','s'])
    print(pd.concat([df, df2]).sort_values(by=['f'], ascending=True))
    p = Parse()
    text = p.parse_all_text("CongressWoman Alexandria Ocasio-Cortez has announced Google as a crime syndicate Google")
    print(text)

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


