#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/10/1 下午5:03
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
from typing import Union

from ..core.mohusets import mohuset
# from ..core.mohunum import mohunum
import numpy as np


# TODO(1): There are some bugs.
def dot(f1, f2):
    """
        Returns the dot product of two mohusets.

        Parameters
        ----------
        f1 : mohuset or fuzzNum
            The first mohuset or mohunum.
        f2 : mohuset or mohunum
            The second mohuset or mohunum.

        Returns
        -------
        mohuset or np.float_
            The dot product of f1 and f2.
    """
    if isinstance(f1, mohuset) and isinstance(f2, mohuset):
        if f1.ndim == f2.ndim == 1:
            return np.dot(f1.set, f2.set)
        else:
            result = np.dot(f1.set, f2.set)
            newset = mohuset(f1.qrung, f1.mtype)
            newset.set = result
            return newset

    # from ..runtime import fuzzParent, fuzzType
    # if isinstance(f1, fuzzParent.get(fuzzType[f1.mtype])) \
    #         and isinstance(f2, fuzzParent.get(fuzzType[f2.mtype])):

    from ..core.base import fuzzNum
    if isinstance(f1, fuzzNum) and isinstance(f2, fuzzNum):
        return f1 * f2

    if isinstance(f1, fuzzNum) and isinstance(f2, mohuset):
        if f2.ndim == 1:
            return np.dot(f1, f2.set)
        else:
            result = np.dot(f1, f2.set)
            newset = mohuset(f1.qrung, f1.mtype)
            newset.set = result
            return newset

    if isinstance(f1, mohuset) and isinstance(f2, fuzzNum):
        if f1.ndim == 1:
            return np.dot(f1.set, f2)
        else:
            result = np.dot(f1.set, f2)
            newset = mohuset(f1.qrung, f1.mtype)
            newset.set = result
            return newset

    raise ValueError(f'Invalid input type {type(f1)} and {type(f2)}')


def inner(f1, f2):
    """
        Returns the inner product of two mohusets.

        Parameters
        ----------
        f1 : mohuset or mohunum
            The first mohuset or mohunum.
        f2 : mohuset or mohunum
            The second mohuset or mohunum.

        Returns
        -------
        mohuset or np.float_
            The dot product of f1 and f2.
    """
    if isinstance(f1, mohuset) and isinstance(f2, mohuset):
        if f1.ndim == f2.ndim == 1:
            return np.inner(f1.set, f2.set)
        else:
            result = np.inner(f1.set, f2.set)
            newset = mohuset(f1.qrung, f1.mtype)
            newset.set = result
            return newset

    # from ..runtime import fuzzParent, fuzzType
    # if isinstance(f1, fuzzParent.get(fuzzType[f1.mtype])) \
    #         and isinstance(f2, fuzzParent.get(fuzzType[f2.mtype])):

    from ..core.base import fuzzNum
    if isinstance(f1, fuzzNum) and isinstance(f2, fuzzNum):
        return f1 * f2

    if isinstance(f1, fuzzNum) and isinstance(f2, mohuset):
        if f2.ndim == 1:
            return np.inner(f1, f2.set)
        else:
            result = np.inner(f1, f2.set)
            newset = mohuset(f1.qrung, f1.mtype)
            newset.set = result
            return newset

    if isinstance(f1, mohuset) and isinstance(f2, fuzzNum):
        if f1.ndim == 1:
            return np.inner(f1.set, f2)
        else:
            result = np.inner(f1.set, f2)
            newset = mohuset(f1.qrung, f1.mtype)
            newset.set = result
            return newset
    raise ValueError(f'Invalid input type {type(f1)} and {type(f2)}')


