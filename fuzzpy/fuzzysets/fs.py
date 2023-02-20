#  Copyright (C) yibocat 2023 all Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/17 下午4:43
#  Author: yibow
#  E-mail: yibocat@yeah.net
#  Software: fuzzpy

import numpy as np

from .fuzzyset import fuzzyset
import fuzzpy.fuzzynumbers as fns


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
    elif x.shape != y.shape:
        if info:
            print('Different shapes of fuzzy sets.')
        return False
    else:
        xr, yr = x.ravel(), y.ravel()
        for i in range(x.size):
            if xr.set[i] != yr.set[i]:
                if info:
                    print('There are unequal elements')
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
    elif x.shape != y.shape:
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
    d = fns.get_dict
    assert t in d, 'The type of the fuzzy set does not exist.'

    r = fuzzyset(qrung, t)
    return r.rand(*n, num=num)





























