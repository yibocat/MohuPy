#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/7 下午2:05
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from ...core import Fuzznum, Fuzzarray


def plot(f: (Fuzzarray, Fuzznum),
         other=None,
         add=None,
         sub=None,
         mul=None,
         div=None,
         color='red',
         color_area=None,
         alpha=0.3,
         label='',
         legend=False):
    from .classPlot import Plot
    return Plot()(f, other, add, sub, mul, div,
                  color, color_area, alpha, label, legend)
