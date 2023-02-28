#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/21 上午4:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets

import copy

import numpy as np
cimport numpy as np


from .qdhfe import config as config1
from .qifn import config as config2
from .qivfn import config as config3

qrungdhfe = config1.global_get('type')
qrungifn = config2.global_get('type')
qrungivfn = config3.global_get('type')


cpdef double _adj(np.ndarray d, double tm):
        """
            内置函数，用于计算风险因素得到的标准化元素
            输入：
                d: array 类型
        """
        assert 0 <= tm <= 1, 'The parameter must be in the interval 0-1.'
        return tm * d.max() + (1. - tm) * d.min()

cpdef normalization(d1: qrungdhfe, d2: qrungdhfe, double t=1):
    """
        the normalization function for two Q-rung hesitant fuzzy elements.
        The parameter 't' is the risk factor of normalization process, which in
        the interval [0, 1]. 't=1' indicates optimistic normalization and
        't=0' indicates pessimistic normalization.\n
        ------------------------------------------------

        reference:
            A. R. Mishra, S.-M. Chen, and P. Rani, “Multiattribute decision-making
            based on Fermatean hesitant fuzzy sets and modified VIKOR method,”
            Inform Sciences, vol. 607, pp. 1532–1549, 2022, doi: 10.1016/j.ins.2022.06.037.\n
        ------------------------------------------------

        input：
            d1: Q-rung hesitant fuzzy element.\n
            d2: Q-rung hesitant fuzzy element.\n
            t: the parameter of the normalization function.

        return：
            d1: Q-rung hesitant fuzzy element\n
            d2: Q-rung hesitant fuzzy element
    """

    d_1 = copy.deepcopy(d1)
    d_2 = copy.deepcopy(d2)

    cdef double md_len
    cdef double nmd_len
    md_len = len(d_1.md) - len(d_2.md)
    nmd_len = len(d_1.nmd) - len(d_2.nmd)

    if md_len > 0:  # 说明 d1 隶属度元素个数大于 d2, 需要增加 d2 隶属度的元素
        i = 0.
        m = d_2.md
        while i < md_len:
            d_2.md = np.append(d_2.md, _adj(m, t))
            i += 1
    else:  # 说明 d1 隶属度元素个数小于 d2， 需要增加 d1 隶属度的元素
        i = 0.
        m = d_1.md
        while i < (-md_len):
            d_1.md = np.append(d_1.md, _adj(m, t))
            i += 1

    if nmd_len > 0: # 说明 d1 隶属度元素个数大于 d2, 需要增加 d2 隶属度的元素
        i = 0.
        u = d_2.nmd
        while i < nmd_len:
            d_2.nmd = np.append(d_2.nmd, _adj(u, t))
            i += 1
    else:
        i = 0.
        u = d_1.nmd
        while i < (-nmd_len):
            d_1.nmd = np.append(d_1.nmd, _adj(u, t))
            i += 1

    return d_1.qsort(), d_2.qsort()

cpdef double qdfe_d(d1: qrungdhfe, d2: qrungdhfe, double l, double t, bint indeterminacy=True):
    """
        The generalized distance function for two Q-rung hesitant fuzzy elements.
        The parameter 'l' is the generic distance function parameter. 'l=1' indicates
        the Hamming distance and 'l=2' indicates the Euclidean distance.
        The parameter 't' is the risk factor of normalization process, which in
        the interval [0, 1]. 't=1' indicates optimistic normalization and 't=0' indicates
        pessimistic normalization.\n

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

        reference:
            A. R. Mishra, S.-M. Chen, and P. Rani, “Multiattribute decision-making
            based on Fermatean hesitant fuzzy sets and modified VIKOR method,”
            Inform Sciences, vol. 607, pp. 1532–1549, 2022, doi: 10.1016/j.ins.2022.06.037.\n
    """

    assert 0 <= t <= 1, 'ERROR: The parameter \'t\' must be in the interval [0,1]'
    assert d1.qrung == d2.qrung and not d1.isEmpty() and not d2.isEmpty(), \
        'ERROR! The two DHFEs are not the same DHFE or one of them is a empty DHFE!'
    cdef int q
    d_1 = copy.deepcopy(d1)
    d_2 = copy.deepcopy(d2)

    q = d1.qrung
    d_1, d_2 = normalization(d1, d2, t)

    # 不确定度
    cdef double pi1
    cdef double pi2
    cdef double pi

    cdef double mds
    cdef double nmds
    mds = 0.
    nmds = 0.

    pi1 = d_1.indeterminacy
    pi2 = d_2.indeterminacy
    pi = np.fabs(pi1 ** q - pi2 ** q) ** l

    for x in range(len(d_1.md)):
        mds += np.fabs(d_1.md[x] ** q - d_2.md[x] ** q) ** l
    for y in range(len(d_1.nmd)):
        nmds += np.fabs(d_1.nmd[y] ** q - d_2.nmd[y] ** q) ** l

    mds = mds / len(d_1.md)
    nmds = nmds / len(d_1.nmd)

    cdef double distance

    if indeterminacy:
        distance = (0.5 * (mds + nmds + pi)) ** (1 / l)
    else:
        distance = (0.5 * (mds + nmds)) ** (1 / l)

    return distance

