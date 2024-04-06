#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/6 下午2:49
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import warnings

import numpy as np

from .algebraic import (algebraic_add,algebraic_sub,algebraic_mul,
                        algebraic_div,algebraic_pow,algebraic_times)

from ..regedit import Registry

algebAdd = Registry()
algebSub = Registry()
algebMul = Registry()
algebDiv = Registry()
algebPow = Registry()
algebTim = Registry()


################################################################
# Algebraic Addition
################################################################

@algebAdd('qrofn')
def qrofn_algeb_add(x0, y0, x1, y1, q):
    return algebraic_add(x0, y0, x1, y1, q)


@algebAdd('ivfn')
def ivfn_algeb_add(x0, y0, x1, y1, q):
    return algebraic_add(x0, y0, x1, y1, q)


@algebAdd('qrohfn')
def qrohfn_algeb_add(x0, y0, x1, y1, q):
    mds, nmds = np.array([]), np.array([])

    m = np.array(np.meshgrid(x0, x1)).T.reshape(-1, 2)
    n = np.array(np.meshgrid(y0, y1)).T.reshape(-1, 2)

    for i in range(len(m)):
        mds = np.append(mds, algebraic_add(m[i, 0], 0, m[i, 1], 0, q)[0])
    for i in range(len(n)):
        nmds = np.append(nmds, algebraic_add(0, n[i, 0], 0, n[i, 1], q)[1])
    return mds, nmds


################################################################
# Algebraic Subtraction
################################################################

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


################################################################
# Algebraic Multiplication
################################################################

@algebMul('qrofn')
def qrofn_algeb_mul(x0, y0, x1, y1, q):
    return algebraic_mul(x0, y0, x1, y1, q)


@algebMul('ivfn')
def ivfn_algeb_mul(x0, y0, x1, y1, q):
    return algebraic_mul(x0, y0, x1, y1, q)


@algebMul('qrohfn')
def qrohfn_algeb_mul(x0, y0, x1, y1, q):
    mds, nmds = np.array([]), np.array([])

    m = np.array(np.meshgrid(x0, x1)).T.reshape(-1, 2)
    n = np.array(np.meshgrid(y0, y1)).T.reshape(-1, 2)

    for i in range(len(m)):
        mds = np.append(mds, algebraic_mul(m[i, 0], 0, m[i, 1], 0, q)[0])
    for i in range(len(n)):
        nmds = np.append(nmds, algebraic_mul(0, n[i, 0], 0, n[i, 1], q)[1])
    return mds, nmds


################################################################
# Algebraic Division
################################################################

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


################################################################
# Algebraic Power
################################################################

@algebPow('qrofn')
def qrofn_algeb_pow(p, x0, y0, q):
    return algebraic_pow(p, x0, y0, q)


@algebPow('ivfn')
def ivfn_algeb_pow(p, x0, y0, q):
    return algebraic_pow(p, x0, y0, q)


@algebPow('qrohfn')
def qrohfn_algeb_pow(p, x0, y0, q):
    return algebraic_pow(p, x0, y0, q)


################################################################
# Algebraic Times
################################################################

@algebTim('qrofn')
def qrofn_algeb_times(p, x0, y0, q):
    return algebraic_times(p, x0, y0, q)


@algebTim('ivfn')
def ivfn_algeb_times(p, x0, y0, q):
    return algebraic_times(p, x0, y0, q)


@algebTim('qrohfn')
def qrohfn_algeb_times(p, x0, y0, q):
    return algebraic_times(p, x0, y0, q)
