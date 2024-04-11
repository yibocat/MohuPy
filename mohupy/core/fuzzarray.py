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

    def __init__(self, qrung=None):
        super().__init__()
        self.ndim = 0
        self.size = 0
        self.shape = ()

        from .funcitonClass import InitializeSet
        self.qrung, self.mtype = InitializeSet()(qrung)

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
        from .attributeClass import Score
        vec_func = np.vectorize(Score())
        return vec_func(self.__array)

    @property
    def acc(self):
        from .attributeClass import Accuracy
        vec_func = np.vectorize(Accuracy())
        return vec_func(self.__array)

    @property
    def ind(self):
        from .attributeClass import Indeterminacy
        vec_func = np.vectorize(Indeterminacy())
        return vec_func(self.__array)

    @property
    def comp(self) -> 'Fuzzarray':
        from .attributeClass import Complement
        vec_func = np.vectorize(Complement())
        newset = Fuzzarray(self.qrung)
        newset.array = vec_func(self.__array)
        return newset

    @property
    def md(self):
        if self.__array.size != 0:
            def membership(t):
                if isinstance(t.md, (int, float, np.float_, np.int_)):
                    return np.float_(t.md)
                if isinstance(t.md, (np.ndarray, list)):
                    return np.array(t.md, dtype=object)

            vec_func = np.vectorize(membership)
            return vec_func(self.__array)
        return None

    @property
    def nmd(self):
        if self.__array.size != 0:
            def membership(t):
                if isinstance(t.nmd, (int, float, np.float_, np.int_)):
                    return np.float_(t.nmd)
                if isinstance(t.nmd, (np.ndarray, list)):
                    return np.array(t.nmd, dtype=object)

            vec_func = np.vectorize(membership)
            return vec_func(self.__array)
        return None

    @property
    def T(self) -> 'Fuzzarray':
        from .funcitonClass import FuzzTranspose
        return FuzzTranspose()(self)

    def valid(self):
        from .funcitonClass import FuzzValidity
        return FuzzValidity()(self)

    def empty(self, onlyfn=False):
        from .funcitonClass import FuzzEmpty
        return FuzzEmpty(onlyfn)(self)

    def initial(self):
        from .funcitonClass import FuzzInitial
        return FuzzInitial()(self)

    def qsort(self, reverse=False):
        from .funcitonClass import FuzzQsort
        return FuzzQsort(reverse)(self)

    def unique(self, onlyfn=False):
        from .funcitonClass import FuzzUnique
        return FuzzUnique(onlyfn)(self)

    def append(self, e):
        from .funcitonClass import FuzzAppend
        return FuzzAppend(e)(self)

    def reshape(self, *shape):
        from .funcitonClass import FuzzReshape
        return FuzzReshape(*shape)(self)

    def squeeze(self, axis=None):
        from .funcitonClass import FuzzSqueeze
        return FuzzSqueeze(axis)(self)

    def clear(self):
        from .funcitonClass import FuzzClear
        return FuzzClear()(self)

    def ravel(self):
        from .funcitonClass import FuzzRavel
        return FuzzRavel()(self)

    def flatten(self):
        from .funcitonClass import FuzzFlatten
        return FuzzFlatten()(self)

    def max(self, show=False, axis=None):
        from .funcitonClass import FuzzGetMax
        return FuzzGetMax(show, axis)(self)

    def min(self, show=False, axis=None):
        from .funcitonClass import FuzzGetMin
        return FuzzGetMin(show, axis)(self)

    def sum(self, axis=None, keepdims=False):
        from .funcitonClass import FuzzGetSum
        return FuzzGetSum(axis, keepdims)(self)

    def prod(self, axis=None, keepdims=False):
        from .funcitonClass import FuzzGetProd
        return FuzzGetProd(axis, keepdims)(self)

    def mean(self, axis=None):
        from .funcitonClass import FuzzMean
        return FuzzMean(axis)(self)

    def fmax(self, func, *params, show=False, axis=None):
        from .funcitonClass import FuzzGetFmax
        return FuzzGetFmax(show, axis, func, *params)(self)

    def fmin(self, func, *params, show=False, axis=None):
        from .funcitonClass import FuzzGetFmin
        return FuzzGetFmin(show, axis, func, *params)(self)

    def remove(self, e):
        from .funcitonClass import FuzzRemove
        return FuzzRemove(e)(self)

    def pop(self, e):
        from .funcitonClass import FuzzPop
        return FuzzPop(e)(self)