cpdef double qifn_d(d1: qrungifn, d2: qrungifn, double l=1, bint indeterminacy=True):
    """
        The generalized distance function for two Q-rung intuitionistic fuzzy elements.
        The parameter 'l' is the generic distance function parameter. 'l=1' indicates
        the Hamming distance and 'l=2' indicates the Euclidean distance.

        Parameters:
        -----------
            d1: Q-rung fuzzy element.
            d2: Q-rung fuzzy element.
            l: the generic distance function parameter.
                l=1 indicates the Hamming distance
                l=2 indicates the Euclidean distance
            indeterminacy: Bool
                Determine whether the distance formula contains indeterminacy.

        Return:
        --------
            float: The generalized distance between the two FNs.
    """
    assert d1.qrung == d2.qrung and not d1.isEmpty() and not d2.isEmpty(), \
        'ERROR! The two FNs are not the same FN or one of them is a empty FN!'
    cdef int q
    cdef double pi1
    cdef double pi2
    cdef double pi

    q = d1.qrung
    pi1 = d1.indeterminacy
    pi2 = d2.indeterminacy
    pi = np.fabs(pi1 ** q - pi2 ** q) ** l

    cdef double distance

    if indeterminacy:
        distance = (0.5 * (np.fabs(d1.md ** q - d2.md ** q) ** l +
                           np.fabs(d1.nmd ** q - d2.nmd ** q) ** l + pi)) ** (1 / l)
    else:
        distance = (0.5 * (np.fabs(d1.md ** q - d2.md ** q) ** l +
                           np.fabs(d1.nmd ** q - d2.nmd ** q) ** l)) ** (1 / l)
    return distance

cpdef double qivfn_d(d1: qrungivfn, d2: qrungivfn, double l=1, bint indeterminacy=True):
    """
        The generalized distance function for two Q-rung interval-valued fuzzy elements.
        The parameter 'l' is the generic distance function parameter. 'l=1' indicates
        the Hamming distance and 'l=2' indicates the Euclidean distance.

        Parameters:
            d1: Q-rung interval-valued fuzzy number.
            d2: Q-rung interval-valued fuzzy number.
            l: the generic distance function parameter.
                l=1 indicates the Hamming distance
                l=2 indicates the Euclidean distance
            indeterminacy: Bool
                Determine whether the distance formula contains indeterminacy.

        Return:
            float: The generalized distance between the two IVFNS.


        reference:
            [1] J. S, “Ordering of interval-valued Fermatean fuzzy sets and its
                applications,” Expert Syst Appl, vol. 185, p. 115613, 2021,
                doi: 10.1016/j.eswa.2021.115613.
            [2] Z. Xu, “A method based on distance measure for interval-valued
                intuitionistic fuzzy group decision-making,” Inform Sciences,
                vol. 180, no. 1, pp. 181–190, 2010, doi: 10.1016/j.ins.2009.09.005.
    """
    assert d1.qrung == d2.qrung and not d1.isEmpty() and not d2.isEmpty(), \
        'ERROR! The two interval-valued intuitionistic fuzzy numbers are not same(Q-rung) ' \
        'or one of them is empty!'

    cdef int q
    cdef double pi1
    cdef double pi2
    cdef double pi

    q = d1.qrung
    pi1 = d1.indeterminacy
    pi2 = d2.indeterminacy
    pi = np.fabs(pi1 ** q - pi2 ** q) ** l

    cdef double distance

    if indeterminacy:
        distance = 0.25 * (
                np.fabs(d1.md[0] ** q - d2.md[0] ** q) ** l +
                np.fabs(d1.md[1] ** q - d2.md[1] ** q) ** l +
                np.fabs(d1.nmd[0] ** q - d2.nmd[0] ** q) ** l +
                np.fabs(d1.nmd[1] ** q - d2.nmd[1] ** q) ** l + pi) ** (1 / l)
    else:
        distance = 0.25 * (
                np.fabs(d1.md[0] ** q - d2.md[0] ** q) ** l +
                np.fabs(d1.md[1] ** q - d2.md[1] ** q) ** l +
                np.fabs(d1.nmd[0] ** q - d2.nmd[0] ** q) ** l +
                np.fabs(d1.nmd[1] ** q - d2.nmd[1] ** q) ** l) ** (1 / l)

    return distance
