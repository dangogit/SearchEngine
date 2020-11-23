import time
from datetime import datetime
import pandas as pd
import json
class Indexer:

    def __init__(self, config, word_dict):
        self.inverted_idx = {}
        self.postingDict = {}
        self.config = config
        self.word_dict = word_dict
        self.key = 0
        self.curr = 0
        self.term_index = 0
        #self.updated_terms = {}

    def add_new_doc(self, document, doc_idx):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """
        document_dictionary = document.term_doc_dictionary
        # Go over each term in the doc
        for term in document_dictionary.keys():
            try:
                if not term.isalpha():
                    continue
                    #find term freq in doc
                if term.lower() in self.word_dict.keys():
                    freq = self.word_dict[term.lower()]
                elif term in self.word_dict.keys():
                    freq = self.word_dict[term]
                else:
                    self.word_dict[term] = 1
                    freq = 1

                # Update inverted index and posting
                if term not in self.inverted_idx.keys():
                    number_of_docs = 1
                    index_in_post = self.key
                    self.term_index+=1
                    term_index = self.term_index
                else:
                    number_of_docs = self.inverted_idx[term][1] + 1
                    index_in_post = self.inverted_idx[term][3]
                    term_index = self.inverted_idx[term][0]

                self.inverted_idx[term] = (term_index, number_of_docs, freq, index_in_post)
                self.inverted_idx = sorted(self.inverted_idx)
                print(self.inverted_idx)

                self.postingDict[self.curr] = [term_index, doc_idx, document_dictionary[term], self.index_term_in_text(term, document.full_text), document.doc_length, self.count_unique(document_dictionary)]
            except:
                print('problem with the following key {}'.format(term))


            self.key += 1
            #self.updated_terms[term] = self.curr
            self.curr += 1

            if self.curr==1000000:
                self.update_posting_file()
                self.curr = 0
                #self.updated_terms.clear()
                self.postingDict.clear()

    def index_term_in_text(self, term, text):
        indexes = []
        count = 0
        spllited_text = text.split()
        for word in spllited_text:
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
        #'term_index' , 'doc#', 'freq', 'location_list', 'n', 'unique num of words'
        print("updating posting file")
        fmt = '%Y-%m-%d %H:%M:%S'
        d1 = datetime.strptime(datetime.now().strftime(fmt), fmt)
        d1_ts = time.mktime(d1.timetuple())
        print("loading json")
        try:
            df = pd.read_json("posting_file.json", lines=True)
            df.columns = ['1', '2', '3', '4', '5', '6']
        except:
            df = pd.DataFrame(self.postingDict.values(), columns=['1', '2', '3', '4', '5', '6'])
            df.to_json("posting_file.json", orient='records', lines=True)
            return
        df2 = pd.DataFrame(self.postingDict.values(), columns=['1', '2', '3', '4', '5', '6'])
        df3 = pd.concat([df, df2]).sort_values(by=['1', '2'], ascending=True)
        #for term in self.updated_terms:
            #index_in_posting_file = self.inverted_idx[term][2]+self.inverted_idx[term][0]-1
            #line = pd.DataFrame([self.postingDict[self.updated_terms[term]]], columns=['1', '2', '3', 'l4', '5', '6', '7'])
            #print("concat:")
            #print(datetime.now())
            #df = pd.concat([df.iloc[:index_in_posting_file], line, df.iloc[index_in_posting_file:]]).reset_index(drop=True)
            #print(datetime.now())
        df3.to_json("posting_file.json", orient='records', lines=True)
        d2 = datetime.strptime(datetime.now().strftime(fmt), fmt)
        d2_ts = time.mktime(d2.timetuple())
        print(str(int(d2_ts-d1_ts)) + " seconds")
