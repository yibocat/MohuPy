#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/11 下午11:36
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from typing import Union

from .base import Library


class TensorAsFuzztensor(Library):

    def __init__(self, copy):
        self.copy = copy

    def function(self, x):
        from ...corelib.lib.classUtils import AsFuzzarray
        from ...tensor.utils import as_fuzztensor
        f = AsFuzzarray()(x, self.copy)
        return as_fuzztensor(f)
