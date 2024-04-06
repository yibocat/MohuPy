#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/6 下午12:48
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import numpy as np

from .base import MohuBase


class Fuzzarray(MohuBase):
    __array_priority__ = 200
    __array = np.array([], dtype=object)

    def __init__(self, qrung=None, mtype=None):
        super().__init__()
        self.ndim = 0
        self.size = 0
        self.shape = ()
        from .function import initializeSet
        self.qrung, self.mtype = initializeSet(qrung, mtype)

    def __len__(self):
        return len(self.__array)

    @property
    def array(self):
        return self.__array

    @array.setter
    def array(self, value: np.ndarray):
        from .fuzznums import Fuzznum
        if isinstance(np.all(value), Fuzznum):
            try:
                self.__array = value
                self.ndim = value.ndim
                self.size = value.size
                self.shape = value.shape

                flatten = value.flatten()
                e = np.random.choice(flatten)

                self.qrung = e.qrung
                self.mtype = e.mtype
            except ValueError as e:
                raise ValueError(f'Setup failed: {e}')
        elif value.size == 0:
            self.__array = np.array([], dtype=object)
            self.ndim = value.ndim
            self.size = value.size
            self.shape = value.shape
        else:
            raise TypeError(f"Invalid fuzzy type.")

    @property
    def score(self):
        from .attribute import score
        vec_func = np.vectorize(score)
        return vec_func(self.__array)

    @property
    def acc(self):
        from .attribute import acc
        vec_func = np.vectorize(acc)
        return vec_func(self.__array)

    @property
    def ind(self):
        from .attribute import ind
        vec_func = np.vectorize(ind)
        return vec_func(self.__array)

    @property
    def comp(self) -> 'Fuzzarray':
        from .attribute import comp
        vec_func = np.vectorize(comp)
        newset = Fuzzarray(self.qrung, self.mtype)
        newset.array = vec_func(self.__array)
        return newset

    @property
    def md(self):
        def membership(t):
            if isinstance(t.md, (int, float, np.float_, np.int_)):
                return np.float_(t.md)
            if isinstance(t.md, (np.ndarray, list)):
                return np.array(t.md, dtype=object)

        vec_func = np.vectorize(membership)
        return vec_func(self.__array)

    @property
    def nmd(self):
        def membership(t):
            if isinstance(t.nmd, (int, float, np.float_, np.int_)):
                return np.float_(t.nmd)
            if isinstance(t.nmd, (np.ndarray, list)):
                return np.array(t.nmd, dtype=object)

        vec_func = np.vectorize(membership)
        return vec_func(self.__array)

    @property
    def T(self) -> 'Fuzzarray':
        from .function import transpose
        return transpose(self)

    def valid(self):
        from .function import valid
        return valid(self)

    def empty(self, onlyfn=False):
        from .function import empty
        return empty(self, onlyfn)

    def initial(self):
        from .function import initial
        return initial(self)

    def qsort(self, reverse=False):
        from .function import qsort
        return qsort(self, reverse)

    def unique(self, onlyfn=False):
        from .function import unique
        return unique(self, onlyfn)

    def append(self, e):
        from .function import append
        return append(self, e)

    def reshape(self, *shape):
        from .function import reshape
        return reshape(self, *shape)

    def squeeze(self, axis=None):
        from .function import squeeze
        return squeeze(self, axis)

    def clear(self):
        from .function import clear
        return clear(self)

    def ravel(self):
        from .function import ravel
        return ravel(self)

    def flatten(self):
        from .function import flatten
        return flatten(self)

    def max(self, show=False, axis=None):
        from .function import getmax
        return getmax(self, show, axis)

    def min(self, show=False, axis=None):
        from .function import getmin
        return getmin(self, show, axis)

    def sum(self, axis=None, keepdims=False):
        from .function import getsum
        return getsum(self, axis, keepdims)

    def prod(self, axis=None, keepdims=False):
        from .function import getprod
        return getprod(self, axis, keepdims)

    def mean(self, axis=None):
        from .function import mean
        return mean(self, axis)

    def fmax(self, func, *args, show=False, axis=None):
        from .function import fmax
        return fmax(self, func, *args, show, axis)

    def fmin(self, func, *args, show=False, axis=None):
        from .function import fmin
        return fmin(self, func, *args, show, axis)

    def remove(self, e):
        from .function import remove
        return remove(self, e)

    def pop(self, e):
        from .function import pop
        return pop(self, e)

