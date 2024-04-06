#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/6 下午1:40
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
from typing import Union

from .funcitonClass import *
from .fuzzarray import Fuzzarray
from .fuzznums import Fuzznum


def initializeNum(qrung, md, nmd):
    return InitializeNum()(qrung, md, nmd)


def initializeSet(qrung, mtype):
    return InitializeSet()(qrung, mtype)


def isValid(x):
    # TODO: 未来版本可能抛弃
    return Validity()(x)


def valid(x):
    return Validity()(x)


def isEmpty(x, onlyfn=False):
    # TODO: 未来版本可能抛弃
    return Empty()(x, onlyfn)


def empty(x, onlyfn=False):
    return Empty()(x, onlyfn)


def isInitial(x):
    # TODO: 未来版本可能抛弃
    return Initial()(x)


def initial(x):
    return Initial()(x)


def convert(x):
    return Convert()(x)


def qsort(x, reverse=True) -> Union[Fuzznum, Fuzzarray]:
    return Qsort()(x, reverse)


def unique(x, onlyfn=False) -> Union[Fuzznum, Fuzzarray]:
    return Unique()(x, onlyfn)


def transpose(x) -> Union[Fuzznum, Fuzzarray]:
    return Transpose()(x)


def append(x, e) -> Fuzzarray:
    return Append()(x, e)


def remove(x, e) -> Fuzzarray:
    return Remove()(x, e)


def pop(x, e) -> Fuzzarray:
    return Pop()(x, e)


def reshape(x, *shape) -> Union[Fuzznum, Fuzzarray]:
    return Reshape()(x, *shape)


def squeeze(x, axis=None) -> Union[Fuzznum, Fuzzarray]:
    return Squeeze()(x, axis)


def broadcast_to(x, shape) -> Fuzzarray:
    return Broadcast()(x, shape)


def clear(x) -> Union[Fuzznum, Fuzzarray]:
    return Clear()(x)


def ravel(x) -> Union[Fuzznum, Fuzzarray]:
    return Ravel()(x)


def flatten(x) -> Union[Fuzznum, Fuzzarray]:
    return Flatten()(x)


def getmax(x, show=False, axis=None) -> Union[Fuzznum, Fuzzarray]:
    return GetMax()(x, show, axis)


def getmin(x, show=False, axis=None) -> Union[Fuzznum, Fuzzarray]:
    return GetMin()(x, show, axis)


def fmax(x, func, *args, show=False, axis=None) -> Union[Fuzznum, Fuzzarray]:
    return GetMax()(x, func, *args, show, axis)


def fmin(x, func, *args, show=False, axis=None) -> Union[Fuzznum, Fuzzarray]:
    return GetFmin()(x, func, *args, show, axis)


def getsum(x, axis=None, keepdims=False) -> Union[Fuzznum, Fuzzarray]:
    return GetSum()(x, axis, keepdims)


def getprod(x, axis=None, keepdims=False) -> Union[Fuzznum, Fuzzarray]:
    return GetProd()(x, axis, keepdims)


def mean(x, axis=None) -> Union[Fuzznum, Fuzzarray]:
    return Mean()(x, axis)


def normalize(d1, d2, t=1.) -> (Fuzznum, Fuzznum):
    return Normalize()(d1, d2, t)


def absolute(x, y) -> Union[Fuzznum, Fuzzarray]:
    return Absolute()(x, y)
