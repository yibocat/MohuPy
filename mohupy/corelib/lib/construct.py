#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/7 下午1:45
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from typing import Union
from ...core import Fuzznum, Fuzzarray


def zeros(q, mtype, *n) -> Union[Fuzznum, Fuzzarray]:
    from .classConstruct import Zeros
    return Zeros()(q, mtype, *n)


def poss(q, mtype, *n) -> Union[Fuzznum, Fuzzarray]:
    from .classConstruct import Poss
    return Poss()(q, mtype, *n)


def negs(q, mtype, *n) -> Union[Fuzznum, Fuzzarray]:
    from .classConstruct import Negs
    return Negs()(q, mtype, *n)


def full(x: Fuzznum, *n) -> Union[Fuzznum, Fuzzarray]:
    from .classConstruct import Full
    return Full()(x, *n)


def zeros_like(f: Fuzzarray) -> Union[Fuzznum, Fuzzarray]:
    from .classConstruct import ZerosLike
    return ZerosLike()(f)


def poss_like(f: Fuzzarray) -> Union[Fuzznum, Fuzzarray]:
    from .classConstruct import PossLike
    return PossLike()(f)


def negs_like(f: Fuzzarray) -> Union[Fuzznum, Fuzzarray]:
    from .classConstruct import NegsLike
    return NegsLike()(f)


def full_like(f: Fuzzarray) -> Union[Fuzznum, Fuzzarray]:
    from .classConstruct import FullLike
    return FullLike()(f)







