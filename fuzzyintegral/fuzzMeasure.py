#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/1 下午5:37
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzPy

import numpy as np
from scipy.optimize import fsolve


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
            sets: numpy.ndarray
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


def lambda_fuzzy_measure(fuzz_d, fuzz_measure, l):
    """
        The lambda fuzzy measure function.
        We have a subset of the fuzzy measure sets, then use the
        function to calculate the fuzzy measure of the subset.
        The parameter lambda can put in this function, but when
        this function is called, fsolve must be executed every
        time, which will greatly reduce the calculation efficiency.
        So the lambda is passed into the function as a parameter.

        Parameters
        ----------
            fuzz_d: numpy.ndarray or list
                fuzzy density subset
            fuzz_measure: numpy.ndarray or list
                fuzzy measure set
            l: float
                lambda parameter, 5 digits of precision

        Returns
        -------
            float: fuzzy measure of the subset

        Examples
        --------
            In [1]: fuzz_den = np.array([0.4,0.25,0.37,0.2])
            In [2]: lambda_fuzzy_measure([0.25,0.37], fuzz_den, lambda)
            Out[2]: 0.5793
    """

    def _issubset(a, b):
        return len(np.setdiff1d(a, b)) == 0

    f = np.asarray(fuzz_d)
    ise = _issubset(f, fuzz_measure)
    assert ise, 'ERROR! The subset is not an element of the set.'
    if np.round(l, 5) == 0:
        return f.sum()
    else:
        return (np.prod(1 + l * f) - 1) / l


def discrete_choquet_integral(fuzz_density, measurable_func=None):
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
            fuzz_density: numpy.ndarray or list
                fuzzy density list
            measurable_func: function
                measurable function

        Returns
        -------
            float: the value of choquet integral of the lambda fuzzy
                    measure function
    """
    f = np.asarray(fuzz_density)
    n = len(f)
    l = fsolve(lamda(f), np.array([-1]))[0]

    if hasattr(measurable_func, '__call__'):
        RI = measurable_func(f)
    else:
        RI = fuzz_density
    rank = np.sort(RI)
    index = np.argsort(RI)
    A = f[index]
    integral = np.array([])

    for i in index:
        if i == n - 1:
            lmAi_ = 0                               # marked
        else:
            Ai_ = A[i + 1:n]
            lmAi_ = lambda_fuzzy_measure(Ai_, f, float(l))
        Ai = A[i:n]
        lmAi = lambda_fuzzy_measure(Ai, f, float(l))
        integral = np.append(integral, rank[i] * (lmAi - lmAi_))
    return integral.sum()
