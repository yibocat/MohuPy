#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/12 下午3:51
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from ...tensor import Fuzztensor
from ...core import Fuzznum, Fuzzarray


def tensor_zeros(*n, qrung=1) -> Fuzztensor:
    """
    创建一个全隶属度与非隶属度为 0 的任意形状模糊张量
    :param n:       要创建的模糊数或模糊数组形状
    :param qrung:   q阶序对
    :return:        模糊张量 Fuzztensor
    """
    from ..lib import TensorZerosConstruct
    return TensorZerosConstruct(qrung)(*n)


def tensor_poss(*n, qrung=1) -> Fuzztensor:
    from ..lib import TensorPossConstruct
    return TensorPossConstruct(qrung)(*n)


def tensor_negs(*n, qrung=1) -> Fuzztensor:
    from ..lib import TensorNegsConstruct
    return TensorNegsConstruct(qrung)(*n)


def tensor_full(*n, fuzz: Fuzzarray | Fuzzarray | Fuzztensor) -> Fuzztensor:
    from ..lib import TensorFullConstruct
    return TensorFullConstruct(fuzz)(*n)


def tensor_zeros_like(fuzz: Fuzztensor) -> Fuzztensor:
    from ..lib import TensorZerosLikeConstruct
    return TensorZerosLikeConstruct(fuzz)()


def tensor_poss_like(fuzz: Fuzztensor) -> Fuzztensor:
    from ..lib import TensorPossLikeConstruct
    return TensorPossLikeConstruct(fuzz)()


def tensor_negs_like(fuzz: Fuzztensor) -> Fuzztensor:
    from ..lib import TensorNegsLikeConstruct
    return TensorNegsLikeConstruct(fuzz)()


def tensor_full_like(fuzz: Fuzznum, y: Fuzztensor) -> Fuzztensor:
    from ..lib import TensorFullLikeConstruct
    return TensorFullLikeConstruct(y)(fuzz)
