#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/8 下午5:28
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from .base import Random
from ...tensor import Fuzztensor


class TensorRandom(Random):

    def __init__(self, q):
        self.q = q

    def function(self, *n):
        from ...corelib.random import rand
        newTensor = Fuzztensor()
        # newTensor.data = rand(self.q, 'qrofn', *n)
        newTensor.data = rand(*n, qrung=self.q)
        return newTensor

