from nltk.corpus import lin_thesaurus

class _Thesaurus:
    def __init__(self):
        self.terms_dict = {}

    def get_similar_words(self, term):
        if term in self.terms_dict.keys():
            return self.terms_dict[term]
        scored_synonyms = lin_thesaurus.scored_synonyms(term, fileid="simN.lsp")
        best_2 = sorted(scored_synonyms, key = lambda x: x[1], reverse=True)[:2]
        best_2_list = [tup[0] for tup in best_2]
        self.terms_dict[term] = best_2_list
        return best_2_list

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



