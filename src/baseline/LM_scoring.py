#!/usr/bin/env python

## Outputs the sentence with the best LM score.
## BLEU score : 0.2462
import optparse
from numpy import argmax,argmin,mean
from nltk import word_tokenize;
from math import exp

optparser = optparse.OptionParser()
optparser.add_option("-i", "--input", dest="input", default="../../data/turk_translations_w_logprob_eurparl_2.tsv", help="MTurk translations file with language model probabilities")


opts = optparser.parse_args()[0]


wbp = 0.1 ;
wtp = 0.9;

all_hyps = [line.split('\t')[2:] for line in open(opts.input)]

for (ind,hyp) in enumerate(all_hyps[1:]) :
    sents = hyp[0:4];
    avg_len = mean([len(s) for s in sents ]);
    penalty = [ exp(abs(len(s)-avg_len)*1.0 / avg_len) for s in sents ]
    bprob = [ float(h)*penalty[ind] for (ind,h) in enumerate(hyp[4:8]) ];
    tprob = [ float(h)*penalty[ind] for (ind,h) in enumerate(hyp[8:12]) ];

    #bprob = [ float(h) for h in hyp[4:8] ];
    #tprob = [ float(h) for h in hyp[8:12] ];
    for (ind,sent) in enumerate(sents) :
         if len(word_tokenize(sent)) < 2 or "NO TRANSLATION FOUND" in sent or "n/a" in sent:
             bprob[ind] = -10000;
             tprob[ind] = -10000;

    max_ind = argmax( [ (wbp*b+ wtp*t) for (b,t) in zip(bprob, tprob) ] );  
    print sents[max_ind];
