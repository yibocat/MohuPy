#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/11/28 下午7:49
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import warnings

import numpy as np

from .base import Library
from ..core import Fuzznum, Fuzzarray


class Isscalar(Library):
    def function(self, x):
        if isinstance(x, Fuzznum):
            return True
        if isinstance(x, Fuzzarray):
            return False
        raise TypeError(f'Unsupported type: {type(x)}')


def isscalar(x):
    return Isscalar()(x)


class FuncForFuzz(Library):
    def function(self, x, func, *args):
        """
            Apply a function to a fuzzy set.

            Parameters
            ----------
                func:  function
                    The function to apply to the all num of fuzzy set
                x:  Fuzzarray
                    The fuzzy set.
                *args:  list
                    The arguments of the function.
            Returns
            -------
                Fuzzarray

            Notes
            -----
                This is a method for fuzzy numbers in fuzzy sets
        """

        if isinstance(x, Fuzznum):
            return func(x, *args)
        if isinstance(x, Fuzzarray):
            vec_func = np.vectorize(func)
            newset = Fuzzarray(x.qrung, x.mtype)
            newset.array = vec_func(x, *args)
            return newset


def func4fuzz(x, func, *args):
    return FuncForFuzz()(x, func, *args)


class AsFuzzarray(Library):
    def function(self, x, copy):
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
                Fuzzarray
                    A fuzzy set.
        """
        if copy:
            xt = np.copy(x)
        else:
            xt = x

        fl = np.asarray(xt, dtype=object)
        flat = fl.flatten()
        r = np.random.choice(flat)

        newset = Fuzzarray(r.qrung, r.mtype)
        newset.array = fl
        return newset


def asfuzzyarray(x, copy=False):
    return AsFuzzarray()(x, copy)


# TODO: 有待商榷，该函数暂时以两者个差为返回值。实际上该方法并不合理
class Absolute(Library):
    def function(self, a, b):
        y = lambda t, s: t - s if t > s else s - t
        if isinstance(a, Fuzznum) and isinstance(b, Fuzznum):
            return y(a, b)
        if isinstance(a, Fuzznum) and isinstance(b, Fuzzarray):
            vec_func = np.vectorize(y)
            result = vec_func(a, b.array)
            newset = Fuzzarray(b.qrung, b.mtype)
            newset.array = result
            return newset
        if isinstance(a, Fuzzarray) and isinstance(b, Fuzznum):
            vec_func = np.vectorize(y)
            result = vec_func(a.array, b)
            newset = Fuzzarray(a.qrung, a.mtype)
            newset.array = result
            return newset
        if isinstance(a, Fuzzarray) and isinstance(b, Fuzzarray):
            vec_func = np.vectorize(y)
            result = vec_func(a.array, b.array)
            newset = Fuzzarray(a.qrung, a.mtype)
            newset.array = result
            return newset
        raise TypeError(f'Unsupported type: {type(a)} or {type(b)}.')


def absolute(a, b):
    warnings.warn(f'This function calculates the difference between the two fuzzy numbers, but it is not reasonable. '
                  f'It is recommended to use the \'abs()\'.')
    return Absolute()(a, b)


class Relu(Library):
    def function(self, x, op):
        def relu(t, o):
            return Fuzznum(t.qrung, 0., 1.) if t < o else t

        if op is None:
            op = Fuzznum(x.qrung, 0.5, 0.5)
        if isinstance(x, Fuzznum) and isinstance(op, Fuzznum):
            return relu(x, op)
        if isinstance(x, Fuzznum) and isinstance(op, Fuzzarray):
            vec_func = np.vectorize(relu)
            newset = Fuzzarray(x.qrung, x.mtype)
            newset.array = vec_func(x, op.array)
            return newset
        if isinstance(x, Fuzzarray) and isinstance(op, Fuzznum):
            vec_func = np.vectorize(relu)
            newset = Fuzzarray(x.qrung, x.mtype)
            newset.array = vec_func(x.array, op)
            return newset
        if isinstance(x, Fuzzarray) and isinstance(op, Fuzzarray):
            vec_func = np.vectorize(relu)
            newset = Fuzzarray(x.qrung, x.mtype)
            newset.array = vec_func(x.array, op.array)
            return newset
        raise TypeError(f'Unsupported type: {type(x)} or {type(op)}.')


def relu(x, op=None):
    return Relu()(x, op)

