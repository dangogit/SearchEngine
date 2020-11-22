import re

import nltk
import spacy

import pandas as pd
import search_engine
from parser_module import Parse
from reader import ReadFile
from urllib.parse import urlparse
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer




def parse_entites(text):
    proccesing_word=False
    temp_term=""
    entity_list=[]
    word_list=str.split(text," ")
    for i in range(len(word_list)):
        if word_list[i][0].isupper()==False and proccesing_word==True:
            check_list=str.split(temp_term)
            if (len(check_list) > 1):
                entity_list.append(temp_term)
            temp_term=""
            proccesing_word=False
        elif i==len(word_list)-1 and proccesing_word==True:
            temp_term = temp_term + " " + word_list[i]
            if(len(temp_term)>1):
                entity_list.append(temp_term)
        elif word_list[i][0].isupper()==True:
            temp_term = temp_term + " " + word_list[i]
            proccesing_word = True
    return entity_list


if __name__ == '__main__':
    #search_engine.main()
    #newReader= ReadFile(r"C:\Users\dorle\Data")
    #newReader.Read_Files()
    #testing:
   # print(re.sub('[0-9\[\]/"{},.:-]+', '', "COVID-19:"))
    p = Parse()
    df = pd.DataFrame([[1, 2], [3, 4]], columns=list('AB'))



