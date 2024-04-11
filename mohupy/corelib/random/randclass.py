#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/7 下午1:35
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import numpy as np

from .base import Random
# from ...core import Fuzznum, Fuzzarray
from ...config import Config


class RandNum(Random):
    def __init__(self, qrung, minnum, maxnum):
        self.qrung = qrung
        self.minnum = minnum
        self.maxnum = maxnum

    def function(self):
        from ..regedit import fuzzRandom
        return fuzzRandom[Config.mtype](self.qrung, self.minnum, self.maxnum)


# def randnum(q: int, minnum=1, maxnum=5) -> Fuzznum:
#     return RandNum(q, minnum, maxnum)()


class RandSet(Random):

    def __init__(self, qrung, minnum, maxnum):
        self.qrung = qrung
        self.minnum = minnum
        self.maxnum = maxnum

    def function(self, *n):

        # from ..lib import zeros

        from ..lib.classConstruct import ZerosConstruct
        newset = ZerosConstruct(self.qrung)(*n)
        vec_func = np.vectorize(lambda _: RandNum(self.qrung, self.minnum, self.maxnum)())
        result = vec_func(newset.array)
        newset.array = result
        return newset


# def randset(*n, q=1, minnum=1, maxnum=5) -> Fuzzarray:
#     return RandSet(q, minnum, maxnum)(*n)


class Rand(Random):

    def __init__(self, qrung, minnum, maxnum):
        self.qrung = qrung
        self.minnum = minnum
        self.maxnum = maxnum

    def function(self, *n):
        if len(n) == 0:
            return RandNum(self.qrung, self.minnum, self.maxnum)()
        else:
            return RandSet(self.qrung, self.minnum, self.maxnum)(*n)


class Choice(Random):
    def function(self, f, n, replace):

        if n is not None:
            from ...core import Fuzzarray
            if replace:
                t = np.random.choice(f.array, size=n, replace=replace)
                f.array = t
                return f
            else:
                newset = Fuzzarray(f.qrung)
                newset.array = np.random.choice(f.array, size=n, replace=replace)
                return newset
        else:
            return np.random.choice(f.array.flatten())


def seed(x):
    np.random.seed(x)
