#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/10/16 下午8:22
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import numpy as np

from ..registry.random import fuzzRandom


def randnum(q: int, mtype: str):
    """
        randomly generate a fuzzy number

        Parameters
        ----------
            q : int
                The q-rung
            mtype : str
                The type of fuzzy number to be generated

        Returns
        -------
            fuzzNum
    """
    return fuzzRandom[mtype](q)


def randset(q: int, mtype: str, *n):
    """
        Randomly generate a fuzzy set

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
            mohuset
    """
    from ..core.base import fuzzNum

    def __rand(f: fuzzNum):
        return randnum(f.qrung, f.mtype)

    from ..utils.construct import zeros
    newset = zeros(q, mtype, *n)
    vec_func = np.vectorize(__rand)
    result = vec_func(newset.set)
    newset.set = result
    return newset


def rand(q: int, mtype: str, *n):
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
            mohuset or fuzzNum
    """
    if len(n) == 0:
        return randnum(q, mtype)
    else:
        return randset(q, mtype, *n)


from ..core.mohusets import mohuset
from ..core.base import fuzzNum


def choice(f: mohuset) -> fuzzNum:
    """
        Randomly select a fuzzy number

        Parameters
        ----------
            f:  mohuset
                The fuzzy set.

        Returns
        -------
            fuzzNum
    """
    return np.random.choice(f.set.flatten())
