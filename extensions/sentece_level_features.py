from nltk.corpus import brown
from nltk.util import ngrams
from collections import Counter
import optparse
import operator
import math
from operator import add
from numpy import argmin,mean, argmax

#bigrams = ngrams(brown.words(), 2)
#trigrams = ngrams(brown.words(),3)
#fourgrams = ngrams(brown.words(),4)


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
	for l1 in dbsGram:
		for ngram in hyp_ngrams:
			if ngram in matched:
				continue
			else:
				if ngram == l1:
					matched.append(ngram)

	#matched=[]
	#matched= [ngram for l1 in bigrams for ngram in hyp_ngrams if ngram not in matched and ngram == l1]
	matched_len = len((matched))
	#print matched_len
	percentage = (matched_len/float(total_bi)) *100
	return percentage
	
optparser = optparse.OptionParser()
optparser.add_option("-i", "--input", dest="input", default="data/turk_translations_w_logprob.tsv", help="MTurk translations file")
optparser.add_option("-n", "--ngram", dest="ngram", default="data/trigram_europarl.srilm", help="Europarl file")

(opts,_) = optparser.parse_args()

all_ngrams = [line.strip().split('\t') for line in open(opts.ngram)]

unigrams= all_ngrams[301648]
bigrams= all_ngrams[301650:5063124]
trigrams = all_ngrams[5063127:9047914]

all_hyps = [line.split('\t')[1:] for line in open(opts.input)]
for (ind,hyp) in enumerate(all_hyps) :
    sents = hyp[0:5];
    ref = sents[0];
    lp={};
    for (ind,sent) in enumerate(sents[1:5]) :
    	lp[ind+1] = length_penalty(sent, ref);
    	
        
    min_val = sorted(lp.items(), key = operator.itemgetter(1), reverse= True)[0]
    #print min_val
    print sents[min_val[0]];
