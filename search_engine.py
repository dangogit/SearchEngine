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


def run_engine(corpus_path=None, output_path="output", stemming=False):
    """

    :return:
    """

    os.mkdir(output_path + "/Inverted_files")
    os.mkdir(output_path + "/Posting_files")

    config = ConfigClass()
    r = ReadFile(corpus_path=corpus_path)
    p = Parse()
    if stemming:
        p.steamer = Stemmer()
    indexer = Indexer(config, output_path, p)
    fmt = '%Y-%m-%d %H:%M:%S'
    parsed_files_names = []
    idx = 0
    print(datetime.now())
    print("[" + str(datetime.now()) + "] " + "Reading files...")
    d1 = datetime.strptime(datetime.now().strftime(fmt), fmt)
    d1_ts = time.mktime(d1.timetuple())

    total_num_of_docs = 0

    for subdir, dirs, files in os.walk(r.corpus_path):
        for dir in dirs:
            new_path = r.corpus_path + "\\" + dir
            for subdir, dirs, files in os.walk(new_path):
                for filename in files:
                    if ".parquet" in filename:
                        new_path = new_path + "\\" + filename
                        tweet_list = r.read_file(new_path)  # holds list of the tweets as text
                        idx = parse_and_index_tweet_list(output_path, tweet_list, fmt, p, indexer, filename,
                                                         parsed_files_names, idx)
                        total_num_of_docs += idx

    d2 = datetime.strptime(datetime.now().strftime(fmt), fmt)
    d2_ts = time.mktime(d2.timetuple())
    print("[" + str(datetime.now()) + "] " + "Finished Parsing and Indexing documents in " + str(
        float(d2_ts - d1_ts) / 60) + " minutes")

    print("[" + str(datetime.now()) + "] " + "Fixing inverted files...")
    d1 = datetime.strptime(datetime.now().strftime(fmt), fmt)
    d1_ts = time.mktime(d1.timetuple())

    for i in range(len(indexer.letters_dict)):
        indexer.update_inv_file(i)
        indexer.fix_inverted_files(i)
        indexer.update_posting_file(i)
        # indexer.fix_posting_files(i)

    # testing:
    d2 = datetime.strptime(datetime.now().strftime(fmt), fmt)
    d2_ts = time.mktime(d2.timetuple())
    print("[" + str(datetime.now()) + "] " + "Finished fixing inverted files in " + str(
        float(d2_ts - d1_ts) / 60) + " minutes")

    # fix_big_small_letters_in_documents(output_path, fmt, p, parsed_files_names)

    return total_num_of_docs, p


def parse_and_index_tweet_list(output_path, tweet_list, fmt, p, indexer, filename, parsed_files_names, idx):
    parsed_tweets = {}
    print("[" + str(datetime.now()) + "] " + "Parsing and Indexing documents in file: " + filename + " " + str(
        sys.getsizeof(tweet_list) / 1000000) + "mb")
    d1 = datetime.strptime(datetime.now().strftime(fmt), fmt)
    d1_ts = time.mktime(d1.timetuple())

    for document in tweet_list:
        # parse the document
        p.curr_idx = idx
        parsed_document = p.parse_doc(document)
        # parsed_tweets[idx] = parsed_document
        # add the doucment to indexer here
        indexer.add_new_doc(parsed_document, idx)
        idx += 1

    new_filename = filename.replace(".snappy.parquet", ".json")

    # with open(output_path + "/Parsed_files/" + new_filename, 'w', encoding='utf-8') as parsed_file:
    #   json.dump(parsed_tweets, parsed_file)
    # parsed_files_names.append(new_filename)

    # with open(output_path + "/Parsed_files/words_to_fix_" + new_filename, 'w', encoding='utf-8') as fix_file:
    #  json.dump(p.tweets_with_terms_to_fix, fix_file)
    #   p.tweets_with_terms_to_fix.clear()

    print("[" + str(datetime.now()) + "] " + "Finished Parsing and Indexing documents in file: " + filename)
    d2 = datetime.strptime(datetime.now().strftime(fmt), fmt)
    d2_ts = time.mktime(d2.timetuple())
    print(str(float(d2_ts - d1_ts) / 60) + " minutes")

    return idx


