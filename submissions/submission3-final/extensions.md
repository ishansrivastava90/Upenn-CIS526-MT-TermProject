


##Extensions##

###1. LM Prob. using Europarl Corpus along with edit distance

As part of generating more informative features, we computed the average edit distance using Levenshtein metric for every translation against all the other translations. The notion behind this being that the translation which is the most similar to all the others is most likely to be the best one. This method gets the top 2 translations according to their edit distance and then uses the language model probabilities to choose the best between them. The language model probabilities are already penalized according to the difference from average translation length for that sentence. Also, random weights were used for the  final score 


**| Sno. | Wt-bigram | Wt-trigram | bleu-score |**

	| 1      | 0.5       | 0.5        | 0.2628     |

	| 2    | 0.75      | 0.25       | 0.2529     |

	| 3    | 0.2       | 0.8        | 0.2817     |

	| 4    | 0.1       | 0.9        | 0.2849     |




###2. Optimization/Reranking
The following optimization techniques were used to choose the best translation:
    
**1. PRO (Pairwise Ranking Optimization)** works by using a perceptron that is trained on the features extracted from the candidate translation and then running over the dataset multiple times to calculate a set of weights. This set of weights is then used on the test set to generate a score when taking the vector dot product of the feature and the weights, which is used to rank the sentences and decide the best candidate translation for a given source sentence. The 'pairwise' portion of the name means that instead of working on the entire set of possible pairs of candidate sentences per source sentence (effectively O(n^2) which is usually intractable), a configurable parameter of how many pairs to consider is provided to the system. The system then chooses this number of random pairs and trains a perceptron based on the features of these pairs and their score against the references (in this case the scoring function is smoothed_bleu against high quality sentences).
Using PRO with bigrams and trigrams gave a BLEU score of 0.20 (on average).

**2. MERT** 
We used MERT for accurate weight estimation for the features instead of randomly assigning weights. Powell Search was used to effectively search over a reduced space of possible weights for every feature one at a time, keeping the others constant. The downside of this was that it becomes increasingly slow with increase in number of features. Used this with language model probs, edit dist, short and long length penalty and TER for estimation of weights for the above mentioned features


**| Sno. | Feature Set               |  bleu-score |**

	| 1    | LM Probs + Edit dist + short + long len penalty       |  0.3152     |
	| 2    | LM Probs + TER + short + long len penalty             |  0.3271     |
    | 3    | LM Probs + Edit Dist + TER + short + long len penalty |  0.3298     |





Switching to PRO seemed like an easier and more viable option because as mentioned in the paper PRO performs better than MERT as  dimensionality and noise in the data increase. The PRO algorithm uses BLEU score along with perceptron training, which is very simple implement and understand. Also, being an online learning method, the perceptron makes prediction while it is still learning.

###3.  Sentence Level Features###
* 	Language Model Probabities (2 features) : The bigram and trigram probabilities in the first extension are used.
*	Length Penalty (2 features) :	This metric penalizes those translations which are shorter(or longer) than the source sentence If the translation is shorter than the source sentence, then the short penalty is e^(1 - translation_length/source_length). If the translation is longer  than the source sentence, then the short penalty is e^(1 - source_length/translation_length). 
*	N-gram Match Percentage (2 features) :	Each translation was given a score based on the percentage of n-gram (bigram and trigram) matches. This percentage was calculate by finding the n-grams present in the translation that were also present in European Parallel corpus. Thus, two features, bigram match percentage and trigram match percentage, were included.
*	Average TER :The mean of TER of each translation with the other 3 translations is calculated.
*	Edit Distance : The mean of Levenshtein distance of each translation with the other 3 translations is calculated. Here, the distance is calculated w.r.t words rather than characters.

The BLEU score using PRO on sentence level features is 0.245

###4.  Worker Level Features ####
We also experimented with worker level features. Evaluation of translation was done based on the information about the translators (given in survey.tsv). 

*	Aggregete Features:(8 features)	Each of the above features was used to form new features to evaluate the translations given by a given worker. The average of the sentence level features for each worker are taken as the aggregate features.
*	Native Speaker:(2 features) The knowledge whether a given translator is native speaker of English/Urdu is a good metric to evaluate the translation given by that translator. The idea is that a native Urdu speaker will tend to give a better translation than a non-native speaker. We created a binary feature indicating whether a translator is native speaker of Urdu. A similar feature for English was also created.
*	Experience in Language:	(2 features) Two features indicating the number of years a translator has been speaking in Urdu/English were created.
*	Worker Location:(2 features) Two binary features indicating location of the translator were included: one reflecting whether the translator is in India, the second indicating whether the translator is in Pakistan.

The BLEU score using PRO on only worker level features is 0.217. The BLEU score using PRO on both the sentence level and worker level features is 0.262
  
