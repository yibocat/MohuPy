#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/11 下午4:50
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
from typing import Union

import numpy as np

from ...core import Fuzznum, Fuzzarray
from ...tensor import Fuzztensor

from .base import Library


class TensorZerosConstruct(Library):
    def __init__(self, qrung):
        self.qrung = qrung

    def function(self, *n):
        from ...corelib.lib.classConstruct import ZerosConstruct
        f = ZerosConstruct(self.qrung)(*n)
        newFTensor = Fuzztensor(f)
        return newFTensor


class TensorPossConstruct(Library):
    def __init__(self, qrung):
        self.qrung = qrung

    def function(self, *n):
        from ...corelib.lib.classConstruct import PossConstruct
        f = PossConstruct(self.qrung)(*n)
        newFTensor = Fuzztensor(f)
        return newFTensor


class TensorNegsConstruct(Library):
    def __init__(self, qrung):
        self.qrung = qrung

    def function(self, *n):
        from ...corelib.lib.classConstruct import NegsConstruct
        f = NegsConstruct(self.qrung)(*n)
        newFTensor = Fuzztensor(f)
        return newFTensor


class TensorFullConstruct(Library):
    def __init__(self, x: Union[Fuzznum, Fuzzarray, Fuzztensor]):
        if x.ndim != 0:
            raise ValueError(f'Fuzztensor must have dimension 1. (ndim: {x.ndim})')
        if isinstance(x, Fuzznum):
            self.fuzz = x
        if isinstance(x, Fuzzarray):
            self.fuzz = x.array
        if isinstance(x, Fuzztensor):
            self.fuzz = x.data.array

    def function(self, *n):
        from ...corelib.lib.classConstruct import FullConstruct
        f = FullConstruct(self.fuzz)(*n)
        newFTensor = Fuzztensor(f)
        return newFTensor


class TensorZerosLikeConstruct(Library):
    def __init__(self, x: Fuzztensor):
        self.fuzz = x

    def function(self):
        return TensorZerosConstruct(self.fuzz.qrung)(*self.fuzz.shape)


class TensorPossLikeConstruct(Library):
    def __init__(self, x: Fuzztensor):
        self.fuzz = x

    def function(self):
        return TensorPossConstruct(self.fuzz.qrung)(*self.fuzz.shape)


class TensorNegsLikeConstruct(Library):
    def __init__(self, x: Fuzztensor):
        self.fuzz = x

    def function(self):
        return TensorNegsConstruct(self.fuzz.qrung)(*self.fuzz.shape)


class TensorFullLikeConstruct(Library):
    """
        按照某个 Fuzztensor 的形状，对某一个数扩展到其相同的形状
        self.x 表示要扩展成的 Fuzztensor 的形状
        y 表示扩展的模糊数
    """
    def __init__(self, x: Fuzztensor):
        self.fuzz = x

    def function(self, y: Fuzztensor):
        return TensorFullConstruct(y)(*self.fuzz.shape)
