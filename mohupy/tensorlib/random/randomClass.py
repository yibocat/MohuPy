#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/8 下午5:28
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from .base import Random
from ...tensor import Fuzztensor


class TensorRandom(Random):

    def __init__(self, qrung):
        self.qrung = qrung

    def function(self, *n):
        from ...corelib.random.randclass import Rand
        r = Rand(self.qrung, 1, 5)(*n)
        return Fuzztensor(r)


class TensorChoice(Random):
    def __init__(self, size, replace):
        self.size = size
        self.replace = replace

    def function(self, fuzztensor):
        from ...corelib.random.randclass import Choice
        r = Choice()(fuzztensor.data, self.size, self.replace)
        return Fuzztensor(r)
