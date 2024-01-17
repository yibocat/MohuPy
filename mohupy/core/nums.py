#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/11/26 下午3:05
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from .base import mohunum
from .attributes import score, acc, ind, comp
from .function import initializeNum, transpose
from .function import (isValid, isEmpty, isInitial, convert, qsort, unique,
                       append, reshape, squeeze, clear,
                       ravel, flatten, getmax, getmin, getsum, getprod, mean)


class Fuzznum(mohunum):
    qrung = None
    mtype = None
    md = None
    nmd = None

    def __init__(self, qrung=None, md=None, nmd=None):
        self.ndim = 0
        self.size = 1
        self.shape = ()

        if qrung is not None and md is not None and nmd is not None:
            self.qrung = qrung
            self.mtype, self.md, self.nmd = initializeNum(qrung, md, nmd)

    @property
    def T(self):
        return transpose(self)

    @property
    def score(self):
        return score(self)

    @property
    def acc(self):
        return acc(self)

    @property
    def ind(self):
        return ind(self)

    @property
    def comp(self): return comp(self)

    def isValid(self): return isValid(self)

    def isEmpty(self, onlyfn=False): return isEmpty(self, onlyfn)

    def isInitial(self): return isInitial(self)

    def convert(self): return convert(self)

    def qsort(self, reverse=False): return qsort(self, reverse)

    def unique(self, onlyfn=False): return unique(self, onlyfn)

    def append(self, e): return append(self, e)

    def reshape(self, *shape): return reshape(self, *shape)

    def squeeze(self, axis=None): return squeeze(self, axis)

    def clear(self): return clear(self)

    def ravel(self): return ravel(self)

    def flatten(self): return flatten(self)

    def max(self, show=False, axis=None): return getmax(self, show, axis)

    def min(self, show=False, axis=None): return getmin(self, show, axis)

    def sum(self, axis=None, keepdims=False): return getsum(self, axis, keepdims)

    def prod(self, axis=None, keepdims=False): return getprod(self, axis, keepdims)

    def mean(self, axis=None): return mean(self, axis)

