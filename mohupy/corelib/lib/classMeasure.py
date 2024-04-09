#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/7 下午2:00
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import numpy as np

from .base import Library
from ..regedit import fuzzDis
from ...core import Fuzznum, Fuzzarray
from ...config import Config


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

        if isinstance(f1, Fuzznum) and isinstance(f2, Fuzznum):
            return fuzzDis[Config.mtype](f1, f2, l, t, indeterminacy)
        if isinstance(f1, Fuzznum) and isinstance(f2, Fuzzarray):
            vec_func = np.vectorize(fuzzDis[Config.mtype])
            return vec_func(f1, f2.array, l, t, indeterminacy)
        if isinstance(f1, Fuzzarray) and isinstance(f2, Fuzznum):
            vec_func = np.vectorize(fuzzDis[Config.mtype])
            return vec_func(f1.array, f2, l, t, indeterminacy)
        if isinstance(f1, Fuzzarray) and isinstance(f2, Fuzzarray):
            vec_func = np.vectorize(fuzzDis[Config.mtype])
            return vec_func(f1.array, f2.array, l, t, indeterminacy)
