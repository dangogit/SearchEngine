import search_engine

if __name__ == '__main__':
    #search_engine.main()
    search_engine.main(corpus_path = 'testData', output_path='output', stemming=False, queries='queries.txt', num_docs_to_retrieve=10)