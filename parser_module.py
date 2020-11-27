import math
from urllib.parse import urlparse
import spacy
from nltk import pos_tag, RegexpParser
from nltk.corpus import stopwords
from nltk.data import path
from nltk.tokenize import word_tokenize
from document import Document
import re
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer

class Parse:

    def __init__(self):
        self.stop_words = stopwords.words('english') + ['?', '!', ',', '+', '-', '*', '/', '"', '.', '<', '>', '=', ':',
                                                        '']
        #self.nlp = spacy.load("en_core_web_sm")
        self.global_dict = {}  # key="word",value=number of docs
        self.post_dict = {}  # key="word",value=[parquet name,index in parquet,tweet id,frequency in tweet,location in tweet,tf]
        self.garbage = []
        self.id = []
        self.entities = {}



    def parse_doc(self, doc_as_list,idx=0,path=''):
        """
        This function takes a tweet document as list and break it into different fields
        :param doc_as_list: list re-preseting the tweet.
        :return: Document object with corresponding fields.
        """
        local_dict={}  # key="word",value=[parquet name,index in parquet,tweet id,frequency in tweet,location in tweet]
        tweet_id = doc_as_list[0]
        tweet_date = doc_as_list[1]
        full_text = doc_as_list[2]
        url = doc_as_list[3]
        retweet_text = doc_as_list[4]
        retweet_url = doc_as_list[5]
        quote_text = doc_as_list[6]
        quote_url = doc_as_list[7]
        term_dict = {}
        #retweet_url = self.parse_url(retweet_url)
        url = self.parse_url(url)
        #quote_url = self.parse_url(quote_url)
        tokenized_text=self.tokenized_parse(full_text)
        doc_length = len(tokenized_text)  # after text operations.

        for i in range(doc_length):
            self.update_global_dict(tokenized_text[i], idx, path)

            if (str.isalpha(tokenized_text[i]) or tokenized_text[i].startswith('#') or tokenized_text[i].startswith('@')):
                term_dict = self.update_doc_dict(term_dict, tokenized_text[i].lower())
                if tokenized_text[i] not in local_dict:
                    local_dict[tokenized_text[i]]=[1,[i]]
                else:
                    local_dict[tokenized_text[i]][0]+=1
                    local_dict[tokenized_text[i]][1].append(i)

            #else:
                #g.append(tokenized_text[i])
        self.update_post_dict(path,idx,tweet_id,local_dict,term_dict)
        a = 5
        #document = Document(tweet_id, tweet_date, full_text, url, retweet_text, retweet_url, quote_text,
         #                   quote_url, term_dict, doc_length)
        #return document

    def parse_sentence(self, text):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """

        text_tokens = word_tokenize(text)
        text_tokens_without_stopwords = [w for w in text_tokens if w.lower() not in self.stop_words]
        text_tokens_without_stopwords_ = [self.extand_contractions(w.lower()) for w in text_tokens if w.lower() not in self.stop_words]
        for text in text_tokens_without_stopwords: text = self.extand_contractions(text)
        return text_tokens_without_stopwords

    def extand_contractions(self, word):
        '''
         function extand contraction and Common Acronyms in Twitter
        :param word:
        :return:
        '''
        contractions = {
            "ain't": "am not / are not",
            "aren't": "are not / am not",
            "can't": "cannot",
            "can't've": "cannot have",
            "'cause": "because",
            "could've": "could have",
            "couldn't": "could not",
            "couldn't've": "could not have",
            "didn't": "did not",
            "doesn't": "does not",
            "don't": "do not",
            "hadn't": "had not",
            "hadn't've": "had not have",
            "hasn't": "has not",
            "haven't": "have not",
            "he'd": "he had / he would",
            "he'd've": "he would have",
            "he'll": "he shall / he will",
            "he'll've": "he shall have / he will have",
            "he's": "he has / he is",
            "how'd": "how did",
            "how'd'y": "how do you",
            "how'll": "how will",
            "how's": "how has / how is",
            "i'd": "I had / I would",
            "i'd've": "I would have",
            "i'll": "I shall / I will",
            "i'll've": "I shall have / I will have",
            "i'm": "I am",
            "i've": "I have",
            "isn't": "is not",
            "it'd": "it had / it would",
            "it'd've": "it would have",
            "it'll": "it shall / it will",
            "it'll've": "it shall have / it will have",
            "it's": "it has / it is",
            "let's": "let us",
            "ma'am": "madam",
            "mayn't": "may not",
            "might've": "might have",
            "mightn't": "might not",
            "mightn't've": "might not have",
            "must've": "must have",
            "mustn't": "must not",
            "mustn't've": "must not have",
            "needn't": "need not",
            "needn't've": "need not have",
            "o'clock": "of the clock",
            "oughtn't": "ought not",
            "oughtn't've": "ought not have",
            "shan't": "shall not",
            "sha'n't": "shall not",
            "shan't've": "shall not have",
            "she'd": "she had / she would",
            "she'd've": "she would have",
            "she'll": "she shall / she will",
            "she'll've": "she shall have / she will have",
            "she's": "she has / she is",
            "should've": "should have",
            "shouldn't": "should not",
            "shouldn't've": "should not have",
            "so've": "so have",
            "so's": "so as / so is",
            "that'd": "that would / that had",
            "that'd've": "that would have",
            "that's": "that has / that is",
            "there'd": "there had / there would",
            "there'd've": "there would have",
            "there's": "there has / there is",
            "they'd": "they had / they would",
            "they'd've": "they would have",
            "they'll": "they shall / they will",
            "they'll've": "they shall have / they will have",
            "they're": "they are",
            "they've": "they have",
            "to've": "to have",
            "wasn't": "was not",
            "we'd": "we had / we would",
            "we'd've": "we would have",
            "we'll": "we will",
            "we'll've": "we will have",
            "we're": "we are",
            "we've": "we have",
            "weren't": "were not",
            "what'll": "what shall / what will",
            "what'll've": "what shall have / what will have",
            "what're": "what are",
            "what's": "what has / what is",
            "what've": "what have",
            "when's": "when has / when is",
            "when've": "when have",
            "where'd": "where did",
            "where's": "where has / where is",
            "where've": "where have",
            "who'll": "who shall / who will",
            "who'll've": "who shall have / who will have",
            "who's": "who has / who is",
            "who've": "who have",
            "why's": "why has / why is",
            "why've": "why have",
            "will've": "will have",
            "won't": "will not",
            "won't've": "will not have",
            "would've": "would have",
            "wouldn't": "would not",
            "wouldn't've": "would not have",
            "y'all": "you all",
            "y'all'd": "you all would",
            "y'all'd've": "you all would have",
            "y'all're": "you all are",
            "y'all've": "you all have",
            "you'd": "you had / you would",
            "you'd've": "you would have",
            "you'll": "you shall / you will",
            "you'll've": "you shall have / you will have",
            "you're": "you are",
            "you've": "you have",
            "AFK": "Away From Keyboard",
            "BBIAB": "Be Back In A Bit",
            "BBL": "Be Back Later",
            "BBS ": "Be Back Soon",
            "BEG": "Big Evil Grin",
            "BRB": "Be Right Back",
            "BTW": "By The Way",
            "EG": "Evil Grin",
            "FISH": "First In, Still Here",
            "IDK": "I Don't Know",
            "IMO": "In My Opinion",
            "IRL": "In Real Life",
            "KISS": "Keep It Simple,Stupid",
            "LMK": "Let Me Know",
            "LOL": "Laughing Out Loud",
            "NYOB": " None of Your Business",
            "OFC ": "Of Course",
            "OMG ": "Oh My God",
            "PANS": "Pretty Awesome New Stuff",
            "PHAT": "Pretty, Hot, And Tempting",
            "POS ": "Parents Over Shoulder",
            "ROFL": "Rolling On the Floor Laughing",
            "SMH ": "Shaking My Head",
            "TTYL": "Talk To You Later",
            "YOLO": "You Only Live Once",
            "WTH ": "What The Heck",
        }
        if (word in contractions):
            return contractions[word]
        return word

    def find_entities(self, text):

        '''
        this function find entities and add them to the dictionary
        :param text: the twit text
        :param term_dict: the words dictionary of document
        :return:
        '''
        doc = self.nlp(text)
        for ent in doc.ents:
            entity = str(ent)
            if entity.isnumeric() == False:
                if entity not in self.entities:
                    self.entities[entity] = 1
                else:
                    self.entities[entity] += 1
            splitted_ent = re.split(', |_|-|!| ', entity)
            if(len(splitted_ent)>1):
                for term in splitted_ent:
                    if term.isnumeric() == False:
                        if term in self.entities:
                            self.entities[term]+=1
                        else:
                            self.entities[term]=1

    def deEmojify(self, text):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002500-\U00002BEF"  # chinese char
                                   u"\U00002702-\U000027B0"
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   u"\U0001f926-\U0001f937"
                                   u"\U00010000-\U0010ffff"
                                   u"\u2640-\u2642"
                                   u"\u2600-\u2B55"
                                   u"\u200d"
                                   u"\u23cf"
                                   u"\u23e9"
                                   u"\u231a"
                                   u"\ufe0f"  # dingbats
                                   u"\u3030"
                                   "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)

    def parse_url(self, url_string):
        """
        This function takes a  url_string from document and break it into to list of word :
        https://www.instagram.com/p/CD7fAPWs3WM/?igshid=o9kf0ugp1l8x ->[https, www, instagram.com, p, CD7fAPWs3WM, igshid, o9kf0ugp1l8x ]
        :param tag: Hashtag word from tweet.
        :return: list include spread world from the url .
        """
      #  if (url_string is None or url_string is ''):
      #      return
      #  lst = []
      #  o = urlparse(url_string)
      #  scheme = o.scheme
      #  lst.append(scheme)
      #  netloc = re.split(', |_|-|!', o.netloc)[0]
      #  if ("www." in netloc):
      #      netloc1 = netloc[0:3]
      #      netloc2 = netloc[4:]
      #      lst.append(netloc1)
      #      lst.append(netloc2)
      #  else:
      #      lst.append(netloc)
      #  path = re.split(', |_|-|!|/', o.path)
      #  for i in range(len(path)):
      #      if (path[i] != ''):
      #          lst.append(path[i])
#
      #  query = re.split(', |_|-|!|=', o.query)
      #  for j in range(len(query)):
      #      if (query[j] != ''):
      #          lst.append(query[j])
#
      #  return ' '.join(map(str, lst))
        tmp_word = ""
        word_list = [url_string]
        # or replace on all : / -  and then split and join
        url = url_string.replace("//", "/")
        for i in range(len(url)):
            if (url[i] == "/" or url[i] == "-" or url[i] == "_"):
                word_list.append(tmp_word)
                tmp_word = ""
            elif i != len(url) - 1:
                tmp_word = tmp_word + url[i]
            else:
                word_list.append(tmp_word)
        return ' '.join(word_list)

    def truncate(self,number, digits) -> float:
        stepper = 10.0 ** digits
        return math.trunc(stepper * number) / stepper

    def fix_number(self,toc_text):
        # sentence = re.split(', |_|-|!|/| ', sentence)
        for i in range(len(toc_text)):
            num = toc_text[i]
            num = num.replace(',', '')
            if(num.isnumeric()):
                flag = False
                for digit in range(len(num)):
                    if (num[digit].isdigit() == False and num[digit] != '.'):
                        flag = True
                if (flag):
                    continue
                try:
                    num = float(num)
                except:
                    continue
                flag1 = False
                if (1000 <= num < 1000000):
                    flag1 = True
                    num = num / 1000
                    num = str(self.truncate(num, 3)) + "K"

                elif (1000000 <= num < 1000000000):
                    flag1 = True
                    num = num / 1000000
                    num = str(self.truncate(num, 3)) + "M"
                elif (num > 1000000000):
                    flag1 = True
                    num = num / 1000000000
                    num = str(self.truncate(num, 3)) + "B"
                num = str(num)
                if (flag1 == False):
                    if (num[-1] == "0"):
                        num = num[0:-1]
                        if (num[-1] == "."):
                            num = num[0:-1]
                if (flag):
                    if (num[-2] == "0"):
                        num = num[0:-2] + num[-1:]
                        if (num[-1] == "."):
                            num = num[0:-2] + num[-1:]

                toc_text[i] = num

                if (i + 1 == len(toc_text)):
                    break
                else:
                    if (toc_text[i + 1] == "Thousand" or toc_text[i + 1] == "thousand"):
                        toc_text[i] = str(toc_text[i]) + "K"
                        toc_text[i + 1] = ""
                    elif (toc_text[i + 1] == "Million" or toc_text[i + 1] == "million"):
                        toc_text[i] = str(toc_text[i]) + "M"
                        toc_text[i + 1] = ""
                    elif (toc_text[i + 1] == "Billion" or toc_text[i + 1] == "billion"):
                        toc_text[i] = str(toc_text[i]) + "B"
                        toc_text[i + 1] = ""
        return toc_text

    def update_doc_dict(self, term_dict, word):
        #try:
        if word not in term_dict :
            term_dict[word] = 1
        else:
        #except:
            term_dict[word] += 1
        return term_dict

    def update_global_dict(self, word, idx, path):
        if word not in self.global_dict:
        #try:
            self.global_dict[word] = [1, [(path,idx)]]
        #except:
        else:
            self.global_dict[word][0] += 1
            self.global_dict[word][1].append((path, idx))

    def Hashtags_parse(self, toc_text):
        """
        This function takes a  Hashtag world from document and break it into to list of word
        :param tag: Hashtag word from tweet.
        :return: list include spread world and #tag .
        """

        copy_toc_text=[]
        for term in toc_text:
            copy_toc_text.append(term)
        count = 0
        parseList = ''
        i=0
        for term in toc_text:
            count += 1
            tag = term
            flag = True
            if (len(tag) <= 0 or tag[0] != '#'):
                continue
            parseList = tag[1:]
            parseList = str.replace(parseList, '_', '')
            #parseList = re.sub(r"([A-Z])", r" \1", parseList)
            #parseList=self.sub_by_upper(parseList)
            #secparseList = parseList.replace(' ', '')
            split_tag = self.sub_by_upper(parseList) + ['#' + parseList.lower()]
            if('' in split_tag):
                split_tag.remove('')
                count-=1

            i=count+i
            for word in split_tag:
                copy_toc_text.insert(i,word)
                i+=1
                if(i-count==len(split_tag)):
                    copy_toc_text.remove(term)
            i=i-count
               # term_dict = self.update_doc_dict(term_dict, word)
              # if (flag):
              #     flag = False
              #     self.upper_lower_global_dict(word)
        return copy_toc_text

    def percent_parse(self, toc_text):
        """
        This function change the representation of Number%,Number percent,Number percentage to Number%
        :param s:  word from tweet.
        :return:string in Format  Number% .
        """
        percent_op = [' percentage', ' PERCENTAGE', ' PERCENT', ' percent']
        for i in range(0, len(toc_text)):
            if (str.isnumeric(toc_text[i]) and i + 1 < len(toc_text) and toc_text[i + 1] in percent_op):
                toc_text[i]=toc_text[i] + '%'
                toc_text[i+1]=""
                #term_dict = self.update_doc_dict(term_dict, toc_text[i] + '%')
                #self.upper_lower_global_dict(toc_text[i] + '%')
        return toc_text

    def currency_parse(self, sentence, term_dict):
        """
              This function converting string currency to multiple ways to show it
              :param sentence:  thw sentece we look up for currency show
              :return:same sentence with extends, $-->$,usd,us dollar .
              """
        curr_lst = []
        currency_dict = {
            'ALL': 'Albania Lek',
            'AFN': 'Afghanistan Afghani',
            'ARS': 'Argentina Peso',
            'AWG': 'Aruba Guilder',
            'AUD': 'Australia Dollar',
            'AZN': 'Azerbaijan New Manat',
            'BSD': 'Bahamas Dollar',
            'BBD': 'Barbados Dollar',
            'BDT': 'Bangladeshi taka',
            'BYR': 'Belarus Ruble',
            'BZD': 'Belize Dollar',
            'BMD': 'Bermuda Dollar',
            'BOB': 'Bolivia Boliviano',
            'BAM': 'Bosnia and Herzegovina Convertible Marka',
            'BWP': 'Botswana Pula',
            'BGN': 'Bulgaria Lev',
            'BRL': 'Brazil Real',
            'BND': 'Brunei Darussalam Dollar',
            'KHR': 'Cambodia Riel',
            'CAD': 'Canada Dollar',
            'KYD': 'Cayman Islands Dollar',
            'CLP': 'Chile Peso',
            'CNY': 'China Yuan Renminbi',
            'COP': 'Colombia Peso',
            'CRC': 'Costa Rica Colon',
            'HRK': 'Croatia Kuna',
            'CU': 'Cuba Peso',
            'CZK': 'Czech Republic Koruna',
            'DKK': 'Denmark Krone',
            'DOP': 'Dominican Republic Peso',
            'XCD': 'East Caribbean Dollar',
            'EGP': 'Egypt Pound',
            'SVC': 'El Salvador Colon',
            'EEK': 'Estonia Kroon',
            'EUR': 'Euro Member Countries',
            'FKP': 'Falkland Islands (Malvinas) Pound',
            'FJD': 'Fiji Dollar',
            'GHC': 'Ghana Cedis',
            'GIP': 'Gibraltar Pound',
            'GTQ': 'Guatemala Quetzal',
            'GGP': 'Guernsey Pound',
            'GYD': 'Guyana Dollar',
            'HNL': 'Honduras Lempira',
            'HKD': 'Hong Kong Dollar',
            'HUF': 'Hungary Forint',
            'ISK': 'Iceland Krona',
            'INR': 'India Rupee',
            'IDR': 'Indonesia Rupiah',
            'IRR': 'Iran Rial',
            'IMP': 'Isle of Man Pound',
            'ILS': 'Israel Shekel',
            'JMD': 'Jamaica Dollar',
            'JPY': 'Japan Yen',
            'JEP': 'Jersey Pound',
            'KZT': 'Kazakhstan Tenge',
            'KPW': 'Korea (North) Won',
            'KRW': 'Korea (South) Won',
            'KGS': 'Kyrgyzstan Som',
            'LAK': 'Laos Kip',
            'LVL': 'Latvia Lat',
            'LBP': 'Lebanon Pound',
            'LRD': 'Liberia Dollar',
            'LTL': 'Lithuania Litas',
            'MKD': 'Macedonia Denar',
            'MYR': 'Malaysia Ringgit',
            'MUR': 'Mauritius Rupee',
            'MXN': 'Mexico Peso',
            'MNT': 'Mongolia Tughrik',
            'MZN': 'Mozambique Metical',
            'NAD': 'Namibia Dollar',
            'NPR': 'Nepal Rupee',
            'ANG': 'Netherlands Antilles Guilder',
            'NZD': 'New Zealand Dollar',
            'NIO': 'Nicaragua Cordoba',
            'NGN': 'Nigeria Naira',
            'NOK': 'Norway Krone',
            'OMR': 'Oman Rial',
            'PKR': 'Pakistan Rupee',
            'PAB': 'Panama Balboa',
            'PYG': 'Paraguay Guarani',
            'PEN': 'Peru Nuevo Sol',
            'PHP': 'Philippines Peso',
            'PLN': 'Poland Zloty',
            'QAR': 'Qatar Riyal',
            'RON': 'Romania New Leu',
            'RUB': 'Russia Ruble',
            'SHP': 'Saint Helena Pound',
            'SAR': 'Saudi Arabia Riyal',
            'RSD': 'Serbia Dinar',
            'SCR': 'Seychelles Rupee',
            'SGD': 'Singapore Dollar',
            'SBD': 'Solomon Islands Dollar',
            'SOS': 'Somalia Shilling',
            'ZAR': 'South Africa Rand',
            'LKR': 'Sri Lanka Rupee',
            'SEK': 'Sweden Krona',
            'CHF': 'Switzerland Franc',
            'SRD': 'Suriname Dollar',
            'SYP': 'Syria Pound',
            'TWD': 'Taiwan New Dollar',
            'THB': 'Thailand Baht',
            'TTD': 'Trinidad and Tobago Dollar',
            'TRY': 'Turkey Lira',
            'TRL': 'Turkey Lira',
            'TVD': 'Tuvalu Dollar',
            'UAH': 'Ukraine Hryvna',
            'GBP': 'United Kingdom Pound',
            'USD': 'United States Dollar',
            'UYU': 'Uruguay Peso',
            'UZS': 'Uzbekistan Som',
            'VEF': 'Venezuela Bolivar',
            'VND': 'Viet Nam Dong',
            'YER': 'Yemen Rial',
            'ZWD': 'Zimbabwe Dollar'}
        sentence = word_tokenize(sentence)
        for i in range(len(sentence)):
            if (sentence[i] in currency_dict):
                cur = sentence[i]
                term_dict = self.update_doc_dict(term_dict, cur)
                term_dict = self.update_doc_dict(term_dict, currency_dict[cur])
                curr_lst.append(cur, currency_dict[cur])
                self.upper_lower_global_dict(cur)
                self.upper_lower_global_dict(currency_dict[cur])
            elif (sentence[i] in currency_dict.values()):
                cur = sentence[i]
                term_dict = self.update_doc_dict(term_dict, cur)
                term_dict = self.update_doc_dict(term_dict, currency_dict[cur])
                curr_lst.append(cur, currency_dict[cur])
                self.upper_lower_global_dict(cur)
                self.upper_lower_global_dict(currency_dict[cur])
        for word in curr_lst:
            self.upper_lower_global_dict(word)

    def stemmer(self, sentence):
        porter = PorterStemmer()
        lancaster = LancasterStemmer()

        print("Porter Stemmer")
        print(porter.stem("cats"))
        print(porter.stem("trouble"))
        print(porter.stem("troubling"))
        print(porter.stem("troubled"))
        print("Lancaster Stemmer")
        print(lancaster.stem("cats"))
        print(lancaster.stem("trouble"))
        print(lancaster.stem("troubling"))
        print(lancaster.stem("troubled"))

    def update_post_dict(self, path, idx, tweet_id, local_dict,term_dict):
        for term in local_dict:
            if (term in self.global_dict):
                tf = local_dict[term][0] / max(term_dict.values())
                if term not in self.post_dict:
                    self.post_dict[term] = [[tweet_id, local_dict[term][0], local_dict[term][1], tf,len(term_dict)]]
                else:
                    self.post_dict[term].append([tweet_id, local_dict[term][0], local_dict[term][1], tf,len(term_dict)])

    def get_global_dict(self):
        dict = self.global_dict
        self.global_dict={}
        return dict

    def get_posting_dict(self):
        dict =self.post_dict
        self.post_dict={}
        return dict

    def sub_by_upper(self,text):
        parseList=[]
        tmp=[]
        word=""
        for i in range(len(text)):
            if text[i].isupper():
              tmp.append(i)
        for i in range(len(tmp)-1):
            word=text[tmp[i]:tmp[i+1]]
            parseList.append(word.lower())
        if(len(tmp)>0):
            text=text[tmp[-1]:]
            parseList.append(text.lower())
        return parseList





    def tokenized_parse(self, full_text):
        full_text = self.deEmojify(full_text)
        tokenized_text1 = full_text.split(' ')

        tokenized_text = []
        for i in tokenized_text1:
            if "RT" in i:
                i = i.replace("RT", '')
            if "\n\n" in i:
                i = i.replace("\n\n", '')
            if "\n" in i:
                i = i.replace("\n", '')
            if '.' in i:
                i = i.replace(".", '')
            if ',' in i:
                i = i.replace(",", '')

            if i.lower() not in self.stop_words:
                tokenized_text.append(i)

        if ('' in tokenized_text):
            tokenized_text.remove('')
        if (' ' in tokenized_text):
            tokenized_text.remove(' ')

        # save #tag
        tokenized_text = self.Hashtags_parse(tokenized_text)
        # save word begin in @
        # save numbers end with M K B
        tokenized_text = self.fix_number(tokenized_text)
        # save num%
        tokenized_text = self.percent_parse(tokenized_text)
        # save entity
        # self.find_entities(full_text)
        return tokenized_text


