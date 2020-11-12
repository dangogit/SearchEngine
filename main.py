import re

import nltk

import search_engine
from reader import ReadFile
from urllib.parse import urlparse


if __name__ == '__main__':
    #search_engine.main()
    #newReader= ReadFile(r"C:\Users\dorle\Data")
    #newReader.Read_Files()

    URL="https://www.instagram.com/p/CD7fAPWs3WM/?igshid=o9kf0ugp1l8x"
    parsed = urlparse(URL, allow_fragments=True)
    parsed_url = []
    netloc=parsed.netloc
    netloc=netloc.split('.')
    parsed_url.append(parsed.scheme)
    for i in netloc:
        if (i != ""):
            parsed_url.append(i)
    path = parsed.path
    path = re.split(', |_|-|!|\+|=|/',path)
    for i in path:
        if(i != ""):
            parsed_url.append(i)
    query = parsed.query
    query = re.split(', |_|-|!|\+|=|/', query)
    for i in query:
        parsed_url.append(i)
    text="The big star of the evening was without a doubt CongressWoman Alexandria Ocasio-Cortez"
    nltk.pos(text)



    print(parsed_url)
