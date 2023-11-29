#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/11/28 下午7:38
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import numpy as np
from matplotlib import pyplot as plt

from .base import Library
from ..regedit import fuzzPlot
from ..core import Fuzznum, Fuzzarray


class Plot(Library):
    def function(self, f: (Fuzzarray, Fuzznum), other, add, sub, mul, div,
                 color, color_area, alpha, label, legend):

        if color_area is None:
            color_area = ['red', 'green', 'blue', 'yellow']

        q = f.qrung
        mtype = f.mtype

        plt.gca().spines['top'].set_linewidth(False)
        plt.gca().spines['bottom'].set_linewidth(True)
        plt.gca().spines['left'].set_linewidth(True)
        plt.gca().spines['right'].set_linewidth(False)
        plt.axis((0, 1.1, 0, 1.1))
        plt.axhline(y=0)
        plt.axvline(x=0)

        if isinstance(f, Fuzznum):
            fuzzPlot[mtype](f,
                            other=other,
                            add=add,
                            sub=sub,
                            mul=mul,
                            div=div,
                            color=color,
                            color_area=color_area,
                            alpha=alpha)
        if isinstance(f, Fuzzarray):
            plot_vec = np.vectorize(fuzzPlot[mtype])
            plot_vec(f.array,
                     other=other,
                     color=color,
                     alpha=alpha,
                     add=add,
                     sub=sub,
                     mul=mul,
                     div=div,
                     color_area=None)

        x = np.linspace(0, 1, 1000)
        y = (1 - x ** q) ** (1 / q)
        plt.plot(x, y, label=label)
        if legend: plt.legend(loc='upper right', fontsize='small')
        plt.show()


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
    return Plot()(f, other, add, sub, mul, div,
                  color, color_area, alpha, label, legend)
