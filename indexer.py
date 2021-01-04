# DO NOT MODIFY CLASS NAME
import json
import sys
import traceback
import pickle

class Indexer:
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def __init__(self, config):
        self.curr_idx=0
        self.term_indexer_dict={} # key = term, value = [number_of_docs(df), docs_list ,last_doc_idx]

        self.file_indexer_dict={} # key = doc_idx, value = { key = term, value = tf}
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
        unique_terms_in_doc = self.count_unique(document_dictionary)
        max_tf = max(document_dictionary.values())
        # Go over each term in the doc
        for term in document_dictionary.keys():
            try:
                # freq of term in all corpus until now
                freq_in_doc = document_dictionary[term]
                self.insert_term_to_inv_idx(term, freq_in_doc, self.curr_idx, unique_terms_in_doc, max_tf,
                                            document)
                self.insert_file_to_inv_idx(term, freq_in_doc, max_tf)
                #{doc_id:[(term,tf).(term,tf)...]}
                #freq_in_doc/max_tf=tf
                #df=num_of_docs

            except:
                traceback.print_exc()

    def insert_term_to_inv_idx(self, term, freq_in_doc, doc_idx,
                               unique_terms_in_doc, max_tf, document):
       # index = self.letters_dict[term[0]]

        if term in self.term_indexer_dict.keys():
            number_of_docs = self.term_indexer_dict[term][0] + 1
            docs_list = self.term_indexer_dict[term][1]
            last_doc_idx = self.term_indexer_dict[term][2]
        else:
            number_of_docs = 1
            docs_list = []
            last_doc_idx = doc_idx

        tf = float(freq_in_doc) / float(max_tf)
        docs_list.append(doc_idx)

        self.term_indexer_dict[term] = [number_of_docs, self.differnce_method(docs_list, last_doc_idx),
                                        doc_idx]

    def insert_file_to_inv_idx(self, term, freq_in_doc, max_tf):

        tf = float(freq_in_doc) / float(max_tf)
        if self.curr_idx not in self.file_indexer_dict.keys():
            self.file_indexer_dict[self.curr_idx] = {}

        self.file_indexer_dict[self.curr_idx][term] = tf

        # list of tuples(doc_num, number of apperances in doc)
    def differnce_method(self, list, last_doc_index):
        i = len(list) - 1
        if i != 0:
            new_value = list[i] - last_doc_index
            list[i] = new_value
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

    #def merge_inverted_idx_dicts(self, inverted_idx_from_file, inverted_idx_dict):
    #    if len(inverted_idx_from_file.keys()) == 0:
    #        return inverted_idx_dict
    #    while len(inverted_idx_dict.keys()) > 0:
    #        term, values_of_term = inverted_idx_dict.popitem()
#
    #        if term in inverted_idx_from_file.keys():
    #            number_of_docs = inverted_idx_from_file[term][0] + values_of_term[0]
    #            docs_list_from_file = inverted_idx_from_file[term][1]
    #            docs_list_from_local = values_of_term[1]
    #            last_doc_idx_from_file = inverted_idx_from_file[term][2]
    #            docs_list_from_file.append(docs_list_from_local[0])
    #            docs_list_from_file = self.differnce_method(docs_list_from_file, last_doc_idx_from_file)
    #            docs_list_from_file.extend(docs_list_from_local[1:])
    #            last_doc_idx_from_local = values_of_term[2]

    #            inverted_idx_from_file[term] = [
    #                number_of_docs, docs_list_from_file, last_doc_idx_from_local]
    #        else:
    #            inverted_idx_from_file[term] = values_of_term

    #    return inverted_idx_from_file

    #def update_posting_file(self, index):
    #    # print("[" + str(datetime.now()) + "] " + "updating posting file of :" + str(index))
    #    try:
    #        with open(self.output_path + self.posting_files_list[index], 'a', encoding='utf-8') as posting_file:
    #            jsonstr = json.dumps(self.posting_dicts_list[index])
    #            posting_file.write((jsonstr + "\n"))
    #            self.posting_dicts_list[index].clear()
    #    except:
    #        traceback.print_exc()
#
   #def update_inv_file(self, index):
   #    # print("[" + str(datetime.now()) + "] " + "updating inverted file of :" + str(index))
   #    try:
   #        with open(self.output_path + self.inverted_idx_files_list[index], 'a', encoding='utf-8') as inverted_file:
   #            jsonstr = json.dumps(self.inverted_idx_dicts_list[index])
   #            inverted_file.write((jsonstr + "\n"))
   #            self.inverted_idx_dicts_list[index].clear()
   #    except:
   #        traceback.print_exc()

    #def fix_inverted_files(self, index):
    #    # print("[" + str(datetime.now()) + "] " + "fixing inverted files of :" + str(index))
    #    inverted_dicts_from_file = []
    #    try:
    #        with open(self.output_path + self.inverted_idx_files_list[index], 'r',
    #                  encoding='utf-8') as inverted_file:
    #            for line in inverted_file.readlines():
    #                inverted_dicts_from_file.append(json.loads(line))
    #    except:
    #        traceback.print_exc()
#
    #    # print("[" + str(datetime.now()) + "] " + "merging...")
    #    for i in range(1, len(inverted_dicts_from_file)):
    #        base_dict = inverted_dicts_from_file[0]
    #        inverted_dicts_from_file[0] = self.merge_inverted_idx_dicts(base_dict, inverted_dicts_from_file[i])
    #    try:
    #        fixed_inverted_dict = self.fix_big_and_small_letters(inverted_dicts_from_file[0])
    #    # to json:
    #    except:
    #        traceback.print_exc()
    #    try:
    #        with open(self.output_path + self.inverted_idx_files_list[index], 'w',
    #                  encoding='utf-8') as posting_file:
    #            json.dump(fixed_inverted_dict, posting_file)
#
    #    except:
    #        traceback.print_exc()
#
    ## print("[" + str(datetime.now()) + "] " + "finished fixing inverted file of :" + str(index))
#
    #def fix_posting_files(self, index):
    #    #  print("[" + str(datetime.now()) + "] " + "fixing posting files of :" + str(index))
    #    posting_dict_from_file = []
    #    try:
    #        with open(self.output_path + self.posting_files_list[index], 'r',
    #                  encoding='utf-8') as posting_file:
    #            for line in posting_file.readlines():
    #                posting_dict_from_file.append(json.loads(line))
    #    except:
    #        traceback.print_exc()
    #    #   print("[" + str(datetime.now()) + "] " + "sorting...")
    #    posting_dict_from_file = self.sort_dictionarys(posting_dict_from_file)
#
    #    # to json:
    #    try:
    #        with open(self.output_path + self.posting_files_list[index], 'w',
    #                  encoding='utf-8') as posting_file:
    #            json.dump(posting_dict_from_file, posting_file)
    #    except:
    #        traceback.print_exc()
#
    ##    print("[" + str(datetime.now()) + "] " + "finished fixing posting file of :" + str(index))



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
                #data=[self.term_indexer_dict,self.file_indexer_dict]
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
            pickle.dump([self.term_indexer_dict,self.file_indexer_dict], folder)

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
        return self.postingDict[term] if self._is_term_exist(term) else []
