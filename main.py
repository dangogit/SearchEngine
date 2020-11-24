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
    dict['ab']= 4
    dict['abc']=17
    return {k: dict[k] for k in sorted(dict)}


if __name__ == '__main__':
    lst=[(1,3),(4,7),(11,9)]
    print(lst)