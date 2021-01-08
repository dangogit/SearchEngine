# DO NOT MODIFY CLASS NAME
import json
import sys
import traceback
import pickle
#a
class Indexer:
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def __init__(self, config):
        self.curr_idx=0
        self.file_indexer_dict={} # key = doc_idx, value = { key = term, value = tf}
        self.term_indexer_dict = {}
        self.config = config
        #self.output_path = output_path
        #self.words_dict = p.word_set

    #####################################################################################################
    #ours
    def set_idx(self,idx):
        self.curr_idx=idx

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def add_new_doc(self, document):
        """
               This function perform indexing process for a document object.
               Saved information is captures via two dictionaries ('inverted index' and 'posting')
               :param document: a document need to be indexed.
               :return: -
               """
        document_dictionary = document.term_doc_dictionary  # term_dict
        if len(document_dictionary) == 0:
            return
        #unique_terms_in_doc = self.count_unique(document_dictionary)
        max_tf = max(document_dictionary.values())
        # Go over each term in the doc
        for term in document_dictionary.keys():
            try:
                # freq of term in all corpus until now
                freq_in_doc = document_dictionary[term]
                tf = float(freq_in_doc) / float(max_tf)
                self.insert_term_to_inv_idx(term, self.curr_idx, tf)
                self.insert_file_to_inv_idx(term, tf)
            except:
                traceback.print_exc()

    def insert_term_to_inv_idx(self, term, doc_idx, tf):
        if term in self.term_indexer_dict.keys():
            number_of_docs = self.term_indexer_dict[term][0] + 1
            docs_list = self.term_indexer_dict[term][1]
        else:
            number_of_docs = 1
            docs_list = []

        docs_list.append([doc_idx, tf])

        self.term_indexer_dict[term] = [number_of_docs, docs_list]


    def insert_file_to_inv_idx(self, term, tf):

        if self.curr_idx not in self.file_indexer_dict.keys():
            self.file_indexer_dict[self.curr_idx] = {}

        self.file_indexer_dict[self.curr_idx][term] = tf

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

    # asdasd
    #?
    def fix_big_and_small_letters(self, inverted_dict):
        fixed_dict = {}
        for term in inverted_dict.keys():
            if term[0] != '#' and term not in self.term_indexer_dict.keys():
                new_term = term.upper()
                fixed_dict[new_term] = inverted_dict[term]
            else:
                fixed_dict[term] = inverted_dict[term]
        return fixed_dict


    ####################################################################################

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.

    def load_index(self, fn):
        """
        Loads a pre-computed index (or indices) so we can answer queries.
        Input:
            fn - file name of pickled index.
        """
        try:
            with open(fn, 'rb') as index_file:
                data = pickle.load(index_file)
                #data=(self.term_indexer_dict,self.file_indexer_dict)
        except:
            traceback.print_exc()
        return data
        #

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def save_index(self, fn):
        """
        Saves a pre-computed index (or indices) so we can save our work.
        Input:
              fn - file name of pickled index.
        """
        with open(fn,'wb') as folder:
            pickle.dump((self.term_indexer_dict,self.file_indexer_dict), folder)

    # feel free to change the signature and/or implementation of this function 
    # or drop altogether.
    def _is_term_exist(self, term):
        """
        Checks if a term exist in the dictionary.
        """
        return term in self.term_indexer_dict.keys()

    # feel free to change the signature and/or implementation of this function 
    # or drop altogether.
    def get_term_posting_list(self, term):
        """
        Return the posting list from the index for a term.
        """
        return self.term_indexer_dict[term][1] if self._is_term_exist(term) else []
