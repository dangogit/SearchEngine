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


    search_engine.main()
    #newReader= ReadFile(r"C:\Users\dorle\Data")
    #newReader.Read_Files()
    #testing:
   # print(re.sub('[0-9\[\]/"{},.:-]+', '', "COVID-19:"))









