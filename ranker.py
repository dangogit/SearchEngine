import math


class Ranker:
    def __init__(self):
        pass


    @staticmethod
    def rank_relevant_doc(tf_idf_dict,relevent_doc_id_list,query_as_list):
        final_doc_dict={} #list of tuples: (doc_id,rank with this query)
        #need to run on all documents recived here, give them a score, and sort them
        """
        This function provides rank for each relevant document and sorts them by their scores.
        The current score considers solely the number of terms shared by the tweet (full_text) and query.
        @:param:param relevant_doc: dictionary of documents that contains at least one term from the query.
        @:return: sorted list of documents by score
        """
        #need to implment cosine simularity using tf-idf
        for doc_id in relevent_doc_id_list:
            mone=0
            mechane=0
            for term in query_as_list:
                num_of_apprences_in_query=sum(term in s for s in query_as_list)
                list_of_appernces_in_corpus=tf_idf_dict[term]
                for tmp_list in list_of_appernces_in_corpus: #run on all list of the term
                    if tmp_list[0]==doc_id: #if this is the document we are looking at right now
                        Wij =tmp_list[1]
                        mone += num_of_apprences_in_query*Wij
                        mechane +=(num_of_apprences_in_query**2)*(Wij**2)
            mechane=math.sqrt(mechane)
            final_doc_dict[doc_id]=mone/mechane
        return sorted(final_doc_dict.items(), key=lambda item: item[1], reverse=True)

    @staticmethod
    def retrieve_top_k(sorted_relevant_doc, k=1):
        """
        return a list of top K tweets based on their ranking from highest to lowest
        :param sorted_relevant_doc: list of all candidates docs.
        :param k: Number of top document to return
        :return: list of relevant document
        """
        return sorted_relevant_doc[:k]
