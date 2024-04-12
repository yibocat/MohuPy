#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/12 下午3:01
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from ...core import Fuzznum, Fuzzarray


def fuzz_dot(x: Fuzznum | Fuzzarray, y: Fuzznum | Fuzzarray) -> Fuzznum | Fuzzarray:
    """
    两个模糊数或模糊数组(向量)的点积
    """
    from ..math import Dot
    return Dot()(x, y)


def fuzz_inner(x: Fuzznum | Fuzzarray, y: Fuzznum | Fuzzarray) -> Fuzznum | Fuzzarray:
    """
    两个模糊数或模糊数组（向量）的内积
    """
    from ..math import Inner
    return Inner()(x, y)


def fuzz_outer(x: Fuzznum | Fuzzarray, y: Fuzznum | Fuzzarray) -> Fuzznum | Fuzzarray:
    """
    两个模糊数或模糊数组（向量）的外积
    """
    from ..math import Outer
    return Outer()(x, y)


def fuzz_cartadd(x: Fuzznum | Fuzzarray, y: Fuzznum | Fuzzarray) -> Fuzznum | Fuzzarray:
    """
    两个模糊数或模糊数组（向量）的笛卡尔和
    """
    from ..math import Cartadd
    return Cartadd()(x, y)


def fuzz_cartprod(x: Fuzznum | Fuzzarray, y: Fuzznum | Fuzzarray) -> Fuzznum | Fuzzarray:
    """
    两个模糊数或模糊数组（向量）的笛卡尔积
    """
    from ..math import Cartprod
    return Cartprod()(x, y)
