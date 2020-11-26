import time
import traceback
from datetime import datetime
import pandas as pd
import json
import collections
import sys

class Indexer:

    def __init__(self, config):
        # new_dictonaries
        self.letters_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10,
                             'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20,
                             'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25, '#': 26}
        self.inverted_idx_dicts_list = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {},
                                        {}, {}, {}, {}, {}, {}, {}]
        self.inverted_idx_files_list = ["inverted_idx_a.json",
                                        "inverted_idx_b.json",
                                        "inverted_idx_c.json",
                                        "inverted_idx_d.json",
                                        "inverted_idx_e.json",
                                        "inverted_idx_f.json",
                                        "inverted_idx_g.json",
                                        "inverted_idx_h.json",
                                        "inverted_idx_i.json",
                                        "inverted_idx_j.json",
                                        "inverted_idx_k.json",
                                        "inverted_idx_l.json",
                                        "inverted_idx_m.json",
                                        "inverted_idx_n.json",
                                        "inverted_idx_o.json",
                                        "inverted_idx_p.json",
                                        "inverted_idx_q.json",
                                        "inverted_idx_r.json",
                                        "inverted_idx_s.json",
                                        "inverted_idx_t.json",
                                        "inverted_idx_u.json",
                                        "inverted_idx_v.json",
                                        "inverted_idx_w.json",
                                        "inverted_idx_x.json",
                                        "inverted_idx_y.json",
                                        "inverted_idx_z.json",
                                        "inverted_idx_hashtags.json"]
        self.posting_dicts_list = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {},
                                   {}, {}, {}, {}, {}, {}]
        self.posting_files_list = ["posting_file_a.json",
                                   "posting_file_b.json",
                                   "posting_file_c.json",
                                   "posting_file_d.json",
                                   "posting_file_e.json",
                                   "posting_file_f.json",
                                   "posting_file_g.json",
                                   "posting_file_h.json",
                                   "posting_file_i.json",
                                   "posting_file_j.json",
                                   "posting_file_k.json",
                                   "posting_file_l.json",
                                   "posting_file_m.json",
                                   "posting_file_n.json",
                                   "posting_file_o.json",
                                   "posting_file_p.json",
                                   "posting_file_q.json",
                                   "posting_file_r.json",
                                   "posting_file_s.json",
                                   "posting_file_t.json",
                                   "posting_file_u.json",
                                   "posting_file_v.json",
                                   "posting_file_w.json",
                                   "posting_file_x.json",
                                   "posting_file_y.json",
                                   "posting_file_z.json",
                                   "posting_file_hashtags.json"]
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

                self.insert_term_to_inv_idx_and_post_dict(term, freq_in_doc, doc_idx, unique_terms_in_doc, document)

            except:
                print('problem with the following key {}'.format(term))
                traceback.print_exc()

            self.curr += 1

            if self.curr == 1000000:
                #self.update_inverted_and_posting_file()  # this function updates and sorts the dictionries
                # self.update_inverted_idx_files(document_dictionary,doc_idx)
                self.curr = 0

    def insert_term_to_inv_idx_and_post_dict(self, term, freq_in_doc, doc_idx,
                                             unique_terms_in_doc, document):
        index = self.letters_dict[term[0]]
        inverted_idx = self.inverted_idx_dicts_list[index]
        posting_dict = self.posting_dicts_list[index]

        self.inverted_idx_dicts_list[index], self.posting_dicts_list[index] = self.update_inverted_idx_and_posting_dict(
            term, inverted_idx, posting_dict, freq_in_doc, doc_idx, document, unique_terms_in_doc)

        if sys.getsizeof(self.inverted_idx_dicts_list[index]) > 8000000:
            self.update_inverted_file(index)
        if sys.getsizeof(self.posting_dicts_list[index]) > 8000000:
            self.update_posting_file(index)

    def update_inverted_idx_and_posting_dict(self, term, inverted_idx, posting_dict, freq_in_doc, doc_idx, document,
                                             unique_terms_in_doc):
        if term in inverted_idx.keys():
            number_of_docs = inverted_idx[term][0] + 1
            freq_in_corpus = inverted_idx[term][1] + freq_in_doc
            docs_list = inverted_idx[term][2]
            last_doc_idx = inverted_idx[term][3]
        else:
            number_of_docs = 1
            freq_in_corpus = freq_in_doc
            docs_list = []
            last_doc_idx = doc_idx

        docs_list.append((doc_idx, freq_in_doc))

        inverted_idx[term] = (number_of_docs, freq_in_corpus, self.differnce_method(docs_list, last_doc_idx), doc_idx)
        key = term + " " + str(doc_idx)
        posting_dict[key] = [freq_in_doc, self.index_term_in_text(term, document[2]), document[5], unique_terms_in_doc]

        return inverted_idx, posting_dict

    # list of tuples(doc_num, number of apperances in doc)
    def differnce_method(self, list, last_doc_index):
        i = len(list) - 1
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

    def create_tuple_from_string(self, string):
        res = tuple(map(str, string.split(' ')))
        new_value = int(res[1])
        new_tuple = (res[0], new_value)
        return new_tuple

    def merge_inverted_idx_dicts(self, inverted_idx_from_file, inverted_idx_dict):
        for term in inverted_idx_dict.keys():
            if term in inverted_idx_from_file.keys():
                number_of_docs = inverted_idx_from_file[term][0] + inverted_idx_dict[term][0]
                freq_in_corpus = inverted_idx_from_file[term][1] + inverted_idx_dict[term][1]
                docs_list_from_file = inverted_idx_from_file[term][2]
                docs_list_from_local = inverted_idx_dict[term][2]
                last_doc_idx_from_file = inverted_idx_from_file[term][3]
                docs_list_from_file.append(docs_list_from_local[0])
                docs_list_from_file = self.differnce_method(docs_list_from_file, last_doc_idx_from_file)
                docs_list_from_file.append(docs_list_from_local[1:])
                last_doc_idx_from_local = inverted_idx_dict[term][3]

                inverted_idx_from_file[term] = (
                    number_of_docs, freq_in_corpus, docs_list_from_file, last_doc_idx_from_local)
            else:
                inverted_idx_from_file[term] = inverted_idx_dict[term]

        return inverted_idx_from_file

    def update_inverted_and_posting_file(self):
        # 'term_index' , 'doc#', 'freq', 'location_list', 'n', 'unique num of words'
        print("[" + str(datetime.now()) + "] " + "updating inverted files:")
        fmt = '%Y-%m-%d %H:%M:%S'
        d1 = datetime.strptime(datetime.now().strftime(fmt), fmt)
        d1_ts = time.mktime(d1.timetuple())

        # sort all dictionaries here
        # for i in range(len(self.inverted_idx_dicts_list)):
        #    self.inverted_idx_dicts_list[i] = {k: self.inverted_idx_dicts_list[i][k] for k in sorted(self.inverted_idx_dicts_list[i])}

        for i in range(len(self.inverted_idx_files_list)):
            try:
                with open("Inverted_files/" +self.inverted_idx_files_list[i], 'r', encoding='utf-8') as inverted_idx_file:
                    inverted_idx_from_file = json.load(inverted_idx_file)
            except:
                inverted_idx_from_file = {}

            inverted_idx_to_file = self.merge_inverted_idx_dicts(inverted_idx_from_file,
                                                                 self.inverted_idx_dicts_list[i])
            # to json:
            try:
                with open("Inverted_files/" +self.inverted_idx_files_list[i], 'w', encoding='utf-8') as inverted_idx_file:
                    json.dump(inverted_idx_to_file, inverted_idx_file)
                    inverted_idx_to_file.clear()
                    inverted_idx_from_file.clear()
                    self.inverted_idx_dicts_list[i].clear()
            except:
                traceback.print_exc()
        d2 = datetime.strptime(datetime.now().strftime(fmt), fmt)
        d2_ts = time.mktime(d2.timetuple())
        print(str(float(d2_ts - d1_ts) / 60) + " minutes")

        print("[" + str(datetime.now()) + "] " + "updating posting files:")
        d1 = datetime.strptime(datetime.now().strftime(fmt), fmt)
        d1_ts = time.mktime(d1.timetuple())

        # for i in range(len(self.posting_dicts_list)):
        #   self.posting_dicts_list[i] = self.sort_dictionarys(self.posting_dicts_list[i])

        for i in range(len(self.posting_files_list)):
            try:
                with open("Posting_files/" +self.posting_files_list[i], 'r', encoding='utf-8') as posting_file:
                    posting_dict_from_file = json.load(posting_file)
            except:
                posting_dict_from_file = {}

            posting_dict_to_file = {**posting_dict_from_file, **self.posting_dicts_list[i]}
            #  posting_dict_to_file = self.sort_dictionarys(posting_dict_to_file)
            # to json:
            try:

                with open("Posting_files/" +self.posting_files_list[i], 'w', encoding='utf-8') as posting_file:
                    json.dump(posting_dict_to_file, posting_file)
                    posting_dict_to_file.clear()
                    posting_dict_from_file.clear()
                    self.posting_dicts_list[i].clear()
            except:
                traceback.print_exc()

        d2 = datetime.strptime(datetime.now().strftime(fmt), fmt)
        d2_ts = time.mktime(d2.timetuple())
        print(str(float(d2_ts - d1_ts) / 60) + " minutes")

    def update_inverted_file(self, index):
        print("[" + str(datetime.now()) + "] " + "updating inverted file of :"+ str(index))
        try:
            with open("Inverted_files/" +self.inverted_idx_files_list[index], 'r', encoding='utf-8') as inverted_idx_file:
                inverted_idx_from_file = json.load(inverted_idx_file)
        except:
            inverted_idx_from_file = {}

        inverted_idx_to_file = self.merge_inverted_idx_dicts(inverted_idx_from_file,
                                                             self.inverted_idx_dicts_list[index])
            # to json:
        try:
            with open("Inverted_files/" +self.inverted_idx_files_list[index], 'w', encoding='utf-8') as inverted_idx_file:
                json.dump(inverted_idx_to_file, inverted_idx_file)
                inverted_idx_to_file.clear()
                inverted_idx_from_file.clear()
                self.inverted_idx_dicts_list[index].clear()
        except:
            traceback.print_exc()


    def update_posting_file(self, index):
        print("[" + str(datetime.now()) + "] " + "updating posting file of :"+ str(index))
        try:
            with open("Posting_files/" +self.posting_files_list[index], 'a', encoding='utf-8') as posting_file:
                json.dump(self.posting_dicts_list[index], posting_file)
                self.posting_dicts_list[index].clear()
        except:
            traceback.print_exc()
