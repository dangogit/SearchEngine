
from spellchecker import SpellChecker

class _SpellChecker:

    def __init__(self):
        self.spell_checker = SpellChecker()
        self.spell_checker.word_frequency.add("coronavirus")
        self.spell_checker.word_frequency.add("corona")
        self.spell_checker.word_frequency.add("covid")

    def improve_query(self, query):
        if isinstance(query,str):
            fixed_query = [self.spell_checker.correction(query)]
        elif isinstance(query,list):
            fixed_query = []
            for word in query:
                fixed_word = self.spell_checker.correction(word)
                if fixed_word is None:
                    fixed_query.append(word)
                else:
                    fixed_query.append(fixed_word)
        else:
            return None

        if fixed_query is None:
            return query
        else:
            return fixed_query

