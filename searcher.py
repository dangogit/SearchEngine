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

    def calculate_cos_simulatry(self,term):
        return True
    def calaclate_tf_idf(self,document):
        return True

    #the big matrix is the base for the functions

    def create_weight_matrix_for_corpus(self):
        matrix=np.array((self.inverted_index))

    def get_similar_words(self,term):
        synomus=[]
        for syn in wordnet.synsets(term):
            for l in syn.lemmas():
                synomus.append(l.name())

        return synomus

    def relevant_docs_from_posting(self, query):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query: query
        :return: dictionary of relevant documents.
        """


        #expend and get more words using WordNet?
        #build metrix here, and pass it to ranker
        posting = utils.load_obj("posting")
        relevant_docs = {}
        for term in query:
            #query expansion??
            similar_words=self.get_similar_words(term) #list
            similar_words.append(term)
            for new_term in similar_words:
                try: # an example of checks that you have to do
                    posting_doc = posting[term]
                    for doc_tuple in posting_doc:
                        doc = doc_tuple[0]
                        if doc not in relevant_docs.keys():
                            relevant_docs[doc] = 1
                        else:
                            relevant_docs[doc] += 1
                except:
                    print('term {} not found in posting'.format(term))
        return relevant_docs
