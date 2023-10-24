#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/10/1 下午3:33
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

# from ..core.fuzznum import fuzznum
from ..core.mohusets import mohuset
from ..core.base import mohunum

import numpy as np

# def zeros(q, mtype, *n):
#     """
#          Generate an *n all-zero fuzzy set
#
#         Parameters
#         ----------
#             q : int
#                     The qrung of the fuzzy set
#             mtype : str
#                     The type of the fuzzy set
#             n : int
#                     The shape of the fuzzy set
#         Returns
#         -------
#             newset : mohuset
#     """
#     if mtype == 'qrofn':
#         s = np.full(n, fuzznum(q, 0., 0.), dtype=object)
#     elif mtype == 'ivfn':
#         s = np.full(n, fuzznum(q, [0., 0.], [0., 0.]), dtype=object)
#     else:
#         raise TypeError(f'Unknown mtype: {mtype}')
#     newset = mohuset(q, mtype)
#     newset.set = s
#     return newset
#
#
# def poss(q, mtype, *n):
#     """
#         Generate an *n all-positive fuzzy set
#
#         Parameters
#         ----------
#             q : int
#                     The qrung of the fuzzy set
#             mtype : str
#                     The type of the fuzzy set
#             n : int
#                     The shape of the fuzzy set
#         Returns
#         -------
#             newset : mohuset
#     """
#     if mtype == 'qrofn':
#         s = np.full(n, fuzznum(q, 1., 0.), dtype=object)
#     elif mtype == 'ivfn':
#         s = np.full(n, fuzznum(q, [1., 1.], [0., 0.]), dtype=object)
#     else:
#         raise TypeError(f'Unknown mtype: {mtype}')
#     newset = mohuset(q, mtype)
#     newset.set = s
#     return newset
#
#
# def negs(q, mtype, *n):
#     """
#         Generate an *n all-negative fuzzy set
#
#         Parameters
#         ----------
#             q : int
#                     The qrung of the fuzzy set
#             mtype : str
#                     The type of the fuzzy set
#             n : int
#                     The shape of the fuzzy set
#         Returns
#         -------
#             newset : mohuset
#     """
#     if mtype == 'qrofn':
#         s = np.full(n, fuzznum(q, 0., 1.), dtype=object)
#     elif mtype == 'ivfn':
#         s = np.full(n, fuzznum(q, [0., 0.], [1., 1.]), dtype=object)
#     else:
#         raise TypeError(f'Unknown mtype: {mtype}')
#     newset = mohuset(q, mtype)
#     newset.set = s
#     return newset
#

from ..registry.construct import fuzzZeros, fuzzPoss, fuzzNegs
from .constant import fuzzZero, fuzzPos, fuzzNeg


def zeros(q, mtype, *n):
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


def poss(q, mtype, *n):
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


def negs(q, mtype, *n):
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
    if len(n)!= 0:
        return fuzzNegs[mtype](q, *n)
    else:
        return fuzzNeg[mtype](q)


def full(x: mohunum, *n):
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
    newset = mohuset(x.qrung, x.mtype)
    newset.set = s
    return newset
