#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/10 下午9:18
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import numpy as np

from typing import Union

from ..core import Fuzznum, Fuzzarray

from .fuzztensor import Fuzztensor
from .utils import as_array, as_fuzztensor, as_fuzzarray


def tensor_add(x0, x1) -> Fuzztensor:
    if isinstance(x0, Union[Fuzzarray, Fuzznum]):
        x0 = as_fuzztensor(as_fuzzarray(x0))
    if isinstance(x1, Union[Fuzzarray, Fuzznum]):
        x1 = as_fuzztensor(as_fuzzarray(x1))
    from .operation import Add
    return Add()(x0, x1)


def tensor_sub(x0, x1) -> Fuzztensor:
    if isinstance(x0, Union[Fuzzarray, Fuzznum]):
        x0 = as_fuzztensor(as_fuzzarray(x0))
    if isinstance(x1, Union[Fuzzarray, Fuzznum]):
        x1 = as_fuzztensor(as_fuzzarray(x1))
    from .operation import Sub
    return Sub()(x0, x1)


def tensor_mul(x0, x1) -> Fuzztensor:
    if isinstance(x0, Union[Fuzznum, Fuzzarray]):
        x0 = as_fuzztensor(as_fuzzarray(x0))
    if isinstance(x1, Union[Fuzznum, Fuzzarray]):
        x1 = as_fuzztensor(as_fuzzarray(x1))
    if isinstance(x0, Union[np.ndarray, int, float, np.int_, np.float_]):
        x0 = as_array(x0)
    if isinstance(x1, Union[np.ndarray, int, float, np.int_, np.float_]):
        x1 = as_array(x1)
    from .operation import Mul
    return Mul()(x0, x1)


def tensor_div(x0, x1) -> Fuzztensor:
    if isinstance(x0, Union[Fuzznum, Fuzzarray]):
        x0 = as_fuzztensor(as_fuzzarray(x0))
    if isinstance(x1, Union[Fuzznum, Fuzzarray]):
        x1 = as_fuzztensor(as_fuzzarray(x1))
    if isinstance(x0, Union[np.ndarray, int, float, np.int_, np.float_]):
        x0 = as_array(x0)
    if isinstance(x1, Union[np.ndarray, int, float, np.int_, np.float_]):
        x1 = as_array(x1)
    from .operation import Div
    return Div()(x0, x1)


def tensor_powers(x, p) -> Fuzztensor:
    if isinstance(x, Union[Fuzznum, Fuzzarray]):
        x = as_fuzztensor(as_fuzzarray(x))
    from .operation import Power
    return Power(p)(x)


def tensor_matmul(x0, x1) -> Fuzztensor:
    if isinstance(x0, Union[Fuzznum, Fuzzarray]):
        x0 = as_fuzztensor(as_fuzzarray(x0))
    if isinstance(x1, Union[Fuzznum, Fuzzarray]):
        x1 = as_fuzztensor(as_fuzzarray(x1))
    from .operation import Matmul
    return Matmul()(x0, x1)


def tensor_transpose(x) -> Fuzztensor:
    if isinstance(x, Union[Fuzznum, Fuzzarray]):
        x = as_fuzztensor(as_fuzzarray(x))
    from .operation import Transpose
    return Transpose()(x)


def tensor_reshape(x, *shape) -> Fuzztensor:
    if x.shape == shape:
        return as_fuzztensor(x)
    from .operation import Reshape
    return Reshape(shape)(x)


def tensor_sum(x, axis=None, keepdims=False) -> Fuzztensor:
    from .operation import Sum
    return Sum(axis, keepdims)(x)


def tensor_mean(x, axis=None) -> Fuzztensor:
    # TODO: 暂未完成
    from .operation import Mean
    return Mean(axis)(x)


def tensor_prod(x, axis=None, keepdims=False) -> Fuzztensor:
    # TODO: 暂未完成
    from .operation import Prod
    return Prod(axis, keepdims)(x)


def tensor_broadcast_to(x, *shape) -> Fuzztensor:
    if x.shape == shape:
        return as_fuzztensor(x)
    from .operation import BroadcastTo
    return BroadcastTo(*shape)(x)


def tensor_getitem(x, slices) -> Fuzztensor:
    from .operation import GetItem
    return GetItem(slices)(x)
