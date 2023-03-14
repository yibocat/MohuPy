#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/21 上午4:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets

import numpy as np

from .math import subsets
from .fuzzm import fuzzm


def derivative(x, sub, f):
    """
        Derivative of a fuzzy measure function(derivatives of set functions).
        The notion of discrete derivatives [Gra16,GL07] can be seen as a basis
        for determining the contribution of inputs to various coalitions,
        as well as for observing interaction effects.
        The function can be seen as a derivative of x to the fuzzy measure function
        at subset.

        Parameters
        ----------
        x:  numpy.float64 or float
            element of the set
        sub: list or ndarray
            subset of the set
        f: fuzzm
            fuzzy measure function

        Returns
        -------
        derivative: float
            derivative of x to the fuzzy measure function at subset

        Examples
        --------
        In [1]: s1 = np.array([0.4,0.25,0.37,0.2])
        In [2]: derivative(0.4, s1, fuzzm(s1))
        Out[2]: 0.27173851436111696

    """
    assert f.__class__.__name__ == 'fuzzm', 'f must be a fuzzm function.'
    return f(np.union1d(sub, x)) - f(np.setdiff1d(sub, x))


def shapley_value(ss, sets, m='lambda'):
    """
        Shapley value of a set. The Shapley value is interpreted as a kind
        of average value of the contribution of each criterion alone in all
        coalitions. The Shapley value is the vector of the average marginal.
        One important property of the Shapley value is that the sum of the
        vector is 1.

        Note: The fuzzy measure used in the shapley value here is the lambda
        fuzzy measure. Replacing other fuzzy measures is not supported for
        the time being.

        Parameters
        ----------
        ss: list or ndarray
            the subset of the set
        sets: list or ndarray
            the set of fuzzy measure
        m: str
            fuzzy measure function, default is 'lambda'

        Returns
        -------
        shapley value: ndarray
            Shapley value vector
    """

    lam = fuzzm(sets, meas=m)
    n = lam.len
    shapley = np.array([])
    for x in ss:
        ts = np.array([])
        for sub in subsets(np.setdiff1d(ss, x)):
            coef = np.math.factorial(n - sub.size - 1) * \
                   np.math.factorial(sub.size) / np.math.factorial(n)
            ts = np.append(ts, coef * derivative(x, sub, lam))
        shapley = np.append(shapley, np.sum(ts))
    return shapley


def banzhaf_value(ss, sets, m='lambda'):
    """
        An alternative to the Shapley value is the Banzhaf value. It measures the
        same concept as the Shapley value, but weights the terms [μ(A ∪{i}) − μ(A)]
        in the sum equally.

        Note: The fuzzy measure used in the shapley value here is the lambda
        fuzzy measure. Replacing other fuzzy measures is not supported for
        the time being.

        Parameters
        ----------
        ss: list or ndarray
            set of the set
        sets: list or ndarray
            the set of fuzzy measure
        m: str
            fuzzy measure function, default is 'lambda'

        Returns
        -------
        banzhaf value: ndarray
            Banzhaf value vector
    """
    lam = fuzzm(sets, meas=m)
    n = lam.len
    coef = 1/(2**n - 1)
    banzhaf = np.array([])
    for x in ss:
        ts = np.array([])
        for sub in subsets(np.setdiff1d(ss, x)):
            ts = np.append(ts, derivative(x, sub, lam))
        banzhaf = np.append(banzhaf, coef * np.sum(ts))
    return banzhaf


def shannon_entropy(ss, sets, m='lambda'):
    """
    Shannon entropy of a fuzzy measure.
    Parameters
    ----------
    ss: list or ndarray
        set of the set
    sets: list or ndarray
        the set of fuzzy measure
    m: str
        fuzzy measure function, default is 'lambda'

    Returns
    -------
    shannon entropy: float
        Shannon entropy of a fuzzy measure

    Examples
    --------
    In [1]: s1 = np.array([0.4,0.25,0.37,0.2])
    In [2]: shannon_entropy(s1)
    Out[2]: 1.3311003453061803

    """
    def h(t):
        return -t*np.log(t)
    lam = fuzzm(sets, meas=m)
    n = lam.len
    shannon = np.array([])
    for x in ss:
        ts = np.array([])
        for sub in subsets(np.setdiff1d(ss, x)):
            coef = np.math.factorial(n - sub.size - 1) * \
                   np.math.factorial(sub.size) / np.math.factorial(n)
            ts = np.append(ts, coef * h(derivative(x, sub, lam)))
        shannon = np.append(shannon, np.sum(ts))
    return np.sum(shannon)
