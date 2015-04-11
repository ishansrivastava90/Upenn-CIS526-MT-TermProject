#!/usr/bin/env python

#############################################################
## Default System.
## Outputs the first sentence.
import optparse
from numpy import argmax


optparser = optparse.OptionParser()
optparser.add_option("-i", "--input", dest="input", default="data/turk_translations.tsv", help="MTurk translations file")
(opts,_) = optparser.parse_args()


all_hyps = [line.split('\t')[1:] for line in open(opts.input)]
for hyp in all_hyps[1:] :
    sents = hyp[0:4];
    print sents[0];
