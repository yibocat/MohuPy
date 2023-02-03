#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/3 下午4:01
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzyKit
from fuzzysets import fuzzyset
import config as cfg

d = cfg.load_dict(False)


def __dot11(x, y, norm='algeb'):
    assert x[0].__class__ == y[0].__class__, 'ERROR: the two fuzzy set are not the same set!'
    assert x[0].qrung == y[0].qrung, 'ERROR: the qrung of two fuzzy sets are not equal!'
    assert len(x.shape) == 1 and len(y.shape) == 1, 'Both fuzzy sets must be 1-dimensional fuzzy sets.'
    assert len(x) == len(y), 'ERROR: The number of elements in the two fuzzy sets must be the same.'

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


def __dot21(x, y, norm='algeb'):
    assert x[0, 0].__class__ == y[0].__class__, 'ERROR: the two fuzzy set are not the same set!'
    assert x[0, 0].qrung == y[0].qrung, 'ERROR: the qrung of two fuzzy sets are not equal!'
    assert len(x.shape) == 2 and len(
        y.shape) == 1, 'The first set must be 2-dimensional and the second set must be 1-dimensional'
    assert x.shape[-1] == len(y), 'shape {} and {} not aligned'.format(x.shape, y.shape)

    newf = fuzzyset(x[0, 0].qrung, y[0].__class__.__name__)

    for i in range(x.shape[0]):
        newf.append(__dot11(x[i, :], y, norm).set[0])
    return newf


def __dot12(x, y, norm='algeb'):
    assert x[0].__class__ == y[0, 0].__class__, 'ERROR: the two fuzzy set are not the same set!'
    assert x[0].qrung == y[0, 0].qrung, 'ERROR: the qrung of two fuzzy sets are not equal!'
    assert len(x.shape) == 1 and len(
        y.shape) == 2, 'The first set must be 1-dimensional and the second set must be 2-dimensional'
    assert len(x) == y.shape[0], 'shape {} and {} not aligned'.format(x.shape, y.shape)

    newf = fuzzyset(x[0].qrung, y[0, 0].__class__.__name__)

    for i in range(y.shape[1]):
        newf.append(__dot11(x, y[:, i], norm).set[0])
    return newf


def __dot22(x, y, norm='algeb'):
    """
        Dot product of two fuzzy sets
    """
    assert x[0, 0].__class__ == y[0, 0].__class__, 'ERROR: the two fuzzy set are not the same set!'
    assert x[0, 0].qrung == y[0, 0].qrung, 'ERROR: the qrung of two fuzzy sets are not equal!'
    assert len(x.shape) == 2 and len(y.shape) == 2, 'Fuzzy sets must be 2-dimensional.'
    assert x.shape[1] == y.shape[0], 'shapes {} and {} not aligned: %d (dim 1) != %d (dim0)'.format(x.shape, y.shape) \
                                     % (x.shape[1], y.shape[0])

    newf = fuzzyset(x[0, 0].qrung, y[0, 0].__class__.__name__)
    newf.zeros(x.shape[0], y.shape[1])

    for i in range(x.shape[0]):
        for j in range(y.shape[1]):
            newf.set[i, j] = __dot11(x[i, :], y[:, j], norm=norm).set[0]
    return newf
