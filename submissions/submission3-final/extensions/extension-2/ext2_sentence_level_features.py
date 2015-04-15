#!/usr/bin/env python

from nltk.corpus import brown
from nltk.util import ngrams
from collections import Counter
import optparse
import operator
import math
from operator import add
from numpy import argmin,mean, argmax



def length_penalty(hyp,ref):
    c = len(hyp)
    r = len(ref)

    if c<r:
        return (math.exp(1-(r/float(c)))) #short
    elif c>r:
        return (math.exp(1-(c/float(r))))  #long
    else:
        return (1)	#same length
    #return 0;

def ngram_matches(hyp,n):
    hyp_ngrams = ngrams(hyp,n)
    if n == 2:
        dbsGram= bigrams
    elif n==3:
        dbsGram = trigrams
    elif n==4:
        dbsGram = fourgrams
	
    total_bi = len(dbsGram)
    matched = []

    matched=[ngram for ngram in hyp_ngrams if ngram not in matched and ngram in dbsGram]
	
    matched_len = len((matched))
    percentage = (matched_len/float(total_bi)) *100
    return float(percentage)

"""
Driver code below
"""

optparser = optparse.OptionParser()
optparser.add_option("-i", "--input", dest="input", default="data/turk_translations_w_logprob.tsv", help="MTurk translations file")
optparser.add_option("-n", "--ngram", dest="ngram", default="data/trigram_europarl.srilm", help="Europarl file")

(opts,_) = optparser.parse_args()

all_ngrams = [line.strip().split('\t') for line in open(opts.ngram)]
unigrams = [line[1] for line in all_ngrams[7:301648]]
bigrams= [tuple(line[1].strip().split())for line in all_ngrams[301650:5063124]]
trigrams = [tuple(line[1].split()) for line in all_ngrams[5063127:9047914]]

all_hyps = [line.split('\t')[1:] for line in open(opts.input)]
for (ind,hyp) in enumerate(all_hyps[:10]) :
    sents = hyp[0:5];
    ref = sents[0];
    lp={};
    bigram_match_percent = []
    for (ind,sent) in enumerate(sents[1:5]) :
    	bigram_match_percent.append(ngram_matches(sent,2))

    max_per = argmax(bigram_match_percent)
    print sents[max_per+1];
