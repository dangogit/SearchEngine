import datetime
from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
import utils
from pathlib import Path


def run_engine():
    """

    :return:
    """
    doc_list=[]



    number_of_documents = 0

    config = ConfigClass()
    r = ReadFile(corpus_path=config.get__corpusPath())
    p = Parse()
    indexer = Indexer(config)


    entries = Path(r.corpus_path)
    for entry in entries.iterdir():
        print(entry.name)
        if (entry.is_dir()):
            for inner_entry in entry.iterdir():
                if (Path(inner_entry).suffix == '.parquet'):
                    doc_list.append(inner_entry);

    for i in range (len(doc_list)):
        tmp_list=r.read_file(file_name=doc_list[i])
        for idx, document in enumerate(tmp_list):
            if number_of_documents % 1000000 == 0:
                now=datetime.datetime.now()
            number_of_documents += 1
            parsed_document = p.parse_doc(document, idx, i)
            if number_of_documents%1000000==0:
                print(number_of_documents)
                print("parseing time:'")
                print( datetime.datetime.now()-now)
                now1 = datetime.datetime.now()
                indexer.update_index_data(p.get_global_dict(), p.get_posting_dict())
                print("indexer time:'")
                print(datetime.datetime.now()-now1)
                now = datetime.datetime.now()
    global num_of_tweets
    num_of_tweets=number_of_documents

    print('Finished parsing and indexing. Starting to export files')


    ##documents_list = r.read_file(file_name='sample3.parquet')
    # Iterate over every document in the file


def load_index():
    print('Load inverted index')
    inverted_index = utils.load_obj("inverted_idx")
    return inverted_index


def search_and_rank_query(query, inverted_index, k):
    p = Parse()
    query_as_list = p.tokenized_parse(query)
    searcher = Searcher(inverted_index)
    searcher.set_num_of_docs(num_of_tweets)
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
