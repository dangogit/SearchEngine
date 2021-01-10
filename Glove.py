import traceback

from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.models import KeyedVectors

from configuration import ConfigClass


class Glove:

    def __init__(self):
        #glove2word2vec('glove.twitter.27B.25d.txt', 'glove.twitter.27B.25d.txt.word2vec')
        #self.model = KeyedVectors.load_word2vec_format('glove.twitter.27B.25d.txt.word2vec', binary=False)
        glove2word2vec(ConfigClass.glove_twitter_27B_25d_path, 'glove.twitter.27B.25d.txt.word2vec')
        self.model = KeyedVectors.load_word2vec_format('glove.twitter.27B.25d.txt.word2vec', binary=False)
        self.terms_dict = {}

    def get_similar_words(self, term):
        if term in self.terms_dict.keys():
            return self.terms_dict[term]
        synomus = []
        try:
           synomus_mat = self.model.most_similar(term)
           synomus = [synomus_mat[0][0], synomus_mat[1][0]]
           self.terms_dict[term] = synomus
        except:
            pass
        return synomus

    def improve_query(self, query):
        results = []
        if query is None:
            return None
        if query is str:
            query = [query]
        for term in query:
            results.append(term)
            results.extend(self.get_similar_words(term))
        return results