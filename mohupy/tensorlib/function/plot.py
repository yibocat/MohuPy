#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/12 下午4:13
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from ...tensor import Fuzztensor
from ...core import Fuzznum


def tensor_plot(tensor: Fuzztensor,
                other: Fuzznum = None,
                add=None,
                sub=None,
                mul=None,
                div=None,
                color='red',
                color_area=None,
                alpha=0.3,
                label='',
                legend=False):
    from ..lib import TensorPlot
    TensorPlot(other, add, sub, mul, div, color, color_area, alpha, label,legend)(tensor)
