#!/usr/bin/env python

## Class to store sentence level features

from  edit_dist_levenshtein import  levenshteinDistance
from math import exp
from numpy import mean
from nltk.util import ngrams
from nltk import word_tokenize

class SegIDInfo:
    FVlength_full = 16;
    FVlength_sent = 8;
 
    def __init__(self, sent):
        tokens = [ t.strip() for t in sent.split('\t')];
        self.tokens = tokens;
        self.segID = tokens[0];
	self.src_sent = tokens[1];
        self.turk_sents = [ t.lower() for t in tokens[2:6] ];
        self.worker_ids = tokens[6:];
        self.bilmprobs = [];
	self.trilmprobs = [];
	self.TER=[];
        self.FV = [];


    def getSegID(self):
        return self.segID;

    def getSourceSentence(self):
        return self.src_sent;

    def getTurkerSentences(self):
        return self.turk_sents;

    def getWorkerIds(self):
        return self.worker_ids;
    
    def getLMprobs(self):
        return [ self.bilmprobs, self.trilmprobs ];

    def setLMprobs(self,lstb,lstt):
        self.bilmprobs = [float(l) for l in lstb];
	self.trilmprobs = [float(l) for l in lstt];

    def getTER(self):
        return self.TER;
    
    def getFinalVector(self):
        return self.FV;

    def setTER(self,lst):
	#print lst;
        self.TER = [float(l) for l in lst];

    def getFinalVectorString(self, w_features, worker_data):
        FVlength_sent = SegIDInfo.FVlength_sent;
        wids = self.worker_ids;
        fv = self.FV;
	wkeys = worker_data.keys();
        fstr = "\t".join( [ t for t in self.tokens[:6] ] );
        fstr2 = "" 
    	for (i,ind) in enumerate(range(0,FVlength_sent*4,FVlength_sent)) :
            vec =  fv[ind:ind+FVlength_sent];
	    w = wids[i];
            if w not in wkeys :
		vec.extend([0.0]*14)
            else :
	    	vec.extend(w_features[w])
	    	vec.extend(worker_data[w])
            fstr2 += "\t" + "\t".join([ str(t) for t in vec ]);  
        return fstr.strip() + "\t" + fstr2.strip();

    def setFinalVector(self, bigrams, trigrams) :

        vec = []; 
	# LM probabilities
        lpb = self.bilmprobs;
	lpt = self.trilmprobs;
	# TER metric
	ter = self.TER;
        #print ter
        ts =  [len(s) for s in self.turk_sents];
        sents = self.turk_sents;
        src = len(self.src_sent);
	
	# Penalties (long and short)
        p_short = [ ( 1.0 - l*1.0/src ) if l < src else 0.0 for l in ts ]
        p_long = [ ( 1.0 - src*1.0/l ) if l > src else 0.0 for l in ts ]
        
	# bigram match percentage
        ngrams2 = [ self.ngram_matches(s,2, bigrams) for s in sents ];

	# trigram match percentage
        ngrams3 = [ self.ngram_matches(s,3, trigrams) for s in sents ];

	# Edit distance       
	edit_dis = [];
        for (ind,sent) in enumerate(sents) :
            edit_dis.append(mean([ levenshteinDistance(s,sent) for s in sents ]));

        for ind in range(len(ts)) :
	    vec.extend( [ lpb[ind], lpt[ind], p_short[ind]*100, p_long[ind]*100, edit_dis[ind], ter[ind]*100, 100-ngrams2[ind], 100-ngrams3[ind]  ] );
		
	vec = [ abs(f) for f in vec ];
        self.FV = vec;  
        
    def ngram_matches(self, hyp,n, ngs):
        tokens = word_tokenize(hyp); 
	if len(tokens)==0 :
		return 0.0	
	hyp_ngrams = ngrams(tokens,n);
	hyp_ngrams = [ ' '.join(str(i) for i in ngram) for ngram in hyp_ngrams ];
	matched = list(set(hyp_ngrams).intersection(ngs));	 
        matched_len = sum([ 1.0 if ngram in matched else 0.0 for ngram in hyp_ngrams ] ) ;
        
	percentage = (matched_len/float(len(tokens))) *100
	return percentage
