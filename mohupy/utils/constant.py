#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/10/24 下午4:26
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from ..core import fuzznum
from ..registry.regedit import Register

fuzzZero = Register()
fuzzPos = Register()
fuzzNeg = Register()

ZERO_QROFN = lambda q: fuzznum(q, 0., 0.)
ZERO_IVFN = lambda q: fuzznum(q, (0., 0.), (0, 0.))
ZERO_QROHFN = lambda q: fuzznum(q, [0], [0.])

POS_QROFN = lambda q: fuzznum(q, 1., 0.)
POS_IVFN = lambda q: fuzznum(q, (1., 1.), (0, 0.))
POS_QROHFN = lambda q: fuzznum(q, [1], [0.])

NEG_QROFN = lambda q: fuzznum(q, 0., 1.)
NEG_IVFN = lambda q: fuzznum(q, (0., 0.), (1, 1.))
NEG_QROHFN = lambda q: fuzznum(q, [0], [1.])


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
