#!/usr/bin/env python
__author__ = 'ishan'

import sys,os
from collections import namedtuple
from collections import defaultdict

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'model_gen'))
import lm_gen

def parse_references_from_file(filename):
    reference = namedtuple("reference", "id, ldc1, ldc2, ldc3, ldc4")

    total_references = []
    # all_hyps = [pair.split(' ||| ') for pair in open(opts.input)][0:opts.n]
    for line in open(filename):
        ln_split = line.strip().split("\t")

        total_references.append(reference(ln_split[0], ln_split[1], ln_split[2], ln_split[3], ln_split[4]))
    return total_references

# print len(parse_references_from_file("../../data/training/LDCtranslations.tsv"))

def parse_translations_from_file(filename):
    translation = namedtuple("translation", "id, src, turk_translation, bigram_prob, trigram_prob")
    # translation = namedtuple("translation", "id, src, turk_translation, bigram_prob, trigram_prob, worker_id")

    total_translations = []
    # all_hyps = [pair.split(' ||| ') for pair in open(opts.input)][0:opts.n]

    # For skipping header
    count = 0
    for line in open(filename):
        if count == 0:
            count = 1
            continue
        ln_split = line.strip().split("\t")

        prob_zip = zip(ln_split[2:6], ln_split[6:10], ln_split[10:14])
        # prob_zip = zip(ln_split[2:6], ln_split[6:10], ln_split[10:14], ln_split[14:18])
        # print "prob_zip {}".format(prob_zip)
        translations = [translation(ln_split[0], ln_split[1], pair[0], float(pair[1]), float(pair[2])) for pair in prob_zip]
        # translations = [translation(ln_split[0], ln_split[1], pair[0], float(pair[1]), float(pair[2]), pair[3]) for pair in prob_zip]
        total_translations.extend(translations)
        # break
    return total_translations

# print parse_translations_from_file("../../data/turk_translations_w_logprob_eurparl_2.tsv")
# print len(parse_translations_from_file("../../data/training/turk_translations_w_logprob_eurparl_2.tsv"))

# """
# Parsing all the translations and metadata from
# the file and returning a dict with translation
# key id
# """
# def parse_from_file(file_n):
#     f = open(file_n)

#     translations = namedtuple("translations",["src","turk_trans", "turk_md"])
#     trans_dict = defaultdict()

#     # Reading all the lines from the file
#     for ln in f.readlines():
#         ln_split = ln.strip().split("\t")

#         ldc_lst = list()
#         for tran in ln_split[2:6]:
#             ldc_lst.append(tran)

#         turk_lst = list()
#         for tran in ln_split[6:10]:
#             turk_lst.append(tran)

#         turk_md = list()
#         for tran in ln_split[10:]:
#             turk_md.append(tran)

#         trans_dict[ln_split[0]] = translations(ln_split[1], ldc_lst, turk_lst, turk_md)
#     f.close()

#     return trans_dict


"""
Generating all the LDC translations and writing
them to a file
"""
def gen_HQ_trans(file_n, file_out):
    f = open(file_n)
    fw = open(file_out,"w")

    # Reading all the lines from the file
    for ln in f.readlines():
        ln_split = ln.strip().split("\t")

        ldc_str = ln_split[0]
        for tran in ln_split[2:6]:
            ldc_str+="\t"+tran
        fw.write(ldc_str+"\n")
    fw.close()
    f.close()

    return


def gen_HQ_trans_with_lmprob(file_n, file_out, lm_file_lst):
    f = open(file_n)
    fw = open(file_out,"w")

    print "Generating HQ translations with Log probabilities"

    header_str = "SegID\tUrdu\tTurk_Translation_1\tTurk_Translation_2\tTurk_Translation_3\tTurk_Translation_4\t"
    header_str += "Bigram_Lprob1\tBigram_Lprob2\tBigram_Lprob3\tBigram_Lprob4\t"
    header_str += "Trigram_Lprob1\tTrigram_Lprob2\tTrigram_Lprob3\tTrigram_Lprob4\n"
    fw.write(header_str)

    # Reading all the lines from the file
    for ln_no,ln in enumerate(f.readlines()[1:]):
        print "Processing ln: "+str(ln_no)
        ln_split = ln.strip().split("\t")

        ldc_str = ln_split[0]+"\t"+ln_split[1]

        logprobs = defaultdict()
        for tran in ln_split[6:10]:
            ldc_str+="\t"+tran
            for lm_file in lm_file_lst:
                if lm_file not in logprobs:
                    logprobs[lm_file] = list()
                logprobs[lm_file].append(lm_gen.get_srilm_logprob_for_sen(lm_file, tran.lower()))

        for lm_file in lm_file_lst:
            for logprob in logprobs[lm_file]:
                ldc_str+="\t"+str(logprob)

        fw.write(ldc_str+"\n")
    fw.close()
    f.close()

    return




