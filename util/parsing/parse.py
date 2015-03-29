#!/usr/bin/env python
__author__ = 'ishan'

from collections import namedtuple
from collections import defaultdict

"""
Parsing all the translations and metadata from
the file and returning a dict with translation
key id
"""
def parse_from_file(file_n):
    f = open(file_n)

    translations = namedtuple("translations",["src","ldc_trans", "turk_trans", "turk_md"])
    trans_dict = defaultdict()

    # Reading all the lines from the file
    for ln in f.readlines():
        ln_split = ln.strip().split("\t")

        ldc_lst = list()
        for tran in ln_split[2:6]:
            ldc_lst.append(tran)

        turk_lst = list()
        for tran in ln_split[6:10]:
            turk_lst.append(tran)

        turk_md = list()
        for tran in ln_split[10:]:
            turk_md.append(tran)

        trans_dict[ln_split[0]] = translations(ln_split[1], ldc_lst, turk_lst, turk_md)
    f.close()

    return trans_dict


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





