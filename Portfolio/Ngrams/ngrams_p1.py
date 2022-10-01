# Tera Parish       txp200011
# Bridgette Bryant

import nltk
import pickle
from nltk import word_tokenize
from nltk import ngrams


def readIn(fileName):
    # open file and read in raw text
    with open(fileName, 'r') as file:
        # remove new line
        raw= file.read().replace('\n', ' ')

    # tokenize
    tokens= word_tokenize(raw)
    unigrams= [w for w in tokens if w.isalpha()]
    bigrams= list(ngram(unigrams, 2))

    # dictionary {word: count}
    uni_dict= {u:unigrams.count(u) for u in set(unigrams)}
    bi_dict= list(ngrams(unigrams, 2))

    return uni_dict, bi_dict


if __name__ == '__main__':

    files= ['LangId.train.English', 'LangId.train.French', 'LangId.train.Italian']
    uni_pickle= ['uni_English.pickle', 'uni_French.pickle', 'uni_Italian.pickle']
    bi_pickle= ['bi_English.pickle', 'bi_French.pickle', 'bi_Italian.pickle']

    # counter for pickling
    i= 0

    for name in files:
        # read in files
        uni, bi= readIn(name)

        # pickle the dictionaries
        pickle.dump(uni, open(uni_pickle[i], 'wb'))
        pickle.dump(bi, open(bi_pickle[i], 'wb'))
        i+= 1
