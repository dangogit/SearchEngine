import os
import pandas as pd
#asdasd
#a

class ReadFile:
    def __init__(self, corpus_path):
        self.corpus_path = corpus_path

    def read_file(self, file_name):
        """
        This function is reading a parquet file contains several tweets
        The file location is given as a string as an input to this function.
        :param file_name: string - indicates the path to the file we wish to read.
        :return: a dataframe contains tweets.
        """
        if self.corpus_path not in file_name:
            file_name = os.path.join(self.corpus_path, file_name)
        #full_path = os.path.join(self.corpus_path, file_name)
        df = pd.read_parquet(file_name, engine="pyarrow")
        return df.values.tolist()

    def Read_Files(self):
        counter = 1
        tweets_list = []  # list of lists where every list represents a single tweet with its components
        # main directory where the data sits
        for subdir, dirs, files in os.walk(self.corpus_path):
            for dir in dirs:
                new_path = self.corpus_path + "\\" + dir
                for subdir, dirs, files in os.walk(new_path):
                    for filename in files:
                        if ".parquet" in filename:
                            new_path = new_path + "\\" + filename;
                            tweets_list.append(self.read_file(new_path, counter))
                            counter += 1
