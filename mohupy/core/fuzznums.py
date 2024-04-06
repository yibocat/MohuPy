#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/6 下午12:47
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
from typing import Union

from .base import MohuBase


class Fuzznum(MohuBase):
    qrung = None
    mtype = None
    md = None
    nmd = None

    def __init__(self, qrung=None, md=None, nmd=None):
        self.ndim = 0
        self.size = 1
        self.shape = ()

        from .function import initializeNum
        if qrung is not None and md is not None and nmd is not None:
            self.qrung = qrung
            self.mtype, self.md, self.nmd = initializeNum(qrung, md, nmd)

    @property
    def T(self):
        from .function import transpose
        return transpose(self)

    @property
    def score(self):
        from .attribute import score
        return score(self)

    @property
    def acc(self):
        from .attribute import acc
        return acc(self)

    @property
    def ind(self):
        from .attribute import ind
        return ind(self)

    @property
    def comp(self):
        from .attribute import comp
        return comp(self)

    def valid(self):
        from .function import valid
        return valid(self)

    def empty(self, onlyfn=False):
        from .function import empty
        return empty(self, onlyfn)

    def initial(self):
        from .function import initial
        return initial(self)

    def convert(self):
        from .function import convert
        return convert(self)

    def qsort(self, reverse=False):
        from .function import qsort
        return qsort(self, reverse=reverse)

    def unique(self, onlyfn=False):
        from .function import unique
        return unique(self, onlyfn)

    def append(self, e):
        from .function import append
        return append(self, e)

    def reshape(self, *shape):
        from .function import reshape
        return reshape(self, *shape)

    def squeeze(self, axis=None):
        from .function import squeeze
        return squeeze(self, axis)

    def clear(self):
        from .function import clear
        return clear(self)

    def ravel(self):
        from .function import ravel
        return ravel(self)

    def flatten(self):
        from .function import flatten
        return flatten(self)

    def max(self, show=False, axis=None):
        from .function import getmax
        return getmax(self, show, axis)

    def min(self, show=False, axis=None):
        from .function import getmin
        return getmin(self, show, axis)

    def sum(self, axis=None, keepdims=False):
        from .function import getsum
        return getsum(self, axis, keepdims)

    def prod(self, axis=None, keepdims=False):
        from .function import getprod
        return getprod(self, axis, keepdims)

    def mean(self, axis=None):
        from .function import mean
        return mean(self, axis)
