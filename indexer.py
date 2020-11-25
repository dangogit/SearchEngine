import time
import traceback
from datetime import datetime
import pandas as pd
import json
import collections


class Indexer:

    def __init__(self, config):
        #new_dictonaries
        ############################################
        self.posting_hashtag_dict={}
        self.posting_dict_a_to_c = {}
        self.posting_dict_d_to_h = {}
        self.posting_dict_i_to_o = {}
        self.posting_dict_p_to_r = {}
        self.posting_dict_s_to_z = {}
        ############################################
        self.inverted_idx_a_to_c = {}
        self.inverted_idx_d_to_h = {}
        self.inverted_idx_i_to_o = {}
        self.inverted_idx_p_to_r = {}
        self.inverted_idx_s_to_z = {}
        self.inverted_idx_hashtag={}


        self.config = config
        self.key = 0
        self.curr = 0
        self.term_index = 0
        self.updated_terms = {}

    def add_new_doc(self, document, doc_idx):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """
        document_dictionary = document[4]
        unique_terms_in_doc = self.count_unique(document_dictionary)
        # Go over each term in the doc
        for term in document_dictionary.keys():
            try:
                if not term.isalpha():
                    continue
                # freq of term in all corpus until now
                freq_in_doc = document_dictionary[term]
                #self.inverted_idx[term] = (number_of_docs, freq_in_corpus, self.differnce_method(docs_list, last_doc_idx), doc_idx)
                #send curruent doucment to it's proper posting file
                #self.term_to_posting_dict_and_inv_idx(term, doc_idx, freq_in_doc, document, number_of_docs, unique_terms_in_doc,freq_in_corpus,self.differnce_method(docs_list, last_doc_idx))
                #self.postingDict[self.curr] = [term_index, doc_idx, document_dictionary[term], self.index_term_in_text(term, document.full_text), document.doc_length, self.count_unique(document_dictionary)]
            except:
                print('problem with the following key {}'.format(term))
                traceback.print_exc()

            self.curr += 1

            if self.curr==1000000:
                self.update_posting_file() #this function updates and sorts the dictionries
                #self.update_inverted_idx_files(document_dictionary,doc_idx)
                self.curr = 0


    def differnce_method(self, list, last_doc_index):
        i = len(list) -1
        if i != 0:
            new_value = list[i][0] - last_doc_index
            list[i] = (new_value, list[i][1])
        return list

    def index_term_in_text(self, term, text):
        indexes = []
        count = 0
        spllited_text = text.split()
        for word in spllited_text:
            if word.lower() == term:
                indexes.append(count)
            count += 1
        return indexes

    def count_unique(self, document_dictionary):
        count = 0
        for term in document_dictionary:
            if document_dictionary[term] == 1:
                count += 1
        return count


    def sort_dictionarys(self, dictionary):
        return {k: dictionary[k] for k in sorted(dictionary, key=self.create_tuple_from_string)}
        #dictionary1= collections.OrderedDict(sorted(dictionary1.items()))

    #sorted(dict, key=lambda element: (element[0], element[1]))
    def create_tuple_from_string(self, string):
        res = tuple(map(str, string.split(' ')))
        new_value = int(res[1])
        new_tuple = (res[0], new_value)
        return new_tuple


    def update_posting_file(self):
        #'term_index' , 'doc#', 'freq', 'location_list', 'n', 'unique num of words'
        print("updating posting files:")
        fmt = '%Y-%m-%d %H:%M:%S'
        d1 = datetime.strptime(datetime.now().strftime(fmt), fmt)
        d1_ts = time.mktime(d1.timetuple())

        #sort all dictionaries here

        self.posting_dict_a_to_c=self.sort_dictionarys(self.posting_dict_a_to_c)
        self.posting_dict_d_to_h=self.sort_dictionarys(self.posting_dict_d_to_h)
        self.posting_dict_i_to_o=self.sort_dictionarys(self.posting_dict_i_to_o)
        self.posting_dict_p_to_r=self.sort_dictionarys(self.posting_dict_p_to_r)
        self.posting_dict_s_to_z=self.sort_dictionarys(self.posting_dict_s_to_z)
        self.posting_hashtag_dict=self.sort_dictionarys(self.posting_hashtag_dict)
        #self.inverted_idx={k: self.inverted_idx[k] for k in sorted(self.inverted_idx)}

        # a_to_c:
        # from json:
        try:
            with open("posting_file_a_to_c.json", 'r', encoding='utf-8') as posting_file:
                posting_dict_a_to_c_from_file = json.load(posting_file)
        except:
            posting_dict_a_to_c_from_file = {}

        posting_dict_a_to_c_to_file = {**posting_dict_a_to_c_from_file, **self.posting_dict_a_to_c}
        posting_dict_a_to_c_to_file = self.sort_dictionarys(posting_dict_a_to_c_to_file)
        # to json:
        try:
            with open("posting_file_a_to_c.json", 'w', encoding='utf-8') as posting_file:
                json.dump(posting_dict_a_to_c_to_file, posting_file)
                posting_dict_a_to_c_to_file.clear()
                posting_dict_a_to_c_from_file.clear()
                self.posting_dict_a_to_c.clear()
        except:
            traceback.print_exc()

        # d_to_h
        # from json:
        try:
            with open("posting_file_d_to_h.json", 'r', encoding='utf-8') as posting_file:
                posting_dict_d_to_h_from_file = json.load(posting_file)
        except:
            posting_dict_d_to_h_from_file = {}

        posting_dict_d_to_h_to_file = {**posting_dict_d_to_h_from_file, **self.posting_dict_d_to_h}
        posting_dict_d_to_h_to_file = self.sort_dictionarys(posting_dict_d_to_h_to_file)
        # to json:
        try:
            with open("posting_file_d_to_h.json", 'w', encoding='utf-8') as posting_file:
                json.dump(posting_dict_d_to_h_to_file, posting_file)
                posting_dict_d_to_h_to_file.clear()
                posting_dict_d_to_h_from_file.clear()
                self.posting_dict_d_to_h.clear()
        except:
            traceback.print_exc()

        # i_to_o:
        # from json:
        try:
            with open("posting_file_i_to_o.json", 'r', encoding='utf-8') as posting_file:
                posting_dict_i_to_o_from_file = json.load(posting_file)
        except:
            posting_dict_i_to_o_from_file = {}

        posting_dict_i_to_o_to_file = {**posting_dict_i_to_o_from_file, **self.posting_dict_i_to_o}
        posting_dict_i_to_o_to_file = self.sort_dictionarys(posting_dict_i_to_o_to_file)
        # to json:
        try:
            with open("posting_file_i_to_o.json", 'w', encoding='utf-8') as posting_file:
                json.dump(posting_dict_i_to_o_to_file, posting_file)
                posting_dict_i_to_o_to_file.clear()
                posting_dict_i_to_o_from_file.clear()
                self.posting_dict_i_to_o.clear()
        except:
            traceback.print_exc()

        #  p_to_r:
        # from json:
        try:
            with open("posting_file_p_to_r.json", 'r', encoding='utf-8') as posting_file:
                posting_dict_p_to_r_from_file = json.load(posting_file)
        except:
            posting_dict_p_to_r_from_file = {}

        posting_dict_p_to_r_to_file = {**posting_dict_p_to_r_from_file, **self.posting_dict_p_to_r}
        posting_dict_p_to_r_to_file = self.sort_dictionarys(posting_dict_p_to_r_to_file)
        # to json:
        try:
            with open("posting_file_p_to_r.json", 'w', encoding='utf-8') as posting_file:
                json.dump(posting_dict_p_to_r_to_file, posting_file)
                posting_dict_p_to_r_to_file.clear()
                posting_dict_p_to_r_from_file.clear()
                self.posting_dict_p_to_r.clear()
        except:
            traceback.print_exc()

        # s_to_z:
        # from json:
        try:
            with open("posting_file_s_to_z.json", 'r', encoding='utf-8') as posting_file:
                posting_dict_s_to_z_from_file = json.load(posting_file)
        except:
            posting_dict_s_to_z_from_file = {}

        posting_dict_s_to_z_to_file = {**posting_dict_s_to_z_from_file, **self.posting_dict_s_to_z}
        posting_dict_s_to_z_to_file = self.sort_dictionarys(posting_dict_s_to_z_to_file)
        # to json:
        try:
            with open("posting_file_s_to_z.json", 'w', encoding='utf-8') as posting_file:
                json.dump(posting_dict_s_to_z_to_file, posting_file)
                posting_dict_s_to_z_to_file.clear()
                posting_dict_s_to_z_from_file.clear()
                self.posting_dict_s_to_z.clear()
        except:
            traceback.print_exc()
        d2 = datetime.strptime(datetime.now().strftime(fmt), fmt)
        d2_ts = time.mktime(d2.timetuple())
        print(str(float(d2_ts-d1_ts)/60) + " minutes")




    def insert_term_to_inv_idx_and_post_dict(self,term,inv_idx_list,post_dict_list,freq_in_doc,doc_idx,unique_term_in_doc):
        index=0
        if 'a' <= term[0] <= 'c':
            index=0
        elif 'd' <= term[0] <= 'h':
            index=1
        elif 'i' <= term[0] <= 'o':
            index=2
        elif 'p' <= term[0] <= 'r':
            index=3
        elif 's' <= term[0] <= 'z':
            index=4
        elif term[0]=="#":
            index=5

        inv_idx=inv_idx_list[index]
        post_dict=post_dict_list[index]

        number_of_docs, freq_in_corpus, docs_list, last_doc_idx=self.extract_data_from_inv_idx(term,inv_idx,freq_in_doc,doc_idx)


        self.term_to_posting_dict_and_inv_idx(term,doc_idx,freq_in_doc,number_of_docs,unique_term_in_doc,freq_in_corpus,inv_idx,post_dict)



    def extract_data_from_inv_idx(self,term,inv_idx,freq_in_doc,doc_idx):
        if term in inv_idx.keys():
            number_of_docs = inv_idx[term][0] + 1
            freq_in_corpus = inv_idx[term][1] + freq_in_doc
            docs_list = inv_idx[term][2]
            last_doc_idx =inv_idx[term][3]
        else:
            number_of_docs = 1
            freq_in_corpus = freq_in_doc
            docs_list = []
            last_doc_idx = doc_idx

        docs_list.append((doc_idx, freq_in_doc))

        return number_of_docs,freq_in_corpus,docs_list,last_doc_idx

    def term_to_posting_dict_and_inv_idx(self,term,doc_idx,freq_in_doc,number_of_docs,
    unique_term_in_doc,freq_in_corpus,inv_idx,post_dict):
        inv_idx[term]=(number_of_docs,freq_in_corpus,post_dict_with_differnce_method,doc_idx)
        post_dict[term]=()



