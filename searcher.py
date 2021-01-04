import json
import math
import traceback

from nltk.corpus import wordnet

from parser_module import Parse
from ranker import Ranker
import utils
##stamagainsdads

class Searcher:
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit. The model
    # parameter allows you to pass in a precomputed model that is already in
    # memory for the searcher to use such as LSI, LDA, Word2vec models.
    # MAKE SURE YOU DON'T LOAD A MODEL INTO MEMORY HERE AS THIS IS RUN AT QUERY TIME.
    def __init__(self, parser, indexer, model=None):
        self._parser = parser
        self._indexer = indexer
        self._ranker = Ranker()
        self._model = model

    ###############################################################################################
    #
    #ours
    # the big matrix is the base for the functions
    def get_similar_words(self, term):
        synomus = []
        try:
            count = 0
            for syns in wordnet.synsets(term):
                for l in syns.lemmas():
                    if (l.name() != term and count < 2 and l.name not in synomus):
                        synomus.append(l.name())
                        count += 1
                    elif count >= 2:
                        return synomus
        except:
            pass
        return synomus

    # return list of list

    def revocer_doc_ids(self, doc_id_tf_list):
        tmp_add = 0
        for tmp_list in doc_id_tf_list:
            tmp_add += tmp_list
            tmp_list = tmp_add
        return doc_id_tf_list


    # N= total amount of document in the corpus
    def relevant_docs_from_posting(self, output_path, query_as_list, total_num_of_docs):
        # query is list
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query_as_list: query
        :return: dictionary of relevant documents.
        """
        relevant_docs = []
        # dictionary that will be passed to the ranker in the following form:
        # tf_idf_dict={term:[[doc_id,num of appearnces in this doc],...],term:[[]],idf}
        tf_idf_dict = {}

        terms_idf = {}
        similar_terms = []
        doc_id_dict = {}
        query_as_list = self.parser.parse_all_text(' '.join(query_as_list).lower())  #
        for term in query_as_list:
            # query expansion
            similar_terms += set(self.get_similar_words(term))  # list
        query_as_list = set(query_as_list + similar_terms)
        total_id_dict_list = []  # lists that holds all suspuicous id's and then find the common
        for new_term in query_as_list:
            try:
                if new_term not in self._indexer.term_indexer_dict.keys():
                    if new_term.lower() in self._indexer.term_indexer_dict.keys():
                        new_term = new_term.lower()
                    elif new_term.upper() in self._indexer.term_indexer_dict.keys():
                        new_term = new_term.upper()


                if new_term in self._indexer.term_indexer_dict.keys():
                    terms_idf[new_term] = math.log2(float(total_num_of_docs)/float(self._indexer.term_indexer_dict[new_term][0]))
                    # recover doc_id
                    # inverted_index[1]=[[doc id,tf],[doc_id,tf]...]
                    docs_list = self.revocer_doc_ids(self._indexer.term_indexer_dict[new_term][1])  # fix difference method
                    # now dictionary
                    # sort by tf
                    sorted_docs_list = sorted(docs_list, key=lambda x: float(x[1]), reverse=True)
                    # get 2000 best results
                    best_2000_docs = sorted_docs_list[:2000]
                    doc_id_dict.update(dict(best_2000_docs))
                    self.terms_searched[new_term] = dict(best_2000_docs)
                    # get seperate doc_id list
                    # doc_id_list = [item[0] for item in inverted_index[new_term][1]]
                    # [[dict_1,tf1],[dict2,tf2]...]
                  #  total_id_dict_list.append([inverted_index[new_term][1], inverted_index[new_term][0]])
            except:
                traceback.print_exc()

        doc_id_list = doc_id_dict.keys()
        final_dict = {}

        try:
            for term in query_as_list:
                if term in self.terms_searched.keys():
                    df = terms_idf[term]
                    for doc_id in doc_id_list:
                        if doc_id in self.terms_searched[term].keys():
                            tf = self.terms_searched[term][doc_id]
                            if term not in final_dict.keys():
                                final_dict[term] = [[tf, df, doc_id]]
                            else:
                                final_dict[term].append([tf, df, doc_id])
        except:
            traceback.print_exc()

        return final_dict, doc_id_list


    ######################################################################################################################################




    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def search(self, query, k=None):
        """ 
        Executes a query over an existing index and returns the number of 
        relevant docs and an ordered list of search results (tweet ids).
        Input:
            query - string.
            k - number of top results to return, default to everything.
        Output:
            A tuple containing the number of relevant search results, and 
            a list of tweet_ids where the first element is the most relavant 
            and the last is the least relevant result.
        """
        query_as_list = self._parser.parse_sentence(query)

        relevant_docs = self._relevant_docs_from_posting(query_as_list)
        n_relevant = len(relevant_docs)
        ranked_doc_ids = Ranker.rank_relevant_docs(relevant_docs)
        return n_relevant, ranked_doc_ids



    # feel free to change the signature and/or implementation of this function 
    # or drop altogether.
    def _relevant_docs_from_posting(self, query_as_list):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query_as_list: parsed query tokens
        :return: dictionary of relevant documents mapping doc_id to document frequency.
        """
        relevant_docs = {}
        for term in query_as_list:
            posting_list = self._indexer.get_term_posting_list(term)
            for doc_id, tf in posting_list:
                df = relevant_docs.get(doc_id, 0)
                relevant_docs[doc_id] = df + 1
        return relevant_docs
