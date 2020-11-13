import math
import spacy
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from document import Document
from urllib.parse import urlparse
import re




class Parse:


    def __init__(self):
        self.stop_words = stopwords.words('english')
        self.suspucious_words_for_entites={}#dictionary of suspicious words for entites, key is the term and value is the nubmer of apperances



    def parse_sentence(self, text):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """
        text_tokens = word_tokenize(text)
        text_tokens_without_stopwords = [w.lower() for w in text_tokens if w not in self.stop_words]
        return text_tokens_without_stopwords

    def parse_doc(self, doc_as_list):
        """
        This function takes a tweet document as list and break it into different fields
        :param doc_as_list: list re-preseting the tweet.
        :return: Document object with corresponding fields.
        """
        tweet_id = doc_as_list[0]
        tweet_date = doc_as_list[1]
        full_text = doc_as_list[2]
        self.parse_all_text(full_text) #parse text with our functions, need to parse this one or retweet text?
        url = doc_as_list[3]
        retweet_text = doc_as_list[4]
        retweet_url = doc_as_list[5]
        quote_text = doc_as_list[6]
        quote_url = doc_as_list[7]
        term_dict = {}
        tokenized_text = self.parse_sentence(full_text)
        doc_length = len(tokenized_text)  # after text operations.

        for term in tokenized_text:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1

        document = Document(tweet_id, tweet_date, full_text, url, retweet_text, retweet_url, quote_text,
                            quote_url, term_dict, doc_length)
        return document


    #returns a list of all the terms in the URL divided by /, = and .

    def parse_all_text(self,text):
        validator = URLValidator()
        copy_text=text
        num_flag=False
        temp_num=""
        replace_with=""
        self.parse_Entities(text) #need to pass self?
        for word in text:
            if(num_flag): #if found number on previous iteration
                if(word=="Thousand" or word=="Million" or word=="Billion"):
                    copy_text.replace(word,"")
                    copy_text.replace(temp_num,self.parse_big_number(temp_num+word))
                    return
                else:
                    copy_text.replace(temp_num,self.parse_clean_number(temp_num))
                    continue
                num_flag=False
            #if hastag
            if word[0]=="#":
                copy_text.replace(word,self.parse_hashtag(word))
            elif validator(word):
                copy_text.replace(word, self.parse_URL(word))
            elif "%" in word or "percent" in word or "percentage" in word or "Percentage" in word or "Percent":
                copy_text.replace(word,self.parse_precentage(word))
            elif word[0].isisnumeric(): # if found number check next word
                word.replace(",","")
                num_flag=True
                temp_num=word
            elif entites_and_name: #needs to be saved in the INDEX(!) according to instructions
                do_something()
            elif BigSmallLetters:
                do_something()

        return copy_text




    def parse_URL(self,URL):
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
        string=' '.join(parsed_url)
        return string


    def parse_hashtag(self,text):
        if '_' in text:
            pattern = re.compile(r"[a-z]+|\d+|[][a-z]+(?![a-z])-[]")
        else:
            pattern = re.compile(r"[A-Z][a-z]+|\d+|[a-z]+(?![a-z])")
        splitted = pattern.findall(text[1:])
        splitted.append('#' + "".join(splitted))
        mylist= [x.lower() for x in splitted]
        string=' '.join(mylist)
        return string

    def parse_precentage(self,text):
        return text.replace("percentage", "%").replace("percent", "%").replace(" ", "")

    def parse_clean_number(self,text):

        millnames = ['', 'K', 'M', 'B']
        n = float(text)
        # print(n)
        millidx = max(0, min(len(millnames) - 1,
                             int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))))

        mylist= '{:.3f}{}'.format(n / 10 ** (3 * millidx), millnames[millidx])
        string = ' '.join(mylist)
        return string

    def parse_big_number(self,text):
        return text.replace(' Thousand', 'K').replace(' Million', 'M').replace(' Billion', 'B')

    def parse_Entities(self,text):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        for entity in doc.ent:
            if(entity in self.suspucious_words_for_entites): #if term already exists
                self.suspucious_words_for_entites[entity] += 1
            else:
                self.suspucious_words_for_entites[entity] = 1






