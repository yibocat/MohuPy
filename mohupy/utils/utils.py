#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/10/1 下午4:29
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import copy
import re
from typing import Union

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from ..core.mohusets import mohuset
from ..core.base import mohunum
from ..registry.image import fuzzPlot
from ..registry.distance import fuzzDis
from ..registry.string2num import fuzzString


def isscalar(x: Union[mohuset, mohunum]):
    if isinstance(x, mohunum):
        return True
    if isinstance(x, mohuset):
        return False
    raise TypeError('unsupported type: {}'.format(type(x)))


def str2mohu(s: str, q, mtype: str) -> mohunum:
    return fuzzString[mtype](s, q)


def distance(f1: mohunum,
             f2: mohunum,
             t: (float, np.float_) = 1,
             l: (int, np.int_) = 1,
             indeterminacy=True):
    mtype = f1.mtype
    return fuzzDis[mtype](f1, f2, l, t, indeterminacy)


def plot(f: (mohuset, mohunum),
         other=None,
         area=None,
         color='red',
         color_area=None,
         alpha=0.3,
         label='',
         legend=False):
    if area is None:
        area = [False, False, False, False]
    if color_area is None:
        color_area = ['red', 'green', 'blue', 'yellow']

    q = f.qrung
    mtype = f.mtype

    plt.gca().spines['top'].set_linewidth(False)
    plt.gca().spines['bottom'].set_linewidth(True)
    plt.gca().spines['left'].set_linewidth(True)
    plt.gca().spines['right'].set_linewidth(False)
    plt.axis((0, 1.1, 0, 1.1))
    plt.axhline(y=0)
    plt.axvline(x=0)

    if isinstance(f, mohunum):
        fuzzPlot[mtype](f,
                        other=other,
                        area=area,
                        color=color,
                        color_area=color_area,
                        alpha=alpha)
    if isinstance(f, mohuset):
        plot_vec = np.vectorize(fuzzPlot[mtype])
        plot_vec(f.set,
                 other=other,
                 color=color,
                 alpha=alpha,
                 area=None,
                 color_area=None)

    x = np.linspace(0, 1, 1000)
    y = (1 - x ** q) ** (1 / q)
    plt.plot(x, y, label=label)
    if legend: plt.legend(loc='upper right', fontsize='small')
    plt.show()


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


def load_csv(path: str, q: int, mtype: str):
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
        vec_func = np.vectorize(str2mohu)
        f = vec_func(m, q, mtype)

        newset = mohuset(q, mtype)
        newset.set = f
        return newset
    except Exception as e:
        raise ValueError("Failed to load " + str(e))
        # print(e, 'Load failed.')


def abs(f1: Union[mohuset, mohunum], f2: Union[mohuset, mohunum]):
    """
        Calculate the absolute value of two fuzzy sets or numbers.

        Parameters
        ----------
            f1:  Union[mohuset, mohunum]
                The first fuzzy set or number.
            f2:  Union[mohuset, fuzzNum]
                The second fuzzy set or number.

        Returns
        -------
            Union[mohuset, fuzzNum]
                The absolute value of f1 and f2.
    """
    y = lambda x, t: x - t if x > t else t - x
    if isinstance(f1, mohunum) and isinstance(f2, mohunum):
        return y(f1, f2)
    if isinstance(f1, mohuset) and isinstance(f2, mohuset):
        vec_func = np.vectorize(y)
        result = vec_func(f1.set, f2.set)
        newset = mohuset(f1.qrung, f1.mtype)
        newset.set = result
        return newset
    if isinstance(f1, mohunum) and isinstance(f2, mohuset):
        vec_func = np.vectorize(y)
        result = vec_func(f1, f2.set)
        newset = mohuset(f2.qrung, f2.mtype)
        newset.set = result
        return newset
    if isinstance(f1, mohuset) and isinstance(f2, mohunum):
        vec_func = np.vectorize(y)
        result = vec_func(f1.set, f2)
        newset = mohuset(f1.qrung, f1.mtype)
        newset.set = result
        return newset


def zeros_like(f: mohuset):
    from .construct import zeros
    return zeros(f.qrung, f.mtype, *f.shape)


def poss_like(f: mohuset):
    from .construct import poss
    return poss(f.qrung, f.mtype, *f.shape)


def negs_like(f: mohuset):
    from .construct import negs
    return negs(f.qrung, f.mtype, *f.shape)


def full_like(f: mohuset, x):
    from .construct import full
    return full(x, *f.shape)


def broadcast_to(f: mohuset, shape):
    newset = mohuset(f.qrung, f.mtype)
    newset.set = np.broadcast_to(f.set, shape)
    return newset


def squeeze(f: mohuset, axis=None):
    newset = mohuset(f.qrung, f.mtype)
    newset.set = np.squeeze(f.set, axis)
    return newset


def relu(f: mohuset):
    newset = mohuset(f.qrung, f.mtype)
    res = copy.copy(f.set)
    from ..core import fuzznum
    res[res < fuzznum(f.qrung, 0.3, 0.7)] = fuzznum(f.qrung, 0., 1.)
    newset.set = res
    del res
    return newset
