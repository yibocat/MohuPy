#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/12 下午4:09
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import numpy as np

from ...tensor import Fuzztensor


def tensor_distance(tensor1: Fuzztensor, tensor2: Fuzztensor,
                    param_l=2, param_t=1, indeterminacy=True) -> np.ndarray | float:
    from ..lib import TensorDistance
    return TensorDistance(param_l, param_t, indeterminacy)(tensor1, tensor2)
