#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/12 下午4:04
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import numpy as np

from ...core import Fuzznum, Fuzzarray
from ...tensor import Fuzztensor


def asfuzztensor(x: Fuzznum | Fuzzarray | Fuzztensor |
                    np.ndarray[Fuzznum | Fuzzarray] |
                    list[Fuzznum | Fuzzarray], copy=False) -> Fuzztensor:
    from ..lib import TensorAsFuzztensor
    return TensorAsFuzztensor(copy)(x)
