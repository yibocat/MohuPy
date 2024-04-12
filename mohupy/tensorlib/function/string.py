#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/12 下午4:17
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from ...tensor import Fuzztensor


def tensor_str2fuzz(s: str, qrung: int) -> Fuzztensor:
    from ..lib import TensorStrToFuzz
    return TensorStrToFuzz(qrung)(s)
