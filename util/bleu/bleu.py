import math
from collections import Counter
# Collect BLEU-relevant statistics for a single hypothesis/ multiple references pair.
# Return value is a generator yielding:
# (c, r, numerator1, denominator1, ... numerator4, denominator4)
# Summing the columns across calls to this function on an entire corpus will
# produce a vector of statistics that can be used to compute BLEU (below)

def bleu_stats(hypothesis, references):
  yield len(hypothesis)
  # take min length of references as done in NIST
  yield min([len(reference) for reference in references])
  for n in xrange(1,5):
    s_ngrams = Counter([tuple(hypothesis[i:i+n]) for i in xrange(len(hypothesis)+1-n)])
    r_ngrams = [None for _ in xrange(len(references))]
    pairing = []
    for i_ref, reference in enumerate(references):
        r_ngrams[i_ref] = Counter([tuple(reference[i:i+n]) for i in xrange(len(reference)+1-n)])
        pairing.append(s_ngrams & r_ngrams[i_ref])
    # print "pairing {} \n max {}".format(pairing, reduce(max, pairing))
    # for each hyp, ref pair, calculate intersection, then take max of each intersection value
    yield max([sum(reduce(max, pairing).values()), 0])
    # yield max([sum((s_ngrams & r_ngram).values()), 0])
    yield max([len(hypothesis)+1-n, 0])

# Compute BLEU from collected statistics obtained by call(s) to bleu_stats
def bleu(stats):
  if len(filter(lambda x: x==0, stats)) > 0:
    return 0
  # stats = map(lambda x: 1 if x == 0 else x, stats)
  (c, r) = stats[:2]
  log_bleu_prec = sum([math.log(float(x)/y) for x,y in zip(stats[2::2],stats[3::2])]) / 4.
  return math.exp(min([0, 1-float(r)/c]) + log_bleu_prec)

# hyp = ["there is a cat on the drawer genius".split(' '), "stella has gone quiet over the years".split(' ')]
# refs = [["there was a cat on the drawer over there".split(' '), "there was a cat on the over there drawer genius".split(' ')],
#         ["stella has gone quiet over time".split(' '), "stella has gone quiet as time passed".split(' ')]]
# # print list(compute_bleu(hyp, refs))
# print compute_bleu(hyp, refs)