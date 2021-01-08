import math

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from document import Document
import re

from stemmer import Stemmer


class Parse:

    def __init__(self):
        self.asci_code_to_remove = {33: None, 34: None, 36: None, 38: None, 39: None, 40: None, 41: None, 42: None,
                                    43: None, 44: None, 45: " ", 46: None, 58: None, 59: None, 60: None, 61: None,
                                    62: None, 63: None, 91: None, 92: None, 93: None, 94: None, 96: None, 123: None,
                                    124: None, 125: None, 126: None}
        stopwords_list = stopwords.words('english') + ['?', '!', ',', '+', '-', '*', '"', '.', '<', '>', '=', ':', '', '{', '{}', '}', '[', ']', '[]', 'are',
           'and', 'an', 'at', 'am', 'a', 'even', 'every', 'everyone']
        self.stop_words = {k.lower(): "" for k in stopwords_list}
        self.suspucious_words_for_entites = {}  # dictionary of suspicious words for entites, key is the term and value is the nubmer of apperances
        self.word_set = {}
        self.tweets_with_terms_to_fix = {}
        self.steamer = None
        #  self.countries_codes = pd.read_csv("countries_codes").to_dict(orient='list')
        # self.nlp = spacy.load("en_core_web_sm")
        self.curr_idx = -1
        self.doc_idx_tweet_id = {}


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
        terms_list = self.parse_all_text(full_text)
        full_text = ' '.join(terms_list)
        url = doc_as_list[3]
        # url = self.parse_URL(url)
        # indices = doc_as_list[4]
        # retweet_text = doc_as_list[5]
        # retweet_text=self.parse_all_text(
        #   retweet_text, self.curr_idx)
        # retweet_url = doc_as_list[6]
        # retweet_url = self.parse_URL(url)
        # retweet_indices = doc_as_list[7]
        # quote_text = doc_as_list[8]
        # quote_url = doc_as_list[9]

        term_dict = {}
        # tokenized_text = self.parse_sentence(full_text)
        doc_length = len(terms_list)  # after text operations.

        for term in terms_list:
            if self.steamer is not None and term.isalpha() and '@' not in term and '#' not in term and 'http' not in term:
                term = self.steamer.stem_term(term)
            term = term.lower()
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1

        # document = Document(tweet_id, tweet_date, full_text, url,
        #                    term_dict, doc_length)

        self.doc_idx_tweet_id[self.curr_idx] = tweet_id

        # return [tweet_id, tweet_date, full_text, url,term_dict, doc_length]
        return Document(tweet_id, tweet_date, full_text, url, term_dict, doc_length)

    # returns a list of all the terms in the URL divided by /, = and .

    def parse_all_text(self, text):
        if text is None:
            return text
        text = text.encode('ascii', 'replace').decode()
        text = text.replace("/n", "")
        text = text.translate(
            self.asci_code_to_remove)  # Removing: - | , | . | : | ! | " | & | ( | ) | * | + | ; | > | < | ?
        self.parse_entites(text)
        copy_text = text.split()
        copy_text = [w for w in copy_text if w[0] != '\/' and w.lower() not in self.stop_words.keys()]
        count = 0
        hashtags = []
        urls = []
        for word in copy_text:
            if word == '':
                count += 1
                continue

            elif word[0] == '@':
                count += 1
                continue

            elif 'http' in word or 'www' in word:
                copy_text[count] = ''
                urls.extend(self.parse_URL(word))

            elif word[0] == '#':
                copy_text[count] = ''
                hashtags.extend(self.parse_hashtag(word))

            elif word[0].isnumeric():  # if found number check next word
                try:  # check if its only number
                    num = float(word)
                except ValueError:
                    count += 1
                    continue
                if num >= 1000:
                    copy_text[count] = self.parse_clean_number(num)

                elif count < len(copy_text) - 1:
                    next_word = copy_text[count + 1]
                    if next_word == "Thousand" or next_word == "Million" or next_word == "Billion" or next_word == "million" or next_word == "billion" or next_word == "thousand":
                        copy_text[count] = str(copy_text[count]) + str(self.parse_big_number(next_word))
                        copy_text[count + 1] = ''

                    elif '%' in next_word or 'percent' in next_word.lower():
                        copy_text[count] = str(word) + '%'
                        copy_text[count + 1] = ''

                    elif next_word[0].isnumeric() and '/' in next_word:
                        try:  # check if its only number
                            next_num = float(next_word)
                        except ValueError:
                            count += 1
                            continue
                        copy_text[count] = str(num + next_num)
                        copy_text[count + 1] = ''

            elif word == "Thousand" or word == "Million" or word == "Billion" or word == "million" or word == "billion" or word == "thousand":
                copy_text[count] = self.parse_big_number(word)

            # elif word in self.countries_codes["Code"]:
            #   index = self.countries_codes["Code"].index(word)
            #  copy_text[count] = self.countries_codes["Name"][index].upper()

            elif word.isalpha() and '@' not in word and '#' not in word and '/' not in word:
                if re.search(r'(.)\1\1', word) is not None:  # cleaning terms with same 3 letters in a row
                    copy_text[count] = ''

                elif word.lower() == 'rt':
                    copy_text[count] = ''

                elif word.islower():
                    if word not in self.word_set.keys():
                        self.word_set[word] = None

                elif word[0].isupper():
                    if word.lower() in self.word_set.keys():
                        copy_text[count] = word.lower()
                    #else:
                        #self.add_word_to_future_change(doc_idx, word)
            count += 1
        hashtags.extend(urls)
        copy_text.extend(hashtags)
        final_list = [w for w in copy_text if w != '']
        return final_list

    def check_numeric(self, text):
        for charcter in text:
            if charcter.isdigit():
                return True
        return False

    def enter_to_entity_dict(self, term):
        if term in self.suspucious_words_for_entites.keys():
            self.suspucious_words_for_entites[term] += 1
        else:
            self.suspucious_words_for_entites[term] = 1

    def parse_entites(self, text):
        lst = text.split()
        saw_big_letter = False
        tmp_entity = ""
        for idx, word in enumerate(lst):
            if word[0].isupper() and saw_big_letter == True:
                tmp_entity += " " + word
                if (idx == len(lst) - 1):
                    self.enter_to_entity_dict(tmp_entity)
            elif word[0].isupper() and saw_big_letter == False:
                saw_big_letter = True
                tmp_entity += word
            elif len(tmp_entity.split()) >= 2:
                self.enter_to_entity_dict(tmp_entity)
                tmp_entity = ""
                saw_big_letter = False
            else:
                tmp_entity = ""

    def parse_hashtag(self, text):
        tmp_word = ""
        word_list = [text.lower()]
        contains_dash = False
        letter_index = 0
        if ("_" in text):
            contains_dash = True
        text = text.replace("_", " ")
        contain_numeric = self.check_numeric(text)

        text = text.replace("#", "")
        if text.isupper() == True:  # in case all capital
            new_text = text.replace("#", "")
            word_list.append(new_text.lower())
            return ' '.join(word_list)
        elif contain_numeric == False and contains_dash == True:  # not numeric and no dashes
            list = text.split()
            word_list = word_list + list
        else:
            # else if all word connected and start with capital letter (besides the first one)

            for i in range(len(text)):
                if text[i].isnumeric() == True:
                    word_list.append(tmp_word.lower())
                    letter_index = i
                    tmp_word = text[i]
                    break

                elif (text[i].isupper() and i != 0):
                    word_list.append(tmp_word.lower())
                    tmp_word = text[i]
                else:
                    tmp_word = tmp_word + text[i]

            for k in range(letter_index + 1, len(text)):
                if (text[k].isnumeric() == True):
                    tmp_word = tmp_word + text[k]
            word_list.append(tmp_word.lower())
        return word_list

    def parse_URL(self, url):
        tmp_word = ""
        word_list = [url]
        # or replace on all : / -  and then split and join
        url = url.replace("//", "/")
        for i in range(len(url)):
            if (url[i] == "/" or url[i] == "-" or url[i] == "_"):
                word_list.append(tmp_word)
                tmp_word = ""
            elif i != len(url) - 1:
                tmp_word = tmp_word + url[i]
            else:
                word_list.append(tmp_word)
        return word_list

    def parse_precentage(self, text):
        return text.replace("percentage", "%").replace("percent", "%").replace(" ", "")

    def parse_clean_number(self, text):
        millfullnames = ["Thousand", "Million", "Billion", "million", "billion", "thousand"]
        if text in millfullnames:
            return text

        millnames = ['', 'K', 'M', 'B']
        n = float(text)
        try:
            millidx = max(0, min(len(millnames) - 1,
                                 int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))))
        except:
            return str(n)

        mylist = '{:2.3f}{}'.format(n / 10 ** (3 * millidx), millnames[millidx])

        return mylist

    def parse_big_number(self, text):
        text = text.replace(",", "")

        return text.replace('Thousand', 'K').replace('Million', 'M').replace('Billion', 'B').replace('thousand',
                                                                                                     'K').replace(
            'billion', 'B').replace('million', 'M')