def outer(f1, f2):
    """
        Returns the outer product of two mohusets.

        Parameters
        ----------
        f1 : mohuset or mohunum
            The first mohuset or mohunum.
        f2 : mohuset or mohunum
            The second mohuset or mohunum.

        Returns
        -------
        mohuset or np.float_
            The dot product of f1 and f2.
    """
    if isinstance(f1, mohuset) and isinstance(f2, mohuset):
        result = np.outer(f1.set, f2.set)
        newset = mohuset(f1.qrung, f1.mtype)
        newset.set = result
        return newset

    # from ..runtime import fuzzParent, fuzzType
    # if isinstance(f1, fuzzParent.get(fuzzType[f1.mtype])) \
    #         and isinstance(f2, fuzzParent.get(fuzzType[f2.mtype])):

    from ..core.base import fuzzNum
    if isinstance(f1, fuzzNum) and isinstance(f2, fuzzNum):
        return f1 * f2

    if isinstance(f1, fuzzNum) and isinstance(f2, mohuset):
        result = np.outer(f1, f2.set)
        newset = mohuset(f1.qrung, f1.mtype)
        newset.set = result
        return newset

    if isinstance(f1, mohuset) and isinstance(f2, fuzzNum):
        result = np.outer(f1.set, f2)
        newset = mohuset(f1.qrung, f1.mtype)
        newset.set = result
        return newset
    raise ValueError(f'Invalid input type {type(f1)} and {type(f2)}')


def set_func(func, f1, f2, *args):
    assert f1.mtype == f2.mtype, 'f1 and f2 must have the same mtype'
    assert f1.qrung == f2.qrung, 'f1 and f2 must have the same qrung'

    result = func(f1.set, f2.set, *args)
    newset = mohuset(f1.qrung, f1.mtype)
    newset.set = result
    del result
    return newset


def cartadd(f1, f2):
    """
        Returns the cartesian sum of two mohusets.

        Parameters
        ----------
        f1 : mohuset or mohunum
            The first mohuset or mohunum.
        f2 : mohuset or mohunum
            The second mohuset or mohunum.

        Returns
        -------
        mohuset or np.float_
            The dot product of f1 and f2.
    """
    if isinstance(f1, mohuset) and isinstance(f2, mohuset):
        result = np.asarray(np.add.outer(f1.set, f2.set))
        newset = mohuset(f1.qrung, f1.mtype)
        newset.set = result
        return newset

    # from ..runtime import fuzzParent, fuzzType
    # if isinstance(f1, fuzzParent.get(fuzzType[f1.mtype])) \
    #         and isinstance(f2, fuzzParent.get(fuzzType[f2.mtype])):

    from ..core.base import fuzzNum
    if isinstance(f1, fuzzNum) and isinstance(f2, fuzzNum):
        return f1 * f2

    if isinstance(f1, fuzzNum) and isinstance(f2, mohuset):
        result = np.asarray(np.add.outer(f1, f2.set))
        newset = mohuset(f1.qrung, f1.mtype)
        newset.set = result
        return newset

    if isinstance(f1, mohuset) and isinstance(f2, fuzzNum):
        result = np.asarray(np.add.outer(f1.set, f2))
        newset = mohuset(f1.qrung, f1.mtype)
        newset.set = result
        return newset
    raise ValueError(f'Invalid input type {type(f1)} and {type(f2)}')


def cartprod(f1, f2):
    """
        Returns the cartesian product of two mohusets.

        Parameters
        ----------
        f1 : mohuset or mohunum
            The first mohuset or mohunum.
        f2 : mohuset or mohunum
            The second mohuset or mohunum.

        Returns
        -------
        mohuset or np.float_
            The dot product of f1 and f2.
    """
    if isinstance(f1, mohuset) and isinstance(f2, mohuset):
        result = np.asarray(np.meshgrid(f1.set, f2.set))
        newset = mohuset(f1.qrung, f1.mtype)
        newset.set = result
        return newset

    # from ..runtime import fuzzParent, fuzzType
    # if isinstance(f1, fuzzParent.get(fuzzType[f1.mtype])) \
    #         and isinstance(f2, fuzzParent.get(fuzzType[f2.mtype])):

    from ..core.base import fuzzNum
    if isinstance(f1, fuzzNum) and isinstance(f2, fuzzNum):
        return f1 * f2

    if isinstance(f1, fuzzNum) and isinstance(f2, mohuset):
        result = np.asarray(np.meshgrid(f1, f2.set))
        newset = mohuset(f1.qrung, f1.mtype)
        newset.set = result
        return newset

    if isinstance(f1, mohuset) and isinstance(f2, fuzzNum):
        result = np.asarray(np.meshgrid(f1.set, f2))
        newset = mohuset(f1.qrung, f1.mtype)
        newset.set = result
        return newset
    raise ValueError(f'Invalid input type {type(f1)} and {type(f2)}')
