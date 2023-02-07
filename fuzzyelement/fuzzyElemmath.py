#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/4 下午8:27
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzPy
import copy

import numpy as np

from .DHFElements import qrunghfe
from .FNumbers import qrungfn
from .IVFNumbers import qrungivfn

from config import load_dict

d = load_dict(False)


def generalized_distance(d1, d2, l=1, t=1, indeterminacy=True):
    """
        Generalized distance between two fuzzy elements.

        Parameters
        ----------
        d1 : FuzzyElement
            First fuzzy element.
        d2 : FuzzyElement
            Second fuzzy element.
        l : float
            The parameter of the distance.
            'l=1' means the Hamming distance and 'l=2' means the Euclidean distance.
            default is 1.
        t : float
            the parameter of the normalization function.
            't=1' indicates optimistic normalization and 't=0' indicates pessimistic
            normalization.
            default is 1 indicates optimistic normalization.
        indeterminacy : bool
            Determine whether the distance formula contains indeterminacy.

        Returns
        -------
            float
            The generalized distance between two fuzzy elements.

        Notes
        -----
            Because the hesitant fuzzy distance needs to be normalized, the
            parameter settings are different. It is necessary to discriminate the
            type of hesitant fuzzy sets.
    """
    assert l > 0, 'ERROR: Generalized distance parameter error, parameter must be > 0.'
    assert d1.__class__.__name__ == d2.__class__.__name__ and \
           d1.__class__.__name__ in d, 'The two fuzzy element types are ' \
                                       'not the same or are incorrect'

    typ = d1.__class__.__name__
    if typ == 'qrunghfe':
        return d[typ]['distance'](d1, d2, l, t, indeterminacy)
    else:
        return d[typ]['distance'](d1, d2, l, indeterminacy)
