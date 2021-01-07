import traceback

from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.models import KeyedVectors
from parser_module import Parse


class Glove:

    def __init__(self):
        self.input_file = r"C:\Users\Daniel\PycharmProjects\glove.twitter.27B.200d.txt"
        self.output_file = 'glove.twitter.27B.25d.txt.word2vec'
        glove2word2vec(self.input_file, self.output_file)
        self.model = KeyedVectors.load_word2vec_format(self.output_file, binary=False)

    def get_similiar_words(self, term):
        if term == None:
            return None
        try:
            res = [self.model.most_similar(term)[0][0], self.model.most_similar(term)[1][0]]
        except:
            traceback.print_exc()
        return res

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
