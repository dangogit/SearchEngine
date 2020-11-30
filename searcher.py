import json
import traceback
import math
from nltk.corpus import stopwords

from parser_module import Parse
from ranker import Ranker
import utils
from nltk.corpus import wordnet
import numpy as np
import nltk

class Searcher:

    def __init__(self):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.parser = Parse()
        self.ranker = Ranker()
        nltk.download()
        #self.inverted_index = inverted_index
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
        self.letters_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10,
                             'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20,
                             'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25, '#': 26}
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
        self.stop_words = {k.lower(): "" for k in stopwords.words('english')}



    #the big matrix is the base for the functions

    def get_similar_words(self,term):
        synomus=[]
        for syn in wordnet.synset(term):
            count=1
            for l in syn.lemmas():
                if (l.wup_similarity(term) > 0.8 and count < 3):  # check similitary and add only 2 words
                    synomus.append(l.name())
                    count+=1
        return synomus


    #return list of list
    def get_tf_from_posting(self, term,inverted_index):
        main_list=[]
        letter_dict=self.letters_dict
        idx=letter_dict[term[0]]
        posting_dict_list=self.posting_files_list
        doc_id_list=[]
        #find the right posting file according to first letter of the term
        try:
            with open("Posting_files/" +posting_dict_list[idx], 'r', encoding='utf-8') as posting_file:
                posting_dict_from_file = json.load(posting_file)
                tmp_doc_list=[]
                location_list=inverted_index[term][2] #location list of the term
                tmp_add=0 #recover the location list
                for tmp_tuple in location_list:
                    #differnce method
                    key = term+str(tmp_add+tmp_tuple[1])
                    tmp_add+=tmp_tuple[1]
                    tmp_doc_list.append(tmp_tuple[0]) #doc_id
                    doc_id_list.append(tmp_tuple[0])
                    Fij=posting_dict_from_file[key][1]#freq in doc
                    Dj=posting_dict_from_file[key][3]#Dj, doucment length
                    tf = Fij / Dj  # calculate tf by formula
                    tmp_doc_list.append(tf)
                    main_list.append(tmp_doc_list)
                    #tmp
        except:
            traceback.print_exc()

        return main_list,doc_id_list

    def get_right_inverted_index(self,letter):
        idx = self.letters_dict[letter]
        inverted_index_dict_list = self.inverted_idx_files_list
        # find the right posting file according to first letter of the term
        try:
            with open("Posting_files/" + inverted_index_dict_list[idx], 'r', encoding='utf-8') as posting_file:
                inverted_idx_from_file = json.load(posting_file)
        except:
            print("could not find right dictionary in searcher")

        return inverted_idx_from_file



    #N= total amount of document in the corpus
    def relevant_docs_from_posting(self, query_as_list, total_num_of_docs):
        #query is list
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query_as_list: query
        :return: dictionary of relevant documents.
        """
        #posting = utils.load_obj("posting") #should be list of all posting files
        relevant_docs = []
        #dictionary that will be passed to the ranker in the following form:
        # tf_idf_dict={term:[[doc_id,num of appearnces in this doc],...],term:[[]],idf}
        tf_idf_dict={}
        query_as_list=self.parser.parse_all_text(' '.join(query_as_list).lower(),0) #
        for term in query_as_list:
            #query expansion
            similar_terms=self.get_similar_words(term) #list
            query_as_list+=similar_terms
        for new_term in query_as_list:
            try:
                inverted_index = self.get_right_inverted_index(new_term[0])
                if new_term in inverted_index.keys():
                    term_doc_id_list=inverted_index[new_term][2] #location list, list of (doc_id,freq_in_doc) that the term appears in
                    if new_term not in tf_idf_dict.keys():
                        idf = math.log10((total_num_of_docs / inverted_index[new_term][0]))
                        tf_list,doc_id_list = self.get_tf_from_posting(new_term,inverted_index)
                        relevant_docs+=doc_id_list #all relevent doc id's in one list
                        #tf_idf_dict={term:[[doc_id,num of appearnces in doc_id],...],term:[[]],idf}
                        tf_idf_dict[new_term]=[tf_list,idf]
            except:
                    print("could not find term "+ new_term+" in inverted index")

        return tf_idf_dict,relevant_docs

