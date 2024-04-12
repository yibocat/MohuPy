#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/7 下午1:39
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from typing import Union

from ...core import Fuzznum, Fuzzarray
from .randclass import Rand, Choice


# def rand(q: int, mtype: str = 'qrofn', *n, minnum=1, maxnum=5) -> Union[Fuzzarray, Fuzznum]:
#     return Rand(minnum, maxnum)(q, mtype, *n)
#
#
# def choice(f, size: (int, tuple[int], list[int]) = None, replace=False) -> Union[Fuzzarray, Fuzznum]:
#     return Choice()(f, size, replace)
#
# def rand(*n, qrung=1, minnum=1, maxnum=5) -> Union[Fuzzarray, Fuzznum]:
#     return Rand(qrung, minnum, maxnum)(*n)
#
#
# def choice(f: Union[Fuzznum, Fuzzarray], size: (int, tuple[int], list[int]) = None, replace=False):
#     return Choice()(f, size, replace)
