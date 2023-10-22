#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/10/16 下午3:22
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import numpy as np
from matplotlib import pyplot as plt

from ..core.base import mohunum
from .regedit import Register

fuzzPlot = Register()


@fuzzPlot('qrofn')
def plot_qrofn(x: mohunum,
               other: mohunum = None,
               area: list[bool] = None,
               color='red',
               color_area=None,
               alpha=0.3):
    """
        This function plots the Q-ROFN distribution in the fuzzy space.
        If other is not None, it plots the Q-ROFN distribution in the fuzzy space,
        and other is plotted in the fuzzy space. This helps to see which domain
        other is at that point.

        Parameters
        ----------
            x:      MohuQROFN
                    Plot of points to be drawn
            other : MohuQROFN
                    If it is None, only the position of the self point in the fuzzy
                    space is drawn. Otherwise, the position of other in the fuzzy
                    space is also drawn.
            area : list[bool]
                    This is a four-element bool list, representing the addition field,
                    subtraction field, multiplication field and division field in order.
            color : str
                    The color of the Q-ROFN distribution.
            color_area : list[str]
                    The color of the addition field, subtraction field, multiplication field
                    and division field.
            alpha : float
                    The transparency of the Q-ROFN distribution.
    """
    if area is None:
        area = [False, False, False, False]
    if color_area is None:
        color_area = ['red', 'green', 'blue', 'yellow']

    md = x.md
    nmd = x.nmd
    q = x.qrung

    x = np.linspace(0, 1, 1000)
    plt.scatter(md, nmd, color=color, marker='.', alpha=alpha)

    if other is not None:
        assert other.qrung == q, 'ERROR: The qrungs are not equal'
        plt.scatter(other.md, other.nmd, color=color, marker='*')

    y = (1 - x ** q) ** (1 / q)
    if area is not None:
        n = (nmd ** q / (1 - md ** q) * (1 - x ** q)) ** (1 / q)
        m = (md ** q / (1 - nmd ** q) * (1 - x ** q)) ** (1 / q)

        if area[0]:
            # Q-ROFN f addition region
            plt.fill_between(x, n, color=color_area[0], alpha=alpha, where=x > md)
        if area[1]:
            # Q-ROFN f subtraction region
            plt.fill_between(x, n, y, color=color_area[1], alpha=alpha, where=x < md)
        if area[2]:
            # Q-ROFN f multiplication region
            plt.fill_betweenx(x, m, color=color_area[2], alpha=alpha, where=x > nmd)
        if area[3]:
            # Q-ROFN f division region
            plt.fill_betweenx(x, m, y, color=color_area[3], alpha=alpha, where=x < nmd)


@fuzzPlot('ivfn')
def plot_ivfn(x: mohunum,
              other: mohunum = None,
              color='red',
              alpha=0.3,
              area: list[bool] = None,
              color_area=None):
    """
        This function plots the interval-valued Q-ROFN distribution in the fuzzy space.
        If other is not None, it plots the Q-ROFN distribution in the fuzzy space,
        and other is plotted in the fuzzy space. This helps to see which domain
        other is at that point.

        Parameters
        ----------
            x:      MohuQROIVFN
                    Plot of points to be drawn
            other : MohuQROIVFN
                    If it is None, only the position of the self point in the fuzzy
                    space is drawn. Otherwise, the position of other in the fuzzy
                    space is also drawn.
            color : str
                    The color of the Q-ROFN distribution.
            alpha : float
                    The transparency of the Q-ROFN distribution.
            area:   None
            color_area: None
    """
    md = x.md
    nmd = x.nmd
    q = x.qrung

    plt.fill([md[0], md[1], md[1], md[0]],
             [nmd[1], nmd[1], nmd[0], nmd[0]],
             color=color, alpha=alpha)

    if other is not None:
        assert other.qrung == q, \
            'ERROR: The qrungs are not equal'
        plt.fill([other.md[0], other.md[1], other.md[1], other.md[0]],
                 [other.nmd[1], other.nmd[1], other.nmd[0], other.nmd[0]],
                 color=color, alpha=alpha)


@fuzzPlot('qrohfn')
def plot_qrohfn(x: mohunum,
                other: mohunum = None,
                color='red',
                alpha=0.3,
                area: list[bool] = None,
                color_area=None):
    """
        This function plots the q-ROHFN distribution in the fuzzy space.
        If other is not None, it plots the Q-ROFN distribution in the fuzzy space,
        and other is plotted in the fuzzy space. This helps to see which domain
        other is at that point.

        Parameters
        ----------
            x:      MohuQROFN
                    Plot of points to be drawn
            other : MohuQROFN
                    If it is None, only the position of the self point in the fuzzy
                    space is drawn. Otherwise, the position of other in the fuzzy
                    space is also drawn.
            color : str
                    The color of the Q-ROFN distribution.
            alpha : float
                    The transparency of the Q-ROFN distribution.
            area:   None
            color_area: None
    """
    # TODO: q-ROHFN scatter plot is not implemented yet
    raise ValueError('q-rung orthopair hesitant fuzzy number scatter plot is not implemented yet')
