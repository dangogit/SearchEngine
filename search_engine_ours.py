import csv
import json
import os
import time
import traceback
#a

#asdasd
from Search_Engine.reader import ReadFile
from Search_Engine.configuration import ConfigClass
from Search_Engine.parser_module import Parse
from Search_Engine.indexer import Indexer
from Search_Engine.searcher import Searcher
from Search_Engine.stemmer import Stemmer
import pandas as pd
import utils
import sys
from nltk.corpus import stopwords

from datetime import datetime


def run_engine(corpus_path=None, output_path="posting", stemming=False):
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
    idx = 0

    total_num_of_docs = 0

    for subdir, dirs, files in os.walk(r.corpus_path):
        for dir in dirs:
            new_path = r.corpus_path + "\\" + dir
            for subdir, dirs, files in os.walk(new_path):
                for filename in files:
                    if ".parquet" in filename:
                        new_path = new_path + "\\" + filename
                        tweet_list = r.read_file(new_path)  # holds list of the tweets as text
                        idx = parse_and_index_tweet_list(tweet_list, p, indexer, idx)
                        total_num_of_docs += idx

    #for i in range(len(indexer.letters_dict)):
    #    indexer.update_inv_file(i)
    #    indexer.fix_inverted_files(i)
    #    indexer.update_posting_file(i)
    #    # indexer.fix_posting_files(i)


    return total_num_of_docs, p


def parse_and_index_tweet_list(tweet_list, p, indexer, idx):
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
        indexer.set_idx(idx)
        indexer.add_new_doc(parsed_document)
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

def main(corpus_path, output_path, stemming, queries, num_docs_to_retrieve):
    '''
    corpus_path - הנתיב של הקורפוס
    output_path - הנתיב של הפלט שלכם
    stemming - משתנה בוליאני.
    queries.txt- צריך לתמוך בשתי אפשרויות, קובץ של שאילתות בו כל שורה מהווה שאילתא (יסופק לכם קובץ לדוגמא) או רשימה (list) של שאילתות כך שכל איבר ברשימה יהווה שאילתא.
    num_docs_to_retrieve - מספר מסמכים להחזרה עבור כל שאילתא.
    '''
    output_path += '\\'
    total_num_of_docs, p = run_engine(corpus_path, output_path, stemming)
    #print("total number of docs " + str(total_num_of_docs))
    search_and_rank_query(p, queries, num_docs_to_retrieve, total_num_of_docs)


#def load_index():
#    #print('Load inverted index')
#    return utils.load_inverted_index()


def search_and_rank_query(p, queries, k, total_num_of_docs):
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

        final_dict, doc_id_list, file_indexer_dict = searcher._relevant_docs_from_posting(query_as_list, total_num_of_docs)
        ranked_docs_list, ranked_docs_dict = searcher.ranker.rank_relevant_doc(final_dict, doc_id_list,
                                                                               query_as_list, file_indexer_dict)
        ranked_docs_list_top_k = searcher.ranker.retrieve_top_k(ranked_docs_list, k)
        results_dict = {p.doc_idx_tweet_id[k]: ranked_docs_dict[k] for k in ranked_docs_list_top_k}
        if len(results_dict) > 0:
            with open('results.csv', 'a') as csv_file:
                for key, value in sorted(results_dict.items(), key=lambda x: x[1], reverse=True):
                    res_line = "Tweet id: {" + str(key) + "} Score: {" + str(value) + "}"
                    csv_file.write(res_line +"\n")  # query_num, tweet_id, rank
                    print(res_line)
        return sorted(results_dict.items())

def main2():
    total_num_of_docs,p = run_engine()
    query = input("Please enter a query: ")
    k = int(input("Please enter number of docs to retrieve: "))
    # inverted_index = load_index()
    for doc_tuple in search_and_rank_query(p,ConfigClass.savedFileMainFolder,query, k, total_num_of_docs):
        print('tweet id: {}, score (unique common words with query): {}'.format(doc_tuple[0], doc_tuple[1]))
