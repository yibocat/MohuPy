#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/7 下午1:27
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import copy
import numpy as np

from ...core import Registry

fuzzDis = Registry()


@fuzzDis('qrofn')
def distance_qrofn(f1,
                   f2,
                   l: (int, np.int_),
                   t: (int, np.int_) = None,
                   indeterminacy=True):
    assert f1.mtype == f2.mtype == 'qrofn', \
        "The type of f1 and f2 must be qrofn."
    assert f1.qrung == f2.qrung, \
        "q rung of two fuzzy numbers must be equal."
    assert l > 0, \
        "The value of l must be greater than 0."
    q = f1.qrung
    pi1 = f1.ind
    pi2 = f2.ind
    pi = np.fabs(pi1 ** q - pi2 ** q) ** l

    if indeterminacy:
        return (0.5 * (np.fabs(f1.md ** q - f2.md ** q) ** l +
                       np.fabs(f1.nmd ** q - f2.nmd ** q) ** l + pi)) ** (1 / l)
    else:
        return (0.5 * (np.fabs(f1.md ** q - f2.md ** q) ** l +
                       np.fabs(f1.nmd ** q - f2.nmd ** q) ** l)) ** (1 / l)


@fuzzDis('ivfn')
def distance_ivfn(f1,
                  f2,
                  l: (int, np.int_),
                  t: (int, np.int_) = None,
                  indeterminacy=True):
    assert f1.mtype == f2.mtype == 'ivfn', \
        "The type of f1 and f2 must be ivfn."
    assert f1.qrung == f2.qrung, \
        "q rung of two fuzzy numbers must be equal."
    assert l > 0, \
        "The value of l must be greater than 0."
    q = f1.qrung
    pi1 = f1.ind
    pi2 = f2.ind
    pi = np.fabs(pi1 ** q - pi2 ** q) ** l

    if indeterminacy:
        return 0.25 * (
                np.fabs(f1.md[0] ** q - f2.md[0] ** q) ** l +
                np.fabs(f1.md[1] ** q - f2.md[1] ** q) ** l +
                np.fabs(f1.nmd[0] ** q - f2.nmd[0] ** q) ** l +
                np.fabs(f1.nmd[1] ** q - f2.nmd[1] ** q) ** l + pi) ** (1 / l)
    else:
        return 0.25 * (
                np.fabs(f1.md[0] ** q - f2.md[0] ** q) ** l +
                np.fabs(f1.md[1] ** q - f2.md[1] ** q) ** l +
                np.fabs(f1.nmd[0] ** q - f2.nmd[0] ** q) ** l +
                np.fabs(f1.nmd[1] ** q - f2.nmd[1] ** q) ** l) ** (1 / l)


@fuzzDis('qrohfn')
def distance_qrohfn(d1, d2, l, t, indeterminacy=True):
    """
    The generalized distance function for two Q-rung hesitant fuzzy elements.
        The parameter 'l' is the generic distance function parameter. 'l=1' indicates
        the Hamming distance and 'l=2' indicates the Euclidean distance.
        The parameter 't' is the risk factor of normalization process, which in
        the interval [0, 1]. 't=1' indicates optimistic normalization and 't=0' indicates
        pessimistic normalization.

    Parameters
    ----------
        d1: Q-rung hesitant fuzzy element.
        d2: Q-rung hesitant fuzzy element.
        l: the generic distance function parameter.
            l=1 indicates the Hamming distance
            l=2 indicates the Euclidean distance
        t: the parameter of the normalization function.
            t=1 indicates optimistic normalization
            t=0 indicates pessimistic normalization.
        indeterminacy: Bool
            Determine whether the distance formula contains indeterminacy.

    Returns
    -------
        float: The generalized distance between the two DHFEs.

    References
    ----------
        A. R. Mishra, S.-M. Chen, and P. Rani, “Multiattribute decision-making
        based on Fermatean hesitant fuzzy sets and modified VIKOR method,”
        Inform Sciences, vol. 607, pp. 1532–1549, 2022, doi: 10.1016/j.ins.2022.06.037.
    """
    assert 0 <= t <= 1, "risk factor 't' must be in [0,1] range."
    assert d1.qrung == d2.qrung, "the qrung of two fuzzy number must be equal."
    assert not d1.empty() and not d2.empty(), "the two q-rohfns must be not empty."

    d_1 = copy.deepcopy(d1)
    d_2 = copy.deepcopy(d2)
    q = d1.qrung
    # from ...core import normalize

    from ...core.funcitonClass import FuzzNormalize
    d_1, d_2 = FuzzNormalize(t)(d_1, d_2)

    mds = 0.
    nmds = 0.

    pi1 = d_1.ind
    pi2 = d_2.ind
    pi = np.fabs(pi1 ** q - pi2 ** q) ** l

    for x in range(len(d_1.md)):
        mds += np.fabs(d_1.md[x] ** q - d_2.md[x] ** q) ** l
    for y in range(len(d_1.nmd)):
        nmds += np.fabs(d_1.nmd[y] ** q - d_2.nmd[y] ** q) ** l

    mds = mds / len(d_1.md)
    nmds = nmds / len(d_1.nmd)

    if indeterminacy:
        return (0.5 * (mds + nmds + pi)) ** (1 / l)
    else:
        return (0.5 * (mds + nmds)) ** (1 / l)


