#!/usr/bin/env python

## Outputs the sentence with the least edit distance and then the best LM score.
## BLEU score : 0.2849

import optparse
from numpy import mean
from nltk import word_tokenize
from math import exp
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../util', 'feature_gen'))     
import edit_dist_levenshtein

optparser = optparse.OptionParser()
optparser.add_option("-i", "--input", dest="input", default="../../data/turk_translations_w_logprob_eurparl_2.tsv", help="MTurk translations file with language model probabilities")


opts = optparser.parse_args()[0]


wbp = 0.1
wtp = 0.9

all_hyps = [line.split('\t')[2:] for line in open(opts.input)]

for (ind,hyp) in enumerate(all_hyps[1:]) :
    sents = hyp[0:4]
    avg_ln = mean([len(s) for s in sents ])
    penalty = [ exp(abs(len(s)-avg_ln)*1.0 / avg_ln) for s in sents ]
    bprob = [ float(h)*penalty[ind] for (ind,h) in enumerate(hyp[4:8]) ]
    tprob = [ float(h)*penalty[ind] for (ind,h) in enumerate(hyp[8:12]) ]

    #bprob = [ float(h) for h in hyp[4:8] ];
    #tprob = [ float(h) for h in hyp[8:12] ];

    dis =[]
    for s_ind,sent in enumerate(sents) :
         if len(word_tokenize(sent)) <= 2 or "NO TRANSLATION FOUND" in sent:
             bprob[s_ind] = -10000
             tprob[s_ind] = -10000

         dis.append(mean([ edit_dist_levenshtein.levenshteinDistance(s,sent) for s in sents ]))

    # Getting the best 2 ind i.e with lowest edit dist
    dis_sort = dis[:]
    dis_sort.sort()
    max_inds = list()
    for dist in dis_sort[:2]:
        dis_ind = dis.index(dist)
        if dis_ind in max_inds:
            dis[dis_ind] = sys.maxint
        dis_ind = dis.index(dist)
        max_inds.append(dis.index(dist))

    #print dis
    #print max_inds
    
    best_lm_score = -1*sys.maxint
    max_ind = -1
    for m_ind in max_inds:
        if bprob[m_ind]*wbp + tprob[m_ind]*wtp > best_lm_score:
            best_lm_score = bprob[m_ind]*wbp + tprob[m_ind]*wtp
            max_ind = m_ind
    #print max_ind

    print sents[max_ind]
