#!/usr/bin/env python
__author__ = 'ishan'

from collections import namedtuple
import feat_names
import optparse
from nltk import word_tokenize
from numpy import mean
from math import exp
#from edit_dist_levenshtein import levenshteinDistance


def extract_and_format_feat(opts):

    src_sen = [line.strip().split('\t')[1:2] for line in open(opts.trans_data)][1:]
    #ref = [ [reference.strip().split() for reference in line.strip().split('\t')[2:6] ]  for line in open(opts.trans_data)][1:]
    all_trans = [line.strip().split('\t')[6:10] for line in open(opts.trans_data)][1:]
    all_feats = [line.strip().split('\t') for line in open(opts.trans_feat)][1:]
    # all_lm_bigram = [line.strip().split('\t')[6:10] for line in open(opts.trans_lm_file)][1:]
    # all_lm_trigram = [line.strip().split('\t')[10:14] for line in open(opts.trans_lm_file)][1:]


    all_ext_feats = list()
    feature = namedtuple('feature',['feat_type','feat_val'])

    for s_no in xrange(0,len(src_sen)):
        trans_for_one_sen = all_trans[s_no]
        feat_for_one_sen = all_feats[s_no]
        #trigram_for_one_sen = all_lm_trigram[s_no]

        avg_len = mean([len(st) for st in trans_for_one_sen ])
        penalty = [ exp(abs(len(st)-avg_len)*1.0 / avg_len) for st in trans_for_one_sen ]


        trans_list = list()
        for t_no, tran in enumerate(trans_for_one_sen):
            feat_for_tran = feat_for_one_sen[t_no*22:t_no*22+22]
            if len(word_tokenize(tran)) < 2 or "NO TRANSLATION FOUND" in tran or "n/a" in tran:
                feat_for_tran[0] = 10000
                feat_for_tran[1] = 10000


            # TODO Iterate over all feats & Filter based on inclusion map
            feat_list = list()

            # bigram prob feat with len penalty
            feat_list.append(feature(feat_names.BIGRAM,-1*float(feat_for_tran[0])*penalty[t_no]))

            # trigram prob feat with len penalty
            feat_list.append(feature(feat_names.TRIGRAM,-1*float(feat_for_tran[1])*penalty[t_no]))

            # Short and long sen length penalty
            feat_list.append(feature(feat_names.PENALTY_SHORT,-1*float(feat_for_tran[2])))
            feat_list.append(feature(feat_names.PENALTY_LONG,-1*float(feat_for_tran[3])))

            # Edit dist feat
            #edit_dist = mean([levenshteinDistance(st,tran) for st in trans_for_one_sen ])
            feat_list.append(feature(feat_names.EDIT_DIST,-1*float(feat_for_tran[4])))

            trans_list.append(feat_list)

        all_ext_feats.append(trans_list)

    return all_ext_feats



if __name__=="__main__":

    optparser = optparse.OptionParser()
    optparser.add_option("-d", "--trans_data", dest="trans_data", default="../../data/translations.tsv", help="The complete translations data file")
    optparser.add_option("-f", "--trans_feat", dest="trans_feat", default="../../data/turk_translations_features_5.tsv", help="Translation features")
    #optparser.add_option("-f", "--trans_feat", dest="trans_feat", default="../../data/turk_translations_w_logprob_europarl_c.tsv", help="Language model prob")

    (opts, _) = optparser.parse_args()


    all_trans_feat = extract_and_format_feat(opts)


