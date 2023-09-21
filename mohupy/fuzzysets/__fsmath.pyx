#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/21 上午4:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets

import numpy as np
cimport numpy as np

from .fuzzyset import fuzzyset
# import mohusets.fuzzynumbers as fns
from ..fuzzynumbers import glb
d = glb.global_dict()

cpdef __dot11(np.ndarray x, np.ndarray y, str norm='algeb'):
    assert x[0].__class__ == y[0].__class__, 'ERROR: the two fuzzy set are not the same set!'
    assert x[0].qrung == y[0].qrung, 'ERROR: the qrung of two fuzzy sets are not equal!'
    assert x.ndim == 1 and x.ndim == 1, 'Both fuzzy sets must be 1-dimensional fuzzy sets.'
    assert x.size == y.size, 'ERROR: The number of elements in the two fuzzy sets must be the same.'
    cdef int num

    nor = norm + '_multiply'
    assert nor in d[x[0].__class__.__name__], 'KetError: The norm {} is not defined.'.format(nor)

    multipy = d[x[0].__class__.__name__][nor]
    newfuzz = fuzzyset(x[0].qrung, y[0].__class__.__name__)
    num = 0

    for i in range(len(x)):
        newfuzz.append(multipy(x[i], y[i]))
        num += 1
    f = newfuzz.sum()
    newfuzz.clear()
    newfuzz.append(f)
    return newfuzz

cpdef __dot21(np.ndarray x, np.ndarray y, str norm='algeb'):
    assert x[0, 0].__class__ == y[0].__class__, 'ERROR: the two fuzzy set are not the same set!'
    assert x[0, 0].qrung == y[0].qrung, 'ERROR: the qrung of two fuzzy sets are not equal!'
    assert x.ndim == 2 and y.ndim == 1, \
        'The first set must be 2-dimensional and the second set must be 1-dimensional'
    assert len(x[0]) == len(y), 'Shape of two set are not aligned.'

    newf = fuzzyset(x[0, 0].qrung, y[0].__class__.__name__)

    for i in range(len(x)):
        newf.append(__dot11(x[i, :], y, norm).set[0])
    return newf

cpdef __dot12(np.ndarray x, np.ndarray y, str norm='algeb'):
    assert x[0].__class__ == y[0, 0].__class__, 'ERROR: the two fuzzy set are not the same set!'
    assert x[0].qrung == y[0, 0].qrung, 'ERROR: the qrung of two fuzzy sets are not equal!'
    assert x.ndim == 1 and y.ndim == 2, 'The first set must be 1-dimensional and the second set must be 2-dimensional'
    assert len(x) == len(y), 'Shape of two set are not aligned.'

    newf = fuzzyset(x[0].qrung, y[0, 0].__class__.__name__)

    for i in range(len(y[0])):
        newf.append(__dot11(x, y[:, i], norm).set[0])
    return newf

cpdef __dot22(np.ndarray x, np.ndarray y, str norm='algeb'):
    """
        Dot product of two fuzzy sets
    """
    assert x[0, 0].__class__ == y[0, 0].__class__, 'ERROR: the two fuzzy set are not the same set!'
    assert x[0, 0].qrung == y[0, 0].qrung, 'ERROR: the qrung of two fuzzy sets are not equal!'
    assert x.ndim == 2 and y.ndim == 2, 'Fuzzy sets must be 2-dimensional.'
    assert len(x[0]) == len(y), 'Shape of two set are not aligned.'

    newf = fuzzyset(x[0, 0].qrung, y[0, 0].__class__.__name__)
    newf.zeros(len(x), len(y[0]))

    for i in range(len(x)):
        for j in range(len(y[0])):
            newf.set[i, j] = __dot11(x[i, :], y[:, j], norm=norm).set[0]
    return newf













