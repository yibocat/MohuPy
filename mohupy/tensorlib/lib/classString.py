#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/11 下午11:30
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from .base import Library
from ...tensor import Fuzztensor


class TensorStrToFuzz(Library):
    def __init__(self, qrung):
        self.qrung = qrung

    def function(self, s: str):
        from ...corelib.lib.classString import StrToFuzz
        return Fuzztensor(StrToFuzz(self.qrung)(s))

