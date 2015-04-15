#!/usr/bin/env python

from nltk import word_tokenize

'''
The following code of Levenshtein distance is taken from
http://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance
Minor modifcations are made to the code
'''
def levenshteinDistance(s1,s2):
    s1 = word_tokenize(s1)
    s2 = word_tokenize(s2)
    if len(s1) > len(s2):
        s1,s2 = s2,s1
    distances = range(len(s1) + 1)
    for index2,char2 in enumerate(s2):
        newDistances = [index2+1]
        for index1,char1 in enumerate(s1):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(1 + min((distances[index1],
                                             distances[index1+1],
                                             newDistances[-1])))
        distances = newDistances
    return distances[-1]
