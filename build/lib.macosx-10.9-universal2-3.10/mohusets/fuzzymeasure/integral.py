#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/21 上午4:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets

import numpy as np
from .fuzzm import fuzzm


def discrete_choquet_integral(sett, measurable_func=None):
    """
        The choquet integral based on lambda fuzzy measure function.
        For the existing set of fuzzy measures and a measurable function,
        if the measurable function is None, then directly calculate the
        Choquet Integral corresponding to each fuzzy measure. Otherwise,
        computes the value corresponding to the measurable function.

        Measurable functions are currently judged using hasattr.
        In the future, the measurable functions need to be limited.

        It should be noted that when i=n-1, the subset cannot be set to
        Ai_=A[i+1:n], because the [0] subset does not belong to the
        fuzzy measure set (programming bug), and the fuzzy measure is
        assigned a value of 0.

        Parameters
        ----------
            sett: numpy.ndarray or list
                fuzzy density list
            measurable_func: function
                measurable function

        Returns
        -------
            float: the value of choquet integral of the lambda fuzzy
                    measure function
    """
    ss = fuzzm(sett)
    n = ss.len
    if hasattr(measurable_func, '__call__'):
        RI = measurable_func(sett)
    else:
        RI = sett

    rank = np.sort(RI)
    index = np.argsort(RI)
    A = sett[index]
    integral = np.array([])

    for i in index:
        if i == n - 1:
            lmAi_ = 0                               # marked
        else:
            Ai_ = A[i + 1:n]
            lmAi_ = ss(Ai_)
        Ai = A[i:n]
        lmAi = ss(Ai)
        integral = np.append(integral, rank[i] * (lmAi - lmAi_))
    return integral.sum()


def discrete_sugeno_integral(sett, measurable_func=None):
    """
        Discrete Sugeno integral. Same as discrete_choquet_integral,
        the Sugeno integral based on lambda fuzzy measure function.
        For the existing set of fuzzy measures and a measurable function,
        if the measurable function is None, then directly calculate the
        Sugeno Integral corresponding to each fuzzy measure. Otherwise,
        computes the value corresponding to the measurable function.

        Measurable functions are currently judged using hasattr.
        In the future, the measurable functions need to be limited.

        Parameters
        ----------
            sett: numpy.ndarray or list
                fuzzy density list
            measurable_func: function
                measurable function

        Returns
        -------
            float: the value of Sugeno integral of the lambda fuzzy
                measure function
    """
    ss = fuzzm(sett)
    n = ss.len
    if hasattr(measurable_func, '__call__'):
        RI = measurable_func(sett)
    else:
        RI = sett

    rank = np.sort(RI)
    res = np.array([])
    for i in range(n):
        res = np.append(res, min(rank[i], ss(rank[i:])))
    return np.max(res)


def shilkret_integral(sett, measurable_func=None):
    """
        The Shilkret integral is a continuous piecewise linear idempotent
        aggregation function. The Shilkret integral is homogeneous and the
        values of the fuzzy measure are returned at the vertices of the
        unit cube, regardless of whether μ is maxitive.

        Parameters
        ----------
            sett: numpy.ndarray or list
                fuzzy density list
            measurable_func: function
                measurable function

        Returns
        -------
            float: the value of Shilkret integral of the fuzzy measure function
    """
    ss = fuzzm(sett)
    n = ss.len
    if hasattr(measurable_func, '__call__'):
        RI = measurable_func(sett)
    else:
        RI = sett

    rank = np.sort(RI)
    res = np.array([])
    for i in range(n):
        res = np.append(res, rank[i]*ss(rank[i:]))
    return np.max(res)

