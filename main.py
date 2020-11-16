import re

import nltk
import spacy
from math import log


import search_engine
from parser_module import Parse
from reader import ReadFile
from urllib.parse import urlparse

def adir_parse(text):
    lst = str.split(text, " ")
    if (lst._contains_('')):
        lst.remove('')
    count = 0
    parseList = ''
    for term in lst:
        count += 1
        tag = term
        if (len(tag) <= 0 or tag[0] != '#'):
            continue
        parseList = tag[1:]
        parseList = str.replace(parseList, '_', '')
        parseList = re.sub(r"([A-Z])", r" \1", parseList)
        parseList = parseList.lower()
        secparseList = parseList.replace(' ', '')
        split_tag = str.split(parseList, " ") + ['#' + secparseList]
        if (count == len(lst)):
            lst = lst[:len(lst) - 1] + split_tag
        else:
            lst = lst[:count] + split_tag + lst[count:]
    lst = ' '.join(map(str, lst))
    return lst



def parse_hashtag(text):

    idx=0
    final_word=''
    list_to_add=[]
    temp_txt=text
    #if "_" in temp_txt:
    temp_txt=temp_txt.replace("_","").replace("-","")
    temp_txt=temp_txt.lower()
    list_to_add.append(temp_txt)
    list_with_numbers=re.split('(\d+)',text)
    if list_with_numbers.__contains__(""):
        list_with_numbers.remove("")
    parseList = []
    for item in list_with_numbers:
        if item.isnumeric()==False:
            parseList.append(item)
        else:
            list_to_add.append(item)
    for word in parseList:
        idx+=1
        temp=word
        if temp != "#":
            final_word+=temp[1:]
            final_word=final_word.replace("_"," ")
            final_word=final_word.replace("-","")
            final_word=re.sub(r"([A-Z])", r" \1", final_word)
            #final_word=final_word.replace(' ','')
            final_word_as_lst = str.split(final_word, " ")+list_to_add
            if(len(parseList)==idx):
                parseList= parseList[:len(parseList)-1]+final_word_as_lst
            else:
                parseList=parseList[:idx]+final_word_as_lst+parseList[idx:]
    if(parseList.__contains__("")):
        parseList.remove("")
    string = ' '.join(parseList)
    string_lower=string.lower() #turn to lower case
    return string_lower


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

    #testing:
    p = Parse()
    #text = p.parse_all_text("5G")
    #print(text)

    URL="https://www.programiz.com/python-programming/dictionary"

    test=parse_hashtag("#trumpForPresident_2020")
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



    string=parse_URL(URL)
    print(string)







