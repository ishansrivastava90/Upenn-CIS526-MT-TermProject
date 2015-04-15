#!/usr/bin/env python
#__author__ = 'ishan'
import sys

"""
gen_best_translations:
Finds the best translation for every src sentences from
n-best list of translations using the specified parameters(lambdas)

all_trans_feat - list of list of list of feature tuples -
[ [ [(s1_t1_f1,v1),(s1_t1_f2,v2)], [(s1_t2_f3,v3),(s1_t2_f4,v4)] ], [ [(s2_t1_f1,v1),(s2_t1_f2,v2)], [(s2_t2_f3,v3),(s2_t2_f4,v4)] ] ]
"""
def gen_best_translations_by_lambda(all_trans, all_trans_feat, src_sen, lambdas, inc_lambdas ):
    num_sents = len(src_sen)

    best_translations = []
    for s_no in xrange(0,num_sents):
        trans_for_one_sent = all_trans[s_no]
        t_feat_for_one_sent = all_trans_feat[s_no]

        (best_score, best) = (-1e300, '')

        for t_no, tran in enumerate(trans_for_one_sent):
            score = 0.0
            for feature in t_feat_for_one_sent[t_no]:
                if inc_lambdas[feature.feat_type]:
                    score += lambdas[feature.feat_type] * float(feature.feat_val)

            if score > best_score:
                (best_score, best) = (score, tran)
        try:
            best_translations.append( best )
        except Exception:
            sys.exit(1)

    return best_translations

