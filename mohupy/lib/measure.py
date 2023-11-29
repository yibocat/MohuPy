#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/11/28 下午7:09
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
"""
    This file is an implementation of some fuzzy metrics, including distance metrics (implemented),
    similar phase metrics, entropy metrics, and so on
"""
import numpy as np

from .base import Library
from ..regedit import fuzzDis


class Distance(Library):
    def function(self, f1, f2, l, t, indeterminacy):
        """
            The generalized distance function for two Q-rung hesitant fuzzy elements.
            The parameter 'l' is the generic distance function parameter. 'l=1' indicates
            the Hamming distance and 'l=2' indicates the Euclidean distance.
            The parameter 't' is the risk factor of normalization process, which in
            the interval [0, 1]. 't=1' indicates optimistic normalization and 't=0' indicates
            pessimistic normalization.

        Parameters
        ----------
            f1: Q-rung hesitant fuzzy element.
            f2: Q-rung hesitant fuzzy element.
            l: the generic distance function parameter.
                l=1 indicates the Hamming distance
                l=2 indicates the Euclidean distance
            t: the parameter of the normalization function.
                t=1 indicates optimistic normalization
                t=0 indicates pessimistic normalization.
            indeterminacy: Bool
                Determine whether the distance formula contains indeterminacy.
        """
        mtype = f1.mtype
        from ..core import Fuzznum, Fuzzarray
        if isinstance(f1, Fuzznum) and isinstance(f2, Fuzznum):
            return fuzzDis[mtype](f1, f2, l, t, indeterminacy)
        if isinstance(f1, Fuzznum) and isinstance(f2, Fuzzarray):
            vec_func = np.vectorize(fuzzDis[mtype])
            return vec_func(f1, f2.array, l, t, indeterminacy)
        if isinstance(f1, Fuzzarray) and isinstance(f2, Fuzznum):
            vec_func = np.vectorize(fuzzDis[mtype])
            return vec_func(f1.array, f2, l, t, indeterminacy)
        if isinstance(f1, Fuzzarray) and isinstance(f2, Fuzzarray):
            vec_func = np.vectorize(fuzzDis[mtype])
            return vec_func(f1.array, f2.array, l, t, indeterminacy)


def distance(f1, f2, l=2, t=1, indeterminacy=True):
    return Distance()(f1, f2, l, t, indeterminacy)
