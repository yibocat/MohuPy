#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/6 下午2:43
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import numpy as np

from ..base import Archimedean

from ..constant import Approx

"""
The following is a quick calculation of Algebraic norms in fuzzy number. 
The code has been used for the calculation of 'Fuzznum' and 'Fuzzarray', 
so the Archimedean class is no longer used to complete the operation.
"""


def algebraic_add(x0, y0, x1, y1, q):
    """
    :param x0:  第一个数的隶属度
    :param y0:  第一个数的非隶属度
    :param x1:  第二个数的隶属度
    :param y1:  第二个数的非隶属度
    :param q:   Q 阶
    """
    md = np.round(
        (x0 ** q + x1 ** q - x0 ** q * x1 ** q) ** (1. / q), Approx.round)
    nmd = np.round(y0 * y1, Approx.round)
    return md, nmd


def algebraic_sub(x0, y0, x1, y1, q):
    """
    :param x0:  第一个数的隶属度
    :param y0:  第一个数的非隶属度
    :param x1:  第二个数的隶属度
    :param y1:  第二个数的非隶属度
    :param q:   Q 阶
    """
    if x0 == 0. and y0 == 1.:
        return 0., 1.
    if x1 == 1. or y1 == 0.:
        return 0., 1.
    if 0. <= y0 / y1 <= ((1 - x0 ** q) / (1 - x1 ** q)) ** (1 / q) <= 1.:
        md = np.round(((x0 ** q - x1 ** q) / (1 - x1 ** q)) ** (1 / q), Approx.round)
        nmd = np.round(y0 / y1, Approx.round)
        return md, nmd
    return 0., 1.


def algebraic_mul(x0, y0, x1, y1, q):
    """
    :param x0:  第一个数的隶属度
    :param y0:  第一个数的非隶属度
    :param x1:  第二个数的隶属度
    :param y1:  第二个数的非隶属度
    :param q:   Q 阶
    """
    md = np.round(x0 * x1, Approx.round)
    nmd = np.round(
        (y0 ** q + y1 ** q - y0 ** q * y1 ** q) ** (1. / q), Approx.round)
    return md, nmd


def algebraic_div(x0, y0, x1, y1, q):
    """
    :param x0:  第一个数的隶属度
    :param y0:  第一个数的非隶属度
    :param x1:  第二个数的隶属度
    :param y1:  第二个数的非隶属度
    :param q:   Q 阶
    """
    if x0 == 1. and y0 == 0.:
        return 1., 0.
    if x1 == 0. or y1 == 1.:
        return 1., 0.
    if 0. <= x0 / x1 <= ((1 - y0 ** q) / (1 - y1 ** q)) ** (1 / q) <= 1.:
        md = np.round(x0 / x1, Approx.round)
        nmd = np.round(((y0 ** q - y1 ** q) / (1 - y1 ** q)) ** (1 / q), Approx.round)
        return md, nmd
    return 1., 0.


def algebraic_pow(p, x0, y0, q):
    """
    :param p:   幂
    :param x0:  第一个数的隶属度
    :param y0:  第一个数的非隶属度
    :param q:   Q 阶
    """
    md = np.round(x0 ** p, Approx.round)
    nmd = np.round((1. - (1. - y0 ** q) ** p) ** (1. / q), Approx.round)
    return md, nmd


def algebraic_times(p, x0, y0, q):
    """
    :param p:   幂
    :param x0:  第一个数的隶属度
    :param y0:  第一个数的非隶属度
    :param q:   Q 阶
    """
    md = np.round((1. - (1. - x0 ** q) ** p) ** (1. / q), Approx.round)
    nmd = np.round(y0 ** p, Approx.round)
    return md, nmd


"""
The following is a calculation of Algebraic norms in fuzzy number.
"""


class AlgebT(Archimedean):
    def function(self, x):
        return np.log2(x)


def algebTao(x):
    return AlgebT()(x)


class AlgebInT(Archimedean):
    def function(self, x):
        return 1 / (2 ** x)


def algebInTao(x):
    return AlgebInT()(x)


class AlgebS(Archimedean):
    def function(self, x):
        return np.log2(1 - x)


def algebS(x):
    return AlgebS()(x)


class AlgebInS(Archimedean):
    def function(self, x):
        return 1 - 1 / (2 ** x)


def algebInS(x):
    return AlgebInS()(x)


class AlgebTNorm(Archimedean):
    def function(self, x, y):
        """
            AlgebInT()((AlgebT()(x) + AlgebT()(y)))
        """
        return x * y


def algebTNorm(x, y):
    return AlgebTNorm()(x, y)


class AlgebSNorm(Archimedean):
    def function(self, x, y):
        """
            AlgebInS()((AlgebS()(x) + AlgebS()(y)))
        """
        return x + y - x * y


def algebSNorm(x, y):
    return AlgebSNorm()(x, y)
