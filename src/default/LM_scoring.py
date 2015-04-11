## Outputs the sentence with the best LM score.
## BLEU score : 0.216
import optparse
from numpy import argmax,argmin,mean
from nltk import word_tokenize;
import models,editdistance

optparser = optparse.OptionParser()
optparser.add_option("-i", "--input", dest="input", default="../../data/turk_translations_w_logprob_eurparl.tsv", help="MTurk translations file with language model probabilities")


opts = optparser.parse_args()[0]


wbp = 0.0 ;
wtp = 1.0;

all_hyps = [line.split('\t')[2:] for line in open(opts.input)]

for (ind,hyp) in enumerate(all_hyps[1:]) :
    sents = hyp[0:4];
    bprob = [ float(h) for h in hyp[4:8] ];
    tprob = [ float(h) for h in hyp[8:12] ];
    for (ind,sent) in enumerate(sents) :

         if len(word_tokenize(sent)) <= 2 or "NO TRANSLATION FOUND" in sent:
             bprob[ind] = -10000;
             tprob[ind] = -10000;

    max_ind = argmax( [ (wbp*b+ wtp*t) for (b,t) in zip(bprob, tprob) ] );  
    print sents[max_ind];
