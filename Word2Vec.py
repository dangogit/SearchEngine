import gensim
class Word2Vec:

    def __init__(self):
        self.model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True,encoding='utf-8')


    def get_similar_words(self, term):
        synomus = []
        try:
           synomus_mat = self.model.most_similar(term, topn=3)
           synomus = [synomus_mat[0][0], synomus_mat[1][0]]
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
        return set(results)