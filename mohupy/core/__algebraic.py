#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.109
#  Date: 2023/10/26 下午12:58
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import warnings
import numpy as np

from .__algebraic_norms import *
from ..registry.regedit import Register

algebAdd = Register()
algebSub = Register()
algebMul = Register()
algebDiv = Register()
algebPow = Register()
algebTim = Register()


@algebAdd('qrofn')
def qrofn_algeb_add(x0, y0, x1, y1, q):
    return algebraic_add(x0, y0, x1, y1, q)


@algebAdd('ivfn')
def ivfn_algeb_add(x0, y0, x1, y1, q):
    return algebraic_add(x0, y0, x1, y1, q)


@algebAdd('qrohfn')
def qrohfn_algeb_add(x0, y0, x1, y1, q):
    mds, nmds = np.array([]), np.array([])

    m = np.array(np.meshgrid(x0, y0)).T.reshape(-1, 2)
    n = np.array(np.meshgrid(x1, y1)).T.reshape(-1, 2)

    for i in range(len(m)):
        mds = np.append(mds, algebraic_add(m[i, 0], 0, m[i, 1], 0, q)[0])
    for i in range(len(n)):
        nmds = np.append(nmds, algebraic_add(0, n[i, 0], 0, n[i, 1], q)[1])
    return mds, nmds


@algebSub('qrofn')
def qrofn_algeb_sub(x0, y0, x1, y1, q):
    return algebraic_sub(x0, y0, x1, y1, q)


@algebSub('ivfn')
def ivfn_algeb_sub(x0, y0, x1, y1, q):
    # TODO
    warnings.warn('Subtraction of q-roivfn is not implemented. Return None.')
    return None


@algebSub('qrohfn')
def qrohfn_algeb_sub(x0, y0, x1, y1, q):
    # TODO
    warnings.warn('Subtraction of q-rohfn is not implemented. Return None.')
    return None


@algebMul('qrofn')
def qrofn_algeb_mul(x0, y0, x1, y1, q):
    return algebraic_mul(x0, y0, x1, y1, q)


@algebMul('ivfn')
def ivfn_algeb_mul(x0, y0, x1, y1, q):
    return algebraic_mul(x0, y0, x1, y1, q)


@algebMul('qrohfn')
def qrohfn_algeb_mul(x0, y0, x1, y1, q):
    mds, nmds = np.array([]), np.array([])

    m = np.array(np.meshgrid(x0, y0)).T.reshape(-1, 2)
    n = np.array(np.meshgrid(x1, y1)).T.reshape(-1, 2)

    for i in range(len(m)):
        mds = np.append(mds, algebraic_mul(m[i, 0], 0, m[i, 1], 0, q)[0])
    for i in range(len(n)):
        nmds = np.append(nmds, algebraic_mul(0, n[i, 0], 0, n[i, 1], q)[1])
    return mds, nmds


@algebDiv('qrofn')
def qrofn_algeb_div(x0, y0, x1, y1, q):
    return algebraic_div(x0, y0, x1, y1, q)


@algebDiv('ivfn')
def ivfn_algeb_div(x0, y0, x1, y1, q):
    # TODO
    warnings.warn('Division of q-roivfn is not implemented. Return None.')
    return None


@algebDiv('qrohfn')
def qrohfn_algeb_div(x0, y0, x1, y1, q):
    # TODO
    warnings.warn('Division of q-rohfn is not implemented. Return None.')
    return None


@algebPow('qrofn')
def qrofn_algeb_pow(p, x0, y0, q):
    return algebraic_pow(p, x0, y0, q)


@algebPow('ivfn')
def ivfn_algeb_pow(p, x0, y0, q):
    return algebraic_pow(p, x0, y0, q)


@algebPow('qrohfn')
def qrohfn_algeb_pow(p, x0, y0, q):
    return algebraic_pow(p, x0, y0, q)


@algebTim('qrofn')
def qrofn_algeb_times(p, x0, y0, q):
    return algebraic_times(p, x0, y0, q)


@algebTim('ivfn')
def ivfn_algeb_times(p, x0, y0, q):
    return algebraic_times(p, x0, y0, q)


@algebTim('qrohfn')
def qrohfn_algeb_times(p, x0, y0, q):
    return algebraic_times(p, x0, y0, q)
