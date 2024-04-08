#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/9/21 下午8:25
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import re

import numpy as np
from ..core import Approx


def dirac_meas(e, s):
    """
        Dirac_measure(Bool fuzzy measure). The Dirac measure is a simple
            0-1 fuzzy measure. The element and subset must be a subset of the set.
            When the element is in the subset the Dirac measure is 1. Otherwise, the
            Dirac measure is 0.

        Parameters
        ----------
            e: float, int, np.float_, np.int_, list, np.ndarray
                The element.
            sub: list, np.ndarray
                The subset.
            s: list, np.ndarray
                The fixed set.

        Returns
        -------
            np.int_
                The Dirac measure of 'e' in set 's'.

        Examples
        --------
            1.  In [1]: dirac(1, [1, 2, 3, 4])
                Out[1]: 1
            2.  In [2]: dirac(5, [1, 2, 3, 4])
                Out[2]: 0
    """
    assert len(np.setdiff1d(e, s)) == 0, \
        'ERROR: The element must be in the set.'
    return np.int_(1) if len(np.setdiff1d(e, s)) == 0 else np.int_(0)


def add_meas(e, s):
    """
        Additive fuzzy measure. Compute the additive measure of a subset or
            element in a set

        Parameters
        ----------
            e : float, np.ndarray, list
                Element or subset
            s : list or np.ndarray
                The set.

        Returns
        -------
            np.float_
            The additive measure of the element or the subset 'e'

        Examples
        --------
            1.  In [1]: add_meas([0.2,0.3], [0.2,0.1,0.3,0.15,0.25])
                Out[1]: 0.5
            2.  In [2]: add_meas(0.2, [0.2,0.1,0.3,0.15,0.25])
                Out[2]: 0.2
    """
    assert np.round(sum(s), Approx.round) == 1, \
        "ERROR: The sum of the measurements must be 1."
    assert len(np.setdiff1d(e, s)) == 0, \
        'ERROR: The element must be in the set.'
    return np.sum(e)


def sym_meas(e, s):
    """
        Symmetric fuzzy measure. Compute the symmetric measure of a subset or
            element in a set

        Parameters
        ----------
            e : float, np.ndarray, list
                Element or subset
            s : list or np.ndarray
                The set.

        Returns
        -------
            np.float_
            The symmetric measure of the element or the subset 'e'

        Examples
        --------
            In [1]: sym_meas([0.2,0.4],[0.5,0.1,0.2,0.6,0.4])
            Out[1]: 0.4
    """
    assert len(np.setdiff1d(e, s)) == 0, \
        'ERROR: The element must be in the set.'
    return np.float_(len(e) / len(s))


def lambda_meas(e, s):
    """
        The lambda fuzzy measure function.
            We have a subset of the fuzzy measure sets, then use the
            function to calculate the fuzzy measure of the subset.
            In this function, an anonymous function is defined that
            calculates the parameter lambda of lambda fuzzy measure,
            which returns an anonymous function.

            The calculation of lambda needs to use optimize.fsolve
            optimization calculation of the scipy library, because
            the equation is a high-order nonlinear equation.

            The initial value of lambda optimization calculation
            is usually 1, as shown in the example below.

        Parameters
        ----------
            e : float or list
                Need to calculate a subset of lambda fuzzy measure.
            s : float or list
                The fixed set.

        Returns
        -------
            np.float_
            The lambda fuzzy measure of the subset 'e'.

        Examples
        --------
            In[1]:  lambda_meas([0.14,0.33], [0.45,0.16,0.33,0.14])
            Out[1]: 0.46058088141950154

        Notes
        -----
            The __lamda function is to calculate the parameter lambda.
            This anonymous equation needs to be calculated using optimize.fsolve
            with the scipy library. The calculation is as follows.

            In [1]: x = [0.4,0.25,0.37,0.2]
            In [2]: np.float_(scipy.optimize.fsolve(lamda(x), np.array(-1)))
            Out[2]: -0.4403002498696017
    """

    def __lamda(sets):
        return lambda lam: np.prod(1 + lam * sets) - lam - 1

    assert len(np.setdiff1d(e, s)) == 0, \
        'ERROR: The element or list must be in the set.'

    from scipy.optimize import fsolve
    l = fsolve(__lamda(np.asarray(s)), np.array(-1))

    if np.round(l, Approx.round) == 0:
        return np.float_(np.sum(e))
    else:
        return np.float_((np.prod(1 + l * e) - 1) / l)


