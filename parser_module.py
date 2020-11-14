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
    # todo:
    # 1. funtion to fix all the capital and non capital words in the cursor
    # 2. add the 2 new parsing methods
    # 3. tests

    def __init__(self):
        self.stop_words = stopwords.words('english')
        self.suspucious_words_for_entites = {}  # dictionary of suspicious words for entites, key is the term and value is the nubmer of apperances
        self.word_set = set()
        self.tweets_with_terms_to_fix = {}

    def parse_sentence(self, text):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """

        text_tokens = word_tokenize(text)
        text_tokens_without_stopwords = [w.lower() for w in text_tokens if w not in self.stop_words]
        return text_tokens_without_stopwords

    def parse_doc(self, doc_as_list, idx):
        """
        This function takes a tweet document as list and break it into different fields
        :param doc_as_list: list re-preseting the tweet.
        :return: Document object with corresponding fields.
        """
        if idx in self.tweets_with_terms_to_fix:
            #doc_as_list[2] = self.fix_word_with_future_change(doc_as_list[2])
            doc_as_list[5] = self.fix_word_with_future_change(doc_as_list[5])

        tweet_id = doc_as_list[0]
        tweet_date = doc_as_list[1]
        full_text = doc_as_list[2]
        full_text = self.parse_all_text(
            full_text)  # parse text with our functions, need to parse this one or retweet text?
        url = doc_as_list[3]
        url = self.parse_URL(url)
        indices = doc_as_list[4]
        retweet_text = doc_as_list[5]
        retweet_url = doc_as_list[6]
        retweet_url = self.parse_URL(url)
        retweet_indices = doc_as_list[7]
        quote_text = doc_as_list[8]
        quote_url = doc_as_list[9]
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

    # returns a list of all the terms in the URL divided by /, = and .

    def parse_all_text(self, text):
        text.replace("/n", "")
        copy_text = text.split()
        num_flag = False
        temp_num = ""
        self.parse_Entities(text)  # need to pass self?
        count = 0
        for word in copy_text:
            if (num_flag):  # if found number on previous iteration
                if word == "Thousand" or word == "Million" or word == "Billion" or word == "million" or word == "billion" or word == "thousand":
                    copy_text.remove(word)
                    copy_text[count - 1] = self.parse_big_number(temp_num + " " + word)
                    # copy_text.replace(word,"")
                    # copy_text.replace(temp_num,self.parse_big_number(temp_num+word))
                else:
                    try:
                        num = float(copy_text[count - 1])
                    except ValueError:
                        continue
                    copy_text[count - 1] = self.parse_clean_number(temp_num)
                num_flag = False

            if num_flag == False and (
                    word == "Thousand" or word == "Million" or word == "Billion" or word == "million" or word == "billion" or word == "thousand"):
                # in case a million appeared without any number before it
                copy_text[count] = self.parse_big_number(word)
            # if hastag
            if word[0] == "#":
                copy_text[count] = self.parse_hashtag(word)

            elif word.find('%') > -1 or word.find('percent') > -1 or word.find('percentage') > -1 or word.find(
                    'Percentage') > -1 or word.find('Percent') > -1:
                copy_text[count] = self.parse_precentage(word)
            elif word[0].isnumeric():  # if found number check next word
                word.replace(",", "")
                num_flag = True
                temp_num = word
            # elif BigSmallLetters:
            #   do_something()
            count += 1
        parsed_text_as_str = ' '.join(copy_text)
        return parsed_text_as_str

    def parse_URL(self, URL):
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

    def parse_hashtag(self, text):
        if '_' in text:
            pattern = re.compile(r"[a-z]+|\d+|[][a-z]+(?![a-z])-[_]")
        else:
            pattern = re.compile(r"[A-Z][a-z]+|\d+|[a-z]+(?![a-z])")
        splitted = pattern.findall(text[1:])
        splitted.append('#' + "".join(splitted))
        mylist = [x.lower() for x in splitted]
        string = ' '.join(mylist)
        return string

    def parse_precentage(self, text):
        return text.replace("percentage", "%").replace("percent", "%").replace(" ", "")

    def parse_clean_number(self, text):

        text = text.replace(",", "")
        text = text.replace(":", "")
        millfullnames = ["Thousand", "Million", "Billion", "million", "billion", "thousand"]
        if text in millfullnames:
            return text
        if "th" in text or "G" in text:  # not sure, may need to create file of endings and check from there
            return text
        if ("/" in text):  # in case of fraction x/y
            converted_num = float(text[0]) / float(text[2])
            return str(converted_num)
        if float(text) < 1000:
            return text

        millnames = ['', 'K', 'M', 'B']
        n = float(text)
        # print(n)
        millidx = max(0, min(len(millnames) - 1,
                             int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))))

        mylist = '{:.3f}{}'.format(n / 10 ** (3 * millidx), millnames[millidx])
        string = ' '.join(mylist)
        return string

    def parse_big_number(self, text):
        text = text.replace(",", "")

        return text.replace(' Thousand', 'K').replace(' Million', 'M').replace(' Billion', 'B').replace(' thousand',
                                                                                                        'K').replace(
            ' billion', 'B').replace(' million', 'M')

    def parse_Entities(self, text):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        for entity in doc.ents:
            if (entity in self.suspucious_words_for_entites):  # if term already exists
                self.suspucious_words_for_entites[entity] += 1
            else:
                self.suspucious_words_for_entites[entity] = 1

    def word_to_lower(self, text, idx):
        if text is None:
            return
        words_list = text.split()
        for word in words_list:
            if word not in self.word_set:
                if word.lower() not in self.word_set and "http" not in word and "#" not in word and "@" not in word:  # word was not in the set at all
                    self.word_set.add(word)
                    if word[0].upper() + word[1:] in self.word_set:  # found lower case word first time
                        self.word_set.remove(word[0].upper() + word[1:])
                    if word.lower() != word:  # word is capital, maybe will need change in future
                        self.add_word_to_future_change(idx, word)
                else:  # word was with capital but in set with lower
                    word = word.lower()
            elif word.lower() != word:  # word is capital, maybe will need change in future
                self.add_word_to_future_change(idx, word)
        text = ' '.join(words_list)

        return text

    def add_word_to_future_change(self, idx, word):
        if idx not in self.tweets_with_terms_to_fix.keys():  # new tweet
            self.tweets_with_terms_to_fix[idx] = set()
            self.tweets_with_terms_to_fix[idx].add(word)

        elif word not in self.tweets_with_terms_to_fix[idx]:  # old tweet, new word
            self.tweets_with_terms_to_fix[idx].add(word)

    def fix_word_with_future_change(self, text):
        if text is None:
            return None
        words_list = text.split()
        for word in words_list:
            if "http" not in word and "#" not in word and "@" not in word:
                if word.lower() in self.word_set:
                    text = text.replace(word, word.lower())
                else:
                    text = text.replace(word, word.upper())
        return text
