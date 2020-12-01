import time
import traceback
from datetime import datetime
import pandas as pd
import json
import collections
import sys


class Indexer:

    def __init__(self, config, output_path, p):
        # new_dictonaries
        self.letters_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10,
                             'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20,
                             'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25, '#': 26}
        self.inverted_idx_dicts_list = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {},
                                        {}, {}, {}, {}, {}, {}, {}]
        self.inverted_idx_count_for_update = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                        0, 0, 0, 0, 0, 0, 0]
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
        self.output_path = output_path
        self.words_dict = p.word_set

    def add_new_doc(self, document, doc_idx):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """
        document_dictionary = document.term_doc_dictionary #term_dict
        if len(document_dictionary) == 0:
            return
        unique_terms_in_doc = self.count_unique(document_dictionary)
        max_tf = max(document_dictionary.values())
        # Go over each term in the doc
        for term in document_dictionary.keys():
            try:
                if term[0] not in self.letters_dict.keys():
                    continue
                # freq of term in all corpus until now
                freq_in_doc = document_dictionary[term]

                self.insert_term_to_inv_idx_and_post_dict(term, freq_in_doc, doc_idx, unique_terms_in_doc, max_tf, document)

            except:
                print('problem with the following key {}'.format(term))
                traceback.print_exc()


    def insert_term_to_inv_idx_and_post_dict(self, term, freq_in_doc, doc_idx,
                                             unique_terms_in_doc, max_tf, document):
        index = self.letters_dict[term[0]]

        if term in self.inverted_idx_dicts_list[index].keys():
            number_of_docs = self.inverted_idx_dicts_list[index][term][0] + 1
            docs_list = self.inverted_idx_dicts_list[index][term][1]
            last_doc_idx = self.inverted_idx_dicts_list[index][term][2]
        else:
            number_of_docs = 1
            docs_list = []
            last_doc_idx = doc_idx

        tf = float(freq_in_doc)/float(document.doc_length)
        docs_list.append([doc_idx, tf])

        self.inverted_idx_dicts_list[index][term] = [number_of_docs, self.differnce_method(docs_list, last_doc_idx), doc_idx]
        key = term + " " + str(doc_idx)
        term_indices = [idx for idx, word in enumerate(document.full_text.split(), 1) if word == term]
        self.posting_dicts_list[index][key] = [doc_idx, freq_in_doc, term_indices, document.doc_length, unique_terms_in_doc, max_tf]

        if sys.getsizeof(self.posting_dicts_list[index]) > 4000000:
            self.inverted_idx_count_for_update[index] += 1
            self.update_posting_file(index)
            if self.inverted_idx_count_for_update[index] == 3:
                self.update_inv_file(index)
                self.inverted_idx_count_for_update[index] = 0


    # list of tuples(doc_num, number of apperances in doc)
    def differnce_method(self, list, last_doc_index):
        i = len(list) - 1
        if i != 0:
            new_value = list[i][0] - last_doc_index
            list[i] = [new_value, list[i][1]]
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
        if len(inverted_idx_from_file.keys()) == 0:
            return inverted_idx_dict
        while len(inverted_idx_dict.keys()) > 0:
            term, values_of_term = inverted_idx_dict.popitem()

            if term in inverted_idx_from_file.keys():
                number_of_docs = inverted_idx_from_file[term][0] + values_of_term[0]
                docs_list_from_file = inverted_idx_from_file[term][1]
                docs_list_from_local = values_of_term[1]
                last_doc_idx_from_file = inverted_idx_from_file[term][2]
                docs_list_from_file.append(docs_list_from_local[0])
                docs_list_from_file = self.differnce_method(docs_list_from_file, last_doc_idx_from_file)
                docs_list_from_file.extend(docs_list_from_local[1:])
                last_doc_idx_from_local = values_of_term[2]

                inverted_idx_from_file[term] = [
                    number_of_docs, docs_list_from_file, last_doc_idx_from_local]
            else:
                inverted_idx_from_file[term] = values_of_term

        return inverted_idx_from_file



    def update_posting_file(self, index):
        print("[" + str(datetime.now()) + "] " + "updating posting file of :"+ str(index))
        try:
            with open(self.output_path+"/Posting_files/" +self.posting_files_list[index], 'a', encoding='utf-8') as posting_file:
                jsonstr = json.dumps(self.posting_dicts_list[index])
                posting_file.write((jsonstr + "\n"))
                self.posting_dicts_list[index].clear()
        except:
            traceback.print_exc()

    def update_inv_file(self, index):
        print("[" + str(datetime.now()) + "] " + "updating inverted file of :"+ str(index))
        try:
            with open(self.output_path+"/Inverted_files/" +self.inverted_idx_files_list[index], 'a', encoding='utf-8') as inverted_file:
                jsonstr = json.dumps(self.inverted_idx_dicts_list[index])
                inverted_file.write((jsonstr + "\n"))
                self.inverted_idx_dicts_list[index].clear()
        except:
            traceback.print_exc()


    def fix_inverted_files(self, index):
        print("[" + str(datetime.now()) + "] " + "fixing inverted files of :" + str(index))
        inverted_dicts_from_file = []
        try:
            with open(self.output_path+"/Inverted_files/" +self.inverted_idx_files_list[index], 'r', encoding='utf-8') as inverted_file:
                for line in inverted_file.readlines():
                    inverted_dicts_from_file.append(json.loads(line))
        except:
            traceback.print_exc()

        print("[" + str(datetime.now()) + "] " + "merging...")
        for i in range(1, len(inverted_dicts_from_file)):
            base_dict = inverted_dicts_from_file[0]
            inverted_dicts_from_file[0] = self.merge_inverted_idx_dicts(base_dict, inverted_dicts_from_file[i])

        fixed_inverted_dict = self.fix_big_and_small_letters(inverted_dicts_from_file[0])
        # to json:
        try:
            with open(self.output_path+"/Inverted_files/" +self.inverted_idx_files_list[index], 'w', encoding='utf-8') as posting_file:
                json.dump(fixed_inverted_dict, posting_file)
        except:
            traceback.print_exc()

        print("[" + str(datetime.now()) + "] " + "finished fixing inverted file of :" + str(index))


    def fix_posting_files(self, index):
        print("[" + str(datetime.now()) + "] " + "fixing posting files of :" + str(index))
        posting_dict_from_file = []
        try:
            with open(self.output_path+"/Posting_files/" +self.posting_files_list[index], 'r', encoding='utf-8') as posting_file:
                for line in posting_file.readlines():
                    posting_dict_from_file.append(json.loads(line))
        except:
            traceback.print_exc()
        print("[" + str(datetime.now()) + "] " + "sorting...")
        posting_dict_from_file = self.sort_dictionarys(posting_dict_from_file)

        # to json:
        try:
            with open(self.output_path+"/Posting_files/" +self.posting_files_list[index], 'w', encoding='utf-8') as posting_file:
                json.dump(posting_dict_from_file, posting_file)
        except:
            traceback.print_exc()

        print("[" + str(datetime.now()) + "] " + "finished fixing posting file of :" + str(index))



    def fix_big_and_small_letters(self, inverted_dict):
        fixed_dict = {}
        for term in inverted_dict.keys():
            if term not in self.words_dict.keys():
                new_term = term.upper()
                fixed_dict[new_term] = inverted_dict[term]
            else:
                fixed_dict[term] = inverted_dict[term]
        return fixed_dict

