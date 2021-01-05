
class Word2Vec:

    def __init__(self):
        self.model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True,encoding='utf-8')


    def get_similar_words(self, term):
        synomus = []
        try:
           synomus = self.model.most_similar(term, topn=3)
        except:
            pass
        return synomus
