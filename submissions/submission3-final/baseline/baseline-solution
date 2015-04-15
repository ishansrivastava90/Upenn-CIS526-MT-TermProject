#!/usr/bin/env python

"""
Uses Lm probs (modified with  avg sen penalty) + avg TER + Length penalty of long and short
Outputs the sentence with the best LM score.

BLEU score : 0.2646
"""
import optparse
import sys
from numpy import mean
from nltk import word_tokenize
from math import exp

optparser = optparse.OptionParser()
optparser.add_option("-i", "--input", dest="trans_lm_file", default="../../data/translations.tsv", help="MTurk translations file with language model probabilities")
optparser.add_option("-f", "--feat", dest="trans_feat", default="../../data/turk_translations_features_5.tsv", help="MTurk translations feature file")
opts = optparser.parse_args()[0]

w_bigram = 0.05
w_trigram = 0.4
w_pen_short = 0.1
w_pen_long = 0.1
w_edit_dist = 0
w_avg_ter = 0.55

all_hyps = [line.split('\t')[6:10] for line in open(opts.trans_lm_file)]
all_feats = [line.strip().split('\t') for line in open(opts.trans_feat)][1:]

for (ind,hyp) in enumerate(all_hyps[1:]):
    sents = hyp[0:4]
    avg_len = mean([len(s) for s in sents ])
    penalty = [ exp(abs(len(s)-avg_len)*1.0 / avg_len) for s in sents ]

    max_ind = -1
    max_score = -1*sys.maxint

    for (t_no,tran) in enumerate(sents) :
        feat_for_one_tran = all_feats[ind][t_no*22:t_no*22+22]

        if len(word_tokenize(tran)) < 2 or "NO TRANSLATION FOUND" in tran or "n/a" in tran:
             feat_for_one_tran[0] = 10000
             feat_for_one_tran[1] = 10000

        score = 0.0
        # Bigram score
        score += -1*float(feat_for_one_tran[0]) * penalty[t_no] * w_bigram

        # Trigram score
        score += -1*float(feat_for_one_tran[1]) * penalty[t_no] * w_trigram

        # Short sen len penalty score
        score += -1*float(feat_for_one_tran[2]) * w_pen_short

        # Long sen len penalty score
        score += -1*float(feat_for_one_tran[3]) * w_pen_long

        # Edit dist penalty score
        score += -1*float(feat_for_one_tran[4]) * w_edit_dist

        # Avg TER score
        score += -1*float(feat_for_one_tran[5]) * w_avg_ter

        if score > max_score:
            max_score = score
            max_ind = t_no

    print sents[max_ind]
