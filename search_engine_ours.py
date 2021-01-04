import csv
import json
import os
import time
import traceback

from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
from stemmer import Stemmer
import pandas as pd
import utils
import sys
from nltk.corpus import stopwords

from datetime import datetime
class SearchEngine:

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation, but you must have a parser and an indexer.
    def __init__(self, config=None):
        self._config = config
        self._parser = Parse()
        self._indexer = Indexer(config)
        self._model = None

    def run_engine(self, corpus_path=None, output_path="posting", stemming=False):
        """

        :return:
        """

        if not os.path.isdir(output_path):
            os.mkdir(output_path)

        config = ConfigClass()
        r = ReadFile(corpus_path=corpus_path)
        p = Parse()
        if stemming:
            p.steamer = Stemmer()
        indexer = Indexer(config, output_path, p)
        #fmt = '%Y-%m-%d %H:%M:%S'
        idx = 0
        #print(datetime.now())
        #print("[" + str(datetime.now()) + "] " + "Reading files...")
        #d1 = datetime.strptime(datetime.now().strftime(fmt), fmt)
       # d1_ts = time.mktime(d1.timetuple())

        total_num_of_docs = 0

        for subdir, dirs, files in os.walk(r.corpus_path):
            for dir in dirs:
                new_path = r.corpus_path + "\\" + dir
                for subdir, dirs, files in os.walk(new_path):
                    for filename in files:
                        if ".parquet" in filename:
                            new_path = new_path + "\\" + filename
                            tweet_list = r.read_file(new_path)  # holds list of the tweets as text
                            idx = self.parse_and_index_tweet_list(tweet_list, p, indexer, idx)
                            total_num_of_docs += idx
    #
        #
        #d2 = datetime.strptime(datetime.now().strftime(fmt), fmt)
        #d2_ts = time.mktime(d2.timetuple())
        #print("[" + str(datetime.now()) + "] " + "Finished Parsing and Indexing documents in " + str(
         #   float(d2_ts - d1_ts) / 60) + " minutes")

       # print("[" + str(datetime.now()) + "] " + "Fixing inverted files...")
        #d1 = datetime.strptime(datetime.now().strftime(fmt), fmt)
        #d1_ts = time.mktime(d1.timetuple())

        for i in range(len(indexer.letters_dict)):
            indexer.update_inv_file(i)
            indexer.fix_inverted_files(i)
            indexer.update_posting_file(i)
            # indexer.fix_posting_files(i)

        # testing:
        #d2 = datetime.strptime(datetime.now().strftime(fmt), fmt)
        #d2_ts = time.mktime(d2.timetuple())
        #print("[" + str(datetime.now()) + "] " + "Finished fixing inverted files in " + str(
         #   float(d2_ts - d1_ts) / 60) + " minutes")

        # fix_big_small_letters_in_documents(output_path, fmt, p, parsed_files_names)

        return total_num_of_docs, p


    def parse_and_index_tweet_list(self, tweet_list, p, indexer, idx):
       # print("[" + str(datetime.now()) + "] " + "Parsing and Indexing documents in file: " + filename + " " + str(
        #    sys.getsizeof(tweet_list) / 1000000) + "mb")
        #d1 = datetime.strptime(datetime.now().strftime(fmt), fmt)
        #d1_ts = time.mktime(d1.timetuple())

        for document in tweet_list:
            # parse the document
            p.curr_idx = idx
            parsed_document = p.parse_doc(document)
            # parsed_tweets[idx] = parsed_document
            # add the doucment to indexer here
            indexer.add_new_doc(parsed_document, idx)
            idx += 1

        #new_filename = filename.replace(".snappy.parquet", ".json")

        # with open(output_path + "/Parsed_files/" + new_filename, 'w', encoding='utf-8') as parsed_file:
        #   json.dump(parsed_tweets, parsed_file)
        # parsed_files_names.append(new_filename)

        # with open(output_path + "/Parsed_files/words_to_fix_" + new_filename, 'w', encoding='utf-8') as fix_file:
        #  json.dump(p.tweets_with_terms_to_fix, fix_file)
        #   p.tweets_with_terms_to_fix.clear()

        #print("[" + str(datetime.now()) + "] " + "Finished Parsing and Indexing documents in file: " + filename)
        #d2 = datetime.strptime(datetime.now().strftime(fmt), fmt)
        #d2_ts = time.mktime(d2.timetuple())
        #print(str(float(d2_ts - d1_ts) / 60) + " minutes")

        return idx

    def main(self, corpus_path, output_path, stemming, queries, num_docs_to_retrieve):
        '''
        corpus_path - הנתיב של הקורפוס
        output_path - הנתיב של הפלט שלכם
        stemming - משתנה בוליאני.
        queries.txt- צריך לתמוך בשתי אפשרויות, קובץ של שאילתות בו כל שורה מהווה שאילתא (יסופק לכם קובץ לדוגמא) או רשימה (list) של שאילתות כך שכל איבר ברשימה יהווה שאילתא.
        num_docs_to_retrieve - מספר מסמכים להחזרה עבור כל שאילתא.
        '''
        output_path += '\\'
        total_num_of_docs, p = self.run_engine(corpus_path, output_path, stemming)
        #print("total number of docs " + str(total_num_of_docs))
        self.search_and_rank_query(p, output_path, queries, num_docs_to_retrieve, total_num_of_docs)


    def load_index(self):
        #print('Load inverted index')
        return utils.load_inverted_index()


    def search_and_rank_query(self, p, output_path, queries, k, total_num_of_docs):
        searcher = Searcher()
        queries_list = []
        if isinstance(queries, list):
            queries_list = queries
        else:
            with open(queries, 'r', encoding='utf-8') as query_file:
                queries_lists = [line.split('\n') for line in query_file.readlines() if line != '\n']
                for query in queries_lists:
                    queries_list.extend(query)

        with open('results.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)

        for query in queries_list:
            if len(query) <= 1:
                continue
            query_as_list = query.split()
            final_dict, doc_id_list = searcher.relevant_docs_from_posting(output_path, query_as_list, total_num_of_docs)
            ranked_docs_list, ranked_docs_dict = searcher.ranker.rank_relevant_doc(final_dict, doc_id_list,
                                                                                   query_as_list)
            ranked_docs_list_top_k = searcher.ranker.retrieve_top_k(ranked_docs_list, k)
            results_dict = {p.doc_idx_tweet_id[k]: ranked_docs_dict[k] for k in ranked_docs_list_top_k}
            if len(results_dict) > 0:
                with open('results.csv', 'a') as csv_file:
                    for key, value in sorted(results_dict.items(), key=lambda x: x[1], reverse=True):
                        res_line = "Tweet id: {" + str(key) + "} Score: {" + str(value) + "}"
                        csv_file.write(res_line +"\n")  # query_num, tweet_id, rank
                        print(res_line)

    def main2(self):
        total_num_of_docs = self.run_engine()
        query = input("Please enter a query: ")
        k = int(input("Please enter number of docs to retrieve: "))
        # inverted_index = load_index()
        for doc_tuple in self.search_and_rank_query(query, k, total_num_of_docs):
            print('tweet id: {}, score (unique common words with query): {}'.format(doc_tuple[0], doc_tuple[1]))
