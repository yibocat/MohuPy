#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/9/21 下午8:25
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from ..config import import_cupy_lib

np = import_cupy_lib()

from ..mohusets import mohuset


def dot(f1: mohuset, f2: mohuset):
    """
        Returns the dot product of two mohusets.

        Parameters
        ----------
        f1 : mohuset
            The first mohuset.
        f2 : mohuset
            The second mohuset.

        Returns
        -------
        mohuset or np.float_
            The dot product of f1 and f2.
    """
    assert f1.mtype == f2.mtype, \
        'ERROR: The mohusets must be of the same type.'
    assert f1.qrung == f2.qrung, \
        'ERROR: The qrungs must be equal.'
    assert 0 < f1.ndim <= 2 and 0 < f2.ndim <= 2, \
        'ERROR: The mohusets must be 1D or 2D.'

    if f1.ndim == f2.ndim == 2:
        return f1 @ f2
    if (f1.ndim == 2 and f2.ndim == 1) or \
            (f1.ndim == 1 and f2.ndim == 2):
        result = np.dot(f1.set, f2.set)
        newset = mohuset(f1.qrung, f1.mtype)
        newset.setter(result, result.shape, result.ndim, result.size)
        return newset
    if f1.ndim == 1 and f2.ndim == 1:
        return np.dot(f1.set, f2.set)
    raise ValueError('ERROR')


def inner(f1: mohuset, f2: mohuset):
    """
        Returns the inner product of two mohusets.

        Parameters
        ----------
        f1 : mohuset
            The first mohuset.
        f2 : mohuset
            The second mohuset.

        Returns
        -------
        mohuset or np.float_
            The inner product of f1 and f2.
    """
    assert f1.mtype == f2.mtype, \
        'ERROR: The mohusets must be of the same type.'
    assert f1.qrung == f2.qrung, \
        'ERROR: The qrungs must be equal.'
    if f1.ndim == 1 and f2.ndim == 1:
        return np.inner(f1.set, f2.set)
    else:
        result = np.inner(f1.set, f2.set)
        newset = mohuset(f1.qrung, f1.mtype)
        newset.setter(result, result.shape, result.ndim, result.size)
        return newset


def outer(f1: mohuset, f2: mohuset):
    """
        Returns the outer product of two 1D and 2D mohusets.

        Parameters
        ----------
        f1 : mohuset
            The first mohuset.
        f2 : mohuset
            The second mohuset.

        Returns
        -------
        mohuset or np.float_
            The outer product of f1 and f2.
    """
    assert f1.mtype == f2.mtype, \
        'ERROR: The mohusets must be of the same type.'
    assert f1.qrung == f2.qrung, \
        'ERROR: The qrungs must be equal.'
    assert 0 < f1.ndim <= 2 and 0 < f2.ndim <= 2, \
        'ERROR: The mohusets must be 1D or 2D.'

    result = np.outer(f1.set, f2.set)
    newset = mohuset(f1.qrung, f1.mtype)
    newset.setter(result, result.shape, result.ndim, result.size)
    return newset


def mohu_func(func, f1: mohuset, f2: mohuset, *args):
    """
        Apply a function to two fuzzy set.
        Operate two fuzzy sets based on a custom function.

        Parameters
        ----------
            func :  function
                    The function to apply.
            f1 :    mohuset
                    The first mohuset.
            f2 :    mohuset
                    The second mohuset.
            *args : The arguments to the function.

        Returns
        -------
            mohuset
    """
    assert f1.mtype == f2.mtype, \
        'ERROR: The mohusets must be of the same type.'
    assert f1.qrung == f2.qrung, \
        'ERROR: The qrungs must be equal.'

    result = func(f1.set, f2.set, *args)
    newset = mohuset(f1.qrung, f1.mtype)
    newset.setter(result, result.shape, result.ndim, result.size)
    del result
    return newset


def cartadd(f1: mohuset, f2: mohuset):
    """
        Returns the cartesian sum of two mohusets.

        Parameters
        ----------
        f1 : mohuset
            The first mohuset.
        f2 : mohuset
            The second mohuset.

        Returns
        -------
            mohuset
    """
    newset = mohuset(f1.qrung, f1.mtype)
    result = np.asarray(np.add.outer(f1.set, f2.set))
    newset.setter(result, result.shape, result.ndim, result.size)
    del result
    return newset


def cartprod(f1: mohuset, f2: mohuset):
    """
        Returns the cartesian product of two mohusets.

        Parameters
        ----------
        f1 : mohuset
            The first mohuset.
        f2 : mohuset
            The second mohuset.

        Returns
        -------
            mohuset
    """
    newset = mohuset(f1.qrung, f1.mtype)
    result = np.asarray(np.meshgrid(f1.set, f2.set))
    newset.setter(result, result.shape, result.ndim, result.size)
    del result
    return newset
