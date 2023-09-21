#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/21 上午4:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets

import numpy as np
from .fuzzm import fuzzm


# def discrete_choquet_integral(sett, measurable_func=None):
#     """
#         The choquet integral based on lambda fuzzy measure function.
#         For the existing set of fuzzy measures and a measurable function,
#         if the measurable function is None, then directly calculate the
#         Choquet Integral corresponding to each fuzzy measure. Otherwise,
#         computes the value corresponding to the measurable function.
#
#         Measurable functions are currently judged using hasattr.
#         In the future, the measurable functions need to be limited.
#
#         It should be noted that when i=n-1, the subset cannot be set to
#         Ai_=A[i+1:n], because the [0] subset does not belong to the
#         fuzzy measure set (programming bug), and the fuzzy measure is
#         assigned a value of 0.
#
#         Parameters
#         ----------
#             sett: numpy.ndarray or list
#                 fuzzy density list
#             measurable_func: function
#                 measurable function
#
#         Returns
#         -------
#             float: the value of choquet integral of the lambda fuzzy
#                     measure function
#     """
#     ss = fuzzm(sett)
#     n = ss.len
#     if hasattr(measurable_func, '__call__'):
#         RI = measurable_func(sett)
#     else:
#         RI = sett
#
#     rank = np.sort(RI)
#     index = np.argsort(RI)
#     A = sett[index]
#     integral = np.array([])
#
#     for i in index:
#         if i == n - 1:
#             lmAi_ = 0                               # marked
#         else:
#             Ai_ = A[i + 1:n]
#             lmAi_ = ss(Ai_)
#         Ai = A[i:n]
#         lmAi = ss(Ai)
#         integral = np.append(integral, rank[i] * (lmAi - lmAi_))
#     return integral.sum()


def discrete_choquet_integral(fuzz_d, measurable_func=None, info=False):
    """
        The choquet integral based on lambda fuzzy measure function.
        For the existing set of fuzzy measures and a measurable function,
        if the measurable function is None, then directly calculate the
        Choquet Integral corresponding to each fuzzy measure. Otherwise,
        computes the value corresponding to the measurable function.

        Measurable functions are currently judged using hasattr.
        In the future, the measurable functions need to be limited.

        Parameters
        ----------
            fuzz_d: numpy.ndarray or list
                fuzzy density list
            info: bool
                whether to print the information of fuzzy measure
            measurable_func: function
                measurable function

        Returns
        -------
            float: the value of choquet integral of the lambda fuzzy
                    measure function
    """

    f = fuzzm(fuzz_d)
    if hasattr(measurable_func, '__call__'):
        RI = measurable_func(fuzz_d)
    else:
        RI = fuzz_d

    index = np.argsort(-RI)                      # 得到模糊测度按升序排列的下标
    fdp = fuzz_d[index]                         # 将模糊测度按升序排列

    p = []
    for i in range(len(index)):
        p.append(f(fdp[:i+1])-f(fdp[:i]))
    p = np.asarray(p)
    p = p[::-1]                                 # 将模糊测度集函数的导数按照降序排列

    fz = np.sort(RI)                             # 将 RI 按照升序排列

    if info:
        print('The fuzzy measure: ' + str(fuzz_d))
        print('The ascending sorting of fuzzy measures: \n  '+str(fdp))
        print('Index of fuzzy measures in ascending order: \n  '+ str(index+1))
        print('Descending Order of Function Derivatives of Fuzzy Measure Set: \n  ' + str(p))
        print('Measurable functions in ascending order: \n  ' + str(fz))

    integral = np.array([])                     # 初始化返回的结果

    for i in range(len(index)):
        integral = np.append(integral, fz[i] * p[i])

    return np.sum(integral)


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

