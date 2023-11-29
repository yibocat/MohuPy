#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/11/26 下午3:05
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
from typing import Union

from .base import mohunum
from .attributes import score, acc, ind, comp
from .function import initializeNum, transpose


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
    def comp(self):
        return comp(self)


from .attributes import report, string
from .function import (isValid, isEmpty, isInitial, convert, qsort, unique,
                       append, reshape, squeeze, clear,
                       ravel, flatten, getmax, getmin, getsum, getprod, mean)

Fuzznum.__repr__ = report
Fuzznum.__str__ = string
Fuzznum.isValid = isValid
Fuzznum.isEmpty = isEmpty
Fuzznum.isInitial = isInitial
Fuzznum.convert = convert
Fuzznum.qsort = qsort
Fuzznum.unique = unique
Fuzznum.append = append
Fuzznum.reshape = reshape
Fuzznum.squeeze = squeeze
Fuzznum.clear = clear
Fuzznum.ravel = ravel
Fuzznum.flatten = flatten
Fuzznum.max = getmax
Fuzznum.min = getmin
Fuzznum.sum = getsum
Fuzznum.prod = getprod
Fuzznum.mean = mean

