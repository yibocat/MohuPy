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
            return FuzzEmpty(self.onlyfn)(x.data)


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
        newFTensor = Fuzztensor()
        newFTensor.data = FuzzUnique(False)(x.data)
        return newFTensor


class TensorAppend(Function):
    def __init__(self, e: Union[Fuzznum, Fuzzarray, Fuzztensor]):
        if isinstance(e, Union[Fuzznum, Fuzzarray]):
            self.e = e
        else:
            self.e = e.data

    def forward(self, x: Fuzztensor):
        if x.data is None:
            newFTensor = Fuzztensor()
            newFTensor.data = copy.deepcopy(self.e)
            return newFTensor
        else:
            from ..core.funcitonClass import FuzzAppend
            newFTensor = Fuzztensor()
            newFTensor.data = FuzzAppend(self.e)(x.data)
            return newFTensor


class TensorRemove(Function):

    def __init__(self, e: Union[Fuzznum, Fuzzarray, Fuzztensor]):
        if not isinstance(e, Union[Fuzznum, Fuzzarray, Fuzztensor]):
            raise TypeError(f'Not implemented of {type(e)} for remove function.')
        if isinstance(e, Fuzznum):
            self.e = e
        if isinstance(e, Fuzzarray):
            self.e = e.array
        if isinstance(e, Fuzztensor):
            self.e = e.data.array

    def forward(self, x: Fuzztensor):
        from ..core.funcitonClass import FuzzRemove
        newFTensor = Fuzztensor()
        newFTensor.data = FuzzRemove(self.e)(x.data)
        return newFTensor


class TensorPop(Function):

    def __init__(self, index):
        self.index = index

    def forward(self, x: Fuzztensor):
        from ..core.funcitonClass import FuzzPop
        newFTensor = Fuzztensor()
        newFTensor.data = FuzzPop(self.index)(x.data)
        return newFTensor


class TensorSqueeze(Function):

    def __init__(self, axis):
        self.axis = axis

    def forward(self, x: Fuzztensor):
        from ..core.funcitonClass import FuzzSqueeze
        newFTensor = Fuzztensor()
        newFTensor.data = FuzzSqueeze(self.axis)(x.data)
        return newFTensor


class TensorClear(Function):

    def __init__(self, to_none):
        self.to_none = to_none

    def forward(self, x: Fuzztensor):
        if self.to_none:
            newFTensor = copy.deepcopy(x)
            newFTensor.data = None
            return newFTensor
        else:
            from ..core.funcitonClass import FuzzClear
            newFTensor = Fuzztensor(FuzzClear()(x.data))
            return newFTensor


class TensorInitialize(Function):
    def forward(self, x: Fuzztensor):
        newFTensor = copy.deepcopy(x)
        newFTensor.data = None
        return newFTensor


class TensorRavel(Function):
    def forward(self, x: Fuzztensor):
        from ..core.funcitonClass import FuzzRavel
        newFTensor = Fuzztensor()
        newFTensor.data = FuzzRavel()(x.data)
        return newFTensor


class TensorFlatten(Function):
    def forward(self, x: Fuzztensor):
        from ..core.funcitonClass import FuzzFlatten
        newFTensor = Fuzztensor()
        newFTensor.data = FuzzFlatten()(x.data)
        return newFTensor


class TensorGetMax(Function):
    def __init__(self, show, axis):
        self.show = show
        self.axis = axis

    def forward(self, x: Fuzztensor):
        from ..core.funcitonClass import FuzzGetMax
        newFTensor = Fuzztensor()
        newFTensor.data = FuzzGetMax(self.show, self.axis)(x.data)
        return newFTensor


class TensorGetMin(Function):
    def __init__(self, show, axis):
        self.show = show
        self.axis = axis

    def forward(self, x: Fuzztensor):
        from ..core.funcitonClass import FuzzGetMin
        newFTensor = Fuzztensor()
        newFTensor.data = FuzzGetMin(self.show, self.axis)(x.data)
        return newFTensor


class TensorGetFmax(Function):
    def __init__(self, show, axis, func, *params):
        self.show = show
        self.axis = axis
        self.func = func
        self.params = params

    def forward(self, x: Fuzztensor):
        from ..core.funcitonClass import FuzzGetFmax
        newFTensor = Fuzztensor()
        newFTensor.data = FuzzGetFmax(self.show, self.axis, self.func, *self.params)(x)
        return newFTensor


class TensorGetFmin(Function):
    def __init__(self, show, axis, func, *params):
        self.show = show
        self.axis = axis
        self.func = func
        self.params = params

    def forward(self, x: Fuzztensor):
        from ..core.funcitonClass import FuzzGetFmin
        newFTensor = Fuzztensor()
        newFTensor.data = FuzzGetFmin(self.show, self.axis, self.func, *self.params)(x)
        return newFTensor
