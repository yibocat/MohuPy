#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/21 上午4:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets

import numpy as np


def subsets(su):
    """
    Generate all subsets of a set.
    Parameters
    ----------
    su: list or ndarray
        set of the set

    Returns
    -------
    subsets: ndarray
        all subsets of a set
    """
    ans = []
    m = 1 << len(su)
    for i in range(m):
        res = np.array([])
        num = i
        idx = 0
        while num:
            if num & 1:
                res = np.append(res, su[idx])
            num >>= 1
            idx += 1
        ans.append(res)
    return np.asarray(ans, dtype=object)


def lamda(sets):
    """
        The equation for computing the lambda fuzzy measure
        parameter, which returns an anonymous function.

        The calculation of lambda needs to use optimize.fsolve
        optimization calculation of the scipy library, because
        the equation is a high-order nonlinear equation.

        The initial value of lambda optimization calculation
        is usually 1, as shown in the example below.

        Parameters
        ----------
            sets: ndarray or list
                fuzzy density list: fuzzy measures for single elements

        Returns
        -------
            function: anonymous function
                Equation of lambda fuzzy measure parameter

        Examples
        --------
            In [1]: x = np.array([0.4,0.25,0.37,0.2])
            In [2]: scipy.optimize.fsolve(lamda(x), np.array(-1))
            Out[2]: array(-0.4403)
    """
    return lambda lam: np.prod(1 + lam * sets) - lam - 1