def fix_big_small_letters_in_documents(output_path, fmt, p, parsed_files_names):
    print("[" + str(datetime.now()) + "] " + "Fixing big&small letters in all documents...")
    d1 = datetime.strptime(datetime.now().strftime(fmt), fmt)
    d1_ts = time.mktime(d1.timetuple())
    parsed_tweets_dict = {}
    for filename in parsed_files_names:
        try:
            with open(output_path + "/Parsed_files/" + filename, 'r', encoding='utf-8') as parsed_file:
                parsed_tweets_dict = json.load(parsed_file)

            with open(output_path + "/Parsed_files/words_to_fix_" + filename, 'r', encoding='utf-8') as fix_file:
                p.tweets_with_terms_to_fix = json.load(fix_file)
        except:
            traceback.print_exc()

        for index in parsed_tweets_dict.keys():
            if int(index) in p.tweets_with_terms_to_fix.keys():
                parsed_tweets_dict[index][2] = p.fix_word_with_future_change(int(index), parsed_tweets_dict[index][2])
        # to json:
        try:
            with open(output_path + "/Parsed_files/" + filename, 'w', encoding='utf-8') as parsed_file:
                json.dump(parsed_tweets_dict, parsed_file)

        except:
            traceback.print_exc()

    d2 = datetime.strptime(datetime.now().strftime(fmt), fmt)
    d2_ts = time.mktime(d2.timetuple())
    print("[" + str(datetime.now()) + "] " + "Finished fixing documents in " + str(
        float(d2_ts - d1_ts) / 60) + " minutes")


def main(corpus_path, output_path, stemming, queries, num_docs_to_retrieve):
    '''
    corpus_path - הנתיב של הקורפוס
    output_path - הנתיב של הפלט שלכם
    stemming - משתנה בוליאני.
    queries- צריך לתמוך בשתי אפשרויות, קובץ של שאילתות בו כל שורה מהווה שאילתא (יסופק לכם קובץ לדוגמא) או רשימה (list) של שאילתות כך שכל איבר ברשימה יהווה שאילתא.
    num_docs_to_retrieve - מספר מסמכים להחזרה עבור כל שאילתא.
    '''
    total_num_of_docs, p = run_engine(corpus_path, output_path, stemming)
    print("total number of docs " + str(total_num_of_docs))
    search_and_rank_query(p, output_path, queries, num_docs_to_retrieve, total_num_of_docs)


def load_index():
    print('Load inverted index')
    inverted_idx_files_list = ["inverted_idx_a",
                               "inverted_idx_b",
                               "inverted_idx_c",
                               "inverted_idx_d",
                               "inverted_idx_e",
                               "inverted_idx_f",
                               "inverted_idx_g",
                               "inverted_idx_h",
                               "inverted_idx_i",
                               "inverted_idx_j",
                               "inverted_idx_k",
                               "inverted_idx_l",
                               "inverted_idx_m",
                               "inverted_idx_n",
                               "inverted_idx_o",
                               "inverted_idx_p",
                               "inverted_idx_q",
                               "inverted_idx_r",
                               "inverted_idx_s",
                               "inverted_idx_t",
                               "inverted_idx_u",
                               "inverted_idx_v",
                               "inverted_idx_w",
                               "inverted_idx_x",
                               "inverted_idx_y",
                               "inverted_idx_z",
                               "inverted_idx_hashtags"]
    inverted_index = {}
    for filename in inverted_idx_files_list:
        inverted_index.update(utils.load_obj(filename))
    return inverted_index


def search_and_rank_query(p, output_path, queries, k, total_num_of_docs):
    searcher = Searcher()
    i = 1
    if isinstance(queries, list):
        queries_list = queries
    else:
        with open(queries, 'r') as query_file:
            queries_list = [line.split(',') for line in query_file.readlines()]

    for query in queries_list:
        query_as_list = query.split()
        final_dict, doc_id_list = searcher.relevant_docs_from_posting(output_path, query_as_list, total_num_of_docs)
        ranked_docs_list, ranked_docs_dict = searcher.ranker.rank_relevant_doc(final_dict, doc_id_list,
                                                                               query_as_list)
        ranked_docs_list_top_k = searcher.ranker.retrieve_top_k(ranked_docs_list, k)
        results_dict = {p.doc_idx_tweet_id[k]: ranked_docs_dict[k] for k in ranked_docs_list_top_k}
        with open('results', 'a') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in results_dict.items():
                writer.writerow([i, key, value])  # query_num, tweet_id, rank
    i += 1


def main2():
    total_num_of_docs = run_engine()
    query = input("Please enter a query: ")
    k = int(input("Please enter number of docs to retrieve: "))
    # inverted_index = load_index()
    for doc_tuple in search_and_rank_query(query, k, total_num_of_docs):
        print('tweet id: {}, score (unique common words with query): {}'.format(doc_tuple[0], doc_tuple[1]))
