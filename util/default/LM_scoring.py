#!/usr/bin/env python

#############################################################
## Default System.
## Outputs the sentence with the best LM score.

import optparse
from numpy import argmax


optparser = optparse.OptionParser()
optparser.add_option("-i", "--input", dest="input", default="../../data/turk_translations_w_logprob.tsv", help="MTurk translations file with language model probabilities")
(opts,_) = optparser.parse_args()

wbp = 0.5 ;
wtp = 0.5;

all_hyps = [line.split('\t')[2:] for line in open(opts.input)]
for hyp in all_hyps[1:] :
    bprob = [ float(h) for h in hyp[4:8] ];
    tprob = [ float(h) for h in hyp[8:12] ];
    max_ind = argmax( [ (wbp*b+ wtp*t) for (b,t) in zip(bprob, tprob) ] );  
    sents = hyp[0:4];
    print sents[max_ind];
