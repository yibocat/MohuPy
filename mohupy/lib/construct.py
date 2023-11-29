#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/11/28 下午4:25
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import numpy as np

from ..core import Fuzznum, Fuzzarray
from ..regedit.construct import fuzzZeros, fuzzPoss, fuzzNegs, fuzzZero, fuzzPos, fuzzNeg
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


def zeros(q, mtype, *n):
    return Zeros()(q, mtype, *n)


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


def poss(q, mtype, *n):
    return Poss()(q, mtype, *n)


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


def negs(q, mtype, *n):
    return Negs()(q, mtype, *n)


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


def full(x: Fuzznum, *n):
    return Full()(x, *n)


class ZerosLike(Library):
    """
        Constructing full zeros fuzzy arrays of the same shape
    """
    def function(self, f: Fuzzarray):
        return zeros(f.qrung, f.mtype, *f.shape)


def zeros_like(f: Fuzzarray):
    return ZerosLike()(f)


class PossLike(Library):
    """
        Constructing full zeros fuzzy arrays of the same shape
    """
    def function(self, f: Fuzzarray):
        return poss(f.qrung, f.mtype, *f.shape)


def poss_like(f: Fuzzarray):
    return PossLike()(f)


class NegsLike(Library):
    """
        Constructing full zeros fuzzy arrays of the same shape
    """
    def function(self, f: Fuzzarray):
        return negs(f.qrung, f.mtype, *f.shape)


def negs_like(f: Fuzzarray):
    return NegsLike()(f)


class FullLike(Library):
    """
        Constructing full zeros fuzzy arrays of the same shape
    """
    def function(self, f: Fuzzarray, x: Fuzznum):
        return full(x, *f.shape)


def full_like(f: Fuzzarray):
    return FullLike()(f)
