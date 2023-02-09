#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/2 上午11:59
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzPy

import numpy as np

from .fuzzyset import fuzzyset
from .__fuzzysetmath import __dot11
from .__fuzzysetmath import __dot12
from .__fuzzysetmath import __dot21
from .__fuzzysetmath import __dot22

from config.dictionary import load_dict


def dot(x, y, norm='algeb'):
    """
        Dot product operation of two lists of fuzzy elements.
        The result operation satisfies the matrix multiplication algorithm.
        When both x and y are 1D fuzzy vectors, return their inner product;
        when x or y is a 2D fuzzy matrix, perform fuzzy matrix operation,
        and then return a 2D fuzzy set (fuzzy matrix).

        Parameters
        ----------
            x:  numpy.ndarray
                A 1D or 2D list of fuzzy elements.
            y:  numpy.ndarray
                A 1D or 2D list of fuzzy elements.
            norm:   str
                Arithmetic paradigm, defaults to algebraic operations.
                Options are 'algeb' and 'eins' Norm
        Returns
        -------
            fuzzyset
                A 2D list of fuzzy elements.
            fuzzyelement    if x and y are both 1D lists.
            fuzzyset        other

        Notes
        -----
            x and y are not fuzzyset types, but a numpy.ndarray array type.
    """

    assert 0 < len(x.shape) <= 2 and \
           0 < len(y.shape) <= 2, 'ERROR: Dot product only supports fuzzy sets below 2D'

    if len(x.shape) == 1 and len(y.shape) == 1:
        return __dot11(x, y, norm=norm)
    elif len(x.shape) == 1 and len(y.shape) == 2:
        return __dot12(x, y, norm)
    elif len(x.shape) == 2 and len(y.shape) == 1:
        return __dot21(x, y, norm)
    else:
        return __dot22(x, y, norm)


def fuzz_add(f1: fuzzyset, f2: fuzzyset, norm='algeb'):
    """
        Add two fuzzy sets.

        Parameters
        ----------
            f1:  fuzzyset
                A fuzzy set.
            f2:  fuzzyset
                A fuzzy set.
            norm:   str
                Arithmetic paradigm, defaults to algebraic operations.
        Returns
        -------
            fuzzyset
                A fuzzy set.
        Notes
        -----
    """
    assert f1.shape == f2.shape, 'ERROR: The shape of the two fuzzy sets must be the same shape.'
    assert f1.qrung == f2.qrung, 'ERROR: The Q-rung of the two fuzzy sets must be equal.'

    add_op = norm + '_plus'
    newf = fuzzyset(f1.qrung, f1.dict['type'].__name__)
    newf.zeros(*f1.shape)

    for i in range(f1.shape[0]):
        for j in range(f1.shape[1]):
            newf.set[i, j] = f1.dict[add_op](f1.set[i, j], f2.set[i, j])
    newf.reshape(f2.shape)
    return newf


def fuzz_multiply(f1: fuzzyset, f2: fuzzyset, norm='algeb'):
    """
        Multiply two fuzzy sets.

        Parameters
        ----------
            f1:  fuzzyset
                A fuzzy set.
            f2:  fuzzyset
                A fuzzy set.
            norm:   str
                Arithmetic paradigm, defaults to algebraic operations.
        Returns
        -------
            fuzzyset
                A fuzzy set.
        Notes
        -----
    """
    assert f1.shape == f2.shape, 'ERROR: The shape of the two fuzzy sets must be the same shape.'
    assert f1.qrung == f2.qrung, 'ERROR: The Q-rung of the two fuzzy sets must be equal.'

    mult_op = norm + '_multiply'
    newf = fuzzyset(f1.qrung, f1.dict['type'].__name__)
    newf.zeros(*f1.shape)

    for i in range(f1.shape[0]):
        for j in range(f1.shape[1]):
            newf.set[i, j] = f1.dict[mult_op](f1.set[i, j], f2.set[i, j])
    newf.reshape(f2.shape)
    return newf


def fuzz_and(f1: fuzzyset, f2: fuzzyset):
    """
        Logical and of two fuzzy sets.

        Parameters
        ----------
            f1:  fuzzyset
                A fuzzy set.
            f2:  fuzzyset
                A fuzzy set.
        Returns
        -------
            fuzzyset
                A fuzzy set.
        Notes
        -----
    """
    assert f1.shape == f2.shape, 'ERROR: The shape of the two fuzzy sets must be the same shape.'
    assert f1.qrung == f2.qrung, 'ERROR: The Q-rung of the two fuzzy sets must be equal.'

    newf = fuzzyset(f1.qrung, f1.dict['type'].__name__)
    newf.zeros(*f1.shape)

    for i in range(f1.shape[0]):
        for j in range(f1.shape[1]):
            newf.set[i, j] = f1.dict['intersection'](f1.set[i, j], f2.set[i, j])
    newf.reshape(f2.shape)
    return newf


