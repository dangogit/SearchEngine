import os
import time

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
    number_of_documents = 0
    tweet_list =[]
    parsed_tweets = []
    config = ConfigClass()
    r = ReadFile(corpus_path=config.get__corpusPath())
    p = Parse()
    indexer = Indexer(config)
    fmt = '%Y-%m-%d %H:%M:%S'

    print(datetime.now())
    print("Reading files...")
    d1 = datetime.strptime(datetime.now().strftime(fmt), fmt)
    d1_ts = time.mktime(d1.timetuple())
    for subdir, dirs, files in os.walk(r.corpus_path):
        for dir in dirs:
            new_path = r.corpus_path + "\\" + dir
            for subdir, dirs, files in os.walk(new_path):
                for filename in files:
                    if ".parquet" in filename:
                        new_path = new_path + "\\" + filename;
                        documents_list = r.read_file(new_path)  #holds list of the tweets as text

                        tweet_list += documents_list

    del documents_list
    print("Finished reading files.")
    d2 = datetime.strptime(datetime.now().strftime(fmt), fmt)
    d2_ts = time.mktime(d2.timetuple())
    print(str(float(d2_ts-d1_ts)) + " seconds")
    total = len(tweet_list)
    print("Parsing and Indexing documents...")
    d1 = datetime.strptime(datetime.now().strftime(fmt), fmt)
    d1_ts = time.mktime(d1.timetuple())
    keeper = 0
    for idx, document in enumerate(tweet_list):
        # parse the document
        #before.append(document[2])
        p.curr_idx = idx
        parsed_document = p.parse_doc(document)
        parsed_tweets.append(parsed_document)
        tweet_list[idx] = None
        number_of_documents += 1
        if int(float(number_of_documents + 1) / float(total) * 100) > keeper:
            keeper = int(float(number_of_documents + 1) / float(total) * 100)
            print("progress: " + str(keeper) + "%")
            d2 = datetime.strptime(datetime.now().strftime(fmt), fmt)
            d2_ts = time.mktime(d2.timetuple())
            print(str(float(d2_ts - d1_ts) / 60) + " minutes")
        #add the doucment to indexer here
        #indexer.add_new_doc(parsed_document, idx)

    print("Finished Parsing and Indexing documents")
    d2 = datetime.strptime(datetime.now().strftime(fmt), fmt)
    d2_ts = time.mktime(d2.timetuple())
    print(str(float(d2_ts - d1_ts) / 60) + " minutes")

    number_of_documents = 0
    print("Fixing big&small letters in documents...")
    d1 = datetime.strptime(datetime.now().strftime(fmt), fmt)
    d1_ts = time.mktime(d1.timetuple())
    keeper = 0
    for idx, parsed_document in enumerate(parsed_tweets):
        p.curr_idx = idx
        if idx in p.tweets_with_terms_to_fix.keys():
            parsed_document.full_text = p.fix_word_with_future_change(idx, parsed_document.full_text)

        #after.append(parsed_document.full_text)
        # index the document data
        #indexer.add_new_doc(parsed_document, idx)

        number_of_documents += 1
        if int(float(number_of_documents + 1) / float(total) * 100) > keeper:
            keeper = int(float(number_of_documents + 1) / float(total) * 100)
            print("progress: " + str(keeper) + "%")

    print("Finished fixing documents")
    d2 = datetime.strptime(datetime.now().strftime(fmt), fmt)
    d2_ts = time.mktime(d2.timetuple())
    print(str(float(d2_ts - d1_ts) / 60) + " minutes")
    # testing:
    print("Saving data...")
    utils.save_obj(indexer.inverted_idx, "inverted_idx")
    utils.save_obj(indexer.postingDict, "posting")

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
