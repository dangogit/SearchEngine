import json
import os
import time
import traceback

from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
import pandas as pd
import utils

from datetime import datetime

def run_engine():
    """

    :return:
    """

    config = ConfigClass()
    r = ReadFile(corpus_path=config.get__corpusPath())
    p = Parse()
    indexer = Indexer(config)
    fmt = '%Y-%m-%d %H:%M:%S'
    parsed_files_names = []
    idx = 0
    print(datetime.now())
    print("[" + str(datetime.now()) + "] " + "Reading files...")
    d1 = datetime.strptime(datetime.now().strftime(fmt), fmt)
    d1_ts = time.mktime(d1.timetuple())

    for subdir, dirs, files in os.walk(r.corpus_path):
        for dir in dirs:
            new_path = r.corpus_path + "\\" + dir
            for subdir, dirs, files in os.walk(new_path):
                for filename in files:
                    if ".parquet" in filename:
                        new_path = new_path + "\\" + filename
                        tweet_list = r.read_file(new_path)  #holds list of the tweets as text
                        idx = parse_and_index_tweet_list(tweet_list, fmt, p, indexer, filename, parsed_files_names, idx)


    # testing:
    d2 = datetime.strptime(datetime.now().strftime(fmt), fmt)
    d2_ts = time.mktime(d2.timetuple())
    print("[" + str(datetime.now()) + "] " + "Finished Parsing and Indexing documents in " + str(float(d2_ts - d1_ts) / 60) + " minutes")

    fix_big_small_letters_in_documents(fmt, p, parsed_files_names)

    print("[" + str(datetime.now()) + "] " + "Saving data...")
    utils.save_obj(indexer.inverted_idx, "inverted_idx")
    utils.save_obj(indexer.postingDict, "posting")

def parse_and_index_tweet_list(tweet_list, fmt, p, indexer, filename, parsed_files_names, idx):
    parsed_tweets = {}
    print("[" + str(datetime.now()) + "] " + "Parsing and Indexing documents in file: "+ filename)
    d1 = datetime.strptime(datetime.now().strftime(fmt), fmt)
    d1_ts = time.mktime(d1.timetuple())

    for document in tweet_list:
        # parse the document
        #before.append(document[2])
        p.curr_idx = idx
        parsed_document = p.parse_doc(document)
        parsed_tweets[idx]=parsed_document
        #add the doucment to indexer here
        #indexer.add_new_doc(parsed_document, idx)
        idx += 1

    new_filename = filename.replace(".snappy.parquet", ".json")
    with open(new_filename, 'w', encoding='utf-8') as parsed_file:
        json.dump(parsed_tweets, parsed_file)
        parsed_files_names.append(new_filename)


    print("[" + str(datetime.now()) + "] " + "Finished Parsing and Indexing documents in file: " + filename)
    d2 = datetime.strptime(datetime.now().strftime(fmt), fmt)
    d2_ts = time.mktime(d2.timetuple())
    print(str(float(d2_ts - d1_ts)) + " seconds")

    return idx

def fix_big_small_letters_in_documents(fmt, p, parsed_files_names):
    print("[" + str(datetime.now()) + "] " + "Fixing big&small letters in all documents...")
    d1 = datetime.strptime(datetime.now().strftime(fmt), fmt)
    d1_ts = time.mktime(d1.timetuple())
    parsed_tweets_dict = {}
    for filename in parsed_files_names:
        try:
            with open(filename, 'r', encoding='utf-8') as parsed_file:
                parsed_tweets_dict = json.load(parsed_file)
        except:
            traceback.print_exc()
        for index in parsed_tweets_dict.keys():
            if int(index) in p.tweets_with_terms_to_fix.keys():
                parsed_tweets_dict[index][2] = p.fix_word_with_future_change(int(index), parsed_tweets_dict[index][2])
        # to json:
        try:
            with open(filename, 'w', encoding='utf-8') as parsed_file:
                json.dump(parsed_tweets_dict, parsed_file)

        except:
            traceback.print_exc()

    d2 = datetime.strptime(datetime.now().strftime(fmt), fmt)
    d2_ts = time.mktime(d2.timetuple())
    print("[" + str(datetime.now()) + "] " + "Finished fixing documents in "+str(float(d2_ts - d1_ts) / 60) + " minutes")

def main(corpus_path, output_path, stemming, queries, num_docs_to_retrieve):
    '''
    corpus_path - הנתיב של הקורפוס
    output_path - הנתיב של הפלט שלכם
    stemming - משתנה בוליאני.
    queries- צריך לתמוך בשתי אפשרויות, קובץ של שאילתות בו כל שורה מהווה שאילתא (יסופק לכם קובץ לדוגמא) או רשימה (list) של שאילתות כך שכל איבר ברשימה יהווה שאילתא.
    num_docs_to_retrieve - מספר מסמכים להחזרה עבור כל שאילתא.
    '''
    return


def load_index():
    print('Load inverted index')
    inverted_index = utils.load_obj("inverted_idx")
    return inverted_index


def search_and_rank_query(query, inverted_index, k):
    p = Parse()
    query_as_list = p.parse_sentence(query)
    searcher = Searcher(inverted_index)
    relevant_docs = searcher.relevant_docs_from_posting(query_as_list)
    ranked_docs = searcher.ranker.rank_relevant_doc(relevant_docs)
    return searcher.ranker.retrieve_top_k(ranked_docs, k)


def main():
    run_engine()
    query = input("Please enter a query: ")
    k = int(input("Please enter number of docs to retrieve: "))
    inverted_index = load_index()
    for doc_tuple in search_and_rank_query(query, inverted_index, k):
        print('tweet id: {}, score (unique common words with query): {}'.format(doc_tuple[0], doc_tuple[1]))
