#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/12 下午2:16
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import numpy as np

from ...core import Fuzznum, Fuzzarray


def fuzz_distance(f1: Fuzznum | Fuzzarray,
                  f2: Fuzznum | Fuzzarray,
                  param_l=2, param_t=1, indeterminacy=True) -> np.ndarray | float:
    """
    The generalized distance function for two fuzzy arrays or numbers.
            The parameter 'l' is the generic distance function parameter. 'l=1' indicates
            the Hamming distance and 'l=2' indicates the Euclidean distance.
            The parameter 't' is the risk factor of normalization process, which in
            the interval [0, 1]. 't=1' indicates optimistic normalization and 't=0' indicates
            pessimistic normalization.
    :param f1:              the first fuzzy number or array
    :param f2:              the second fuzzy number or array
    :param param_l:         the parameter of generalized distance
    :param param_t:         the risk factor for normalization process
    :param indeterminacy:   determines whether the distance contains indeterminacy
    :return:                the distance between the two fuzzy numbers of fuzzy arrays
    """
    from ..lib import Distance
    return Distance()(f1, f2, param_l, param_t, indeterminacy)
