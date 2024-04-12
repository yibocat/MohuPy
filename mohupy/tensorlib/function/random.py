#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/12 下午4:19
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from ...tensor import Fuzztensor


def rand_tensor(*n, qrung=1) -> Fuzztensor:
    from ..random import TensorRandom
    return TensorRandom(qrung)(*n)


def random_choice_tensor(x: Fuzztensor,
                         size: int | tuple[int] | list[int] = None, replace=False) -> Fuzztensor:
    from ..random import TensorChoice
    return TensorChoice(size, replace)(x)
