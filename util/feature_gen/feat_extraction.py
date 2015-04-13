#!/usr/bin/env python
__author__ = 'ishan'

from collections import namedtuple
import feat_names
import optparse
from nltk import word_tokenize

def extract_and_format_feat(opts):

    src_sen = [line.strip().split('\t')[1:2] for line in open(opts.trans_data)][1:]
    #ref = [ [reference.strip().split() for reference in line.strip().split('\t')[2:6] ]  for line in open(opts.trans_data)][1:]
    all_trans = [line.strip().split('\t')[6:10] for line in open(opts.trans_data)][1:]
    all_lm_bigram = [line.strip().split('\t')[6:10] for line in open(opts.trans_lm_file)][1:]
    all_lm_trigram = [line.strip().split('\t')[10:14] for line in open(opts.trans_lm_file)][1:]

    all_feats = list()
    feature = namedtuple('feature',['feat_type','feat_val'])

    for s_no in xrange(0,len(src_sen)):
        trans_for_one_sen = all_trans[s_no]
        bigram_for_one_sen = all_lm_bigram[s_no]
        trigram_for_one_sen = all_lm_trigram[s_no]

        trans_list = list()
        for t_no, tran in enumerate(trans_for_one_sen):
            if len(word_tokenize(tran)) < 2 or "NO TRANSLATION FOUND" in tran or "n/a" in tran:
                bigram_for_one_sen[t_no] = -10000
                trigram_for_one_sen[t_no] = -10000

            feat_list = list()
            feat_list.append(feature(feat_names.BIGRAM,float(bigram_for_one_sen[t_no])))
            feat_list.append(feature(feat_names.TRIGRAM,float(trigram_for_one_sen[t_no])))
            trans_list.append(feat_list)

        all_feats.append(trans_list)

    return all_feats



if __name__=="__main__":

    optparser = optparse.OptionParser()
    optparser.add_option("-d", "--trans_data", dest="trans_data", default="../../data/translations.tsv", help="The complete translations data file")
    optparser.add_option("-z", "--trans_lm_file", dest="trans_lm_file", default="../../data/turk_translations_w_logprob_eurparl_2.tsv", help="Language model prob")

    (opts, _) = optparser.parse_args()


    all_trans_feat = extract_and_format_feat(opts)

