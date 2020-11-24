import time
from datetime import datetime
import pandas as pd
import json
import collections


class Indexer:

    def __init__(self, config, word_dict):
        #new_dictonaries
        ############################################
        self.posting_hashtag_dict={}
        self.posting_tag_dict={}
        self.posting_dict_a_to_c={}
        self.posting_dict_d_to_h = {}
        self.posting_dict_i_to_o = {}
        self.posting_dict_p_to_r = {}
        self.posting_dict_s_to_z = {}
        ############################################
        self.inverted_idx = {}
        self.postingDict = {}
        self.config = config
        self.word_dict = word_dict
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
        # Go over each term in the doc
        for term in document_dictionary.keys():
            try:
                unique_terms_in_doc = self.count_unique(document.document_dictionary)
                if not term.isalpha():
                    continue
                # freq of term in all corpus until now
                term = term.lower()
                freq_in_doc = document_dictionary[term]

                if term in self.inverted_idx.keys():
                    number_of_docs = self.inverted_idx[term][0] + 1
                    freq_in_corpus = self.inverted_idx[term][1] + freq_in_doc
                    docs_list = self.inverted_idx[term][2]
                else:
                    number_of_docs = 1
                    freq_in_corpus = freq_in_doc
                    docs_list = []

                docs_list.append((doc_idx, freq_in_doc))

                self.inverted_idx[term] = (number_of_docs, freq_in_corpus, self.differnce_method(docs_list))

                #send curruent doucment to it's proper posting file

                self.term_to_posting_dict(term, doc_idx, document, number_of_docs, unique_terms_in_doc)
                #self.postingDict[self.curr] = [term_index, doc_idx, document_dictionary[term], self.index_term_in_text(term, document.full_text), document.doc_length, self.count_unique(document_dictionary)]
            except:
                print('problem with the following key {}'.format(term))

            self.curr += 1

            if self.curr==1000000:
                #sort the dictionaries, update them and write them to json file
                self.update_posting_file()
                self.curr = 0
                self.postingDict.clear()

    def term_to_posting_dict(self, term, doc_idx, document, number_of_docs, count_unique):
        key = term.lower() + str(number_of_docs)
        freq_in_doc = document.document_dictionary[term]
        idx_list_in_doc = self.index_term_in_text(term, document.full_text)

        if 'a' <= term[0] <= 'd':
            self.posting_dict_a_to_d[key] = [doc_idx, freq_in_doc,
            idx_list_in_doc, document.doc_length, count_unique]

        if 'e' <= term[0] <= 'h':
            self.posting_dict_a_to_d[key] = [doc_idx, freq_in_doc,
            idx_list_in_doc, document.doc_length, count_unique]

        if 'i' <= term[0] <= 'p':
            self.posting_dict_a_to_d[key] = [doc_idx, freq_in_doc,
            idx_list_in_doc, document.doc_length, count_unique]

        if 'q' <= term[0] <= 'z':
            self.posting_dict_a_to_d[key] = [doc_idx, freq_in_doc,
            idx_list_in_doc, document.doc_length, count_unique]

    # list of tuples(doc_num, number of apperances in doc)
    def differnce_method(self, list):
        for i in range(1, len(list)):
                new_value = list[i][0] - list[i - 1][0]
                tmp_tuple = (new_value, list[i][1])
                list[i] = tmp_tuple
        return list

    def index_term_in_text(self, term, text):
        indexes = []
        count = 0
        spllited_text = text.split()
        for word in spllited_text:
            if word == term:
                indexes.append(count)
            count += 1
        return indexes

    def count_unique(self, document_dictionary):
        count = 0
        for term in document_dictionary:
            if document_dictionary[term] == 1:
                count += 1
        return count


    def sort_dictionarys(self,dictionary):
        return {k: dictionary[k] for k in sorted(dictionary)}
        #dictionary1= collections.OrderedDict(sorted(dictionary1.items()))




    def update_posting_file(self):
        #'term_index' , 'doc#', 'freq', 'location_list', 'n', 'unique num of words'
        print("updating posting file")
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
        self.posting_tag_dict=self.sort_dictionarys(self.posting_tag_dict)


        # opening json file, should open all files
        print("loading json")
        #*************************
        #new method
        #*************************

        try:
            with open("posting_file.json") as posting_file:
                data =json.load(posting_file)
        except:
            print("loading did not go well")



        try:
            df = pd.read_json("posting_file.json", lines=True)
            df.columns = ['1', '2', '3', '4', '5', '6']
        except:
            df = pd.DataFrame(self.postingDict.values(), columns=['1', '2', '3', '4', '5', '6'])
            df.to_json("posting_file.json", orient='records', lines=True)
            return
        df2 = pd.DataFrame(self.postingDict.values(), columns=['1', '2', '3', '4', '5', '6'])
        df3 = pd.concat([df, df2]).sort_values(by=['1', '2'], ascending=True)
        #for term in self.updated_terms:
            #index_in_posting_file = self.inverted_idx[term][2]+self.inverted_idx[term][0]-1
            #line = pd.DataFrame([self.postingDict[self.updated_terms[term]]], columns=['1', '2', '3', 'l4', '5', '6', '7'])
            #print("concat:")
            #print(datetime.now())
            #df = pd.concat([df.iloc[:index_in_posting_file], line, df.iloc[index_in_posting_file:]]).reset_index(drop=True)
            #print(datetime.now())
        df3.to_json("posting_file.json", orient='records', lines=True)
        d2 = datetime.strptime(datetime.now().strftime(fmt), fmt)
        d2_ts = time.mktime(d2.timetuple())
        print(str(int(d2_ts-d1_ts)) + " seconds")
