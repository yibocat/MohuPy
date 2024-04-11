#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/7 下午1:57
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import warnings

import numpy as np
import pandas as pd

from ...core import Fuzznum, Fuzzarray
from .base import Library


class Savez(Library):
    """
        Save data to npz file
    """
    def __init__(self, x: Fuzzarray):
        self.fuzz = x

    def function(self, path):
        if isinstance(self.fuzz, Fuzznum):
            raise IOError(f'Invalid save for {type(self.fuzz)}.')
        if isinstance(self.fuzz, Fuzzarray):
            try:
                np.savez_compressed(
                    path,
                    array=self.fuzz.array,
                    mtype=self.fuzz.mtype,
                    qrung=self.fuzz.qrung)
            except IOError as e:
                print(f'Save failed.' + str(e))


class Loadz(Library):
    """
        Load data from npz file
    """
    def function(self, path):
        newset = Fuzzarray()
        new = np.load(path, allow_pickle=True)
        from ...config import Config, set_mtype
        mtype = str(new['mtype'])
        if Config.mtype != new['mtype']:
            warnings.warn(f'The fuzzy number type changed: ({Config.mtype} -> {mtype})', Warning)
        set_mtype(mtype)
        newset.qrung = int(new['qrung'])
        newset.mtype = str(new['mtype'])
        newset.array = new['array']
        return newset

        # if isinstance(self.fuzz, Fuzznum):
        #     raise IOError(f'Invalid load for {type(self.fuzz)}.')
        # if isinstance(self.fuzz, Fuzzarray):
        #     if self.fuzz.initial():
        #         new = np.load(path, allow_pickle=True)
        #         from ...config import Config, set_mtype
        #         mtype = new['mtype']
        #         if Config.mtype != new['mtype']:
        #             warnings.warn(f'The fuzzy number type changed: ({Config.mtype} -> {mtype})', Warning)
        #         set_mtype(self.fuzz.mtype)
        #
        #         self.fuzz.qrung = new['qrung']
        #         self.fuzz.mtype = new['mtype']
        #         self.fuzz.array = new['array']
        #     else:
        #         warnings.warn('Loading existing data will overwrite the original data!', Warning)
        #         self.fuzz = self.fuzz.clear()
        #         new = np.load(path, allow_pickle=True)
        #
        #         from ...config import Config, set_mtype
        #         mtype = new['mtype']
        #         if Config.mtype != new['mtype']:
        #             warnings.warn(f'The fuzzy number type changed: ({Config.mtype} -> {mtype})', Warning)
        #         set_mtype(self.fuzz.mtype)
        #
        #         self.fuzz.qrung = new['qrung']
        #         self.fuzz.mtype = new['mtype']
        #         self.fuzz.array = new['array']
        # raise IOError(f'Invalid load for {type(self.fuzz)}.')


class ToCSV(Library):
    """
        Save a fuzzy set to a .csv file.

        This method only saves the fuzzy set, and does not save the related
        information of the set.

        Returns
        -------
            Boolean

        Notes
        -----
            This method saves the fuzzy set to a.csv file.
    """
    def __init__(self, fuzz: Fuzzarray, header, index_col):
        self.fuzz = fuzz
        self.header = header
        self.index_col = index_col

    def function(self, path: str):
        if 0 <= self.fuzz.ndim <= 2:
            try:
                if isinstance(self.fuzz.array, Fuzzarray):
                    pd.DataFrame(self.fuzz.array, columns=self.header, index=self.index_col).to_csv(path)
                else:
                    pd.DataFrame(np.array(self.fuzz), columns=self.header, index=self.index_col).to_csv(path)
            except Exception as e:
                raise IOError(f'{e}: Save failed.')
        else:
            raise ValueError(f'The ndim of fuzzy array is invalid: ndim={self.fuzz.ndim}')


class LoadCSV(Library):
    """
        Load a fuzzy set from a.csv file.

        This method is used to load a fuzzy set table with unknown information. It
        is necessary to judge the content of the fuzzy table during loading. When
        initializing a fuzzy set, Q-rung and fuzzy set type are given, so it is necessary
        to judge whether a fuzzy set meets these two conditions. This method will only
        load when the fuzzy set table is equal to or satisfied with the initial fuzzy set
        condition.


        Returns
        -------
            Fuzzarray
                The fuzzy set.

        Notes
        -----
            This method loads the fuzzy set from a.csv file.
    """
    def __init__(self, qrung, header, index_col):
        self.qrung = qrung
        self.header = header
        self.index_col = index_col

    def function(self, path: str):
        try:
            m = pd.read_csv(path, header=self.header, index_col=self.index_col).to_numpy()
            from .classString import StrToFuzz
            vec_func = np.vectorize(lambda x: StrToFuzz(self.qrung)(x))
            newset = Fuzzarray(self.qrung)
            try:
                newset.array = vec_func(m)
                return newset
            except Exception as e:
                Exception(f'Please check if the mtype type matches. error:{e}')
        except Exception as e:
            print(f'{e}: Load failed.')
