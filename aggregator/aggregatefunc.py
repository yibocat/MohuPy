#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/1 下午5:37
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzyKit
import numpy as np

from fuzzysets.fuzzyset import fuzzyset


def weighted_ave(f: fuzzyset, weights, mode='algeb'):
    """
        weighted average operator of fuzzyset

        Parameters
        ----------
            f : fuzzyset,
                fuzzyset
            weights : list,
                list of weights,
            mode : str,
                Arithmetic paradigm, defaults to algebraic operations.
        Returns
        -------
            Aggregated fuzzy elements
    """
    w = np.asarray(weights)
    fs = f.ravel()
    dlist = []
    if weights == 0:
        for i in range(fs.len):
            dlist.append(fs.set[i])
    else:
        assert 0 <= w.all() <= 1 and w.sum() == 1, 'weights must be between 0 and ' \
                                             '1 and the sum of weights must equal to 1.'
        for i in range(fs.len):
            if mode == 'algeb':
                dlist.append(fs.set[i].algebraicTimes(w[i]))
            elif mode == 'eins':
                dlist.append(fs.set[i].einsteinTimes(w[i]))

    ag = fuzzyset(f.qrung, f.dict['type'].__name__).negs(f.len).set[0]
    for e in dlist:
        ag = f.dict[mode + '_plus'](e, ag)
    return ag


def weighted_geom(f: fuzzyset, weights, mode='algeb'):
    """
        weighted geometric operator of fuzzyset

        Parameters
        ----------
            f : fuzzyset,
                fuzzyset
            weights : list,
                list of weights,
            mode : str,
                Arithmetic paradigm, defaults to algebraic operations.
        Returns
        -------
            Aggregated fuzzy elements
    """
    w = np.asarray(weights)
    fs = f.ravel()
    dlist = []
    if weights == 0:
        for i in range(fs.len):
            dlist.append(fs.set[i])
    else:
        assert 0 <= w.all() <= 1 and w.sum() == 1, 'weights must be between 0 and ' \
                                             '1 and the sum of weights must equal to 1.'
        for i in range(fs.len):
            if mode == 'algeb':
                dlist.append(f.set[i].algebraicPower(w[i]))
            elif mode == 'eins':
                dlist.append(f.set[i].einsteinTimes(w[i]))

    ag = fuzzyset(f.qrung, f.dict['type'].__name__).poss(f.len).set[0]
    for e in dlist:
        ag = f.dict[mode + '_multiply'](e, ag)
    return ag
