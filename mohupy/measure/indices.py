#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/9/21 下午8:25
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import numpy as np


def deriv(e, sub, func, *args):
    """
        Derivative of a fuzzy measure function(derivatives of set functions).
            The notion of discrete derivatives can be seen as a basis for determining
            the contribution of inputs to various coalitions, as well as for observing
            interaction effects.
            The function can be seen as a derivative of x to the fuzzy measure function
            at subset.

        Parameters
        ----------
            e : list or float or np.float_ or np.ndarray
                Elements or subsets to be differentiated
            sub : list or float or np.float_ or np.ndarray
                The subset to be differentiated
            func : function
                The fuzzy measure function
            args : list or np.ndarray
                The fixed sets.
        Returns
        -------
            np.float_
            The derivative of an element or subset with respect to the subset under
                a fixed set

        Examples
        --------
            1.  In [1]: deriv([0.4,0.25],[0.4,0.25,0.37,0.2], mp.lambda_meas, [0.4,0.25,0.37,0.2])
                Out[1]: 0.4625822184903504
            2.  In [2]: deriv([0.4,0.25],[0.4,0.25,0.37], mp.lambda_meas, [0.4,0.25,0.37,0.2])
                Out[2]: 0.5072507443907042
    """
    assert len(np.setdiff1d(e, *args)) == 0, \
        'ERROR: The element or list must be in the set.'
    assert len(np.setdiff1d(sub, *args)) == 0, \
        'ERROR: The subset must be in the set.'

    union = np.union1d(sub, e)
    differ = np.setdiff1d(sub, e)
    return func(union, *args) - func(differ, *args)


def shapley(e, func, *args):
    """
        Shapley value of a set. The Shapley value is interpreted as a kind
            of average value of the contribution of each criterion alone in
            all coalitions. The Shapley value is the vector of the average
            marginal. One important property of the Shapley value is that
            the sum of the vector is 1.

        Parameters
        ----------
            e : list or float or np.float_ or np.ndarray
                Elements or subsets to be differentiated
            func : function
                The fuzzy measure function
            args : list or np.ndarray
                The fixed sets.

        Returns
        -------
            np.ndarray
                The shapley value of any element of e with respect to the
                fixed sets and any fuzzy measure.

        Examples
        --------
            1.  In [1]: shapley([0.4,0.25,0.37,0.2], mp.lambda_meas, [0.4,0.25,0.37,0.2])
                Out[1]: [0.33322906 0.2013346  0.30610416 0.15933218]
            2.  In [2]: shapley([0.4,0.25,0.2], mp.lambda_meas, [0.4,0.25,0.37,0.2])
                Out[2]: [0.1871141  0.1143156  0.09078327]
    """
    n = len(*args)
    shap = np.array([])

    from .utils import subsets
    for x in e:
        ts = np.array([])
        for sub in subsets(np.setdiff1d(e, x)):
            coef = np.math.factorial(n - len(sub) - 1) * \
                   np.math.factorial(len(sub)) / np.math.factorial(n)
            ts = np.append(ts, coef * deriv(x, sub, func, *args))
        shap = np.append(shap, np.sum(ts))
    return shap


def banzhaf(e, func, *args):
    """
        An alternative to the Shapley value is the Banzhaf value. It measures the same
            concept as the Shapley value, but weights the terms [μ(A ∪{i}) − μ(A)] in
            the sum equally.

        Parameters
        ----------
            e : list or float or np.float_ or np.ndarray
                Elements or subsets to be differentiated
            func : function
                The fuzzy measure function
            args : list or np.ndarray
                The fixed sets.

        Returns
        -------
            np.ndarray
                The banzhaf value of any element of e with respect to the
                fixed sets and any fuzzy measure.

        Examples
        --------
            1.  In [1]: banzhaf([0.4,0.25,0.37,0.2], mp.lambda_meas, [0.4,0.25,0.37,0.2])
                Out[1]: [0.17701811 0.10677004 0.16256442 0.08443251]
            2.  In [2]: mp.banzhaf([0.4,0.25,0.37], mp.lambda_meas, [0.4,0.25,0.37,0.2])
                Out[2]: [0.0925856  0.05584383 0.0850259 ]
    """
    n = len(*args)
    coef = 1/2**(n - 1)
    ban = np.array([])

    from .utils import subsets
    for x in e:
        ts = np.array([])
        for sub in subsets(np.setdiff1d(e, x)):
            ts = np.append(ts, coef * deriv(x, sub, func, *args))
        ban = np.append(ban, np.sum(ts))
    return ban


def shannon(e, func, *args):
    """
        The Shannon entropy is a measure of the uncertainty of a fixed set.
            It is used to measure the uncertainty of a subset under the
            fuzzy measure of a set.

        Parameters
        ----------
            e : list or float or np.float_ or np.ndarray
                Elements or subsets to be differentiated
            func : function
                The fuzzy measure function
            args : list or np.ndarray
                The fixed sets.

        Returns
        -------
            np.ndarray
                The Shannon entropy of any element of e with respect to the
                fixed sets and any fuzzy measure.

        Examples
        --------
            In [1]: shannon([0.4,0.25,0.37,0.2], mm.lambda_meas, [0.4,0.25,0.37,0.2])
            Out[1]: [0.36265366 0.31962317 0.3588178  0.29000572]
    """
    def _h(t):
        return -t*np.log(t)
    n = len(*args)
    shan = np.array([])

    from .utils import subsets
    for x in e:
        ts = np.array([])
        for sub in subsets(np.setdiff1d(e, x)):
            coef = np.math.factorial(n - len(sub) - 1) * \
                   np.math.factorial(len(sub)) / np.math.factorial(n)
            ts = np.append(ts, coef * _h(deriv(x, sub, func, *args)))
        shan = np.append(shan, np.sum(ts))
    return shan
