#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/7 下午1:57
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from ..regedit import fuzzString
from .base import Library
from ...config import Config


class StrToFuzz(Library):

    def __init__(self, qrung):
        self.qrung = qrung

    def function(self, s: str):
        mtype = Config.mtype
        return fuzzString[mtype](s, self.qrung)




