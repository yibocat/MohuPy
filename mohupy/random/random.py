#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/10/1 下午3:05
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import numpy as np

from ..core.mohusets import mohuset
from ..core.mohunum import mohunum


def __rand_qrofn(q=1):
    """
        Randomly generate a q-rung orthopair fuzzy number.

        Parameters
        ----------
            q : int
                The q-rung
        Returns
        -------
            newfn : mohunum
    """
    newfn = mohunum(q, 0., 0.)
    while True:
        newfn.md = np.random.rand()
        newfn.nmd = np.random.rand()
        if newfn.is_valid():
            break
    return newfn


def __rand_ivfn(q=1):
    """
        Randomly generate an interval-valued q-rung orthopair fuzzy number.

        Parameters
        ----------
            q : int
                The q-rung
        Returns
        -------
            newfn : mohunum
    """
    newfn = mohunum(q, [0., 0.], [0., 0.])
    while True:
        newfn.md = [np.random.rand(), np.random.rand()]
        newfn.nmd = [np.random.rand(), np.random.rand()]
        if newfn.is_valid():
            break
    return newfn


def __rand_set(q=1, mtype='qrofn', *n):
    """
        Randomly generate a set of fuzzy numbers.

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
            newset : mohuset
    """
    def __random(__damm: mohunum):
        if __damm.mtype == 'qrofn':
            return __rand_qrofn(q)
        if __damm.mtype == 'ivfn':
            return __rand_ivfn(q)
        raise ValueError('Invalid fuzzy type.')

    from ..utils.construct import zeros
    newset = zeros(q, mtype, *n)

    vec_func = np.vectorize(__random)
    result = vec_func(newset.set)
    newset.set = result
    return newset


def random(q: int = 1, mtype: str = 'qrofn', *n):
    """
        Randomly generate a fuzzy number or fuzzy set.

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
            mohunum or mohuset
    """
    if len(n) == 0:
        if mtype == 'qrofn':
            return __rand_qrofn(q)
        if mtype == 'ivfn':
            return __rand_ivfn(q)
        raise ValueError('Invalid fuzzy type.')
    else:
        return __rand_set(q, mtype, *n)


def choice(f: mohuset) -> mohunum:
    """
        Randomly select a fuzzy number

        Parameters
        ----------
            f:  mohuset
                The fuzzy set.

        Returns
        -------
            mohunum
    """
    return np.random.choice(f.set.flatten())
