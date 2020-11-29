import json
import traceback
import math
from nltk.corpus import stopwords

from parser_module import Parse
from ranker import Ranker
import utils
from nltk import wordnet
import numpy as np

class Searcher:

    def __init__(self, inverted_index):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.parser = Parse()
        self.ranker = Ranker()
        self.inverted_index = inverted_index
        self.stop_words = {k.lower(): "" for k in stopwords.words('english')}



    #the big matrix is the base for the functions

    def get_similar_words(self,term):
        synomus=[]
        for syn in wordnet.synsets(term):
            count=1
            for l in syn.lemmas():
                if (l.wup_similarity(term) > 0.8 and count < 3):  # check similitary and add only 2 words
                    synomus.append(l.name())
                    count+=1
        return synomus


    #return list of list
    def get_tf_from_posting(self, term):
        main_list=[]
        letter_dict=self.inverted_index.letters_dict
        idx=letter_dict[term[0]]
        posting_dict_list=self.inverted_index.posting_files_list
        #find the right posting file according to first letter of the term
        try:
            with open("Posting_files/" +posting_dict_list[idx], 'r', encoding='utf-8') as posting_file:
                posting_dict_from_file = json.load(posting_file)
                posting_file_keys=posting_dict_list.keys()
                posting_file_values = [value for key, value in posting_dict_from_file.items() if term in key.lower()]
                tmp_doc_list=[]
                location_list=self.inverted_index[term][2] #location list of the term
                tmp_add=0 #recover the location list
                for tmp_tuple in location_list:
                    #differnce method
                    key = term+str(tmp_add+tmp_tuple[1])
                    tmp_add+=tmp_tuple[1]
                    tmp_doc_list.append(tmp_tuple[0]) #doc_id
                    Fij=posting_dict_from_file[key][1]#freq in doc
                    Dj=posting_dict_from_file[key][3]#Dj, doucment length
                    tf = Fij / Dj  # calculate tf by formula
                    tmp_doc_list.append(tf)
                    main_list.append(tmp_doc_list)
        except:
            traceback.print_exc()

        return main_list

    def get_right_posting_file(self,letter):
        letter_dict = self.inverted_index.letters_dict
        idx = letter_dict[letter]
        posting_dict_list = self.inverted_index.posting_files_list
        # find the right posting file according to first letter of the term
        try:
            with open("Posting_files/" + posting_dict_list[idx], 'r', encoding='utf-8') as posting_file:
                posting_dict_from_file = json.load(posting_file)
        except:
            print("could not find right dictionary in searcher")

        return posting_dict_from_file



    #N= total amount of document in the corpus
    def relevant_docs_from_posting(self, query_as_list, total_num_of_docs):
        #query is list
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query_as_list: query
        :return: dictionary of relevant documents.
        """
        #posting = utils.load_obj("posting") #should be list of all posting files
        relevant_docs = {}
        #dictionary that will be passed to the ranker in the following form:
        # tf_idf_dict={term:[[doc_id,num of appearnces in this doc],...],term:[[]],idf}
        tf_idf_dict={}
        query_as_list=self.parser.parse_all_text(' '.join(query_as_list).lower(),0) #
        for term in query_as_list:
            #query expansion
            similar_terms=self.get_similar_words(term) #list
            similar_terms.append(term)
            for new_term in similar_terms:
                try:
                    posting_doc = self.get_right_posting_file(new_term[0])
                    if new_term in posting_doc.keys():
                        term_doc_id_list=self.inverted_index[new_term][2] #location list, list of (doc_id,freq_in_doc) that the term appears in
                        for tmp_tuple in term_doc_id_list:
                            #need to change
                            if tmp_tuple[0] in relevant_docs:
                                relevant_docs[tmp_tuple[0]]+=1
                            else:
                                relevant_docs[tmp_tuple[0]]=1
                        try:
                            if new_term not in tf_idf_dict.keys():
                                idf = math.log10((total_num_of_docs / self.inverted_index[new_term][0]))
                                tf_list = self.get_tf_from_posting(new_term)
                                #tf_idf_dict={term:[[doc_id,num of appearnces in doc_id],...],term:[[]],idf}
                                tf_idf_dict[new_term]=[tf_list,idf]
                        except:
                            print("could not find term "+ new_term+" in inverted index")
                except:
                    print("could not find posting file")

            return relevant_docs,tf_idf_dict

