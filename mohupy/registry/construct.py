#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/10/16 下午11:58
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import numpy as np

from ..registry.regedit import Register
from ..core.mohusets import mohuset

fuzzZeros = Register()
fuzzPoss = Register()
fuzzNegs = Register()


################################
# qrofn
################################
@fuzzZeros('qrofn')
def zeros_qrofn(q, *n):
    from ..core import fuzznum
    s = np.full(n, fuzznum(q, 0., 0.), dtype=object)
    newset = mohuset(q, 'qrofn')
    newset.set = s
    return newset


@fuzzPoss('qrofn')
def poss_qrofn(q, *n):
    from ..core import fuzznum
    s = np.full(n, fuzznum(q, 1., 0.), dtype=object)
    newset = mohuset(q, 'qrofn')
    newset.set = s
    return newset


@fuzzNegs('qrofn')
def negs_qrofn(q, *n):
    from ..core import fuzznum
    s = np.full(n, fuzznum(q, 0., 1.), dtype=object)
    newset = mohuset(q, 'qrofn')
    newset.set = s
    return newset


################################
# ivfn
################################
@fuzzZeros('ivfn')
def zeros_ivfn(q, *n):
    from ..core import fuzznum
    s = np.full(n, fuzznum(q, (0., 0.), (0., 0.)), dtype=object)
    newset = mohuset(q, 'ivfn')
    newset.set = s
    return newset


@fuzzPoss('ivfn')
def poss_ivfn(q, *n):
    from ..core import fuzznum
    s = np.full(n, fuzznum(q, (1., 1.), (0., 0.)), dtype=object)
    newset = mohuset(q, 'ivfn')
    newset.set = s
    return newset


@fuzzNegs('ivfn')
def negs_ivfn(q, *n):
    from ..core import fuzznum
    s = np.full(n, fuzznum(q, (0., 0.), (1., 1.)), dtype=object)
    newset = mohuset(q, 'ivfn')
    newset.set = s
    return newset


################################
# qrohfn
################################
@fuzzZeros('qrohfn')
def zeros_qrohfn(q, *n):
    from ..core import fuzznum
    s = np.full(n, fuzznum(q, [0], [0]), dtype=object)
    newset = mohuset(q, 'qrohfn')
    newset.set = s
    return newset


@fuzzPoss('qrohfn')
def poss_qrohfn(q, *n):
    from ..core import fuzznum
    s = np.full(n, fuzznum(q, [1], [0]), dtype=object)
    newset = mohuset(q, 'qrohfn')
    newset.set = s
    return newset


@fuzzNegs('qrohfn')
def negs_qrohfn(q, *n):
    from ..core import fuzznum
    s = np.full(n, fuzznum(q, [0], [1]), dtype=object)
    newset = mohuset(q, 'qrohfn')
    newset.set = s
    return newset
