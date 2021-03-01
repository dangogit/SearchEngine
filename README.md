Search Engine project:

Reader Class:
The department is responsible for reading the files from the corpus path, and sending them as a list of lines, each line representing a tweet in the corpus files.
The class reads each file, converts it to a list of tweets and sends them to the presser class.

Parser Class:
The class has a parse_doc method that receives a tweet as a list of fields, and sends the text field to the main parse_all_text method which receives a text and spreads it out according to the following rules:

1. Clear the words that do not belong to the ascii coding (smileys and unfamiliar signs, etc.) - our addition
Which significantly reduces the amount of irrelevant words in the corpus and the runtime of the Parser and Ranker
2. Clear profit lines
3. Clear the marks (- |, |. |: |! | "| & | (|) | * | + |; |> | <|?)
4. Checking the existence of entities and keeping them in the entity's dictionary according to the instructions given.
5. Clear stop words.
6. Change links (URL) according to the instructions given.
7. HASHTAGS change according to the instructions given.
Change numbers greater than 1000 without units, according to the instructions given.
9. Change numbers smaller than 1000 which contain a fraction, according to the instructions given.
Change words containing percent to% according to the instructions given.
11. Clear words that contain three or more letters in a row - our addition
Which significantly reduces the amount of irrelevant words in the corpus and the runtime of the Parser and Ranker
12. Clear the word ‘rt’ - - our insert
Which significantly reduces the amount of irrelevant actions, since the word appears in a very large amount of tweets and does not give much information so we improved the running time of the Parser and Ranker
* The method also saves every word that is written in small letters, and if a word that is written with a capital first letter but has already appeared as small letters, will change to small letters (according to the instructions given).
The method returns a list of words after passing all of the above rules.
parse_doc obtains the scattered text from the above method and creates an object (document) which contains the fields:
Document (tweet_id, tweet_date, full_text, url, term_dict, doc_length)
The tweet_id field contains the unique ID of the tweet
, tweet_date contains the date the tweet was published
, full_text contains the scattered text returned from the above function
, url contains a link which was tweeted
, term_dict contains a dictionary of words that have returned from the text that is spread out as keys, where for each key (word) the value is the number of its occurrences and the current tweet.
If you choose to use a steamer, then the word will be saved in the dictionary as its root representation according to the Porter Steamer package.
, doc_length The number of words in the scattered text.
The method also creates a dictionary which maps the index values of the tweets to their unique identifier values.
(For example: the first tweet read will be in index 0, and its identifier is 345345345554)

Indexer Class:
The department is responsible for creating an inverted_dict dictionary and posting_dict posting files that will be used to search and rank the documents.
We chose to divide the files by the first letter of each word, to create less heavy files and smaller dictionaries, because the memory of our computers was full and the operating system started performing Virtual memorization which drastically slowed down the performance.
The main method in the add_new_doc class: which gets its tweet and index and performs the following actions on it:
1. Saves Max_tf for the most common word in the tweet text.
Using the insert_term_to_inv_idx_and_post_dict method:
2. Add a value to the relevant inverted_dict dictionary according to the first letter of the word when the key is the word, and the value is a list:
1. The first limb - number_of_docs The number of tweets in which the word has appeared so far.
2. The second member - a list of pairs (list of 2 members) in which the first member is the index of the tweet and the second member is the tf which is calculated by the number of occurrences of the word in the tweet divided by the size of the tweet text.
• The indexes in the list are compressed according to the difference method learned in the lecture.
3. The third limb - the last index of the tweet in which the word appeared (used to calculate the difference method)
3. Add an entry to the relevant posting_dict dictionary according to the first letter of the word where the key is the word + file index (for example (ball 11 and the entry is a list:
1. doc_idx- The tweet index
2. freq_in_doc- The number of times the word appeared in the tweet
3. term_indices - list of indexes of the word in the tweet (our addition, for future use when we want to give more weight to the tweets according to the location of the word in the tweet)
4. document.doc_length- The amount of words in the tweet (our addition, normalizes the amount of word appearance in the tweet divided by the size of the tweet - tf)
5. unique_terms_in_doc- The amount of words that appear only once in a tweet.
After each addition of a word to the above dictionaries, a check of the size of the dictionary is performed.
If the size of the posting_dict dictionary exceeds 4mb, the dictionary is emptied into a json file (added to the end according to the append method)
For every 3 updates of posting_dict to a particular letter, the inverted_dict dictionary of the same letter is also emptied into a json file by the same method.
* We conducted many experiments and found that this is the best ratio to maintain Ram utilization in the 80% range.
That is, the division of the files into letters is very convenient to implement and also very fast because the files remain relatively small.
Finally, after running all the tweets in the repository, the inverted_dict files are updated
The update is performed in such a way that it goes through all the dictionaries inserted in a particular file of a particular letter, and merges all the dictionaries and updates all the entries in them using the merge_inverted_idx_dicts function

Searcher Class:
The department is responsible for sending the relevant files in relation to the given query, those files will go to the Ranker department which will set a rating for each of the screens and return the most relevant k documents.
In building this department our guideline was to return the 2000 most relevant documents in terms of tf rating.
In addition, in inverted_idx we decided to keep for each word in the corpus a list of doc_id in which the word appears.
In order not to waste precious memory in preserving large natural numbers, we used the difference method. In the retrieval phase we retrieve this list and start retrieving the original doc_id again. (By using the recover_doc_id's function).
Finally this class will return a dictionary of the words so that the key is each word and the value is the tf and idf rating for each relevant document.

Ranker Class:
This class is responsible for ranking the relevant documents for the query (which are provided by the Searcher class), meaning that each document will receive a rating based on its suitability and relevance to the given query.
The algorithm works as follows: For each document, a vector is constructed that represents all the words in the query (if they are in the document at all), using the vector length calculations we calculate the cosine angle between the query vector and the document vector.
The ranking of each word in the query will be done by calculation: (number of occurrences of the word in the query / size of the query)
Each word in the document will be ranked according to the tf and idf values that will be returned from the searcher class.
In this class we were required to use an external package that we use for Query Expansion. This package is WordNet.
Its great use is the ability to suggest words with a similar (or opposite) meaning to a given word and thus expand the search range in the Posting and inverted_idx files. In implementing this method we decided to return to each word in the query a maximum of 2 synonyms so as not to thicken the query excessively but rather increase the relevance of the new words.
 We will then retrieve the most relevant documents for the new and extended query.
