#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/9/21 下午8:25
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from ..mohunums import mohunum
from .archimedean import *


def ein_plus(f1: mohunum, f2: mohunum):
    """
        The einstein plus of two fuzzy numbers.
    """
    assert f1.qrung == f2.qrung, \
        'ERROR: The qrung of two fuzzy number must be same.'
    assert f1.mtype == f2.mtype, \
        'ERROR: The type of two fuzzy numbers must be same.'
    q = f1.qrung
    mtype = f1.mtype
    if mtype == 'fn':
        newfn = mohunum(q, 0., 0.)
        newfn._mohunum__MEMSHIP_KEY = False
        newfn.md = einstein_S(f1.md ** q, f2.md ** q) ** (1 / q)
        newfn.nmd = einstein_T(f1.nmd ** q, f2.nmd ** q) ** (1 / q)
        newfn._mohunum__MEMSHIP_KEY = True
        return newfn
    if mtype == 'ivfn':
        newfn = mohunum(q, [0., 0.], [0., 0.])
        newfn._mohunum__MEMSHIP_KEY = False
        newfn.md = einstein_S(f1.md ** q, f2.md ** q) ** (1 / q)
        newfn.nmd = einstein_T(f1.nmd ** q, f2.nmd ** q) ** (1 / q)
        newfn._mohunum__MEMSHIP_KEY = True
        return newfn

    raise ValueError('ERROR: Error mtype of fuzzy number.')


def ein_mul(f1: mohunum, f2: mohunum):
    """
        The einstein multiplication of two fuzzy numbers.
    """
    assert f1.qrung == f2.qrung, \
        'ERROR: The qrung of two fuzzy number must be same.'
    assert f1.mtype == f2.mtype, \
        'ERROR: The type of two fuzzy numbers must be same.'
    q = f1.qrung
    mtype = f1.mtype
    if mtype == 'fn':
        newfn = mohunum(q, 0., 0.)
        newfn._mohunum__MEMSHIP_KEY = False
        newfn.md = einstein_T(f1.md ** q, f2.md ** q) ** (1 / q)
        newfn.nmd = einstein_S(f1.nmd ** q, f2.nmd ** q) ** (1 / q)
        newfn._mohunum__MEMSHIP_KEY = True
        return newfn
    if mtype == 'ivfn':
        newfn = mohunum(q, [0., 0.], [0., 0.])
        newfn._mohunum__MEMSHIP_KEY = False
        newfn.md = einstein_T(f1.md ** q, f2.md ** q) ** (1 / q)
        newfn.nmd = einstein_S(f1.nmd ** q, f2.nmd ** q) ** (1 / q)
        newfn._mohunum__MEMSHIP_KEY = True
        return newfn


def ein_times(f: mohunum, l):
    assert 0. <= l <= 1, 'ERROR: The value must be between 0 and 1.'
    q = f.qrung
    if f.mtype == 'fn':
        newfn = mohunum(q, 0., 0.)
        newfn._mohunum__MEMSHIP_KEY = False
        newfn.md = (((1. + f.md ** q) ** l - (1. - f.md ** q) ** l) / (
                (1. + f.md ** q) ** l + (1. - f.md ** q) ** l)) ** (1. / q)
        newfn.nmd = ((2. * (f.nmd ** q) ** l) / (
                (2. - f.nmd ** q) ** l + (f.nmd ** q) ** l)) ** (1. / q)
        newfn._mohunum__MEMSHIP_KEY = True
        return newfn
    if f.mtype == 'ivfn':
        newfn = mohunum(q, [0., 0.], [0., 0.])
        newfn._mohunum__MEMSHIP_KEY = False
        newfn.md = (((1. + f.md ** q) ** l - (1. - f.md ** q) ** l) / (
                (1. + f.md ** q) ** l + (1. - f.md ** q) ** l)) ** (1. / q)
        newfn.nmd = ((2. * (f.nmd ** q) ** l) / (
                (2. - f.nmd ** q) ** l + (f.nmd ** q) ** l)) ** (1. / q)
        newfn._mohunum__MEMSHIP_KEY = True
        return newfn


def ein_power(f: mohunum, l):
    assert 0. <= l <= 1, 'ERROR: The value must be between 0 and 1.'
    q = f.qrung
    if f.mtype == 'fn':
        newfn = mohunum(q, 0., 0.)
        newfn._mohunum__MEMSHIP_KEY = False
        newfn.md = ((2. * (f.md ** q) ** l) / (
                (2. - f.md ** q) ** l + (f.md ** q) ** l)) ** (1. / q)
        newfn.nmd = (((1. + f.nmd ** q) ** l - (1. - f.nmd ** q) ** l) / (
                (1. + f.nmd ** q) ** l + (1. - f.nmd ** q) ** l)) ** (1. / q)
        newfn._mohunum__MEMSHIP_KEY = True
        return newfn
    if f.mtype == 'ivfn':
        newfn = mohunum(q, [0., 0.], [0., 0.])
        newfn._mohunum__MEMSHIP_KEY = False
        newfn.md = ((2. * (f.md ** q) ** l) / (
                (2. - f.md ** q) ** l + (f.md ** q) ** l)) ** (1. / q)
        newfn.nmd = (((1. + f.nmd ** q) ** l - (1. - f.nmd ** q) ** l) / (
                (1. + f.nmd ** q) ** l + (1. - f.nmd ** q) ** l)) ** (1. / q)
        newfn._mohunum__MEMSHIP_KEY = True
        return newfn
