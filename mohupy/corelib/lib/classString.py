#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/7 下午1:57
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from ..regedit import fuzzString
from .base import Library


class StrToFuzz(Library):

    def function(self, s: str, q: int, mtype: str):
        return fuzzString[mtype](s, q)




