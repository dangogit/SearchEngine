import json
import math
import traceback

from ranker import Ranker
import utils


# DO NOT MODIFY CLASS NAME
class Searcher:
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit. The model 
    # parameter allows you to pass in a precomputed model that is already in 
    # memory for the searcher to use such as LSI, LDA, Word2vec models. 
    # MAKE SURE YOU DON'T LOAD A MODEL INTO MEMORY HERE AS THIS IS RUN AT QUERY TIME.
    def __init__(self, parser, indexer, model=None):
        self.terms_searched = {}
        self.parser = Parse()
        self.ranker = Ranker()
        # self.inverted_index = inverted_index
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
        self.stop_words = self.parser.stop_words

    ###############################################################################################
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
            tmp_add += tmp_list[0]
            tmp_list[0] = tmp_add
        return doc_id_tf_list

    def get_right_inverted_index(self, output_path, letter):
        inverted_idx_from_file = {}
        if letter not in self.letters_dict.keys():
            return inverted_idx_from_file
        idx = self.letters_dict[letter]
        inverted_index_dict_list = self.inverted_idx_files_list
        # find the right posting file according to first letter of the term
        try:
            with open(output_path + inverted_index_dict_list[idx], 'r', encoding='utf-8') as posting_file:
                inverted_idx_from_file = json.load(posting_file)
        except:
            traceback.print_exc()

        return inverted_idx_from_file

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
                inverted_index = self.get_right_inverted_index(output_path, new_term[0].lower())
                if new_term not in inverted_index.keys():
                    if new_term.lower() in inverted_index.keys():
                        new_term = new_term.lower()
                    elif new_term.upper() in inverted_index.keys():
                        new_term = new_term.upper()


                if new_term in inverted_index.keys():
                    terms_idf[new_term] = math.log2(float(total_num_of_docs)/float(inverted_index[new_term][0]))
                    # recover doc_id
                    # inverted_index[1]=[[doc id,tf],[doc_id,tf]...]
                    docs_list = self.revocer_doc_ids(inverted_index[new_term][1])  # fix difference method
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
