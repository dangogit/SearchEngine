import os
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
from stemmer import Stemmer
def sort_Dict():
    dict = {}
    dict['b'] = 5
    dict['c'] = 2
    dict['a'] = 1
    dict['ab']=4
    return collections.OrderedDict(sorted(dict.items()))
if __name__ == '__main__':

   # print("Hello and welcome to our search engine")
   # ans_bool=False
    #while (ans != "Y" and ans != "N"):
     #   ans = str(input("would you like to search with stemming? Please enter Y/N?"))
      #  if (ans == "Y"):
       #     ans_bool=True  # run with steemer
        #elif (ans == "N"):
         #   ans_bool = False
        #else:
         #   print("Incorrect answer, please enter Y/N \n")
    #query = input("Please enter a query: ")
    #k = int(input("Please enter number of docs to retrieve: "))
    #corpus_path="r'C:\Users\Daniel\Desktop\BGU\שנה ג\סמסטר ה\אחזור מידע\עבודות\FullData'"
    #output_path="?"
  search_engine.main()

  #  print(re.search(r'(.)\1\1', word) is not None)
    #newReader= ReadFile(r"C:\Users\dorle\Data")
    #newReader.Read_Files()
    #testing:
    #print(re.sub('[0-9\[\]/"{},.:-]+', '', "COVID-19:"))









