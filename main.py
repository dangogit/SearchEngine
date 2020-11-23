import re

import nltk
import time
import collections
import timeit
import search_engine
from parser_module import Parse
from reader import ReadFile
from urllib.parse import urlparse
import pandas as pd

from datetime import datetime
def sort_Dict():
    dict = {}
    dict['b'] = 5
    dict['c'] = 2
    dict['a'] = 1
    dict['ab']=4
    return collections.OrderedDict(sorted(dict.items()))
if __name__ == '__main__':
    fmt = '%Y-%m-%d %H:%M:%S'
    text = "dad wadhfkdshfkjsdhfdsjkhskjsdhsjkhfkjhfkjhkdhhksh48473dskljsdls$#@$#@@#$$@%%@##%@%@%@@%VSSVSVDSVSVs |  + ! > < = a big cutie"

    asci_code_to_remove = {33: None, 34: None, 36: None, 38: None, 39: None, 40: None, 41: None, 42: None,
                                43: None, 44: None, 45: None, 46: None, 47: None, 58: None, 59: None, 60: None,
                                61: None, 62: None, 63: None, 91: None, 92: None, 93: None, 94: None, 96: None,
                                123: None, 124: None, 125: None, 126: None}

    d11 = datetime.strptime(datetime.now().strftime(fmt), fmt)
    d11_ts = time.mktime(d11.timetuple())

    text = text.translate(asci_code_to_remove)

    d22 = datetime.strptime(datetime.now().strftime(fmt), fmt)
    d22_ts = time.mktime(d22.timetuple())
    df=d22_ts - d11_ts

    d1 = datetime.strptime(datetime.now().strftime(fmt), fmt)
    d1_ts = time.mktime(d1.timetuple())

    text=text.replace("/n", "").replace("-", "").replace(",", "").replace(".","").replace(":","").replace("!","")\
    .replace('"','').replace("&","").replace("(","").replace(")","").replace("*","").replace("+","")\
    .replace(";","").replace(">"," ").replace("<","").replace("?","").replace("=","")

    d2 = datetime.strptime(datetime.now().strftime(fmt), fmt)
    d2_ts = time.mktime(d2.timetuple())

    df2=d2_ts - d1_ts

    print (df)
    print(df2)
    #text=text.translate(asci_code_to_remove)



    #search_engine.main()
    #newReader= ReadFile(r"C:\Users\dorle\Data")
    #newReader.Read_Files()
    #testing:
   # print(re.sub('[0-9\[\]/"{},.:-]+', '', "COVID-19:"))
    print(text)









