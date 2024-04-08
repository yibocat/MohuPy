#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/8 下午1:31
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
from typing import Union

import numpy as np

from .base import Function
from .fuzztensor import Fuzztensor
from ..core import Fuzzarray, Fuzznum


class TensorEmpty(Function):

    def __init__(self, only_data: bool):
        self.only_data = only_data

    def function(self, x: Fuzztensor):
        if not self.only_data:
            return True if x.data is None else False
        else:
            from ..core.funcitonClass import FuzzEmpty
            return FuzzEmpty()(x.data, False)


class TensorValidity(Function):
    def function(self, x: Fuzztensor):
        from ..core.funcitonClass import FuzzValidity
        return FuzzValidity()(x.data)


class TensorInitial(Function):
    def function(self, x: Fuzztensor):
        from ..core.funcitonClass import FuzzInitial
        return FuzzInitial()(x.data)


class TensorSort(Function):
    def function(self, x: Fuzztensor):
        # TODO
        raise NotImplementedError('Not implemented for sort function.')


class TensorUnique(Function):
    def function(self, x: Fuzztensor):
        from ..core.funcitonClass import FuzzUnique
        newFTensor = Fuzztensor()
        newFTensor.data = FuzzUnique()(x.data, False)
        return newFTensor


class TensorAppend(Function):
    def function(self, x: Fuzztensor, e: Union[Fuzznum, Fuzzarray]):
        from ..core.funcitonClass import FuzzAppend
        if x.data is None:
            newFTensor = Fuzztensor()
            newFTensor.data = e
            return newFTensor
        else:
            newFTensor = Fuzztensor()
            newFTensor.data = FuzzAppend()(x.data, e)
            return newFTensor


class TensorRemove(Function):
    def function(self, x: Fuzztensor, e):
        if isinstance(e, Union[Fuzznum, Fuzzarray]):
            from ..core.funcitonClass import FuzzRemove
            newFTensor = Fuzztensor()
            newFTensor.data = FuzzRemove()(x.data, e)
            return newFTensor
        else:
            newFTensor = Fuzztensor()
            newFTensor.data = np.delete(x.data, np.where(x.data == e))
            return newFTensor


class TensorPop(Function):
    def function(self, x: Fuzztensor, i):
        from ..core.funcitonClass import FuzzPop
        newFTensor = Fuzztensor()
        newFTensor.data = FuzzPop()(x.data, i)
        return newFTensor


class TensorSqueeze(Function):
    def function(self, x: Fuzztensor, axis):
        from ..core.funcitonClass import FuzzSqueeze
        newFTensor = Fuzztensor()
        newFTensor.data = FuzzSqueeze()(x.data, axis)
        return newFTensor


class TensorClear(Function):
    def function(self, x: Fuzztensor):
        from ..core.funcitonClass import FuzzClear
        newFTensor = Fuzztensor()
        newFTensor.data = FuzzClear()(x.data)
        return newFTensor


class TensorBroadcast(Function):
    def function(self, x: Fuzztensor, shape):
        from ..core.funcitonClass import FuzzBroadcast
        newFTensor = Fuzztensor()
        newFTensor.data = FuzzBroadcast()(x.data, shape)
        return newFTensor


class TensorFlatten(Function):
    def function(self, x: Fuzztensor):
        from ..core.funcitonClass import FuzzFlatten
        newFTensor = Fuzztensor()
        newFTensor.data = FuzzFlatten()(x.data)
        return newFTensor


class TensorGetMax(Function):
    def function(self, x: Fuzztensor, show, axis):
        from ..core.funcitonClass import FuzzGetMax
        newFTensor = Fuzztensor()
        newFTensor.data = FuzzGetMax()(x.data, show, axis)
        return newFTensor


class TensorGetMin(Function):
    def function(self, x: Fuzztensor, show, axis):
        from ..core.funcitonClass import FuzzGetMin
        newFTensor = Fuzztensor()
        newFTensor.data = FuzzGetMin()(x.data, show, axis)
        return newFTensor


class TensorGetFmax(Function):
    def function(self, x: Fuzztensor, func, *args, show, axis):
        from ..core.funcitonClass import FuzzGetFmax
        newFTensor = Fuzztensor()
        newFTensor.data = FuzzGetFmax()(x.data, func, *args, show, axis)
        return newFTensor


class TensorGetFmin(Function):
    def function(self, x: Fuzztensor, func, *args, show, axis):
        from ..core.funcitonClass import FuzzGetFmin
        newFTensor = Fuzztensor()
        newFTensor.data = FuzzGetFmin()(x.data, func, *args, show, axis)
        return newFTensor


class TensorGetSum(Function):
    def function(self, x: Fuzztensor, axis, keepdims):
        from ..core.funcitonClass import FuzzGetSum
        newFTensor = Fuzztensor()
        newFTensor.data = FuzzGetSum()(x.data, axis, keepdims)
        return newFTensor


class TensorGetProd(Function):
    def function(self, x: Fuzztensor, axis, keepdims):
        from ..core.funcitonClass import FuzzGetProd
        newFTensor = Fuzztensor()
        newFTensor.data = FuzzGetProd()(x.data, axis, keepdims)
        return newFTensor


class TensorGetMean(Function):
    def function(self, x: Fuzztensor, axis):
        from ..core.funcitonClass import FuzzMean
        newFTensor = Fuzztensor()
        newFTensor.data = FuzzMean()(x.data, axis)
        return newFTensor