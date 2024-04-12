#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/12 下午1:59
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from ...core import Fuzznum, Fuzzarray


def fuzz_zeros(*n, qrung=1) -> Fuzznum | Fuzzarray:
    """
    创建一个全隶属度与非隶属度为 0 的模糊数或模糊数组
    :param n:       要创建的模糊数或模糊数组形状
    :param qrung:   q阶序对
    :return:        模糊数或模糊集 Fuzznum | Fuzzarray
    """
    from ..lib import ZerosConstruct
    return ZerosConstruct(qrung)(*n)


def fuzz_poss(*n, qrung=1) -> Fuzznum | Fuzzarray:
    from ..lib import PossConstruct
    return PossConstruct(qrung)(*n)


def fuzz_negs(*n, qrung=1) -> Fuzznum | Fuzzarray:
    from ..lib import NegsConstruct
    return NegsConstruct(qrung)(*n)


def fuzz_full(*n, fuzznum: Fuzznum) -> Fuzznum | Fuzzarray:
    from ..lib import FullConstruct
    return FullConstruct(fuzznum)(*n)


def fuzz_zeros_like(fuzznum: Fuzznum | Fuzzarray) -> Fuzznum | Fuzzarray:
    from ..lib import ZerosLikeConstruct
    return ZerosLikeConstruct(fuzznum)()


def fuzz_poss_like(fuzznum: Fuzznum | Fuzzarray) -> Fuzznum | Fuzzarray:
    from ..lib import PossLikeConstruct
    return PossLikeConstruct(fuzznum)()


def fuzz_negs_like(fuzznum: Fuzznum | Fuzzarray) -> Fuzznum | Fuzzarray:
    from ..lib import NegsLikeConstruct
    return NegsLikeConstruct(fuzznum)()


def fuzz_full_like(fuzznum: Fuzzarray|Fuzznum, y: Fuzznum) -> Fuzznum | Fuzzarray:
    """
    将 fuzznum 扩充到与 y 相同的形状
    :param fuzznum: 要扩充的模糊数
    :param y:       被扩充的形状
    :return:        模糊数或模糊集 Fuzznum | Fuzzarray
    """
    from ..lib import FullLikeConstruct
    return FullLikeConstruct(y)(fuzznum)

