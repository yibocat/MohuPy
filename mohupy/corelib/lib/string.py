#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/7 下午1:55
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from ...core import Fuzznum


def str2fuzz(s: str, q: int, mtype:str) -> Fuzznum:
    from .classString import StrToFuzz
    return StrToFuzz()(s, q, mtype)
