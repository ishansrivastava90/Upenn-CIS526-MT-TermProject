from random import *
import os
import pickle
from collections import Counter
from operator import add
import operator

import nltk
from nltk.stem.porter import *

def create_ngram(n, top=2000):
    file = ngram_filemap[n]
    if os.path.isfile(file):
        return pickle.load(open(file))
    n_dict = Counter()
    for src in ["train.100best", "dev+test.100best"]:
        with open("data/" + src, "r") as f:
            for words in [pair.split(' ||| ')[1].lower().split() for pair in f]:
                pres_dict = Counter([tuple(words[i:i+n]) for i in xrange(len(words)+1-n)])
                n_dict = reduce(add, [pres_dict, n_dict])

    for src in ["train.ref", "dev.ref"]:
        with open("data/" + src, "r") as f:
            for words in [pair.lower().split() for pair in f]:
                pres_dict = Counter([tuple(words[i:i+n]) for i in xrange(len(words)+1-n)])
                n_dict = reduce(add, [pres_dict, n_dict])

    fn_dict = dict(sorted(n_dict.items(), key=operator.itemgetter(1), reverse=True)[1:top])
    pickle.dump(fn_dict, open(file, 'wb'))
    return fn_dict


#english_w = set(w.lower() for w in nltk.corpus.words.words())
#pm = PorterStemmer()

# This should accept list of words, not a text sentence
def find_untranslated(text, stem=True):
    if stem == True:
        hyp_w = set(pm.stem(w.lower()) for w in text if w.lower().isalpha())
    else:
        hyp_w = set(w.lower() for w in text if w.lower().isalpha())
    # print "hypw {}".format(hyp_w)
    unusual = hyp_w.difference(english_w)
    return unusual

def vector_diff(vec1, vec2):
    return [vec1[i] - vec2[i] for i in xrange(len(vec1))]

def vector_dot(vec1, vec2):
    return sum([vec1[i] * vec2[i] for i in xrange(0, len(vec1))])

def get_sample(nbest, opts):
    sample = []
    for j in xrange(0, opts.tau):
        # choose two items from nbest s1 and s2
        # if len(nbest) == 0:
        #     print "nbest = {}".format(nbest)
        s1_idx = randint(0, len(nbest)-1)
        s1 = nbest[s1_idx]
        s2_idx = randint(0, len(nbest)-1)
        s2 = nbest[s2_idx]
        # print "sampling s1 {} and s2 {}".format(s1_idx, s2_idx)
        if abs((s1.smoothed_bleu) - (s2.smoothed_bleu)) > opts.alpha:
            if (s1.smoothed_bleu) > (s2.smoothed_bleu):
                sample.append((s1, s2))
            else:
                sample.append((s2, s1))
        else:
            continue
    return sample

    # return [pm.stem(x) for x in text.lower().split()]

def vectorize(feature_space, feature_list):
    return [1 if feature in feature_list else 0 for feature in feature_space]

# unigrams = create_ngram(1)
# bigrams = create_ngram(2)
# trigrams = create_ngram(3)


def vectorize_ngram(hyp, n):
    feature_space = ngram_map[n].keys()
    ngram = dict(Counter([tuple(hyp[i:i+n]) for i in xrange(len(hyp)+1-n)]))
    # print ngram
    return vectorize(feature_space, ngram)

# print vector_diff([1,2,3], [4,5,6])
# print vector_dot([1,2,3], [4,5,6])
# pickle.dump(a, open("unigram.pik", "wb"))
#
# a = ["a", "b", "b", "c"]
# b = Counter([tuple(a[i:i+1]) for i in xrange(len(a)+1-1)])
# print b.keys()
# c = [ "b", "c"]
# #
# # print vectorize(b.keys(), c)
#
# print vectorize_ngram(b.keys(), c, 1)
