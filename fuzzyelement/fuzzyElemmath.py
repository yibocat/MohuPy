#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/4 下午8:27
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzyKit
import copy

import numpy as np

from fuzzyelement.DHFElements import qrunghfe


def normalization(d1: qrunghfe, d2: qrunghfe, t=1) -> (qrunghfe, qrunghfe):
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

    def _adj(d, tm):
        """
            内置函数，用于计算风险因素得到的标准化元素
            输入：
                d: array 类型
        """
        assert 0 <= tm <= 1, 'The parameter must be in the interval 0-1.'
        return tm * d.max() + (1 - tm) * d.min()

    d1 = copy.copy(d1)
    d2 = copy.copy(d2)

    md_len = len(d1.md) - len(d2.md)
    nmd_len = len(d1.nmd) - len(d2.nmd)
    if md_len > 0:  # 说明 d1 隶属度元素个数大于 d2, 需要增加 d2 隶属度的元素
        i = 0
        m = d2.md
        while i < md_len:
            d2.md = np.append(d2.md, _adj(m, t))
            i += 1
    else:  # 说明 d1 隶属度元素个数小于 d2， 需要增加 d1 隶属度的元素
        i = 0
        m = d1.md
        while i < (-md_len):
            d1.md = np.append(d1.md, _adj(m, t))
            i += 1

    if nmd_len > 0:
        i = 0
        m = d2.nmd
        while i < nmd_len:
            d2.nmd = np.append(d2.nmd, _adj(m, t))
            i += 1
    else:
        i = 0
        m = d1.nmd
        while i < (-nmd_len):
            d1.nmd = np.append(d1.nmd, _adj(m, t))
            i += 1

    d1 = d1.qSort()
    d2 = d2.qSort()

    return d1, d2


def generalized_distance(d1: qrunghfe, d2: qrunghfe, l=1, t=1, indeterminacy=True):
    """
        The generalized distance function for two Q-rung hesitant fuzzy elements.
        The parameter 'l' is the generic distance function parameter. 'l=1' indicates
        the Hamming distance and 'l=2' indicates the Euclidean distance.
        The parameter 't' is the risk factor of normalization process, which in
        the interval [0, 1]. 't=1' indicates optimistic normalization and 't=0' indicates
        pessimistic normalization.\n
        ------------------------------------------------

        reference:
            A. R. Mishra, S.-M. Chen, and P. Rani, “Multiattribute decision-making
            based on Fermatean hesitant fuzzy sets and modified VIKOR method,”
            Inform Sciences, vol. 607, pp. 1532–1549, 2022, doi: 10.1016/j.ins.2022.06.037.\n
    """

    assert 0 <= t <= 1, 'ERROR: The parameter \'t\' must be in the interval [0,1]'
    assert d1.qrung == d2.qrung and not d1.isEmpty() and not d2.isEmpty(), \
        'ERROR! The two DHFEs are not the same DHFE or one of them is a empty DHFE!'
    q = d1.qrung

    # 标准化
    d1, d2 = normalization(d1, d2, t)

    # 不确定度
    pi1 = (1 - (d1.md ** q).sum() / len(d1.md) -
           (d1.nmd ** q).sum() / len(d1.nmd)) ** (1 / q)
    pi2 = (1 - (d2.md ** q).sum() / len(d2.md) -
           (d2.nmd ** q).sum() / len(d2.nmd)) ** (1 / q)
    pi = np.fabs(pi1 ** q - pi2 ** q) ** l

    mds, nmds = 0, 0

    for x in range(len(d1.md)):
        mds += np.fabs(d1.md[x] ** q - d2.md[x] ** q) ** l
    for y in range(len(d1.nmd)):
        nmds += np.fabs(d1.nmd[y] ** q - d2.nmd[y] ** q) ** l

    mds = mds / len(d1.md)
    nmds = nmds / len(d1.nmd)

    distance = 0.5 * (mds + nmds + pi) ** (1 / l)

    return distance
