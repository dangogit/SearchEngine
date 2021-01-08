import json
import math
import traceback

from _SpellCheck import _SpellChecker
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
        self.terms_searched={}
        self.total_num_of_docs = parser.curr_idx

    ###############################################################################################
    #
    #ours
    # the big matrix is the base for the functions

    # return list of list

    def revocer_doc_ids(self, doc_id_tf_list):
        tmp_add = 0
        for tmp_list in doc_id_tf_list:
            tmp_add += tmp_list[0]
            tmp_list[0] = tmp_add
        return doc_id_tf_list


    # N= total amount of document in the corpus
    def _relevant_docs_from_posting(self, query_as_list, total_num_of_docs):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query_as_list: query
        :return: dictionary of relevant documents.
        """
        terms_idf = {}
        similar_terms = []
        doc_id_dict = {}
        query_as_list = self._parser.parse_all_text(' '.join(query_as_list).lower())  #

        if self._model is not None:
            if isinstance(self._model,list):
                query_as_list_to_extend = []
                for model in self._model:
                    if model is _SpellChecker():
                        query_as_list = model.improve_query(query_as_list)
                    else:
                        query_as_list_to_extend.extend(model.improve_query(query_as_list))
                query_as_list = set(query_as_list_to_extend)

            else:
                try:
                    query_as_list = self._model.improve_query(query_as_list)
                except AttributeError:
                    print("Failed query expansion")
                    pass

       #     for term in query_as_list:
       #         # query expansion
       #         try:
       #             similar_terms.extend(self._model.get_similar_words(term)) # list
       #
       #         except AttributeError:
       #             print("Failed query expansion")
       #             break
       # if len(similar_terms) > 1:
       #     try:
       #         query_as_list = set(query_as_list.extend(similar_terms))
       #     except TypeError:
       #         pass

        for new_term in query_as_list:
            try:
                if new_term not in self._indexer.term_indexer_dict.keys():
                    if new_term.lower() in self._indexer.term_indexer_dict.keys():
                        new_term = new_term.lower()
                    elif new_term.upper() in self._indexer.term_indexer_dict.keys():
                        new_term = new_term.upper()


                if new_term in self._indexer.term_indexer_dict.keys():
                    df = self._indexer.term_indexer_dict[new_term][0]
                    if df != 0:
                        terms_idf[new_term] = math.log2(float(total_num_of_docs)/float(df))

                    else:
                        terms_idf[new_term] = 0

                    docs_list=self._indexer.term_indexer_dict[new_term][1]
                    doc_id_dict.update(dict(docs_list))
                    self.terms_searched[new_term] = dict(docs_list)

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

        for doc_id in doc_id_list:
            for term in self._indexer.file_indexer_dict[doc_id].keys():
               # if term not in self.terms_searched.keys():
                tf = self._indexer.file_indexer_dict[doc_id][term]
                df = math.log2(float(total_num_of_docs) / float(self._indexer.term_indexer_dict[term][0]))
                if term not in final_dict.keys():
                    final_dict[term] = [[tf, df, doc_id]]
                else:
                    final_dict[term].append([tf, df, doc_id])

        return final_dict, doc_id_list, self._indexer.file_indexer_dict

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

        final_dict, doc_id_list, file_indexer_dict = self._relevant_docs_from_posting(query_as_list, self.total_num_of_docs)

        ranked_docs_list, ranked_docs_dict = self._ranker.rank_relevant_doc(final_dict, doc_id_list,query_as_list, file_indexer_dict)
        #results_dict = {self._parser.doc_idx_tweet_id[k]: ranked_docs_dict[k] for k in ranked_docs_list}

        ranked_docs_list_top_k = self._ranker.retrieve_top_k(ranked_docs_list, k)
        results_list_top_k = [self._parser.doc_idx_tweet_id[key] for key in ranked_docs_list_top_k]


        return len(ranked_docs_list), results_list_top_k



    # feel free to change the signature and/or implementation of this function 
    # or drop altogether.
    def relevant_docs_from_posting(self, query_as_list):
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
