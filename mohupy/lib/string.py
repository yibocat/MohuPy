#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/11/28 下午7:04
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from .base import Library
from ..regedit.str2num import fuzzString


class StrToFuzz(Library):
    def function(self, s: str, q: int, mtype: str):
        return fuzzString[mtype](s, q)


def str2fuzz(s: str, q: int, mtype:str):
    return StrToFuzz()(s, q, mtype)

