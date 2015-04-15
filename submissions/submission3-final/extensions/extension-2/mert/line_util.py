#!/usr/bin/env python

import sys

"""
find_intersecting_line:
Finding the next intersecting line with the current steepest line
"""
def find_intersecting_line(line_steep, lines, lines_done, curr_max_lambda, iter=sys.maxint):

    min_lambda_v = 1e300
    intersect_line = None

    num_iter = 0
    for l in lines:
        if l in lines_done or l.incline == line_steep.incline:
            continue

        if num_iter >= iter:
            break

        lambda_v = float(l.offset - line_steep.offset)/(line_steep.incline - l.incline)
        if  curr_max_lambda < lambda_v < min_lambda_v:
            min_lambda_v = lambda_v
            intersect_line = l

        num_iter += 1

    if intersect_line is None:
        return intersect_line, min_lambda_v, False

    return intersect_line, min_lambda_v, True


"""
Computes the incline and the offset of a hypothesis
using features and required things
"""
def compute_line(tran_feats, lambdas,inc_lambdas, param):
    # Computing Total score => sum(lambda_i * h(x_i))

    if not inc_lambdas[param]:
        sys.stderr.write("The feature corresponding to incline should always be included")
        sys.exit(0)

    tot_score = 0.0
    for feature in tran_feats:
        if inc_lambdas[feature.feat_type]:
            tot_score += lambdas[feature.feat_type] * float(feature.feat_val)

            if param == feature.feat_type:
                incline = float(feature.feat_val)

    #Computing Line l: param -> score
    return incline, tot_score - lambdas[param]*incline


