#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/11/26 下午3:34
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import numpy as np

from .base import mohuset
from .function import initializeSet, transpose
from .attributes import score, acc, ind, comp

from .function import (isValid, isEmpty, isInitial, qsort, unique,
                       append, remove, pop, reshape, squeeze, clear,
                       ravel, flatten, getmax, getmin, getsum, getprod, mean,
                       fmax, fmin)


class Fuzzarray(mohuset):
    __array_priority__ = 200
    __array = np.array([], dtype=object)

    def __init__(self, qrung=None, mtype=None):
        super().__init__()
        self.ndim = 0
        self.size = 0
        self.shape = ()
        self.qrung, self.mtype = initializeSet(qrung, mtype)

        self.init()

    def __len__(self):
        return len(self.array)

    def init(self):
        pass

    @property
    def array(self):
        return self.__array

    @array.setter
    def array(self, value: np.ndarray):
        from .nums import Fuzznum
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
        vec_func = np.vectorize(score)
        return vec_func(self.__array)

    @property
    def acc(self):
        vec_func = np.vectorize(acc)
        return vec_func(self.__array)

    @property
    def ind(self):
        vec_func = np.vectorize(ind)
        return vec_func(self.__array)

    @property
    def comp(self):
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
        return vec_func(self.array)

    @property
    def nmd(self):
        def membership(t):
            if isinstance(t.nmd, (int, float, np.float_, np.int_)):
                return np.float_(t.nmd)
            if isinstance(t.nmd, (np.ndarray, list)):
                return np.array(t.nmd, dtype=object)

        vec_func = np.vectorize(membership)
        return vec_func(self.array)

    @property
    def T(self):
        return transpose(self)

    def isValid(self): return isValid(self)

    def isEmpty(self, onlyfn=False): return isEmpty(self, onlyfn)

    def isInitial(self): return isInitial(self)

    def qsort(self, reverse=False): return qsort(self, reverse)

    def unique(self, onlyfn=False): return unique(self, onlyfn)

    def append(self, e): return append(self, e)

    def reshape(self, *shape): return reshape(self, *shape)

    def squeeze(self, axis=None): return squeeze(self, axis)

    def clear(self): return clear(self)

    def ravel(self): return ravel(self)

    def flatten(self): return flatten(self)

    def max(self, show=False, axis=None): return getmax(self, show, axis)

    def min(self, show=False, axis=None): return getmin(self, show, axis)

    def sum(self, axis=None, keepdims=False): return getsum(self, axis, keepdims)

    def prod(self, axis=None, keepdims=False): return getprod(self, axis, keepdims)

    def mean(self, axis=None): return mean(self, axis)

    def fmax(self, func, *args, show=False, axis=None): return fmax(self, func, *args, show, axis)

    def fmin(self, func, *args, show=False, axis=None): return fmin(self, func, *args, show, axis)

    def remove(self, e): return remove(self, e)

    def pop(self, e): return pop(self, e)


