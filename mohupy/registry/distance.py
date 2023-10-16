#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/10/16 下午3:22
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import numpy as np

# from ..core.mohu import MohuQROFN, MohuQROIVFN
from ..registry.regedit import Register

fuzzDis = Register()


@fuzzDis('qrofn')
def distance_qrofn(f1,
                   f2,
                   l: (int, np.int_),
                   indeterminacy=True):
    assert f1.mtype == f2.mtype == 'qrofn', \
        "The type of f1 and f2 must be qrofn."
    assert f1.qrung == f2.qrung, \
        "q rung of two fuzzy numbers must be equal."
    assert l > 0, \
        "The value of l must be greater than 0."
    q = f1.qrung
    pi1 = f1.ind
    pi2 = f2.ind
    pi = np.fabs(pi1 ** q - pi2 ** q) ** l

    if indeterminacy:
        return (0.5 * (np.fabs(f1.md ** q - f2.md ** q) ** l +
                       np.fabs(f1.nmd ** q - f2.nmd ** q) ** l + pi)) ** (1 / l)
    else:
        return (0.5 * (np.fabs(f1.md ** q - f2.md ** q) ** l +
                       np.fabs(f1.nmd ** q - f2.nmd ** q) ** l)) ** (1 / l)


@fuzzDis('ivfn')
def distance_ivfn(f1,
                  f2,
                  l: (int, np.int_),
                  indeterminacy=True):
    assert f1.mtype == f2.mtype == 'ivfn', \
        "The type of f1 and f2 must be ivfn."
    assert f1.qrung == f2.qrung, \
        "q rung of two fuzzy numbers must be equal."
    assert l > 0, \
        "The value of l must be greater than 0."
    q = f1.qrung
    pi1 = f1.ind
    pi2 = f2.ind
    pi = np.fabs(pi1 ** q - pi2 ** q) ** l

    if indeterminacy:
        return 0.25 * (
                    np.fabs(f1.md[0] ** q - f2.md[0] ** q) ** l +
                    np.fabs(f1.md[1] ** q - f2.md[1] ** q) ** l +
                    np.fabs(f1.nmd[0] ** q - f2.nmd[0] ** q) ** l +
                    np.fabs(f1.nmd[1] ** q - f2.nmd[1] ** q) ** l + pi) ** (1 / l)
    else:
        return 0.25 * (
                    np.fabs(f1.md[0] ** q - f2.md[0] ** q) ** l +
                    np.fabs(f1.md[1] ** q - f2.md[1] ** q) ** l +
                    np.fabs(f1.nmd[0] ** q - f2.nmd[0] ** q) ** l +
                    np.fabs(f1.nmd[1] ** q - f2.nmd[1] ** q) ** l) ** (1 / l)


@fuzzDis('qrohfn')
def distance_qrohfn():
    pass