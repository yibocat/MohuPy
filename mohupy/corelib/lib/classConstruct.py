#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/7 下午1:57
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
from typing import Union

import numpy as np

from ...core import Fuzznum, Fuzzarray
from ..regedit import fuzzZeros, fuzzPoss, fuzzNegs, fuzzZero, fuzzPos, fuzzNeg
from .base import Library
from ...config import Config


class ZerosConstruct(Library):
    def __init__(self, qrung):
        self.qrung = qrung

    def function(self, *n):
        mtype = Config.mtype
        return fuzzZero[mtype](self.qrung) if len(n) == 0 else fuzzZeros[mtype](self.qrung, *n)


class PossConstruct(Library):
    def __init__(self, qrung):
        self.qrung = qrung

    def function(self, *n):
        mtype = Config.mtype
        return fuzzPos[mtype](self.qrung) if len(n) == 0 else fuzzPoss[mtype](self.qrung, *n)


class NegsConstruct(Library):
    def __init__(self, qrung):
        self.qrung = qrung

    def function(self, *n):
        mtype = Config.mtype
        return fuzzNeg[mtype](self.qrung) if len(n) == 0 else fuzzNegs[mtype](self.qrung, *n)


class FullConstruct(Library):
    def __init__(self, x: Fuzznum):
        self.fuzznum = x

    def function(self, *n):
        s = np.full(n, self.fuzznum, dtype=object)
        newset = Fuzzarray(self.fuzznum.qrung)
        newset.array = s
        return newset


class ZerosLikeConstruct(Library):
    def __init__(self, x: Union[Fuzznum, Fuzzarray]):
        self.fuzznum = x

    def function(self):
        return ZerosConstruct(self.fuzznum.qrung)(*self.fuzznum.shape)


class PossLikeConstruct(Library):
    def __init__(self, x: Union[Fuzznum, Fuzzarray]):
        self.fuzznum = x

    def function(self):
        return PossConstruct(self.fuzznum.qrung)(*self.fuzznum.shape)


class NegsLikeConstruct(Library):
    def __init__(self, x: Union[Fuzznum, Fuzzarray]):
        self.fuzznum = x

    def function(self):
        return NegsConstruct(self.fuzznum.qrung)(*self.fuzznum.shape)


class FullLikeConstruct(Library):
    def __init__(self, x: Fuzzarray):
        self.x = x

    def function(self, y: Fuzznum):
        return FullConstruct(y)(*self.x.shape)
