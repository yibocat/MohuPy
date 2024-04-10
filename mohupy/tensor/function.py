#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/10 下午1:27
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import copy
from typing import Union

from .base import Function
from .fuzztensor import Fuzztensor
from ..core import Fuzznum, Fuzzarray


class TensorEmpty(Function):
    """
    Fuzztensor 判空有三种情况：

    1. Fuzztensor 非空，即 Fuzzarray.data 非空
    2. Fuzztensor.data 的 Fuzzarray 数组为空，但是存在 Fuzzarray 这个模糊数集合
    3. Fuzztensor.data 不存在，Fuzzarray 直接 None
    """

    def __init__(self, onlyfn: bool):
        self.onlyfn = onlyfn

    def forward(self, x: Fuzztensor):
        if x.data is None:
            return True
        else:
            from ..core.funcitonClass import FuzzEmpty
            return FuzzEmpty()(x.data, self.onlyfn)


class TensorValidity(Function):
    def forward(self, x: Fuzztensor):
        if x.data is None:
            return False
        from ..core.funcitonClass import FuzzValidity
        return FuzzValidity()(x.data)


class TensorInit(Function):
    def forward(self, x: Fuzztensor):
        if x.data is None:
            return True
        from ..core.funcitonClass import FuzzInitial
        return FuzzInitial()(x.data)


class TensorSort(Function):
    def forward(self, x: Fuzztensor):
        # TODO: Fuzztensor 的排序算法暂未实现，这涉及到采用得分值比较还是减法比较规则
        raise NotImplementedError('Not implemented for sort function.')


class TensorUnique(Function):
    """
    返回 Fuzztensor 的唯一不重复元素
    """
    def forward(self, x: Fuzztensor):
        from ..core.funcitonClass import FuzzUnique
        x.data = FuzzUnique()(x.data, False)
        return x


class TensorAppend(Function):
    def __init__(self, e: Union[Fuzznum, Fuzzarray, Fuzztensor]):
        if isinstance(e, Union[Fuzznum, Fuzzarray]):
            self.e = e
        else:
            self.e = e.data

    def forward(self, x: Fuzztensor):
        if x.data is None:
            x.data = copy.deepcopy(self.e)
            return x
        else:
            from ..core.funcitonClass import FuzzAppend
            x.data = FuzzAppend()(x.data, self.e)
            return x


class TensorRemove(Function):

    def __init__(self, e: Fuzznum):
        if not isinstance(e, Fuzznum):
            raise TypeError(f'Not implemented of {type(e)} for remove function.')
        self.e = e

    def forward(self, x: Fuzztensor):
        from ..core.funcitonClass import FuzzRemove
        x.data = FuzzRemove()(x.data, self.e)
        return x


class TensorPop(Function):

    def __init__(self, index):
        self.index = index

    def forward(self, x: Fuzztensor):
        from ..core.funcitonClass import FuzzPop
        x.data = FuzzPop()(x.data, self.index)
        return x


class TensorSqueeze(Function):

    def __init__(self, axis):
        self.axis = axis

    def forward(self, x: Fuzztensor):
        from ..core.funcitonClass import FuzzSqueeze
        x.data = FuzzSqueeze()(x.data, self.axis)
        return x


class TensorClear(Function):

    def __init__(self, to_none):
        self.to_none = to_none

    def forward(self, x: Fuzztensor):
        if self.to_none:
            x.data = None
        else:
            from ..core.funcitonClass import FuzzClear
            x = Fuzztensor(FuzzClear()(x.data))
        return x


class TensorInitialize(Function):
    def forward(self, x: Fuzztensor):
        x.data = None
        return x





#
# class TensorBroadcastTo(Operation):
#     def __init__(self, shape):
#         self.shape = shape
#
#     def forward(self, x: Fuzztensor):
#         # self.x_shape = x.shape
#         from ..core.functionClass import FuzzBroadcast
#         newFTensor = FuzzBroadcast()(x.data, self.shape)
#         return newFTensor
#
#     def backward(self, grad):
#         ...
#
#
# class TensorSumTo(Operation):
#     def __init__(self, shape):
#         self.shape = shape
#
#     def forward(self, x: Fuzztensor):
#         ...
#
#
#
#
#
#
#
#









