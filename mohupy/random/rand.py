#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/10/16 下午8:22
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from .base import Random

import numpy as np


class RandNum(Random):

    def __init__(self, minnum, maxnum):
        self.minnum = minnum
        self.maxnum = maxnum

    def function(self, q, mtype):
        """
            randomly generate a fuzzy number

            Parameters
            ----------
                q : int
                    The q-rung
                mtype : str
                    The type of fuzzy number to be generated
                num : int
                    Maximum number of membership and non-membership degrees
                    of q-rung orthopair hesitant fuzzy number

            Returns
            -------
                mohunum
        """
        from ..regedit.random import fuzzRandom
        return fuzzRandom[mtype](q, self.minnum, self.maxnum)


def randnum(q: int, mtype: str, minnum=1, maxnum=5):
    return RandNum(minnum, maxnum)(q, mtype)


class RandSet(Random):

    def __init__(self, minnum, maxnum):
        self.minnum = minnum
        self.maxnum = maxnum

    def function(self, q, mtype, *n):
        """
            Randomly generate a fuzzy set

            Parameters
            ----------
                q : int
                    The q-rung
                mtype : str
                    The type of fuzzy number to be generated
                num : int
                    Maximum number of membership and non-membership degrees
                    of q-rung orthopair hesitant fuzzy number

            Returns
            -------
                Fuzzarray
        """
        from ..core import Fuzznum

        def __rand(f: Fuzznum):
            return randnum(f.qrung, f.mtype, self.minnum, self.maxnum)

        from ..lib.construct import zeros
        newset = zeros(q, mtype, *n)
        vec_func = np.vectorize(__rand)
        result = vec_func(newset.array)
        newset.array = result
        return newset


def randset(q: int, mtype: str, *n, minnum=1, maxnum=5):
    return RandSet(minnum, maxnum)(q, mtype, *n)


class Rand(Random):

    def __init__(self, minnum, maxnum):
        self.minnum = minnum
        self.maxnum = maxnum

    def function(self, q, mtype, *n):
        """
            random fuzzy function

            Parameters
            ----------
                q : int
                    The q-rung
                mtype : str
                    The type of fuzzy number to be generated
                n : int
                    The number of fuzzy numbers to be generated

            Returns
            -------
                Fuzzarray or Fuzznum
        """
        if len(n) == 0:
            return randnum(q, mtype, minnum=self.minnum, maxnum=self.maxnum)
        else:
            return randset(q, mtype, *n, minnum=self.minnum, maxnum=self.maxnum)


def rand(q: int, mtype: str, *n, minnum=1, maxnum=5):
    return Rand(minnum, maxnum)(q, mtype, *n)


class Choice(Random):
    def function(self, f, n, replace):
        """
            Randomly select a fuzzy number

            Parameters
            ----------
                f:  Fuzzarray
                    The fuzzy set.
                n:  Randomly extract shapes
                replace:

            Returns
            -------
                Fuzznum or Fuzzarray
                :param replace:
        """

        if n is not None:
            from ..core import Fuzzarray
            if replace:
                t = np.random.choice(f.array, size=n, replace=replace)
                f.array = t
                return f
            else:
                newset = Fuzzarray(f.qrung, f.mtype)
                newset.array = np.random.choice(f.array, size=n, replace=replace)
                return newset
        else:
            return np.random.choice(f.array.flatten())


def choice(f, size: (int, tuple[int], list[int]) = None, replace=False):
    return Choice()(f, size, replace)


def seed(x):
    np.random.seed(x)
