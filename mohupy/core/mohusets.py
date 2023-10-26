#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/9/30 下午3:49
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
from typing import Union

from .base import MohuBase

from matplotlib import pyplot as plt

import numpy as np
import pandas as pd


class mohuset(MohuBase):

    __array_priority__ = 200

    __qrung = None
    __mtype = None
    __size = 0
    __ndim = 0
    __shape = ()
    __set = np.array([], dtype=object)

    def __init__(self, qrung=None, mtype='qrofn'):
        super().__init__()
        if qrung is not None or mtype is None:
            from .mohu import fuzzType
            assert mtype in fuzzType.keys(), f'Unknown fuzzy type: {mtype}'
            assert qrung > 0, 'qrung must be greater than 0.'
            self.__qrung = qrung
            self.__mtype = mtype
        else:
            pass

    def __repr__(self):
        if self.set is None:
            return 'fuzzTensor(None)'
        p = str(self.set).replace('\n', '\n' + ' ' * 8)
        return f'mohuSet({p}, qrung={self.__qrung}, mtype={self.__mtype})'

    def __str__(self):
        return str(self.__set)

    def __len__(self):
        return len(self.__set)

    def __getitem__(self, key):
        return self.__set[key]

    @property
    def qrung(self):
        return self.__qrung

    @property
    def mtype(self):
        return self.__mtype

    @property
    def size(self):
        return self.__size

    @property
    def ndim(self):
        return self.__ndim

    @property
    def shape(self):
        return self.__shape

    @property
    def set(self):
        return self.__set

    @set.setter
    def set(self, s: np.ndarray):
        if isinstance(np.all(s), MohuBase):
            self.__set = s
            self.__size = s.size
            self.__ndim = s.ndim
            self.__shape = s.shape

            flatten = s.flatten()
            e = np.random.choice(flatten)

            self.__mtype = e.mtype
            self.__qrung = e.qrung
        else:
            raise ValueError("Invalid value.")

    @property
    def md(self):
        def __md(x):
            if isinstance(x.md, Union[int, float, np.float_, np.int_]):
                return np.float_(x.md)
            if isinstance(x.md, Union[np.ndarray, list]):
                return np.array(x.md, dtype=object)

        vec_func = np.vectorize(__md)
        return vec_func(self.__set)

    @property
    def nmd(self):
        def __nmd(x):
            if isinstance(x.nmd, Union[int, float, np.float_, np.int_]):
                return x.nmd
            if isinstance(x.nmd, Union[np.ndarray, list]):
                return np.array(x.md, dtype=object)

        vec_func = np.vectorize(__nmd)
        return vec_func(self.__set)

    @property
    def score(self):
        shape = self.__shape
        scoreset = self.__set.ravel()
        slist = np.asarray([scoreset[i].score for i in range(len(scoreset))])
        self.__set.reshape(shape)
        return slist.reshape(shape)

    @property
    def T(self):
        st = self.__set
        s = st.T

        newset = mohuset(self.__qrung, self.__mtype)
        newset.__set = s
        newset.__shape = s.shape
        newset.__ndim = s.ndim
        newset.__size = s.size
        del st, s
        return newset

    @property
    def mat(self):
        assert 0 <= self.__ndim <= 2, 'ndim must be 0 or 1 or 2.'
        return pd.DataFrame(self.__set)

    # def __add__(self, other):
    #     if isinstance(other, mohuset):
    #         assert other.mtype == self.__mtype, \
    #             'ERROR: The two fuzzy sets must be of the same type.'
    #         assert other.qrung == self.__qrung, \
    #             'ERROR: The two fuzzy sets must be of the same Q-rung.'
    #         assert other.shape == self.__shape, \
    #             'ERROR: The two fuzzy sets must be of the same shape.'
    #         assert other.ndim == self.__ndim, \
    #             'ERROR: The two fuzzy sets must be of the same ndim.'
    #         assert other.size == self.__size, \
    #             'ERROR: The two fuzzy sets must be of the same size.'
    #
    #         newset = mohuset(self.__qrung, self.__mtype)
    #         newset.set = self.__set + other.set
    #         return newset
    #
    #     # from ..runtime import fuzzParent, fuzzType
    #     # if isinstance(other, fuzzParent.get(fuzzType[self.__mtype])):
    #
    #     from .base import mohunum
    #     if isinstance(other, mohunum):
    #         assert other.mtype == self.__mtype, \
    #             'ERROR: The fuzzy number and set must be of the same type.'
    #         assert other.qrung == self.__qrung, \
    #             'ERROR: The fuzzy number and set must be of the same Q-rung.'
    #
    #         newset = mohuset(self.__qrung, self.__mtype)
    #         newset.set = self.__set + other
    #         return newset
    #     raise TypeError(f'Invalid type {type(other)}')
    #
    # def __radd__(self, other):
    #     if isinstance(other, mohuset):
    #         assert other.mtype == self.__mtype, \
    #             'ERROR: The two fuzzy sets must be of the same type.'
    #         assert other.qrung == self.__qrung, \
    #             'ERROR: The two fuzzy sets must be of the same Q-rung.'
    #         assert other.shape == self.__shape, \
    #             'ERROR: The two fuzzy sets must be of the same shape.'
    #         assert other.ndim == self.__ndim, \
    #             'ERROR: The two fuzzy sets must be of the same ndim.'
    #         assert other.size == self.__size, \
    #             'ERROR: The two fuzzy sets must be of the same size.'
    #
    #         newset = mohuset(self.__qrung, self.__mtype)
    #         newset.set = other.set + self.__set
    #         return newset
    #
    #     # from ..runtime import fuzzParent, fuzzType
    #     # if isinstance(other, fuzzParent.get(fuzzType[self.__mtype])):
    #
    #     from .base import mohunum
    #     if isinstance(other, mohunum):
    #         assert other.mtype == self.__mtype, \
    #             'ERROR: The fuzzy number and set must be of the same type.'
    #         assert other.qrung == self.__qrung, \
    #             'ERROR: The fuzzy number and set must be of the same Q-rung.'
    #
    #         newset = mohuset(self.__qrung, self.__mtype)
    #         newset.set = other + self.__set
    #         return newset
    #     raise TypeError(f'Invalid type {type(other)}')
    #
    # def __sub__(self, other):
    #     if isinstance(other, mohuset):
    #         assert other.mtype == self.__mtype, \
    #             'ERROR: The two fuzzy sets must be of the same type.'
    #         assert other.qrung == self.__qrung, \
    #             'ERROR: The two fuzzy sets must be of the same Q-rung.'
    #         assert other.shape == self.__shape, \
    #             'ERROR: The two fuzzy sets must be of the same shape.'
    #         assert other.ndim == self.__ndim, \
    #             'ERROR: The two fuzzy sets must be of the same ndim.'
    #         assert other.size == self.__size, \
    #             'ERROR: The two fuzzy sets must be of the same size.'
    #
    #         newset = mohuset(self.__qrung, self.__mtype)
    #         newset.set = self.__set - other.set
    #         return newset
    #
    #     # from ..runtime import fuzzParent, fuzzType
    #     # if isinstance(other, fuzzParent.get(fuzzType[self.__mtype])):
    #
    #     from .base import mohunum
    #     if isinstance(other, mohunum):
    #         assert other.mtype == self.__mtype, \
    #             'ERROR: The fuzzy number and set must be of the same type.'
    #         assert other.qrung == self.__qrung, \
    #             'ERROR: The fuzzy number and set must be of the same Q-rung.'
    #
    #         newset = mohuset(self.__qrung, self.__mtype)
    #         newset.set = self.__set - other
    #         return newset
    #     raise TypeError(f'Invalid type {type(other)}')
    #
    # def __mul__(self, other):
    #     if isinstance(other, mohuset):
    #         assert other.mtype == self.__mtype, \
    #             'ERROR: The two fuzzy sets must be of the same type.'
    #         assert other.qrung == self.__qrung, \
    #             'ERROR: The two fuzzy sets must be of the same Q-rung.'
    #         assert other.shape == self.__shape, \
    #             'ERROR: The two fuzzy sets must be of the same shape.'
    #         assert other.ndim == self.__ndim, \
    #             'ERROR: The two fuzzy sets must be of the same ndim.'
    #         assert other.size == self.__size, \
    #             'ERROR: The two fuzzy sets must be of the same size.'
    #
    #         newset = mohuset(self.__qrung, self.__mtype)
    #         newset.set = self.__set * other.set
    #         return newset
    #
    #     # from ..runtime import fuzzParent, fuzzType
    #     # if isinstance(other, fuzzParent.get(fuzzType[self.__mtype])):
    #
    #     from .base import mohunum
    #     if isinstance(other, mohunum):
    #         assert other.mtype == self.__mtype, \
    #             'ERROR: The fuzzy number and set must be of the same type.'
    #         assert other.qrung == self.__qrung, \
    #             'ERROR: The fuzzy number and set must be of the same Q-rung.'
    #
    #         newset = mohuset(self.__qrung, self.__mtype)
    #         newset.set = self.__set * other
    #         return newset
    #     if isinstance(other, Union[float, np.float_, int, np.int_]):
    #         assert other > 0, 'The value must be greater than 0.'
    #         newset = mohuset(self.__qrung, self.__mtype)
    #         newset.set = self.__set * other
    #         return newset
    #     if isinstance(other, np.ndarray):
    #         assert np.all(other) > 0, 'The values must be greater than 0.'
    #         newset = mohuset(self.__qrung, self.__mtype)
    #         newset.set = self.__set * other
    #         return newset
    #     raise TypeError(f'Invalid type {type(other)}')
    #
    # def __rmul__(self, other):
    #     if isinstance(other, mohuset):
    #         assert other.mtype == self.__mtype, \
    #             'ERROR: The two fuzzy sets must be of the same type.'
    #         assert other.qrung == self.__qrung, \
    #             'ERROR: The two fuzzy sets must be of the same Q-rung.'
    #         assert other.shape == self.__shape, \
    #             'ERROR: The two fuzzy sets must be of the same shape.'
    #         assert other.ndim == self.__ndim, \
    #             'ERROR: The two fuzzy sets must be of the same ndim.'
    #         assert other.size == self.__size, \
    #             'ERROR: The two fuzzy sets must be of the same size.'
    #
    #         newset = mohuset(self.__qrung, self.__mtype)
    #         newset.set = other.set * self.__set
    #         return newset
    #
    #     # from ..runtime import fuzzParent, fuzzType
    #     # if isinstance(other, fuzzParent.get(fuzzType[self.__mtype])):
    #
    #     from .base import mohunum
    #     if isinstance(other, mohunum):
    #         assert other.mtype == self.__mtype, \
    #             'ERROR: The fuzzy number and set must be of the same type.'
    #         assert other.qrung == self.__qrung, \
    #             'ERROR: The fuzzy number and set must be of the same Q-rung.'
    #
    #         newset = mohuset(self.__qrung, self.__mtype)
    #         newset.set = other * self.__set
    #         return newset
    #     if isinstance(other, Union[float, np.float_, int, np.int_]):
    #         assert other > 0, 'The value must be greater than 0.'
    #         newset = mohuset(self.__qrung, self.__mtype)
    #         newset.set = other * self.__set
    #         return newset
    #     if isinstance(other, np.ndarray):
    #         assert np.all(other) > 0, 'The values must be greater than 0.'
    #         newset = mohuset(self.__qrung, self.__mtype)
    #         newset.set = other * self.__set
    #         return newset
    #     raise TypeError(f'Invalid type {type(other)}')
    #
    # def __truediv__(self, other):
    #     if isinstance(other, mohuset):
    #         assert other.mtype == self.__mtype, \
    #             'ERROR: The two fuzzy sets must be of the same type.'
    #         assert other.qrung == self.__qrung, \
    #             'ERROR: The two fuzzy sets must be of the same Q-rung.'
    #         assert other.shape == self.__shape, \
    #             'ERROR: The two fuzzy sets must be of the same shape.'
    #         assert other.ndim == self.__ndim, \
    #             'ERROR: The two fuzzy sets must be of the same ndim.'
    #         assert other.size == self.__size, \
    #             'ERROR: The two fuzzy sets must be of the same size.'
    #         newset = mohuset(self.__qrung, self.__mtype)
    #         newset.set = self.__set / other.set
    #         return newset
    #
    #     # from ..runtime import fuzzParent, fuzzType
    #     # if isinstance(other, fuzzParent.get(fuzzType[self.__mtype])):
    #
    #     from .base import mohunum
    #     if isinstance(other, mohunum):
    #         assert other.mtype == self.__mtype, \
    #             'ERROR: The fuzzy number and set must be of the same type.'
    #         assert other.qrung == self.__qrung, \
    #             'ERROR: The fuzzy number and set must be of the same Q-rung.'
    #         newset = mohuset(self.__qrung, self.__mtype)
    #         newset.set = self.__set / other
    #         return newset
    #     if isinstance(other, Union[float, np.float_, int, np.int_]):
    #         assert other > 1, 'The value must be greater than 1.'
    #         newset = mohuset(self.__qrung, self.__mtype)
    #         newset.set = self.__set / other
    #         return newset
    #     if isinstance(other, np.ndarray):
    #         assert np.all(other) > 1, 'The values must be greater than 1.'
    #         newset = mohuset(self.__qrung, self.__mtype)
    #         newset.set = self.__set / other
    #         return newset
    #     raise TypeError(f'Invalid type {type(other)}')
    #
    # def __pow__(self, power, modulo=None):
    #     if isinstance(power, Union[float, np.float_, int, np.int_]):
    #         assert power > 0, 'The value must be greater than 0.'
    #         newset = mohuset(self.__qrung, self.__mtype)
    #         newset.set = self.__set ** power
    #         return newset
    #     if isinstance(power, np.ndarray):
    #         assert np.all(power) > 0, 'The values must be greater than 0.'
    #         newset = mohuset(self.__qrung, self.__mtype)
    #         newset.set = self.__set ** power
    #         return newset
    #     raise TypeError(f'Invalid type {type(power)}')
    #
    # def __matmul__(self, other):
    #     assert isinstance(other, mohuset), \
    #         'ERROR: The fuzzy set must be a fuzzy set.'
    #     assert self.__ndim == other.__ndim == 2, \
    #         'ERROR: The matrix ndim must be 2.'
    #     assert self.__shape[1] == other.__shape[0], \
    #         'ERROR: Incompatible shapes for matrix multiplication.'
    #     assert self.__qrung == other.__qrung, \
    #         'ERROR: The Q-rung of the two fuzzy sets must match.'
    #     assert self.__mtype == other.__mtype, \
    #         'ERROR: The two fuzzy sets must be of the same type.'
    #     newset = mohuset(self.__qrung, self.__mtype)
    #     newset.set = self.__set @ other.set
    #     return newset
    #
    # def __eq__(self, other) -> np.ndarray:
    #     if isinstance(other, mohuset):
    #         return self.__set == other.__set
    #
    #     # from ..runtime import fuzzParent, fuzzType
    #     # if isinstance(other, fuzzParent.get(fuzzType[self.__mtype])):
    #
    #     from .base import mohunum
    #     if isinstance(other, mohunum):
    #         return self.__set == other
    #     raise TypeError(f'Invalid type {type(other)}')
    #
    # def __ne__(self, other) -> np.ndarray:
    #     if isinstance(other, mohuset):
    #         return self.__set != other.__set
    #
    #     # from ..runtime import fuzzParent, fuzzType
    #     # if isinstance(other, fuzzParent.get(fuzzType[self.__mtype])):
    #
    #     from .base import mohunum
    #     if isinstance(other, mohunum):
    #         return self.__set != other
    #     raise TypeError(f'Invalid type {type(other)}')
    #
    # def __lt__(self, other) -> np.ndarray:
    #     if isinstance(other, mohuset):
    #         return self.__set < other.__set
    #
    #     # from ..runtime import fuzzParent, fuzzType
    #     # if isinstance(other, fuzzParent.get(fuzzType[self.__mtype])):
    #
    #     from .base import mohunum
    #     if isinstance(other, mohunum):
    #         return self.__set < other
    #     raise TypeError(f'Invalid type {type(other)}')
    #
    # def __gt__(self, other) -> np.ndarray:
    #     if isinstance(other, mohuset):
    #         return self.__set > other.__set
    #
    #     # from ..runtime import fuzzParent, fuzzType
    #     # if isinstance(other, fuzzParent.get(fuzzType[self.__mtype])):
    #
    #     from .base import mohunum
    #     if isinstance(other, mohunum):
    #         return self.__set > other
    #     raise TypeError(f'Invalid type {type(other)}')
    #
    # def __le__(self, other) -> np.ndarray:
    #     if isinstance(other, mohuset):
    #         return self.__set <= other.__set
    #
    #     # from ..runtime import fuzzParent, fuzzType
    #     # if isinstance(other, fuzzParent.get(fuzzType[self.__mtype])):
    #
    #     from .base import mohunum
    #     if isinstance(other, mohunum):
    #         return self.__set <= other
    #     raise TypeError(f'Invalid type {type(other)}')
    #
    # def __ge__(self, other) -> np.ndarray:
    #     if isinstance(other, mohuset):
    #         return self.__set >= other.__set
    #
    #     # from ..runtime import fuzzParent, fuzzType
    #     # if isinstance(other, fuzzParent.get(fuzzType[self.__mtype])):
    #
    #     from .base import mohunum
    #     if isinstance(other, mohunum):
    #         return self.__set >= other
    #     raise TypeError(f'Invalid type {type(other)}')

    def append(self, x):
        if self.__mtype is not None and self.__qrung is not None:
            assert x.qrung == self.__qrung, \
                'qrung mismatch.'
            assert x.mtype == self.__mtype, \
                'mtype mismatch.'
            self.__set = np.append(self.__set, x)
            self.__size += 1
            self.__shape = self.__set.shape
            self.__ndim = self.__set.ndim
        else:
            self.__qrung = x.qrung
            self.__mtype = x.mtype
            self.__set = np.append(self.__set, x)
            self.__size += 1
            self.__shape = self.__set.shape
            self.__ndim = self.__set.ndim

    def remove(self, x):
        assert self.__size > 0, 'The set is empty, can not be removed.'
        assert x in self.__set, f'{x} is not in the set.'
        self.__set = np.delete(self.__set, np.where(self.__set == x))
        self.__size -= 1
        self.__shape = self.__set.shape
        self.__ndim = self.__set.ndim

    def pop(self, i):
        self.__set = np.delete(self.__set, i)
        self.__size -= 1
        self.__shape = self.__set.shape
        self.__ndim = self.__set.ndim

    def reshape(self, *shape):
        self.__set = self.__set.reshape(*shape)
        self.__shape = self.__set.shape
        self.__ndim = self.__set.ndim

    def clear(self):
        self.__set = np.array([], dtype=object)
        self.__size = 0
        self.__mtype = None
        self.__qrung = None
        self.__shape = ()
        self.__ndim = 0

    def ravel(self):
        self.__set = self.__set.ravel()
        self.__shape = self.__set.shape
        self.__ndim = self.__set.ndim
        return self

    def is_valid(self):
        fs = lambda x: x.is_valid()
        vec_func = np.vectorize(fs)
        return vec_func(self.__set)

    def isEmpty(self):
        fs = lambda x: x.isEmpty()
        vec_func = np.vectorize(fs)
        return vec_func(self.__set)

    def max(self, show=True, axis=None):
        if axis is None:
            index = np.unravel_index(np.argmax(self.__set), self.__shape)
            if show:
                print(index)
            return self.__set[index]
        else:
            from ..utils import asfuzzset
            return asfuzzset(np.max(self.__set, axis=axis))

    def min(self, show=True, axis=None):
        if axis is None:
            index = np.unravel_index(np.argmin(self.__set), self.__shape)
            if show:
                print(index)
            return self.__set[index]
        else:
            from ..utils import asfuzzset
            return asfuzzset(np.min(self.__set, axis=axis))

    def fmax(self, func, *args, show=True):
        slist = func(self.__set, *args)
        index = np.unravel_index(np.argmax(slist), self.__shape)
        if show:
            print(index)
        return self.__set[index]

    def fmin(self, func, *args, show=True):
        slist = func(self.__set, *args)
        index = np.unravel_index(np.argmin(slist), self.__shape)
        if show:
            print(index)
        return self.__set[index]

    def sum(self, axis=None):
        return np.sum(self.__set, axis=axis)

    def mean(self, axis=None):
        return np.mean(self.__set, axis=axis)

    def savez(self, path):
        np.savez_compressed(
            path,
            set=self.__set,
            mtype=self.__mtype,
            qrung=self.__qrung,
            shape=self.__shape,
            size=self.__size,
            ndim=self.__ndim
        )

    def loadz(self, path):
        mset = np.load(path, allow_pickle=True)
        self.__set = mset['set']
        self.__mtype = mset['mtype']
        self.__qrung = mset['qrung']
        self.__shape = tuple(mset['shape'])
        self.__size = mset['size']
        self.__ndim = mset['ndim']
