#!/usr/bin/env python
import sys,os
import optparse
from collections import namedtuple

from gen_translations import gen_best_translations_by_lambda
from line_util import find_intersecting_line
from line_util import compute_line

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'bleu'))
import compute_bleu

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'feature_gen'))
import feat_extraction
import feat_names


"""
Length Check on References and Translations
"""
def length_check(ref, best_translations):
    # Length Check
    if len(ref) != len(best_translations):
        sys.stderr.write("Ref statements are not equal to best_translations")
        sys.exit(0)
    return



"""
Modified Powell Search - Search for optimum lambda parameters
Modular code. Uses scoring function. Flexibility to encode more features
"""
def powell_search_mod(opts, all_trans_feat):

    sys.stdout.write("Setting up src sentence, hyp, ref lists for processing.....\n\n")

    src_sen = [line.strip().split('\t')[1:2] for line in open(opts.trans_data)][1:1001]
    ref = [ [reference.strip().split() for reference in line.strip().split('\t')[2:6] ]  for line in open(opts.trans_data)][1:1001]
    all_trans = [line.strip().split('\t')[6:10] for line in open(opts.trans_data)][1:]

    #src_tokens = load_src_tokens(opts.token_file)
    num_sents = len(src_sen)

    # Initial values for lambdas
    lambdas = {feat_names.BIGRAM        : float(opts.w_lm_bigram),
               feat_names.TRIGRAM       : float(opts.w_lm_trigram),
               feat_names.EDIT_DIST     : float(opts.w_edit_dist),
               feat_names.PENALTY_SHORT : float(opts.w_pen_short),
               feat_names.PENALTY_LONG  : float(opts.w_pen_long),}


               #'len_d'      : float(opts.ld),
               #'p(e)'       : float(opts.lm),
               #'p(e|f)'     : float(opts.tm1),
               #'p_lex(f|e)' : float(opts.tm2),
               #'trans_w'    : float(opts.tr),
               #'avg_len_d'  : float(opts.av)}
               #"""

    inc_lambdas = {feat_names.BIGRAM  : True,
                   feat_names.TRIGRAM : True,
                   feat_names.EDIT_DIST : True,
                   feat_names.PENALTY_SHORT : True,
                   feat_names.PENALTY_LONG : True}

                # 'len_d'      : False,
                # 'p(e)'       : False,
                # 'p(e|f)'     : False,
                # 'p_lex(f|e)' : False,
                # 'trans_w'    : False,
                # 'avg_len_d'  : False}


    # lambdas_order = ['p(e)', 'p(e|f)', 'p_lex(f|e)', 'len_d']


    # Declaring line with following fields
    line_t = namedtuple('line',['lambda_t', 'lambda_v','incline','offset'])

    # Initialising total_max_bleu_score
    best_translations = gen_best_translations_by_lambda(all_trans, all_trans_feat, src_sen, lambdas, inc_lambdas)
    best_translations_split = [line.strip().split() for line in best_translations]
    total_max_bleu_score = compute_bleu.compute_bleu(best_translations_split, ref)

    sys.stdout.write("Initial bleu score with initial lambda values: %s\n" % str(total_max_bleu_score))

    converged = False
    num_iter = 0
    while not converged and num_iter <= 3:
        sys.stdout.write("\nRunning iteration: %s ....\n" % num_iter)
        num_iter += 1

        # Assuming that this iteration will converge
        converged = True

        # Iterating over every parameter
        for param in lambdas.keys():

            # Running for selected parameters
            if not inc_lambdas[param]:
                continue

            sys.stdout.write("Optimizing for param: %s\n" % param)

            thresh_points = list()

            # Iterating for all sentences
            for s_no in xrange(0,num_sents):
                trans_for_one_sent = all_trans[s_no]
                t_feat_for_one_sent = all_trans_feat[s_no]

                lines = list()
                lines_done = list()

                for t_no, tran in enumerate(trans_for_one_sent):
                    (incline, offset) = compute_line(t_feat_for_one_sent[t_no], lambdas,inc_lambdas, param)
                    lines.append(line_t(param, lambdas[param], incline, offset))

                # Computing the line with the steepest incline
                lines = sorted(lines, key=lambda x: (x.incline, -x.offset))
                line_steep = lines[0]
                lines_done.append(line_steep)

                # Finding all intersection points
                line_found = True
                curr_max_thresh =-1 * sys.maxint
                while line_found:
                    (intersect_line, min_lambda_v, line_found) = find_intersecting_line(line_steep, lines, lines_done, curr_max_thresh)
                    if not line_found:
                        break
                    curr_max_thresh = min_lambda_v
                    thresh_points.append(min_lambda_v)
                    lines_done.append(intersect_line)
                    line_steep = intersect_line

                #print "%s All intersection points found" % s_no



            # Sorting thershold points by param value
            thresh_points.sort()
            #print thresh_points
            len_thresh = len(thresh_points)
            print len_thresh
            #thresh_points = thresh_points[0:len_thresh:3]
            #print len(thresh_points)
            print thresh_points[0], thresh_points[-1]

            print "Found and sorted all threshold points......"

            # Deep copy the lambdas/params
            lambdas_t = dict(lambdas)

            # Generating the best translations
            initial_fuzz = 1
            lambdas_t[param] = thresh_points[0] - initial_fuzz
            best_translations = gen_best_translations_by_lambda(all_trans, all_trans_feat, src_sen, lambdas, inc_lambdas)

            print "Computing best translations......"

            # Computing the initial bleu score
            length_check(ref, best_translations)
            argmax_lambda_v = lambdas_t[param]
            best_translations_split = [line.strip().split() for line in best_translations]
            max_bleu_score = compute_bleu.compute_bleu( best_translations_split, ref)

            print max_bleu_score

            print "Finding the optimal lambda value......"
            # Finding the optimal lambda_v using the best bleu score
            for t_ind in xrange(1,len(thresh_points)):
                #print t_ind
                lambdas_t[param] = float(thresh_points[t_ind-1] + thresh_points[t_ind])/2
                best_translations = gen_best_translations_by_lambda(all_trans, all_trans_feat, src_sen, lambdas, inc_lambdas)

                length_check(ref, best_translations)
                best_translations_split = [line.strip().split() for line in best_translations]
                bleu_score = compute_bleu.compute_bleu( best_translations_split, ref)
                if bleu_score > max_bleu_score:
                    max_bleu_score = bleu_score
                    argmax_lambda_v = lambdas_t[param]

                #print "%s t_ind max_bleu_Score %s" %(t_ind, max_bleu_score)

            print "Checking if the best lambda_v for this feat_wt improves the overall bleu score"
            # Take the param value if the best bleu score is greater
            if max_bleu_score > total_max_bleu_score:
                lambdas[param] = argmax_lambda_v
                total_max_bleu_score = max_bleu_score
                converged = False

                sys.stdout.write("New max bleu score is: %s\n" % total_max_bleu_score)
                print lambdas

    print lambdas
    print total_max_bleu_score
    return lambdas


