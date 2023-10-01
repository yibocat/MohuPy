#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/10/1 下午4:29
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import re

import numpy as np
import pandas as pd

from ..core.mohunum import mohunum
from ..core.mohusets import mohuset


def str_to_mohunum(s: str, q, mtype: str = 'qrofn') -> mohunum:
    """
        Convert a string to a fuzzy number.

        Parameters
        ----------
            s : str
            q : int
            mtype: str
                The type of fuzzy number
                Optional: 'fn','ivfn'

        Returns
        -------
            mohunum

        Notes: When the input data is 0, it should be set to 0.
        Q-rung fuzzy convert function accepts the form: [x,x]
    """
    if mtype == 'qrofn':
        newfn = mohunum(q, 0., 0.)
        t = re.findall(r'^\[(\d.*?\d)]$', s)
        assert len(t) == 1, \
            'data format error.'
        x = re.findall(r'\d.?\d*', t[0])
        assert len(x) == 2, \
            'data format error.'
        newfn.md = float(x[0])
        newfn.nmd = float(x[1])
        assert newfn.is_valid(), 'data format is correct, but the data is invalid.'
        return newfn
    if mtype == 'ivfn':
        newfn = mohunum(q, [0., 0.], [0., 0.])
        t2 = re.findall(r'\[(\d.*?\d)]', s)
        assert len(t2) == 2, \
            'data format error.'
        md = re.findall(r'\d.?\d*', t2[0])
        nmd = re.findall(r'\d.?\d*', t2[1])
        assert len(md) == 2 and len(nmd) == 2, \
            'data format error.'

        m = [float(md[0]), float(md[1])]
        n = [float(nmd[0]), float(nmd[1])]
        newfn.md = m
        newfn.nmd = n
        assert newfn.is_valid(), 'data format is correct, but the data is invalid.'
        return newfn
    raise TypeError(f'unknown mtype: {mtype}')


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


def distance(d1: mohunum, d2: mohunum, l: (int, np.int_), indeterminacy=True):
    """
        The generalized distance function for two fuzzy elements.
        The parameter 'l' is the generalized distance function parameter.
        'l=1' indicates the Hamming distance and 'l=2' indicates the
        Euclidean distance.

        Parameters
        ----------
            d1 : mohunum
                The first fuzzy number.
            d2 : mohunum
                The second fuzzy number.
            l : int, np.int_
                The generalized distance function parameter.
                'l=1' indicates the Hamming distance and 'l=2' indicates
                the Euclidean distance.
            indeterminacy : bool
                If True, the indeterminacy of the two fuzzy numbers will be considered.
                If False, the indeterminacy of the two fuzzy numbers will not be considered.

        Returns
        -------
            float
                The generalized distance between of two fuzzy numbers.

        References
        ----------
            [1] J. S, “Ordering of interval-valued Fermatean fuzzy sets and its
                applications,” Expert Syst Appl, vol. 185, p. 115613, 2021,
                doi: 10.1016/j.eswa.2021.115613.
            [2] Z. Xu, “A method based on distance measure for interval-valued
                intuitionistic fuzzy group decision-making,” Inform Sciences,
                vol. 180, no. 1, pp. 181–190, 2010, doi: 10.1016/j.ins.2009.09.005.

        Example
        -------
            In [1]: f1 = mohunum(2, 0.5, 0.45)
            In [2]: f2 = mohunum(2, 0.67, 0.2)
            In [3]: distance(f1, f2, 2)
            Out[3]: 0.18342903259844126

    """
    assert d1.qrung == d2.qrung, \
        'ERROR: The q rung of two fuzzy numbers must be equal.'
    assert d1.mtype == d2.mtype, \
        'ERROR: The type of two fuzzy numbers must be same.'
    assert l > 0, \
        'ERROR: The value of l must be greater than 0.'
    mtype = d1.mtype
    q = d1.qrung
    pi1 = d1.ind
    pi2 = d2.ind
    pi = np.fabs(pi1 ** q - pi2 ** q) ** l
    if mtype == 'qrofn':
        if indeterminacy:
            return (0.5 * (np.fabs(d1.md ** q - d2.md ** q) ** l +
                           np.fabs(d1.nmd ** q - d2.nmd ** q) ** l + pi)) ** (1 / l)
        else:
            return (0.5 * (np.fabs(d1.md ** q - d2.md ** q) ** l +
                           np.fabs(d1.nmd ** q - d2.nmd ** q) ** l)) ** (1 / l)
    if mtype == 'ivfn':
        if indeterminacy:
            return 0.25 * (
                    np.fabs(d1.md[0] ** q - d2.md[0] ** q) ** l +
                    np.fabs(d1.md[1] ** q - d2.md[1] ** q) ** l +
                    np.fabs(d1.nmd[0] ** q - d2.nmd[0] ** q) ** l +
                    np.fabs(d1.nmd[1] ** q - d2.nmd[1] ** q) ** l + pi) ** (1 / l)
        else:
            return 0.25 * (
                    np.fabs(d1.md[0] ** q - d2.md[0] ** q) ** l +
                    np.fabs(d1.md[1] ** q - d2.md[1] ** q) ** l +
                    np.fabs(d1.nmd[0] ** q - d2.nmd[0] ** q) ** l +
                    np.fabs(d1.nmd[1] ** q - d2.nmd[1] ** q) ** l) ** (1 / l)
    raise TypeError(f'unknown mtype: {mtype}')


