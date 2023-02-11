import numpy as np

# from fuzzpy.fuzzysets import fuzzyset
from fuzzpy.fuzzysets.fuzzyset import fuzzyset


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
