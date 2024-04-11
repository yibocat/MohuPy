#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/7 下午1:45
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from typing import Union
from ...core import Fuzznum, Fuzzarray

#
# def zeros(*n, qrung=1) -> Union[Fuzznum, Fuzzarray]:
#     from .classConstruct import ZerosConstruct
#     return ZerosConstruct(qrung)(*n)
#
#
# def poss(*n, qrung=1) -> Union[Fuzznum, Fuzzarray]:
#     from .classConstruct import PossConstruct
#     return PossConstruct(qrung)(*n)
#
#
# def negs(*n, qrung=1) -> Union[Fuzznum, Fuzzarray]:
#     from .classConstruct import NegsConstruct
#     return NegsConstruct(qrung)(*n)
#
#
# def full(x: Fuzznum, *n) -> Union[Fuzznum, Fuzzarray]:
#     from .classConstruct import FullConstruct
#     return FullConstruct(x)(*n)
#
#
# def zeros_like(x: Union[Fuzznum, Fuzzarray]) -> Union[Fuzznum, Fuzzarray]:
#     from .classConstruct import ZerosLikeConstruct
#     return ZerosLikeConstruct(x)()
#
#
# def poss_like(x: Union[Fuzznum, Fuzzarray]) -> Union[Fuzznum, Fuzzarray]:
#     from .classConstruct import PossLikeConstruct
#     return PossLikeConstruct(x)()
#
#
# def negs_like(x: Union[Fuzznum, Fuzzarray]) -> Union[Fuzznum, Fuzzarray]:
#     from .classConstruct import NegsLikeConstruct
#     return NegsLikeConstruct(x)()
#
#
# def full_like(x: Fuzznum, y: Union[Fuzznum, Fuzzarray]) -> Union[Fuzznum, Fuzzarray]:
#     from .classConstruct import FullLikeConstruct
#     return FullLikeConstruct(x)(y)
#
