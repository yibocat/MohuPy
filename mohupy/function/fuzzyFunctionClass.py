#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/7 下午9:02
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
from typing import Union

from .base import Function
from ..core import Fuzznum, Fuzzarray


class Sort(Function):
    """
        排序
    """


class Append(Function):
    """
        添加元素
        1. Tensor(Fuzznum) + Fuzznum
        2. Tensor(Fuzznum) + Fuzzarray
        3. Tensor(Fuzzarray) + Fuzznum
        4. Tensor(Fuzzarray) + Fuzzarray
        5. Fuzznum + Tensor(Fuzznum)
        6. Fuzznum + Tensor(Fuzzarray)
        7. Fuzzarray + Tensor(Fuzznum)
        8. Fuzzarray + Tensor(Fuzzarray)
    """
    def function(self, x, e):
        if isinstance(x, Union[Fuzznum, Fuzzarray]) and isinstance(e, Union[Fuzznum, Fuzzarray]):
            from ..core.funcitonClass import FuzzAppend
            return FuzzAppend()(x, e)


class Remove(Function):
    ...


class Pop(Function):
    ...


class Reshape(Function):
    ...


class Squeeze(Function):
    ...


class Broadcast(Function):
    ...


class Clear(Function):
    ...


class Ravel(Function):
    ...


class Flatten(Function):
    ...


class GetMax(Function):
    ...


class GetMin(Function):
    ...


class GetFmax(Function):
    ...


class GetFmin(Function):
    ...


class GetSum(Function):
    ...


class GetProd(Function):
    ...


class Mean(Function):
    ...


class Absolute(Function):
    ...


