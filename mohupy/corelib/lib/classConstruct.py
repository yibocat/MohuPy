#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/7 下午1:57
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import numpy as np

from ...core import Fuzznum, Fuzzarray
from ..regedit import fuzzZeros, fuzzPoss, fuzzNegs, fuzzZero, fuzzPos, fuzzNeg
from .base import Library


class Zeros(Library):
    def function(self, q, mtype, *n):
        """
        Generate an *n all-zero fuzzy set

        Parameters
        ----------
            q : int
                    The qrung of the fuzzy set
            mtype : str
                    The type of the fuzzy set
            n : int
                    The shape of the fuzzy set
        Returns
        -------
            newset : mohuset
        """
        if len(n) != 0:
            return fuzzZeros[mtype](q, *n)
        else:
            return fuzzZero[mtype](q)


class Poss(Library):
    def function(self, q, mtype, *n):
        """
        Generate an *n all-positive fuzzy set

        Parameters
        ----------
            q : int
                    The qrung of the fuzzy set
            mtype : str
                    The type of the fuzzy set
            n : int
                    The shape of the fuzzy set
        Returns
        -------
            newset : mohuset
        """
        if len(n) != 0:
            return fuzzPoss[mtype](q, *n)
        else:
            return fuzzPos[mtype](q)


class Negs(Library):
    def function(self, q, mtype, *n):
        """
        Generate an *n all-negative fuzzy set

        Parameters
        ----------
            q : int
                    The qrung of the fuzzy set
            mtype : str
                    The type of the fuzzy set
            n : int
                    The shape of the fuzzy set
        Returns
        -------
            newset : mohuset
        """
        if len(n) != 0:
            return fuzzNegs[mtype](q, *n)
        else:
            return fuzzNeg[mtype](q)


class Full(Library):
    def function(self, x: Fuzznum, *n):
        """
        Generate an *n any fuzzy number fuzzy set

        Parameters
        ----------
            x: mohunum
                    The fuzzy number
            n : int
                    The shape of the fuzzy set
        Returns
        -------
            newset : mohuset
        """
        s = np.full(n, x, dtype=object)
        newset = Fuzzarray(x.qrung, x.mtype)
        newset.array = s
        return newset


class ZerosLike(Library):
    """
        Constructing full zeros fuzzy arrays of the same shape
    """
    def function(self, f: Fuzzarray):
        from .construct import zeros
        return zeros(f.qrung, f.mtype, *f.shape)


class PossLike(Library):
    """
        Constructing full zeros fuzzy arrays of the same shape
    """
    def function(self, f: Fuzzarray):
        from .construct import poss
        return poss(f.qrung, f.mtype, *f.shape)


class NegsLike(Library):
    """
        Constructing full zeros fuzzy arrays of the same shape
    """
    def function(self, f: Fuzzarray):
        from .construct import negs
        return negs(f.qrung, f.mtype, *f.shape)


class FullLike(Library):
    """
        Constructing full zeros fuzzy arrays of the same shape
    """
    def function(self, f: Fuzzarray, x: Fuzznum):
        from .construct import full
        return full(x, *f.shape)


