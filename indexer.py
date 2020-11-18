import pandas as pd
import json
class Indexer:

    def __init__(self, config, word_dict):
        self.inverted_idx = {}
        self.postingDict = {}
        self.config = config
        self.word_dict = word_dict
        self.key = 0
        self.updated_terms = {}

    def add_new_doc(self, document, idx):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """
        curr = 0
        self.updated_terms.clear()
        document_dictionary = document.term_doc_dictionary
        # Go over each term in the doc
        for term in document_dictionary.keys():
            try:
                if term.lower() in self.word_dict.keys():
                    freq = self.word_dict[term.lower()]
                elif term in self.word_dict.keys():
                    freq = self.word_dict[term]
                else:
                    self.word_dict[term] = 1

                # Update inverted index and posting
                if term not in self.inverted_idx.keys():
                    number_of_docs = 1
                else:
                    number_of_docs = self.inverted_idx[term][0] + 1

                self.inverted_idx[term] = (number_of_docs, freq, self.key)

                self.postingDict[curr] = [idx, document_dictionary[term], self.index_term_in_text(term, document.full_text), document.doc_length, self.count_unique(document_dictionary)]
            except:
                print('problem with the following key {}'.format(term))

            self.key += 1
            self.updated_terms[term] = curr
            curr += 1

            if self.key%100 == 0:
                self.update_posting_file()
                curr = 0
                self.updated_terms.clear()
                self.postingDict.clear()

    def index_term_in_text(self, term, text):
        indexes = []
        count = 0
        for word in text.split():
            if word == term:
                indexes.append(count)
            count += 1
        return indexes

    def count_unique(self, document_dictionary):
        count = 0
        for term in document_dictionary:
            if document_dictionary[term] == 1:
                count += 1
        return count

    def update_posting_file(self):
        # columns=["index", "doc #", "freq", "location_list", "unique #"]
        try:
            df = pd.read_json(self.config.savePostingFile)
        except:
            df = pd.DataFrame(self.postingDict.values(),columns=['doc#', 'freq', 'location_list', 'n', 'unique num of words'])


        for term in self.updated_terms:
            index_in_posting_file = self.inverted_idx[term][2]
            line = pd.DataFrame(self.postingDict[self.updated_terms[term]])

            df = pd.concat([df.iloc[:index_in_posting_file], line, df.iloc[index_in_posting_file:]]).reset_index(drop=True)
        print(df)

        text_as_json = json.dumps(df.values.tolist())
        print(text_as_json)

