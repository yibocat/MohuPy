#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/7 下午1:21
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import numpy as np

from ...core import Registry, Fuzzarray, Fuzznum

fuzzZeros = Registry()
fuzzPoss = Registry()
fuzzNegs = Registry()


################################
# qrofn
################################
@fuzzZeros('qrofn')
def zeros_qrofn(q, *n) -> Fuzzarray:
    s = np.full(n, Fuzznum(q, 0., 0.), dtype=object)
    newset = Fuzzarray(q)
    newset.array = s
    return newset


@fuzzPoss('qrofn')
def poss_qrofn(q, *n) -> Fuzzarray:
    s = np.full(n, Fuzznum(q, 1., 0.), dtype=object)
    newset = Fuzzarray(q)
    newset.array = s
    return newset


@fuzzNegs('qrofn')
def negs_qrofn(q, *n) -> Fuzzarray:
    s = np.full(n, Fuzznum(q, 0., 1.), dtype=object)
    newset = Fuzzarray(q)
    newset.array = s
    return newset


################################
# ivfn
################################
@fuzzZeros('ivfn')
def zeros_ivfn(q, *n) -> Fuzzarray:
    s = np.full(n, Fuzznum(q, (0., 0.), (0., 0.)), dtype=object)
    newset = Fuzzarray(q)
    newset.array = s
    return newset


@fuzzPoss('ivfn')
def poss_ivfn(q, *n) -> Fuzzarray:
    s = np.full(n, Fuzznum(q, (1., 1.), (0., 0.)), dtype=object)
    newset = Fuzzarray(q)
    newset.array = s
    return newset


@fuzzNegs('ivfn')
def negs_ivfn(q, *n) -> Fuzzarray:
    s = np.full(n, Fuzznum(q, (0., 0.), (1., 1.)), dtype=object)
    newset = Fuzzarray(q)
    newset.array = s
    return newset


################################
# qrohfn
################################
@fuzzZeros('qrohfn')
def zeros_qrohfn(q, *n) -> Fuzzarray:
    s = np.full(n, Fuzznum(q, [0], [0]), dtype=object)
    newset = Fuzzarray(q)
    newset.array = s
    return newset


@fuzzPoss('qrohfn')
def poss_qrohfn(q, *n) -> Fuzzarray:
    s = np.full(n, Fuzznum(q, [1], [0]), dtype=object)
    newset = Fuzzarray(q)
    newset.array = s
    return newset


@fuzzNegs('qrohfn')
def negs_qrohfn(q, *n) -> Fuzzarray:
    s = np.full(n, Fuzznum(q, [0], [1]), dtype=object)
    newset = Fuzzarray(q)
    newset.array = s
    return newset


fuzzZero = Registry()
fuzzPos = Registry()
fuzzNeg = Registry()

ZERO_QROFN = lambda q: Fuzznum(q, 0., 0.)
ZERO_IVFN = lambda q: Fuzznum(q, (0., 0.), (0., 0.))
ZERO_QROHFN = lambda q: Fuzznum(q, [0.], [0.])

POS_QROFN = lambda q: Fuzznum(q, 1., 0.)
POS_IVFN = lambda q: Fuzznum(q, (1., 1.), (0., 0.))
POS_QROHFN = lambda q: Fuzznum(q, [1.], [0.])

NEG_QROFN = lambda q: Fuzznum(q, 0., 1.)
NEG_IVFN = lambda q: Fuzznum(q, (0., 0.), (1., 1.))
NEG_QROHFN = lambda q: Fuzznum(q, [0.], [1.])


@fuzzZero('qrofn')
def zero_qrofn(q):
    return ZERO_QROFN(q)


@fuzzPos('qrofn')
def pos_qrofn(q):
    return POS_QROFN(q)


@fuzzNeg('qrofn')
def neg_qrofn(q):
    return NEG_QROFN(q)


@fuzzZero('ivfn')
def zero_ivfn(q):
    return ZERO_IVFN(q)


@fuzzPos('ivfn')
def pos_ivfn(q):
    return POS_IVFN(q)


@fuzzNeg('ivfn')
def neg_ivfn(q):
    return NEG_IVFN(q)


@fuzzZero('qrohfn')
def zero_qrohfn(q):
    return ZERO_QROHFN(q)


@fuzzPos('qrohfn')
def pos_qrohfn(q):
    return POS_QROHFN(q)


@fuzzNeg('qrohfn')
def neg_qrohfn(q):
    return NEG_QROHFN(q)
