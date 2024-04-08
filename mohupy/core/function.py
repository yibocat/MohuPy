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


# def initializeNum(qrung, md, nmd):
#     return InitializeNum()(qrung, md, nmd)
#
#
# def initializeSet(qrung, mtype):
#     return InitializeSet()(qrung, mtype)
#
#
# def isValid(x):
#     # TODO: 未来版本可能抛弃
#     return FuzzValidity()(x)
#
#
# def valid(x):
#     return FuzzValidity()(x)
#
#
# def isEmpty(x, onlyfn=False):
#     # TODO: 未来版本可能抛弃
#     return FuzzEmpty()(x, onlyfn)
#
#
# def empty(x, onlyfn=False):
#     return FuzzEmpty()(x, onlyfn)
#
#
# def isInitial(x):
#     # TODO: 未来版本可能抛弃
#     return FuzzInitial()(x)
#
#
# def initial(x):
#     return FuzzInitial()(x)
#
#
# def convert(x):
#     return FuzzConvert()(x)
#
#
# def qsort(x, reverse=True) -> Union[Fuzznum, Fuzzarray]:
#     return FuzzQsort()(x, reverse)
#
#
# def unique(x, onlyfn=False) -> Union[Fuzznum, Fuzzarray]:
#     return FuzzUnique()(x, onlyfn)
#
#
# def transpose(x) -> Union[Fuzznum, Fuzzarray]:
#     return FuzzTranspose()(x)
#
#
# def append(x, e) -> Fuzzarray:
#     return FuzzAppend()(x, e)
#
#
# def remove(x, e) -> Fuzzarray:
#     return FuzzRemove()(x, e)
#
#
# def pop(x, e) -> Fuzzarray:
#     return FuzzPop()(x, e)
#
#
# def reshape(x, *shape) -> Union[Fuzznum, Fuzzarray]:
#     return FuzzReshape()(x, *shape)
#
#
# def squeeze(x, axis=None) -> Union[Fuzznum, Fuzzarray]:
#     return FuzzSqueeze()(x, axis)
#
#
# def broadcast_to(x, shape) -> Fuzzarray:
#     return FuzzBroadcast()(x, shape)
#
#
# def clear(x) -> Union[Fuzznum, Fuzzarray]:
#     return FuzzClear()(x)
#
#
# def ravel(x) -> Union[Fuzznum, Fuzzarray]:
#     return FuzzRavel()(x)
#
#
# def flatten(x) -> Union[Fuzznum, Fuzzarray]:
#     return FuzzFlatten()(x)
#
#
# def getmax(x, show=False, axis=None) -> Union[Fuzznum, Fuzzarray]:
#     return FuzzGetMax()(x, show, axis)
#
#
# def getmin(x, show=False, axis=None) -> Union[Fuzznum, Fuzzarray]:
#     return FuzzGetMin()(x, show, axis)
#
#
# def fmax(x, func, *args, show=False, axis=None) -> Union[Fuzznum, Fuzzarray]:
#     return FuzzGetMax()(x, func, *args, show, axis)
#
#
# def fmin(x, func, *args, show=False, axis=None) -> Union[Fuzznum, Fuzzarray]:
#     return FuzzGetFmin()(x, func, *args, show, axis)
#
#
# def getsum(x, axis=None, keepdims=False) -> Union[Fuzznum, Fuzzarray]:
#     return FuzzGetSum()(x, axis, keepdims)
#
#
# def getprod(x, axis=None, keepdims=False) -> Union[Fuzznum, Fuzzarray]:
#     return FuzzGetProd()(x, axis, keepdims)
#
#
# def mean(x, axis=None) -> Union[Fuzznum, Fuzzarray]:
#     return FuzzMean()(x, axis)
#
#

# def normalize(d1, d2, t=1.) -> (Fuzznum, Fuzznum):
#     return FuzzNormalize()(d1, d2, t)
#
#
# def absolute(x, y) -> Union[Fuzznum, Fuzzarray]:
#     return FuzzAbsolute()(x, y)
