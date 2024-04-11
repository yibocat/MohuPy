#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/11 下午7:50
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import numpy as np

from ...tensor import Fuzztensor
from ...core import Fuzznum, Fuzzarray

from .base import Library


class TensorSavez(Library):
    """
    Save a Fuzztensor to the npz file
    """
    def __init__(self, x: Fuzztensor):
        self.fuzz = x.data

    def function(self, path):
        from ...corelib.lib.classIO import Savez
        Savez(self.fuzz)(path)


class TensorLoadz(Library):
    """
        Load a Fuzztensor from the npz file
    """
    def function(self, path):
        from ...corelib.lib.classIO import Loadz
        from ...config import Config
        newset = Loadz()(path)
        if newset.mtype != Config.mtype:
            raise TypeError(f'Fuzzy type error, load fuzzy data type {newset.mtype} is not matched with {Config.mtype}.')
        newFTensor = Fuzztensor(newset)
        return newFTensor


class TensorToCSV(Library):
    def __init__(self, fuzz: Fuzztensor, header=None, index_col=None):
        from ...tensor.utils import as_fuzzarray
        self.fuzz = fuzz.data
        self.header = header
        self.index_col = index_col

    def function(self, path: str):
        from ...corelib.lib.classIO import ToCSV
        ToCSV(self.fuzz, self.header, self.index_col)(path)


class TensorLoadCSV(Library):
    def __init__(self, qrung, header='infer', index_col=0):
        self.qrung = qrung
        self.header = header
        self.index_col = index_col

    def function(self, path):
        from ...corelib.lib.classIO import LoadCSV
        newset = LoadCSV(self.qrung, self.header, self.index_col)(path)
        from ...config import Config
        if newset.mtype != Config.mtype:
            raise ValueError(f'The mtype {newset.mtype} is not matched with {Config.mtype}')
        return Fuzztensor(newset)
