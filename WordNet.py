from nltk.corpus import wordnet
class WordNet:

    def __init__(self):
        self.terms_dict = {}

    def get_similar_words(self, term):
        if term in self.terms_dict.keys():
            return self.terms_dict[term]
        synomus = []
        try:
            count = 0
            for syns in wordnet.synsets(term):
                for l in syns.lemmas():
                    if count >= 2:
                        self.terms_dict[term] = synomus
                        return synomus
                    elif (l.name() != term and count < 2 and l.name not in synomus):
                        synomus.append(l.name())
                        count += 1
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