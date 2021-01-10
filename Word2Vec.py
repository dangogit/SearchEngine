import gensim

from configuration import ConfigClass


class Word2Vec:

    def __init__(self):
        #self.model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True,encoding='utf-8')
        self.model = gensim.models.KeyedVectors.load_word2vec_format(ConfigClass.google_news_vectors_negative300_path, binary=True,encoding='utf-8')
        self.terms_dict = {}

    def get_similar_words(self, term):
        if term in self.terms_dict.keys():
            return self.terms_dict[term]
        synomus = []
        try:
           synomus_mat = self.model.most_similar(term, topn=2)
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