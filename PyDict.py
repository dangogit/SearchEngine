from PyDictionary import PyDictionary

class PyDict:

    def __init__(self):
        self.terms_dict = {}
        self.dictionary = PyDictionary()

    def get_similar_words(self, term):
        if term in self.terms_dict.keys():
            return self.terms_dict[term]

        results = []
        try:
            results = self.dictionary.synonym(term)
        except TypeError:
            return []
        if results is None:
            return []
        elif len(results) > 2:
            best_2 = results[:2]
            self.terms_dict[term] = best_2
            return best_2
        else:
            self.terms_dict[term] = results
            return results

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