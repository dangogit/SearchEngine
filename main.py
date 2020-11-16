import re
import nltk
import spacy

import spacy
import search_engine
from parser_module import Parse
from reader import ReadFile
from urllib.parse import urlparse

def check_capital(text):
    if "#" in text:
        text=text.replace("#","")
    for letter in text:
        if(letter.isnumeric()==False and letter.isupper()==False):
            return False
    return True


def parse_hashtag(text):
    idx = 0
    final_word = ''
    list_to_add = []
    temp_txt = text
    # if "_" in temp_txt:
    temp_txt = temp_txt.replace("_", "").replace("-", "")
    temp_txt = temp_txt.lower()
    list_to_add.append(temp_txt)
    list_with_numbers = re.split('(\d+)', text)
    if "" in list_with_numbers:
        list_with_numbers.remove("")
    parseList = []
    for item in list_with_numbers:
        if item.isnumeric() == False:
            parseList.append(item)
        else:
            list_to_add.append(item)
    for word in parseList:
        idx += 1
        temp = word
        if temp != "#":
            final_word += temp[1:]
            final_word = final_word.replace("_", " ")
            final_word = final_word.replace("-", "")
            all_capital=check_capital(text)
            if(all_capital==False):
                final_word = re.sub(r"([A-Z])", r" \1", final_word)
            # final_word=final_word.replace(' ','')
            final_word_as_lst = str.split(final_word, " ") + list_to_add
            if (len(parseList) == idx):
                parseList = parseList[:len(parseList) - 1] + final_word_as_lst
            else:
                parseList = parseList[:idx] + final_word_as_lst + parseList[idx:]
    if "" in parseList:
        parseList.remove("")
    string = ' '.join(parseList)
    string_lower = string.lower()  # turn to lower case
    return string_lower

suspucious_words_for_entites={}


if __name__ == '__main__':
    #search_engine.main()
    #newReader= ReadFile(r"C:\Users\dorle\Data")
    #newReader.Read_Files()

    #testing:
    p = Parse()
   # text = p.parse_all_text("2021.1")
   # print(text)

    test = parse_hashtag("#STAYatHOME")
    print(test)






