#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/6 下午2:47
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import numpy as np

from ..base import Archimedean


class EinsT(Archimedean):
    def function(self, x):
        return np.log2((2 - x) / x)


def einsTao(x):
    return EinsT()(x)


class EinsInT(Archimedean):
    def function(self, x):
        return 2 / ((2 ** x) + 1)


def einsInTao(x):
    return EinsInT()(x)


class EinsS(Archimedean):
    def function(self, x):
        return np.log2((1 + x) / (1 - x))


def einsS(x):
    return EinsS()(x)


class EinsInS(Archimedean):
    def function(self, x):
        return (2 ** x - 1) / (2 ** x + 1)


def einsInS(x):
    return EinsInS()(x)


class EinsTNorm(Archimedean):
    def function(self, x, y):
        """
            EinsInT()((EinsT()(x) + EinsT()(y)))
        """
        return (x * y) / (1 + (1 - x) * (1 - y))


def einsTNorm(x, y):
    return EinsTNorm()(x, y)


class EinsSNorm(Archimedean):
    def function(self, x, y):
        """
            EinsInS()((EinsS()(x) + EinsS()(y)))
        """
        return (x + y) / (1 + x * y)


def einsSNorm(x, y):
    return EinsSNorm()(x, y)