if __name__=="__main__":

    optparser = optparse.OptionParser()

    optparser.add_option("-d", "--trans_data", dest="trans_data", default="../../data/translations.tsv", help="The complete translations data file")
    optparser.add_option("-l", "--trans_lm_file", dest="trans_lm_file", default="../../data/turk_translations_w_logprob_europarl_c.tsv", help="Language model prob")
    optparser.add_option("-f", "--trans_feat", dest="trans_feat", default="../../data/turk_translations_features_5.tsv", help="Translation features")

    optparser.add_option("-b", "--lm", dest="w_lm_bigram", default=0.01, type="float", help="Bigram Language model weight")
    optparser.add_option("-t", "--tm1", dest="w_lm_trigram", default=0.09, type="float", help="Trigram Language model weight")
    optparser.add_option("-e", "--ed", dest="w_edit_dist", default=0.7, type="float", help="Edit distance feat weight")
    optparser.add_option("-p", "--lps", dest="w_pen_short", default=0.1, type="float", help="Short sen len penalty weight")
    optparser.add_option("-s", "--lpl", dest="w_pen_long", default=0.1, type="float", help="Long sen len penalty weight")

    (opts, _) = optparser.parse_args()

    sys.stdout.write("Extracting features...\n")
    all_trans_feat = feat_extraction.extract_and_format_feat(opts)
    powell_search_mod(opts, all_trans_feat)

