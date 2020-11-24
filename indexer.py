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
        self.posting_tag_dict={}
        self.posting_dict_a_to_c = {}
        self.posting_dict_d_to_h = {}
        self.posting_dict_i_to_o = {}
        self.posting_dict_p_to_r = {}
        self.posting_dict_s_to_z = {}
        ############################################
        self.inverted_idx = {}
        self.postingDict = {}
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
        document_dictionary = document.term_doc_dictionary
        unique_terms_in_doc = self.count_unique(document_dictionary)
        # Go over each term in the doc
        for term in document_dictionary.keys():
            try:
                if not term.isalpha():
                    continue
                # freq of term in all corpus until now
                freq_in_doc = document_dictionary[term]

                if term in self.inverted_idx.keys():
                    number_of_docs = self.inverted_idx[term][0] + 1
                    freq_in_corpus = self.inverted_idx[term][1] + freq_in_doc
                    docs_list = self.inverted_idx[term][2]
                    last_doc_idx = self.inverted_idx[term][3]

                else:
                    number_of_docs = 1
                    freq_in_corpus = freq_in_doc
                    docs_list = []
                    last_doc_idx = doc_idx

                docs_list.append((doc_idx, freq_in_doc))

                self.inverted_idx[term] = (number_of_docs, freq_in_corpus, self.differnce_method(docs_list, last_doc_idx), doc_idx)

                #send curruent doucment to it's proper posting file

                self.term_to_posting_dict(term, doc_idx, freq_in_doc, document, number_of_docs, unique_terms_in_doc)
                #self.postingDict[self.curr] = [term_index, doc_idx, document_dictionary[term], self.index_term_in_text(term, document.full_text), document.doc_length, self.count_unique(document_dictionary)]
            except:
                print('problem with the following key {}'.format(term))
                traceback.print_exc()

            self.curr += 1

            if self.curr==1000000:
                #sort the dictionaries, update them and write them to json file
                self.update_posting_file()
                self.curr = 0
                self.postingDict.clear()

    def term_to_posting_dict(self, term, doc_idx, freq_in_doc, document, number_of_docs, count_unique):
        key = term + " " + str(doc_idx)
        idx_list_in_doc = self.index_term_in_text(term, document.full_text)

        if 'a' <= term[0] <= 'c':
            self.posting_dict_a_to_c[key] = [freq_in_doc, idx_list_in_doc, document.doc_length, count_unique]

        elif 'd' <= term[0] <= 'h':
            self.posting_dict_d_to_h[key] = [freq_in_doc, idx_list_in_doc, document.doc_length, count_unique]

        elif 'i' <= term[0] <= 'o':
            self.posting_dict_i_to_o[key] = [freq_in_doc, idx_list_in_doc, document.doc_length, count_unique]

        elif 'p' <= term[0] <= 'r':
            self.posting_dict_p_to_r[key] = [freq_in_doc, idx_list_in_doc, document.doc_length, count_unique]

        elif 's' <= term[0] <= 'z':
            self.posting_dict_s_to_z[key] = [freq_in_doc, idx_list_in_doc, document.doc_length, count_unique]

        elif term[0] == '#':
            self.posting_hashtag_dict[key] = [freq_in_doc, idx_list_in_doc, document.doc_length, count_unique]

    # list of tuples(doc_num, number of apperances in doc)
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
        self.inverted_idx={k: self.inverted_idx[k] for k in sorted(self.inverted_idx)}

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

        #try:
         #   df = pd.read_json("posting_file.json", lines=True)
          #  df.columns = ['1', '2', '3', '4', '5', '6']
        #except:
         #   df = pd.DataFrame(self.postingDict.values(), columns=['1', '2', '3', '4', '5', '6'])
          #  df.to_json("posting_file.json", orient='records', lines=True)
           # return
        #df2 = pd.DataFrame(self.postingDict.values(), columns=['1', '2', '3', '4', '5', '6'])
        #df3 = pd.concat([df, df2]).sort_values(by=['1', '2'], ascending=True)
        #for term in self.updated_terms:
            #index_in_posting_file = self.inverted_idx[term][2]+self.inverted_idx[term][0]-1
            #line = pd.DataFrame([self.postingDict[self.updated_terms[term]]], columns=['1', '2', '3', 'l4', '5', '6', '7'])
            #print("concat:")
            #print(datetime.now())
            #df = pd.concat([df.iloc[:index_in_posting_file], line, df.iloc[index_in_posting_file:]]).reset_index(drop=True)
            #print(datetime.now())
        #df3.to_json("posting_file.json", orient='records', lines=True)
        d2 = datetime.strptime(datetime.now().strftime(fmt), fmt)
        d2_ts = time.mktime(d2.timetuple())
        print(str(int(d2_ts-d1_ts)) + " seconds")
