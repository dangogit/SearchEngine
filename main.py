import search_engine
from reader import ReadFile
from urllib.parse import urlparse


if __name__ == '__main__':
    #search_engine.main()
    #newReader= ReadFile(r"C:\Users\dorle\Data")
    #newReader.Read_Files(newReader.corpus_path)



    parsed=urlparse("https://docs.python.org/3/library/urllib.parse.html",allow_fragments=True)
    print(parsed.path)
