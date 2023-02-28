#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/21 上午4:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets

import numpy as np
import copy

from ..fuzzysets import fuzzyset

from ..fuzzynumbers import glb, neg, pos


def weighted_ave(f: fuzzyset, weights=None, mode='algeb'):
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
    assert f.set.ndim == 1, 'weighted average operator only support 1-dimensional fuzzy set'
    fs = copy.deepcopy(f)
    dlist = []
    if weights is None:
        for i in range(fs.size):
            dlist.append(fs.set[i])
    else:
        assert 0. <= w.all() <= 1. and w.sum() == 1., 'weights must be between 0 and ' \
                                                      '1 and the sum of weights must equal to 1.'
        for i in range(fs.size):
            if mode == 'algeb':
                dlist.append(fs.set[i].algeb_times(w[i]))
            elif mode == 'eins':
                dlist.append(fs.set[i].eins_times(w[i]))

    ag = fuzzyset(f.qrung, f.dict['type'].__name__).negs(f.size).set[0]
    for e in dlist:
        ag = f.dict[mode + '_plus'](e, ag)
    assert ag.isLegal(), 'The aggregation element is not legal.'
    return ag


def weighted_geom(f: fuzzyset, weights=None, mode='algeb'):
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
    assert f.set.ndim == 1, 'weighted average operator only support 1-dimensional fuzzy set'
    fs = copy.deepcopy(f)
    dlist = []
    if weights is None:
        for i in range(fs.size):
            dlist.append(fs.set[i])
    else:
        assert 0. <= w.all() <= 1. and w.sum() == 1., 'weights must be between 0 and ' \
                                                      '1 and the sum of weights must equal to 1.'
        for i in range(fs.size):
            if mode == 'algeb':
                dlist.append(fs.set[i].algeb_power(w[i]))
            elif mode == 'eins':
                dlist.append(fs.set[i].eins_power(w[i]))

    ag = fuzzyset(f.qrung, f.dict['type'].__name__).poss(f.size).set[0]
    for e in dlist:
        ag = f.dict[mode + '_multiply'](e, ag)
    assert ag.isLegal(), 'The aggregation element is not legal.'
    return ag


def sub_weighted_ave(f, weights=None, mode='algeb'):
    dictionary = glb.global_get(f[0].__class__.__name__)
    # dictionary = fns.get_dict[f[0].__class__.__name__]
    fv = copy.deepcopy(f)
    dlist = []
    if weights is None:
        for i in range(len(fv)):
            dlist.append(fv[i])
    else:
        w = np.asarray(weights)
        # assert 0. <= w.all() <= 1. and w.sum() == 1., 'weights must be between 0 and' \
        #                                               '1 and the sum of weights must equal to 1.'
        for i in range(len(fv)):
            if mode == 'algeb':
                dlist.append(fv[i].algeb_times(w[i]))
            elif mode == 'eins':
                dlist.append(fv[i].eins_times(w[i]))

    ag = neg(fv[0].__class__.__name__, fv[0].qrung)
    for e in dlist:
        ag = dictionary[mode + '_plus'](e, ag)
    assert ag.isLegal(), 'The aggregation element is not legal.'
    return ag


def sub_weighted_geom(f, weights=None, mode='algeb'):
    dictionary = glb.global_get(f[0].__class__.__name__)
    fv = copy.deepcopy(f)
    dlist = []
    if weights is None:
        for i in range(len(fv)):
            dlist.append(fv[i])
    else:
        w = np.asarray(weights)
        # assert 0. <= w.all() <= 1. and w.sum() == 1., 'weights must be between 0 and' \
        #                                               '1 and the sum of weights must equal to 1.'
        for i in range(len(fv)):
            if mode == 'algeb':
                dlist.append(fv[i].algeb_power(w[i]))
            elif mode == 'eins':
                dlist.append(fv[i].eins_power(w[i]))

    ag = pos(fv[0].__class__.__name__, fv[0].qrung)
    for e in dlist:
        ag = dictionary[mode + '_multiply'](e, ag)
    assert ag.isLegal(), 'The aggregation element is not legal.'
    return ag
