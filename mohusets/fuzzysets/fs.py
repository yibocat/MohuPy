#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/21 上午4:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets

import numpy as np
import pandas as pd

from .fuzzyset import fuzzyset
from ..fuzzynumbers import glb, dh_fn_max, dh_fn_min, dh_fn_mean


def fuzzys(x, copy=True):
    """
        construct a fuzzy set

        Parameters
        ----------
            x:  numpy.array or list
                Can be a numpy.ndarray of any dimension
            copy: bool
        Returns
        -------
            fuzzyset
                A fuzzy set.
    """
    if copy:
        xt = np.copy(x)
    else:
        xt = x
    fl = np.asarray(xt)
    shape = fl.shape
    y = fl.ravel()

    newf = fuzzyset(y[0].qrung, y[0].__class__.__name__)
    for fe in y:
        newf.append(fe)
    newf.reshape(*shape)
    return newf


def asfuzzyset(x):
    """
        Convert a fuzzy numpy array to a fuzzy set.

        Parameters
        ----------
            x:  numpy.ndarray or list
                The fuzzy numpy array.
        Returns
        -------
            fuzzyset
                A fuzzy set.
    """
    return fuzzys(x, copy=False)


def equal(x: fuzzyset, y: fuzzyset, info=False) -> bool:
    """
        Check if two fuzzy sets are equal.

        Parameters
        ----------
            x:  fuzzyset
                The first fuzzy set.
            y:  fuzzyset
                The second fuzzy set.
            info:  bool
                Whether to print information.
        Returns
        -------
            bool
    """
    if x.qrung != y.qrung:
        if info:
            print('The Q-rung of two fuzzyset are not equal.')
        return False
    elif x.dict['type'] != y.dict['type']:
        if info:
            print('Different types of fuzzy sets.')
        return False
    elif (np.asarray(x.shape) != np.asarray(y.shape)).all():
        if info:
            print('Different shapes of fuzzy sets.')
        return False
    else:
        xr, yr = x.ravel(), y.ravel()
        for i in range(x.size):
            if (xr.set[i].md != yr.set[i].md).all():
                if info:
                    print('There are unequal elements.')
                return False
            if (xr.set[i].nmd != yr.set[i].nmd).all():
                if info:
                    print('There are unequal elements.')
                return False
    return True


def similar(x: fuzzyset, y: fuzzyset, info=False):
    """
        Check if two fuzzy sets are similar.
        This function will only check the Q-rung, type and shape
        of the two fuzzy sets, and will not check the equality of
        elements in the fuzzy sets.

        Parameters
        ----------
            x:  fuzzyset
                The first fuzzy set.
            y:  fuzzyset
                The second fuzzy set.
            info:  bool
                Whether to print information.
        Returns
        -------
            bool
    """
    if x.qrung != y.qrung:
        if info:
            print('The Q-rung of two fuzzyset are not equal.')
        return False
    elif x.dict['type'] != y.dict['type']:
        if info:
            print('Different types of fuzzy sets.')
        return False
    elif (np.asarray(x.shape) != np.asarray(y.shape)).all():
        if info:
            print('Different shapes of fuzzy sets.')
        return False
    return True


def similarity_matrix():
    """
        The similarity matrix of q-rung fuzzy set.
        This function is only applicable to Q-rung intuitionistic fuzzy sets and
        Q-rung interval-valued intuitionistic fuzzy sets.

        reference:
            Z. Xu, “A method based on distance measure for interval-valued
            intuitionistic fuzzy group decision-making,” Inform Sciences,
            vol. 180, no. 1, pp. 181–190, 2010, doi: 10.1016/j.ins.2009.09.005.
    """
    pass


def composition_matrix():
    """
        Combination matrix of any two fuzzy set similarity matrices of the same shape.
        This function is only applicable to Q-rung intuitionistic fuzzy sets and
        Q-rung interval-valued intuitionistic fuzzy sets.

        reference:
            Z. Xu, “A method based on distance measure for interval-valued
            intuitionistic fuzzy group decision-making,” Inform Sciences,
            vol. 180, no. 1, pp. 181–190, 2010, doi: 10.1016/j.ins.2009.09.005.

    """

    pass


def rand_set(qrung, t, *n, num=5):
    """
        Generate a random fuzzy set.

        Parameters
        ----------
            qrung:  int
                The q-rung of the fuzzy set.
            t:  str
                The type of the fuzzy set.
            n:  int list
                The size of the fuzzy set.
            num:  int
                The number of membership and non-membership degree
                in dual hesitant fuzzy element.
        Returns
        -------
            fuzzyset
                A random fuzzy set.
    """
    assert qrung > 0, 'q-rung must be greater than 0.'
    d = glb.global_dict()
    assert t in d, 'The type of the fuzzy set does not exist.'

    r = fuzzyset(qrung, t)
    return r.rand(*n, num=num)


def dh_fn_sets(f: fuzzyset, norm='max'):
    """
        Transform a dual hesitant fuzzy set into a fuzzy set

        Parameters
        ----------
            f:  fuzzyset
                The dual hesitant fuzzy set.
            norm:  str
                The norm of the dual hesitant function.
        Returns
        -------
            fuzzyset
                The fuzzy set.
    """
    assert f.dict['type'].__name__ == 'qrungdhfe', \
        'The fuzzy set is not dual hesitant fuzzy set.'
    dm_ffn = []
    for i in range(f.shape[0]):
        dm_a = []
        for j in range(f.shape[1]):
            if norm == 'max':
                dm_a.append(dh_fn_max(f.set[i, j]))
            elif norm == 'min':
                dm_a.append(dh_fn_min(f.set[i, j]))
            else:
                dm_a.append(dh_fn_mean(f.set[i, j]))
        dm_ffn.append(dm_a)
    return asfuzzyset(dm_ffn)


def savez(fs: fuzzyset, path: str):
    try:
        fs.savez(path)
    except Exception as e:
        print(e, 'Save failed.')


def loadz(path: str):
    newfs = fuzzyset()
    try:
        newfs.loadz(path)
    except Exception as e:
        print(e, 'Load failed.')
    return newfs


def sort(t: fuzzyset, func=None, reverse=False, *param):
    """
        Sort a fuzzy set.

        Parameters
        ----------
            t:  fuzzyset
                The fuzzy set.
            func:  function
                The function used to sort the fuzzy set.
                if func is None, the score function will be used.
            reverse:  bool
                Whether to reverse the sort.
            param:  list
                The parameters of the function.
        Returns
        -------
            fuzzyset
                The sorted fuzzy set.

    """
    assert len(t.shape) == 1, 'the fuzzyset must be a 1-d array.'
    if func is None:
        so = t.score
    else:
        so = t.elementfunc(func, *param)
    if reverse is True:
        index = np.argsort(-so)
    else:
        index = np.argsort(so)
    A = np.asarray(t.set[index])
    return asfuzzyset(A)
