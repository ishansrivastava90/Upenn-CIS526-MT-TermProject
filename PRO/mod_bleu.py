from collections import Counter
import math

def bleu_stats(hypothesis, reference, n):
    yield len(hypothesis)
    yield len(reference)
    s_ngrams = Counter([tuple(hypothesis[i:i+n]) for i in xrange(len(hypothesis)+1-n)])
    r_ngrams = Counter([tuple(reference[i:i+n]) for i in xrange(len(reference)+1-n)])
    yield max([sum((s_ngrams & r_ngrams).values()), 0])
    yield max([len(hypothesis)+1-n, 0])

def compute_bleu(hyp, ref):
    # print "computing bleu between {} and {}".format(hyp, ref)
    score = 0.0
    for n in xrange(1, 5):
        stats = [0 for i in xrange(10)]
        stats = [sum(scores) for scores in zip(stats, bleu_stats(hyp,ref,n))]
        score += smooth_bleu(stats) / (2 ** (4-n+1))
        # print "stats {} and smooth bleu {}".format(stats, smooth_bleu(stats))
    return score

def smooth_bleu(stats):
    stats = map(lambda x: 1 if x == 0 else x, stats)
    (c, r) = stats[:2]
    log_bleu_prec = sum([math.log(float(x)/y) for x,y in zip(stats[2::2],stats[3::2])]) / 4.
    return math.exp(min([0, 1-float(r)/c]) + log_bleu_prec)
#
# hyp = "a b c d e".split()
# ref = "a b c d".split()
# b_stats = list(bleu_stats(hyp, ref, 1))
# print b_stats
# # print smooth_bleu(b_stats)
# print compute_bleu(hyp, ref)