def asfuzzset(x, copy=False):
    """
        Convert a fuzzy numpy array to a fuzzy set.

        Parameters
        ----------
            x:  numpy.ndarray or list
                The fuzzy numpy array.
            copy:  bool
                Whether to copy the array.
        Returns
        -------
            fuzzyset
                A fuzzy set.
    """
    if copy:
        xt = np.copy(x)
    else:
        xt = x

    fl = np.asarray(xt, dtype=object)
    flat = fl.flatten()
    r = np.random.choice(flat)
    newset = mohuset(r.qrung, r.mtype)
    newset.set = fl
    return newset


def func4num(func, f: mohuset, *args):
    """
        Apply a function to a fuzzy set.

        Parameters
        ----------
            func:  function
                The function to apply to the all num of fuzzy set
            f:  mohuset
                The fuzzy set.
            *args:  list
                The arguments of the function.
        Returns
        -------
            mohuset

        Notes
        -----
            This is a method for fuzzy numbers in fuzzy sets
    """
    vec_func = np.vectorize(func)
    newset = mohuset(f.qrung, f.mtype)
    newset.set = vec_func(f.set, *args)
    return newset


def savez(f: mohuset, path: str):
    """
        Save a fuzzy set to a file.

        This method not only saves the fuzzy set, but also saves the relevant
        information of the fuzzy set.
        Specific storage content:
            1. The set of the fuzzy set
            2. The qrung of the fuzzy set
            3. The shape of the fuzzy set
            4. The type of the fuzzy set

        Parameters
        ----------
            f:  mohuset
                The fuzzy set.
            path:  str
                The path to the file.

        Returns
        -------
            Boolean

        Notes
        -----
            This method saves the fuzzy set to a .npz file.
    """
    try:
        f.savez(path)
        return True
    except Exception as e:
        print(e, 'Save failed.')
        return False


def loadz(path: str):
    """
        Load a fuzzy set from a .npz file.

        This method not only loads the fuzzy set, but also loads the relevant
        information of the fuzzy set.
        Specific storage content:
            1. The set of the fuzzy set
            2. The qrung of the fuzzy set
            3. The shape of the fuzzy set
            4. The type of the fuzzy set

        Parameters
        ----------
            path:  str
                The path to the file.

        Returns
        -------
            mohuset
                The fuzzy set.

        Notes
        -----
            This method loads the fuzzy set from a.npz file.
    """
    newset = mohuset()
    try:
        newset.loadz(path)
        return newset
    except Exception as e:
        print(e, 'Load failed.')


def to_csv(f: mohuset, path: str):
    """
        Save a fuzzy set to a .csv file.

        This method only saves the fuzzy set, and does not save the related
        information of the set.

        Parameters
        ----------
            f:  mohuset
                The fuzzy set.
            path:  str
                The path to the file.

        Returns
        -------
            Boolean

        Notes
        -----
            This method saves the fuzzy set to a.csv file.
    """
    try:
        f.mat.to_csv(path)
        return True
    except Exception as e:
        print(e, 'Save failed.')
        return False


def load_csv(path: str, q: int, mtype: str = 'qrofn'):
    """
        Load a fuzzy set from a.csv file.

        This method is used to load a fuzzy set table with unknown information. It
        is necessary to judge the content of the fuzzy table during loading. When
        initializing a fuzzy set, Q-rung and fuzzy set type are given, so it is necessary
        to judge whether a fuzzy set meets these two conditions. This method will only
        load when the fuzzy set table is equal to or satisfied with the initial fuzzy set
        condition.

        Parameters
        ----------
            path:  str
                The path to the file.
            q:  int
                The q rung of the fuzzy set.
            mtype:  str
                The type of the fuzzy set.

        Returns
        -------
            mohuset
                The fuzzy set.

        Notes
        -----
            This method loads the fuzzy set from a.csv file.
    """
    try:
        m = np.asarray(pd.read_csv(path, index_col=0))
        vec_func = np.vectorize(str_to_mohunum)
        f = vec_func(m, q, mtype)

        newset = mohuset(q, mtype)
        newset.set = f
        return newset
    except Exception as e:
        print(e, 'Load failed.')

