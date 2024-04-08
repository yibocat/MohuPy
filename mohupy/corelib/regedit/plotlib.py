#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/7 下午1:31
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import numpy as np
from matplotlib import pyplot as plt

from ...core import Fuzznum, Registry

fuzzPlot = Registry()


@fuzzPlot('qrofn')
def plot_qrofn(x: Fuzznum,
               other: Fuzznum = None,
               add=False,
               sub=False,
               mul=False,
               div=False,
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
            x:      Fuzznum
                    Plot of points to be drawn
            other : Fuzznum
                    If it is None, only the position of the self point in the fuzzy
                    space is drawn. Otherwise, the position of other in the fuzzy
                    space is also drawn.
            add : bool
                    Additive field
            sub : bool
                    Subtraction field
            mul : bool
                    Multiplication field
            div : bool
                    Division field
            color : str
                    The color of the Q-ROFN distribution.
            color_area : list[str]
                    The color of the addition field, subtraction field, multiplication field
                    and division field.
            alpha : float
                    The transparency of the Q-ROFN distribution.
    """
    if color_area is None:
        color_area = ['red', 'green', 'blue', 'yellow']

    md = x.md
    nmd = x.nmd
    q = x.qrung

    x = np.linspace(0, 1, 1000)

    # plt.scatter(md, nmd, color=color, marker='.', alpha=alpha)
    #
    # if other is not None:
    #     assert other.qrung == q, 'ERROR: The qrungs are not equal'
    #     plt.scatter(other.md, other.nmd, color=color, marker='*')

    plt.fill([md-0.004, md+0.004, md+0.004, md-0.004],
             [nmd+0.004, nmd+0.004, nmd-0.004, nmd-0.004], color=color, alpha=alpha)
    if other is not None:
        assert other.qrung == q, 'ERROR: The qrungs are not equal'
        plt.fill([other.md-0.004, other.md+0.004, other.md+0.004, other.md-0.004],
                 [other.nmd+0.004, other.nmd+0.004, other.nmd-0.004, other.nmd-0.004],
                 color=color, alpha=alpha)

    y = (1 - x ** q) ** (1 / q)
    if md == 1 and nmd != 1:
        n, m = 1, 0
    elif md != 1 and nmd == 1:
        n, m = 0, 1
    else:
        n = (nmd ** q / (1 - md ** q) * (1 - x ** q)) ** (1 / q)
        m = (md ** q / (1 - nmd ** q) * (1 - x ** q)) ** (1 / q)

    if add:
        # Q-ROFN f addition region
        plt.fill_between(x, n, color=color_area[0], alpha=alpha, where=x > md)
    if sub:
        # Q-ROFN f subtraction region
        plt.fill_between(x, n, y, color=color_area[1], alpha=alpha, where=x < md)
    if mul:
        # Q-ROFN f multiplication region
        plt.fill_betweenx(x, m, color=color_area[2], alpha=alpha, where=x > nmd)
    if div:
        # Q-ROFN f division region
        plt.fill_betweenx(x, m, y, color=color_area[3], alpha=alpha, where=x < nmd)


@fuzzPlot('ivfn')
def plot_ivfn(x: Fuzznum,
              other: Fuzznum = None,
              add=None,
              sub=None,
              mul=None,
              div=None,
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
            x:      Fuzznum
                    Plot of points to be drawn
            other : Fuzznum
                    If it is None, only the position of the self point in the fuzzy
                    space is drawn. Otherwise, the position of other in the fuzzy
                    space is also drawn.
            add : bool
                    Additive field
            sub : bool
                    Subtraction field
            mul : bool
                    Multiplication field
            div : bool
                    Division field
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
def plot_qrohfn(x: Fuzznum,
                other: Fuzznum = None,
                add=None,
                sub=None,
                mul=None,
                div=None,
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
            x:      Fuzznum
                    Plot of points to be drawn
            other : Fuzznum
                    If it is None, only the position of the self point in the fuzzy
                    space is drawn. Otherwise, the position of other in the fuzzy
                    space is also drawn.
            add : bool
                    Additive field
            sub : bool
                    Subtraction field
            mul : bool
                    Multiplication field
            div : bool
                    Division field
            color : str
                    The color of the Q-ROFN distribution.
            alpha : float
                    The transparency of the Q-ROFN distribution.
            area:   None
            color_area: None
    """
    # TODO: q-ROHFN scatter plot is not implemented yet
    raise ValueError('q-rung orthopair hesitant fuzzy number scatter plot is not implemented yet')


