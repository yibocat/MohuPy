#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/6 下午12:47
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

# from typing import Union

from .base import MohuBase


class Fuzznum(MohuBase):
    qrung = None
    md = None
    nmd = None
    ndim = 0
    size = 0
    shape = ()

    def __init__(self, qrung=None, md=None, nmd=None):
        if qrung is None or (md is None and nmd is None):
            from ..config import Config
            self.mtype = Config.mtype
            self.qrung = qrung
            self.size = 0 if qrung is None else 1

        if qrung is not None and md is not None and nmd is not None:
            from .funcitonClass import InitializeNum
            self.qrung = qrung
            self.mtype, self.md, self.nmd = InitializeNum()(qrung, md, nmd)
            self.size = 1

    @property
    def T(self):
        from .funcitonClass import FuzzTranspose
        return FuzzTranspose()(self)

    @property
    def score(self):
        from .attributeClass import Score
        return Score()(self)

    @property
    def acc(self):
        from .attributeClass import Accuracy
        return Accuracy()(self)

    @property
    def ind(self):
        from .attributeClass import Indeterminacy
        return Indeterminacy()(self)

    @property
    def comp(self):
        from .attributeClass import Complement
        return Complement()(self)

    def valid(self):
        from .funcitonClass import FuzzValidity
        return FuzzValidity()(self)

    def empty(self, onlyfn=False):
        from .funcitonClass import FuzzEmpty
        return FuzzEmpty(onlyfn)(self)

    def initial(self):
        from .funcitonClass import FuzzInitial
        return FuzzInitial()(self)

    def convert(self):
        from .funcitonClass import FuzzConvert
        return FuzzConvert()(self)

    def qsort(self, reverse=False):
        from .funcitonClass import FuzzQsort
        return FuzzQsort(reverse)(self)

    def unique(self, onlyfn=False):
        from .funcitonClass import FuzzUnique
        return FuzzUnique(onlyfn)(self)

    def append(self, e):
        from .funcitonClass import FuzzAppend
        return FuzzAppend(e)(self)

    def reshape(self, *shape):
        from .funcitonClass import FuzzReshape
        return FuzzReshape(*shape)(self)

    def squeeze(self, axis=None):
        from .funcitonClass import FuzzSqueeze
        return FuzzSqueeze(axis)(self)

    def clear(self):
        from .funcitonClass import FuzzClear
        return FuzzClear()(self)

    def ravel(self):
        from .funcitonClass import FuzzRavel
        return FuzzRavel()(self)

    def flatten(self):
        from .funcitonClass import FuzzFlatten
        return FuzzFlatten()(self)

    def max(self, show=False, axis=None):
        from .funcitonClass import FuzzGetMax
        return FuzzGetMax(show, axis)(self)

    def min(self, show=False, axis=None):
        from .funcitonClass import FuzzGetMin
        return FuzzGetMin(show, axis)(self)

    def sum(self, axis=None, keepdims=False):
        from .funcitonClass import FuzzGetSum
        return FuzzGetSum(axis, keepdims)(self)

    def prod(self, axis=None, keepdims=False):
        from .funcitonClass import FuzzGetProd
        return FuzzGetProd(axis, keepdims)(self)

    def mean(self, axis=None):
        from .funcitonClass import FuzzMean
        return FuzzMean(axis)(self)
