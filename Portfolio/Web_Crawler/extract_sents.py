# Tera Parish       txp200011
# Bridgette Bryant  bmb180001

import os
import string
import re
import math
import pickle
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords

VOCAB = set()
NUM_FILE = 0

def create_tf_dict(repo):
    global VOCAB, NUM_FILE
    # create a dictionary for each repo
    tf_dict = {}
    all_tokens = []
    token_set = set()

    for filename in os.listdir(repo):
        with open(os.path.join(repo, filename), 'r') as f:
            raw = f.read()
            # if not an empty file, perform text normalizing
            if (len(raw) > 1):
                NUM_FILE += 1
                # text normalizing
                raw = raw.lower()
                raw = word_tokenize(raw)
                # remove punctuaions, numbers, and stopwords
                tokens = [w for w in raw if w.isalpha() and len(w) > 5 and w not in stopwords]
                all_tokens += tokens

    # get term frequencies
    token_set = set(all_tokens)
    tf_dict = {t: all_tokens.count(t) for t in token_set}
    if (len(VOCAB) == 0):
        VOCAB = token_set
    else:
        VOCAB = VOCAB.union(token_set)

    # normalize tf by number of tokens
    for t in tf_dict.keys():
        tf_dict[t] = tf_dict[t] / len(all_tokens)

    return tf_dict


def create_tfidf(tf, idf):
    tf_idf = {}
    for t in tf.keys():
        tf_idf[t] = tf[t] * idf[t]

    return tf_idf


def extract_sents(term):
    results = []
    for filename in os.listdir('data'):
        with open(os.path.join('data', filename), 'r') as f:
            raw = f.read()
            raw = raw.lower()
            sents = nltk.sent_tokenize(raw)
            results += [s for s in sents if term in s]

    return set(results)


if __name__ == '__main__':
    stopwords = stopwords.words('english')
    stopwords.extend(['subnavigation', 'subnav', 'without', 'within', 'group','cursosingles', 'cursos',
              'online', 'ukrainian', 'russian', 'weather', 'cursosonline', 'videos', 'recent',
              'scripps', 'altformatsonly', 'contact', 'people', 'account', 'crimea', 'copied',
              'feedback', 'fitness', 'beauty', 'fashion', 'football', 'subscribe', 'health', 'newsletters',
              'october', 'friday', 'travel', 'february', 'sports', 'images', 'according', 'careers'])

    # create tf dictionaries
    dem_dict = create_tf_dict('dem_urls_out')
    rep_dict = create_tf_dict('rep_urls_out')
    int_dict = create_tf_dict('int_urls_out')

    # create idf dictionary
    idf_dict = {}
    all_vocab = [dem_dict.keys(), rep_dict.keys(), int_dict.keys()]
    for term in VOCAB:
        temp = ['x' for voc in all_vocab if term in voc]
        idf_dict[term] = math.log((1 + NUM_FILE) / (1 + len(temp)))

    # create tf-idf dictionaries
    tfidf_dem = create_tfidf(dem_dict, idf_dict)
    tfidf_rep = create_tfidf(rep_dict, idf_dict)
    tfidf_int = create_tfidf(int_dict, idf_dict)

    tfidf_dem = sorted(tfidf_dem.items(), key=lambda x: x[1], reverse=True)
    print('From CNN (left-leaning):\n', tfidf_dem[:30])
    tfidf_rep = sorted(tfidf_rep.items(), key=lambda x: x[1], reverse=True)
    print('\nFrom FOX (right-leaning):\n', tfidf_rep[:30])
    tfidf_int = sorted(tfidf_int.items(), key=lambda x: x[1], reverse=True)
    print('\nFrom Wall Street Journal (neutral):\n', tfidf_int[:30])

    # top 10 terms
    top_10 = ['ukraine', 'russia', 'nuclear', 'forces', 'military',
              'troops', 'territory', 'zelensky', 'moscow', 'kherson']

    # extract relevant sentences
    base = {}
    for term in top_10:
        base[term] = list(extract_sents(term))

    # pickle the dictionary
    pickle.dump(base, open('base.pickle', 'wb'))