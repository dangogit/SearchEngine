import os
import pandas as pd


class ReadFile:
    def __init__(self, corpus_path):
        self.corpus_path = corpus_path

    def read_file(self, file_name,counter):
        """
        This function is reading a parquet file contains several tweets
        The file location is given as a string as an input to this function.
        :param file_name: string - indicates the path to the file we wish to read.
        :return: a dataframe contains tweets.
        """
        full_path = os.path.join(self.corpus_path, file_name)
        df = pd.read_parquet(full_path, engine="pyarrow")
        new_path=r"C:\Users\dorle\Data\test"+str(counter)+".csv"
        df.to_csv(new_path)
        #read parquet and convert to csv file
        #df.write.csv('C:\Users\dorle')

        return df.values.tolist()

    def Read_Files(self,rootdir):
        counter=1
        # main directory where the data sits
        for subdir, dirs, files in os.walk(rootdir):
            for dir in dirs:
                new_path = rootdir + "\\" + dir
                for subdir, dirs, files in os.walk(new_path):
                    for filename in files:
                        if ".parquet" in filename:
                            new_path = new_path + "\\" + filename;
                            self.read_file(new_path,counter)
                            counter+=1


