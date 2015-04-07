## Outputs the sentence with the minimum average edit distance

import optparse
from numpy import argmax,argmin,mean
from nltk import word_tokenize;
import models,editdistance

optparser = optparse.OptionParser()
optparser.add_option("-i", "--input", dest="input", default="../../data/turk_translations_w_logprob.tsv", help="MTurk translations file with language model probabilities")
opts = optparser.parse_args()[0]

all_hyps = [line.split('\t')[2:] for line in open(opts.input)]
for (ind,hyp) in enumerate(all_hyps[1:]) :
    sents = hyp[0:4];
    bprob = [ float(h) for h in hyp[4:8] ];
    tprob = [ float(h) for h in hyp[8:12] ];
    dis = [];
    for (ind,sent) in enumerate(sents) :
         dis.append(mean([ editdistance.eval(s,sent) for s in sents ]));
    max_ind = argmin(dis);
    print sents[max_ind];