def mobius_rep(e: (list, np.ndarray), func, *args):
    """
        The Möbius representation function.
            The mobius representation is helpful in expressing various
            quantities. It also serves an alternative representation of
            a fuzzy measure.

            It is worth noting that Möbius transformation is reversible.
            Its inverse can be converted into a general fuzzy measure
            through Zeta transformation.

        Parameters
        ----------
            e: list or np.ndarray
                A subset that requires Möbius transform
            func: function
                The fuzzy measure function.
                Optional: dirac_meas, add_meas, sym_meas, lambda_meas, zeta_trans
            args: list
                The parameter of the fuzzy measure function.
                Usually is the fixed set.

        Returns
        -------
            np.float_
                The Möbius representation of the subset 'e'.

        Examples
        --------
            In [1]:  mobius_trans([0.4,0.25], lambda_meas, [0.4,0.25,0.37,0.2])
            Out[1]: -0.04403002498696007

    """
    assert len(np.setdiff1d(e, *args)) == 0, \
        'ERROR: The element or list must be in the set.'

    trans = np.array([])

    from .utils import subsets
    for B in subsets(e):
        ceof = (-1) ** np.setdiff1d(e, B).size
        trans = np.append(trans, ceof * func(B, *args))
    return np.sum(trans)


def zeta_rep(e: (list, np.ndarray), func, *args):
    """
        Zeta representation function.
            The Möbius transformation is invertible, and one recovers
            μ by using its inverse, called Zeta transform.

            Note: the zeta_transform is equal to the fuzzy measure value.
            In other words, when func is mobius_trans, the *args of mobius_trans
            is any fuzzy measure function and zeta_trans will calculate the
            fuzzy measure value of e in *args fuzzy measure.

        Parameters
        ----------
            e: list or np.ndarray
                A subset that requires Zeta transform.
            func: fuzzy measure function
                Optional: dirac_meas, add_meas, sym_meas, lambda_meas, mobius_trans
            args: list or np.ndarray
                The parameter of the fuzzy measure function.
                Note that when func is mobius_trans, the *args should be (func, *args),
                where func is the fuzzy measure function and args is the fixed set.

        Returns
        -------
            np.float_
                The Zeta representation of the subset 'e'.

        Examples
        --------
            1.  In [1]: zeta_trans([0.4,0.25], lambda_meas, [0.4,0.25,0.37,0.2])
                Out[1]: 1.25596997501304
            2.  In [2]: zeta_trans([0.4,0.25], mobius_trans, lambda_meas, [0.4,0.25,0.37,0.2])
                Out[2]: 0.60596997501304
                In [3]: lambda_meas([0.4,0.25], [0.4,0.25,0.37,0.2])
                Out[3]: 0.60596997501304

        Notes
        -----
            From the Examples, we can see that the inverse of Möbius transformation is
            Zeta transformation.
    """
    zeta = np.array([])

    from .utils import subsets
    for t in subsets(e):
        zeta = np.append(zeta, func(t, *args))
    return np.sum(zeta)


def vector_rep(e: (list, np.ndarray), func, *args):
    """
        Vector representation function.
            Vector representation is to directly represent the fuzzy measure
            of subset e in vector form.

        Parameters
        ----------
            e: list or np.ndarray
                A subset that requires Möbius transform
            func: function
                The fuzzy measure function.
                Optional: dirac_meas, add_meas, sym_meas, lambda_meas
            args: list
                The parameter of the fuzzy measure function.
                Usually is the fixed set.
        Returns
        -------
            np.float_
                The Vector representation of the subset 'e'.

        Examples
        --------
            In [1]: vector_rep([0.4,0.25], lambda_meas, [0.4,0.25,0.37,0.2])
            Out[1]: np.array([-0.     0.4     0.25      0.60596998])
    """
    from .utils import subsets
    vector = np.array([])
    for x in subsets(e):
        vector = np.append(vector, func(x, *args))
    return vector


def dict_rep(e: (list, np.ndarray), func, *args, chara='C'):
    """
        Dictionary representation function.
            Dictionary representation is to directly represent the fuzzy measure
            of subset e in dictionary form.

        Parameters
        ----------
            e: list or np.ndarray
                A subset that requires Möbius transform
            func: function
                The fuzzy measure function.
                Optional: dirac_meas, add_meas, sym_meas, lambda_meas
            args: list
                The parameter of the fuzzy measure function.
                Usually is the fixed set.
            chara: str
                Representation symbols for dictionary subsets.
                Default to 'C'.
            r: int
                The number of digits after the decimal point.
                Default to 6.
        Returns
        -------
            dict
                The Dictionary representation of the subset 'e'.
        Examples
        --------
            In [1]: dict_rep([0.4,0.25], lambda_meas, [0.4,0.25,0.37,0.2])
            Out[1]: {'{}': -0.0, 'C1': 0.4, 'C2': 0.25, 'C1,C2': 0.60597}
    """

    def _conversion(sttr):
        tss = re.findall(r'\w\d', sttr)
        sp = tss[0]
        for i in tss[1:]:
            sp += ',' + i
        return sp

    n = np.asarray(e).size

    attributes = []
    for i in range(n):
        attributes.append(chara + str(i + 1))

    from .utils import str_subsets
    subset_attributes = str_subsets(attributes)
    fuzzy_measure = np.round(vector_rep(e, func, *args), Approx.round).tolist()

    sub_att = ['{}']
    for t in subset_attributes[1:]:
        sub_att.append(_conversion(t))
    subbs = dict(zip(sub_att, fuzzy_measure))
    return subbs
