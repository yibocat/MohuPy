#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/11 下午11:10
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from typing import Union

from ...tensor import Fuzztensor
from ...core import Fuzznum, Fuzzarray

from .base import Library


class TensorPlot(Library):
    def __init__(self, other, add, sub, mul, div,
                 color, color_area, alpha, label, legend):
        if not isinstance(other, Union[Fuzznum, None]):
            raise ValueError(f'Unexpected number of dimensions: {other.ndim}')
        self.other = other
        self.add = add
        self.sub = sub
        self.mul = mul
        self.div = div
        self.color = color
        self.color_area = color_area
        self.alpha = alpha
        self.label = label
        self.legend = legend

    def function(self, x: Fuzztensor):
        from ...corelib.lib.classPlot import Plot
        Plot()(x.data, self.other, self.add, self.sub,
               self.mul, self.div, self.color, self.color_area,
               self.alpha, self.label, self.legend)
