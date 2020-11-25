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

def parse_entites(text):
    lst=text.split()
    saw_big_letter=False
    tmp_entity=""
    entity_list=[]
    for idx,word in enumerate(lst):
        if word[0].isupper() and saw_big_letter==True:
            tmp_entity+=" "+word
            if(idx==len(lst)-1):
                entity_list.append(tmp_entity)
        elif word[0].isupper() and saw_big_letter==False:
            saw_big_letter=True
            tmp_entity += word
        elif len(tmp_entity.split())>=2:
            entity_list.append(tmp_entity)
            tmp_entity=""
            saw_big_letter=False
        else:
            tmp_entity = ""
    return entity_list


def check_numeric(text):
    for charcter in text:
        if charcter.isdigit():
            return True
    return False
def parse_hastag_new(text):
    tmp_word=""
    word_list = [text]
    contains_dash=False
    letter_index=0
    if("_" in text):
        contains_dash=True
    text = text.replace("_", " ")
    contain_numeric=check_numeric(text)

    text=text.replace("#","")
    if text.isupper()==True: #in case all capital
        new_text=text.replace("#","")
        word_list.append(new_text.lower())
        return word_list
    elif contain_numeric == False and contains_dash==True: #not numeric and no dashes
        list = text.split()
        word_list = word_list + list
    else:
        #else if all word connected and start with capital letter (besides the first one)

        for i in range(len(text)):
            if text[i].isnumeric()==True:
                word_list.append(tmp_word.lower())
                letter_index=i
                tmp_word=text[i]
                break

            elif (text[i].isupper() and i != 0):
                word_list.append(tmp_word.lower())
                tmp_word = text[i]
            else:
                tmp_word = tmp_word + text[i]

        for k in range(letter_index+1,len(text)):
            if(text[k].isnumeric()==True):
                tmp_word=tmp_word+text[k]
        word_list.append(tmp_word.lower())
    return ' '.join(word_list)


def parse_URL(url):
    tmp_word=""
    word_list=[url]
    #or replace on all : / -  and then split and join
    url=url.replace(":","").replace("//","/")
    for i in range(len(url)):
        if(url[i]==":" or url[i]=="." or url[i]=="/" or url[i]=="-" or url[i]=="_"):
            word_list.append(tmp_word)
            tmp_word=""
        elif i != len(url)-1:
            tmp_word=tmp_word+url[i]
        else:
            word_list.append(tmp_word)
    return ' '.join(word_list)



if __name__ == '__main__':
    url="https://www.whathifi.com/best-buys/home-cinema/best-home-cinema-amplifiers"
    hastag="#seeyouonthebeach"
    entity_sentence="Donald Trump, is the president"
    entity_sentence=entity_sentence.replace("-"," ").replace(","," ")
    entities=parse_entites(entity_sentence)
    string=parse_URL(url)
    hastag=parse_hastag_new(hastag)
    print(string)
    print(hastag)
    #search_engine.main()
    print("Hello and welocme to our search engine")

    search_engine.main()

    #newReader= ReadFile(r"C:\Users\dorle\Data")
    #newReader.Read_Files()
    #testing:
    # print(re.sub('[0-9\[\]/"{},.:-]+', '', "COVID-19:"))