def fuzz_or(f1: fuzzyset, f2: fuzzyset):
    """
        Logical or of two fuzzy sets.

        Parameters
        ----------
            f1:  fuzzyset
                A fuzzy set.
            f2:  fuzzyset
                A fuzzy set.
        Returns
        -------
            fuzzyset
                A fuzzy set.
        Notes
        -----
    """
    assert f1.shape == f2.shape, 'ERROR: The shape of the two fuzzy sets must be the same shape.'
    assert f1.qrung == f2.qrung, 'ERROR: The Q-rung of the two fuzzy sets must be equal.'

    newf = fuzzyset(f1.qrung, f1.dict['type'].__name__)
    newf.zeros(*f1.shape)

    for i in range(f1.shape[0]):
        for j in range(f1.shape[1]):
            newf.set[i, j] = f1.dict['unions'](f1.set[i, j], f2.set[i, j])
    newf.reshape(f2.shape)
    return newf


def fuzz_func(func, f1: fuzzyset, f2: fuzzyset, *args):
    """
        Apply a function to two fuzzy sets.

        Parameters
        ----------
            func: function
                The apply function
            f1:  fuzzyset
                A fuzzy set.
            f2:  fuzzyset
                A fuzzy set.
            args:  list
                The arguments for the function.
        Returns
        -------
            fuzzyset
                A fuzzy set.
        Notes
        -----
    """
    assert f1.shape == f2.shape, 'ERROR: The shape of the two fuzzy sets must be the same shape.'
    assert f1.qrung == f2.qrung, 'ERROR: The Q-rung of the two fuzzy sets must be equal.'

    newf = fuzzyset(f1.qrung, f1.dict['type'].__name__)
    newf.zeros(*f1.shape)

    for i in range(f1.shape[0]):
        for j in range(f1.shape[1]):
            newf.set[i, j] = func(f1.set[i, j], f2.set[i, j], *args)
    newf.reshape(f2.shape)
    return newf


def cartadd(f1, f2, norm='algeb'):
    """
        Cartesian addition of two fuzzy sets.

        Parameters
        ----------
            f1:  numpy.ndarray
                The first fuzzy set.
            f2:  numpy.ndarray
                The second fuzzy set.
            norm: str
                Arithmetic paradigm, defaults to algebraic operations.
                Options are 'algeb' and 'eins' Norm
        Returns
        -------
            numpy.ndarray
                The result of the addition.
        Notes
        -----
    """
    d = load_dict(False)
    x, y = f1.ravel(), f2.ravel()

    assert x[0].__class__.__name__ in d and y[0].__class__.__name__ in d, 'ERROR: fuzzy set type does not exist!'
    assert x[0].__class__.__name__ == y[0].__class__.__name__, 'ERROR: the two fuzzy set are not the same set!'
    assert x[0].qrung == y[0].qrung, 'ERROR: the qrung of two fuzzy sets are not equal!'

    newset1 = fuzzyset(x[0].qrung, y[0].__class__.__name__)
    newset2 = fuzzyset(x[0].qrung, y[0].__class__.__name__)
    l1, l2 = len(x), len(y)

    a = dot(np.atleast_2d(x).T, newset1.poss(1, l2).set, norm)
    b = dot(newset2.poss(l1, 1).set, np.atleast_2d(y), norm)
    # print(type(a),type(b))

    return fuzz_add(a, b, norm)


def cartprod(f1, f2, norm='algeb'):
    """
        Cartesian product of two fuzzy sets.

        Parameters
        ----------
            f1:  numpy.ndarray
                The first fuzzy set.
            f2:  numpy.ndarray
                The second fuzzy set.
            norm: str
                Arithmetic paradigm, defaults to algebraic operations.
                Options are 'algeb' and 'eins' Norm
        Returns
        -------
            numpy.ndarray
                The result of the product.
        Notes
        -----
    """
    d = load_dict(False)
    x, y = f1.ravel(), f2.ravel()

    assert x[0].__class__.__name__ in d and y[0].__class__.__name__ in d, 'ERROR: fuzzy set type does not exist!'
    assert x[0].__class__.__name__ == y[0].__class__.__name__, 'ERROR: the two fuzzy set are not the same set!'
    assert x[0].qrung == y[0].qrung, 'ERROR: the qrung of two fuzzy sets are not equal!'

    newset1 = fuzzyset(x[0].qrung, y[0].__class__.__name__)
    newset2 = fuzzyset(x[0].qrung, y[0].__class__.__name__)
    l1, l2 = len(x), len(y)

    a = dot(np.atleast_2d(x).T, newset1.poss(1, l2).set, norm)
    b = dot(newset2.poss(l1, 1).set, np.atleast_2d(y), norm)

    return fuzz_multiply(a, b, norm)


def distance():
    pass


def similarity():
    pass


def crossentropy():
    pass
