
from spellchecker import SpellChecker

class _SpellCheck:

    def __init__(self):
        self.spell_checker = SpellChecker()
        self.spell_checker.word_frequency.add("coronavirus")

    def improve_query(self, query):
        if query is str:
            return [self.spell_checker.correction(query)]
        elif query is list:
            return [self.spell_checker.correction(word) for word in query]
        else:
            return None

