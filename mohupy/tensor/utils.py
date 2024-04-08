#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/7 下午3:14
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import numpy as np

from .fuzztensor import Fuzztensor


def as_fuzzarray(x):
    """
        因为涉及到0维模糊数，所以需要把模糊数转换为标量
    """
    from ..corelib import isscalar
    if isscalar(x):
        from ..corelib import asfuzzarray
        return asfuzzarray(x)
    return x


def as_fuzztensor(x):
    """
        将模糊集合或模糊数转换为fuzztensor
    """
    if isinstance(x, Fuzztensor):
        return x
    return Fuzztensor(x)


def as_array(x):
    if np.isscalar(x):
        return np.array(x)
    return x
