#!/usr/bin/env python

__author__ = 'ishan'
import nltk
import sys

from subprocess import call
from subprocess import check_output

SRILM_ROOT_PATH = "/home/ishan/Git/Repos/Upenn-CIS526-MT-TermProject/util/srilm/"
NGRAM_COUNT = SRILM_ROOT_PATH+"ngram-count"
NGRAM = SRILM_ROOT_PATH+"ngram"

"""
Loading the corpus from nltk into a file with
1 sen per line
"""
def load_corpus_into_file(file_out, corp_type='brown'):

    # Loading all sen into a list
    if corp_type == 'brown':
        loader = nltk.corpus.brown
        all_sents = [sen for sen in loader.sents()]

    #TODO Consider removing rare words ( <5 in whole corpus)

    # Writing into a file
    fw = open(file_out, "w")
    for sent in all_sents:
        sent_str = ""
        for word in sent:
            sent_str += word.lower()+" "

        fw.write(sent_str+"\n")
    fw.close()

    return

"""
Generating n-gram models using srilm library
"""
def generate_model_srilm(text_file, file_out, ngram="2"):

    call([NGRAM_COUNT,"-unk", "-order", ngram, "-cdiscount", "0.75","interpolate", "-text",text_file, "-lm", file_out])
    return


"""
Finding perplexity value for a sen using the
specified model using srilm
"""
def get_srilm_ppl_for_sen(lm_file, sen):
    fobj = open("temp_translation_file.txt","w")
    fobj.write(sen)
    fobj.close()

    command_output= check_output([NGRAM, "-unk","-lm", lm_file, "-ppl","temp_translation_file.txt"])

    for ind,word in enumerate(command_output.split()):
        if word == 'ppl=':
            ppl = command_output.split()[ind+1]
            break

    return float(ppl)


"""
Finding logprob value for a sen using the
specified model using srilm
"""

def get_srilm_logprob_for_sen(lm_file, sen):
    fobj = open("temp_translation_file.txt","w")
    fobj.write(sen)
    fobj.close()

    command_output= check_output([NGRAM, "-unk", "-lm", lm_file, "-ppl","temp_translation_file.txt"])

    logprob = -1* sys.maxint
    for ind,word in enumerate(command_output.split()):
        if word == 'logprob=':
            logprob = command_output.split()[ind+1]
            break

    return float(logprob)
