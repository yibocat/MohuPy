#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/9/21 下午8:25
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from ..mohusets import mohuset
from ..mohunums import mohunum


def plot(x: (mohuset, mohunum), other=None, area=None,
         color='red', color_area=None, alpha=0.3):
    """
        Draw the plane diagram of fuzzy numbers

        Parameters
        ----------
            x : mohuset, mohunum
                The fuzzy set or fuzzy number to be plotted
            other : mohunum
                The other fuzzy number to be plotted.
                    Often used for comparison viewing
            area : list
                The area of the fuzzy number to be plotted.
                    Addition, subtraction, multiplication and division
            color : str
                The point color of the fuzzy number to be plotted
            color_area : str
                The area color of the fuzzy number to be plotted
            alpha : float
                The transparency of the fuzzy number to be plotted
    """
    if area is not None:
        assert isinstance(area, list), 'ERROR: area must be a list.'
    if isinstance(x, mohuset):
        x.plot(color=color, alpha=alpha)
    if isinstance(x, mohunum):
        x.plot(other=other, area=area, color=color,
               color_area=color_area, alpha=alpha)
