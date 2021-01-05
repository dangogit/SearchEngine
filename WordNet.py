from nltk.corpus import wordnet
class WordNet:
    def get_similar_words(self, term):
        synomus = []
        try:
            count = 0
            for syns in wordnet.synsets(term):
                for l in syns.lemmas():
                    if (l.name() != term and count < 2 and l.name not in synomus):
                        synomus.append(l.name())
                        count += 1
                    elif count >= 2:
                        return synomus
        except:
            pass
        return synomus