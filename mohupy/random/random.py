#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/10/16 下午8:22
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import numpy as np

from ..registry.random import fuzzRandom


def randnum(q: int, mtype: str, num=5):
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
            fuzzNum
    """
    return fuzzRandom[mtype](q, num)


def randset(q: int, mtype: str, *n, num=5):
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
            mohuset
    """
    from ..core.base import fuzzNum

    def __rand(f: fuzzNum):
        return randnum(f.qrung, f.mtype, num)

    from ..utils.construct import zeros
    newset = zeros(q, mtype, *n)
    vec_func = np.vectorize(__rand)
    result = vec_func(newset.set)
    newset.set = result
    return newset


# def rand(q: int, mtype: str, *n, num=5):
#     """
#         random fuzzy function
#
#         Parameters
#         ----------
#             q : int
#                 The q-rung
#             mtype : str
#                 The type of fuzzy number to be generated
#             n : int
#                 The number of fuzzy numbers to be generated
#
#         Returns
#         -------
#             mohuset or fuzzNum
#     """
#     if len(n) == 0:
#         return randnum(q, mtype, num)
#     else:
#         return randset(q, mtype, *n, num)


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
