import math


class Ranker:
    def __init__(self):
        pass

    @staticmethod
    def rank_relevant_doc(final_dict, doc_id_list, query_as_list):
        final_docs_ranking = {}  # list of tuples: (doc_id,rank with this query)
        # need to run on all documents recived here, give them a score, and sort them
        """
        This function provides rank for each relevant document and sorts them by their scores.
        The current score considers solely the number of terms shared by the tweet (full_text) and query.
        @:param:param relevant_doc: dictionary of documents that contains at least one term from the query.
        @:return: sorted list of documents by score
        """

        # cosine simularity using tf-idf
        query_size = len(query_as_list)
        for doc_id in doc_id_list:
            mone = 0
            mechane1 = 0
            mechane2 = 0
            for term in query_as_list:
                if term in final_dict.keys():
                    list_of_appernces_in_corpus = final_dict[term]
                    num_of_apprences_in_query = sum(term in s for s in query_as_list)

                    for tmp_list in list_of_appernces_in_corpus:  # run on all list of the term
                        if tmp_list[2] == doc_id:  # if this is the document we are looking at right now
                            Wij = float(tmp_list[0]) * tmp_list[1]  # tf*idf
                            Wiq = num_of_apprences_in_query / query_size
                            mone += (Wij * Wiq)
                            mechane1 += (Wij ** 2)
                            mechane2 += (Wiq ** 2)
                    mechane = math.sqrt(mechane1 * mechane2)
                    final_docs_ranking[doc_id] = mone / mechane
        return [pair[0] for pair in sorted(final_docs_ranking.items(), key=lambda item: item[1], reverse=True)], final_docs_ranking

    @staticmethod
    def retrieve_top_k(sorted_relevant_doc, k=1):
        """
        return a list of top K tweets based on their ranking from highest to lowest
        :param sorted_relevant_doc: list of all candidates docs.
        :param k: Number of top document to return
        :return: list of relevant document
        """
        return sorted_relevant_doc[:k]
