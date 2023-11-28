#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/11/26 下午3:34
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
from typing import Union

import numpy as np

from .base import mohuset
from .function import initializeSet, transpose


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
    def T(self):
        return transpose(self)


