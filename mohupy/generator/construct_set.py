#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/9/21 下午8:25
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from ..mohusets import mohuset
from ..mohunums import mohunum

import numpy as np


def zeros(qrung, mtype, *n):
    """
         Generate an *n all-zero fuzzy set

        Parameters
        ----------
            qrung : int
                    The qrung of the fuzzy set
            mtype : str
                    The type of the fuzzy set
            n : int
                    The shape of the fuzzy set
        Returns
        -------
            newset : mohuset
    """
    assert qrung > 0, \
        'ERROR: q must be greater than 0.'
    if mtype == 'fn':
        s = np.full(n, mohunum(qrung, 0., 0.), dtype=object)
    elif mtype == 'ivfn':
        s = np.full(n, mohunum(qrung, [0., 0.], [0., 0.]), dtype=object)
    else:
        raise ValueError('ERROR: Unsupported type.')
    newset = mohuset(qrung, mtype)
    newset._mohuset__shape = s.shape
    newset._mohuset__ndim = s.ndim
    newset._mohuset__set = s
    newset._mohuset__size = s.size
    return newset


def poss(qrung, mtype, *n):
    """
        Generate an *n all-positive fuzzy set

        Parameters
        ----------
            qrung : int
                    The qrung of the fuzzy set
            mtype : str
                    The type of the fuzzy set
            n : int
                    The shape of the fuzzy set
        Returns
        -------
            newset : mohuset
    """
    assert qrung > 0, \
        'ERROR: q must be greater than 0.'
    if mtype == 'fn':
        s = np.full(n, mohunum(qrung, 1., 0.), dtype=object)
    elif mtype == 'ivfn':
        s = np.full(n, mohunum(qrung, [1., 0.], [1., 0.]), dtype=object)
    else:
        raise ValueError('ERROR: Unsupported type.')
    newset = mohuset(qrung, mtype)
    newset._mohuset__shape = s.shape
    newset._mohuset__ndim = s.ndim
    newset._mohuset__set = s
    newset._mohuset__size = s.size
    return newset


def negs(qrung, mtype, *n):
    """
        Generate an *n all-negative fuzzy set

        Parameters
        ----------
            qrung : int
                    The qrung of the fuzzy set
            mtype : str
                    The type of the fuzzy set
            n : int
                    The shape of the fuzzy set
        Returns
        -------
            newset : mohuset
    """
    assert qrung > 0, \
        'ERROR: q must be greater than 0.'
    if mtype == 'fn':
        s = np.full(n, mohunum(qrung, 0., 1.), dtype=object)
    elif mtype == 'ivfn':
        s = np.full(n, mohunum(qrung, [0., 1.], [0., 1.]), dtype=object)
    else:
        raise ValueError('ERROR: Unsupported type.')
    newset = mohuset(qrung, mtype)
    newset._mohuset__shape = s.shape
    newset._mohuset__ndim = s.ndim
    newset._mohuset__set = s
    newset._mohuset__size = s.size
    return newset


def nums(x: mohunum, *n):
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
    newset._mohuset__shape = s.shape
    newset._mohuset__ndim = s.ndim
    newset._mohuset__set = s
    newset._mohuset__size = s.size
    return newset
