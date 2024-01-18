#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/11/28 下午6:36
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import warnings

import numpy as np
import pandas as pd

from ..core.nums import Fuzznum
from ..core.array import Fuzzarray

from .base import Library


class Savez(Library):
    """
        Save data to npz file
    """

    def function(self, x, path):
        # from ..base.nums import Fuzznum
        # from ..base.array import Fuzzarray
        if isinstance(x, Fuzznum):
            raise IOError(f'Invalid save for {type(x)}.')
        if isinstance(x, Fuzzarray):
            try:
                np.savez_compressed(
                    path,
                    array=x.array,
                    mtype=x.mtype,
                    qrung=x.qrung)
            except IOError as e:
                print(f'Save failed.' + str(e))


def savez(x, path):
    return Savez()(x, path)


class Loadz(Library):
    """
        Load data from npz file
    """

    def function(self, x, path):
        # from ..base.nums import Fuzznum
        # from ..base.array import Fuzzarray
        if isinstance(x, Fuzznum):
            raise IOError(f'Invalid load for {type(x)}.')
        if isinstance(x, Fuzzarray):
            if x.isInitial():
                new = np.load(path, allow_pickle=True)
                x.qrung = new['qrung']
                x.mtype = new['mtype']
                x.array = new['array']
                return True
            else:
                warnings.warn('Loading existing data will overwrite the original data!', Warning)
                x = x.clear()
                new = np.load(path, allow_pickle=True)
                x.qrung = new['qrung']
                x.mtype = new['mtype']
                x.array = new['array']
                return True
        return False


def loadz(x, path):
    return Loadz()(x, path)


class ToCSV(Library):
    """
        Save a fuzzy set to a .csv file.

        This method only saves the fuzzy set, and does not save the related
        information of the set.

        Parameters
        ----------
            f:  Fuzzarray
                The fuzzy set.
            path:  str
                The path to the file.

        Returns
        -------
            Boolean

        Notes
        -----
            This method saves the fuzzy set to a.csv file.
    """

    def function(self, f: Fuzzarray, path: str):
        if 0 <= f.ndim <= 2:
            try:
                pd.DataFrame(f.array).to_csv(path)
                return True
            except Exception as e:
                print(f'{e}: Save failed.')
                return False
        else:
            raise ValueError(f'The ndim of fuzzy array is invalid: ndim={f.ndim}')


def to_csv(x, path):
    return ToCSV()(x, path)


class LoadCSV(Library):
    """
        Load a fuzzy set from a.csv file.

        This method is used to load a fuzzy set table with unknown information. It
        is necessary to judge the content of the fuzzy table during loading. When
        initializing a fuzzy set, Q-rung and fuzzy set type are given, so it is necessary
        to judge whether a fuzzy set meets these two conditions. This method will only
        load when the fuzzy set table is equal to or satisfied with the initial fuzzy set
        condition.

        Parameters
        ----------
            path:  str
                The path to the file.
            q:  int
                The q rung of the fuzzy set.
            mtype:  str
                The type of the fuzzy set.

        Returns
        -------
            Fuzzarray
                The fuzzy set.

        Notes
        -----
            This method loads the fuzzy set from a.csv file.
    """
    def __init__(self, header, index_col):
        self.header = header
        self.index_col = index_col

    def function(self, path: str, q: int, mtype: str):
        try:
            m = pd.read_csv(path, header=self.header, index_col=self.index_col).to_numpy()
            from .string import str2fuzz
            vec_func = np.vectorize(str2fuzz)
            f = vec_func(m, q, mtype)

            newset = Fuzzarray(q, mtype)
            newset.array = f
            return newset
        except Exception as e:
            print(f'{e}: Load failed.')


def load_csv(path: str, q: int, mtype: str, header='infer', index_col=0):
    return LoadCSV(header, index_col)(path, q, mtype)

