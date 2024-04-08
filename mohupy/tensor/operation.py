#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/7 下午4:10
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import numpy as np
from typing import Union

from ..core import Fuzznum, Fuzzarray

from .fuzztensor import Fuzztensor
from .utils import as_fuzzarray, as_array,as_fuzztensor


def add(x0, x1) -> Fuzztensor:
    if isinstance(x0, Union[Fuzzarray, Fuzznum]):
        x0 = as_fuzztensor(as_fuzzarray(x0))
    if isinstance(x1, Union[Fuzzarray, Fuzznum]):
        x1 = as_fuzztensor(as_fuzzarray(x1))
    from .operationClass import Add
    return Add()(x0, x1)


def sub(x0, x1) -> Fuzztensor:
    if isinstance(x0, Union[Fuzzarray, Fuzznum]):
        x0 = as_fuzztensor(as_fuzzarray(x0))
    if isinstance(x1, Union[Fuzzarray, Fuzznum]):
        x1 = as_fuzztensor(as_fuzzarray(x1))
    from .operationClass import Sub
    return Sub()(x0, x1)


def mul(x0, x1) -> Fuzztensor:
    if isinstance(x0, Union[Fuzznum, Fuzzarray]):
        x0 = as_fuzztensor(as_fuzzarray(x0))
    if isinstance(x1, Union[Fuzznum, Fuzzarray]):
        x1 = as_fuzztensor(as_fuzzarray(x1))
    if isinstance(x0, Union[np.ndarray, int, float, np.int_, np.float_]):
        x0 = as_array(x0)
    if isinstance(x1, Union[np.ndarray, int, float, np.int_, np.float_]):
        x1 = as_array(x1)
    from .operationClass import Mul
    return Mul()(x0, x1)


def div(x0, x1) -> Fuzztensor:
    if isinstance(x0, Union[Fuzznum, Fuzzarray]):
        x0 = as_fuzztensor(as_fuzzarray(x0))
    if isinstance(x1, Union[Fuzznum, Fuzzarray]):
        x1 = as_fuzztensor(as_fuzzarray(x1))
    if isinstance(x0, Union[np.ndarray, int, float, np.int_, np.float_]):
        x0 = as_array(x0)
    if isinstance(x1, Union[np.ndarray, int, float, np.int_, np.float_]):
        x1 = as_array(x1)
    from .operationClass import Div
    return Div()(x0, x1)


def powers(x, p) -> Fuzztensor:
    if isinstance(x, Union[Fuzznum, Fuzzarray]):
        x = as_fuzztensor(as_fuzzarray(x))
    from .operationClass import Power
    return Power(p)(x)


def matmul(x0, x1) -> Fuzztensor:
    if isinstance(x0, Union[Fuzznum, Fuzzarray]):
        x0 = as_fuzztensor(as_fuzzarray(x0))
    if isinstance(x1, Union[Fuzznum, Fuzzarray]):
        x1 = as_fuzztensor(as_fuzzarray(x1))
    from .operationClass import Matmul
    return Matmul()(x0, x1)


def transpose(x) -> Fuzztensor:
    if isinstance(x, Union[Fuzznum, Fuzzarray]):
        x = as_fuzztensor(as_fuzzarray(x))
    from .operationClass import Transpose
    return Transpose()(x)


