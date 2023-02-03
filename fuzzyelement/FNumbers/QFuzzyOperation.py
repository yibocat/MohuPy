#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/1 下午5:37
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzyKit

from .qrungfn import qrungfn
from .archimedean import *


def intersection(fn1: qrungfn, fn2: qrungfn):
    """
        intersection of two FNs
    """
    assert fn1.qrung == fn2.qrung, 'ERROR:the two FNs are not the same FN'
    q = fn1.qrung
    newFN = qrungfn(q, 0., 0.)
    newFN.md = min(fn1.md, fn2.md)
    newFN.nmd = max(fn1.nmd, fn2.nmd)
    return newFN


def unions(fn1: qrungfn, fn2: qrungfn):
    """
        unions of two FNs
    """
    assert fn1.qrung == fn2.qrung, 'ERROR:the two FNs are not the same FN'
    q = fn1.qrung
    newFN = qrungfn(q, 0., 0.)
    newFN.md = max(fn1.md, fn2.md)
    newFN.nmd = min(fn1.nmd, fn2.nmd)
    return newFN


def algeb_multiply(fn1: qrungfn, fn2: qrungfn):
    """
        Algebraic multiplication of two FNs
    """
    assert fn1.qrung == fn2.qrung, 'ERROR:the two FNs are not the same FN'
    q = fn1.qrung
    newFN = qrungfn(q, 0., 0.)
    newFN.md = algebraic_T(fn1.md ** q, fn2.md ** q) ** (1 / q)
    newFN.nmd = algebraic_S(fn1.nmd ** q, fn2.nmd ** q) ** (1 / q)
    return newFN


def algeb_plus(fn1: qrungfn, fn2: qrungfn):
    """
        Algebraic addition of two FNs
    """
    assert fn1.qrung == fn2.qrung, 'ERROR:the two FNs are not the same FN'
    q = fn1.qrung
    newFN = qrungfn(q, 0., 0.)
    newFN.md = algebraic_S(fn1.md ** q, fn2.md ** q) ** (1 / q)
    newFN.nmd = algebraic_T(fn1.nmd ** q, fn2.nmd ** q) ** (1 / q)
    return newFN


def eins_multiply(fn1: qrungfn, fn2: qrungfn):
    """
        Einstein multiplication of two FNs
    """
    assert fn1.qrung == fn2.qrung, 'ERROR:the two FNs are not the same FN'
    q = fn1.qrung
    newFN = qrungfn(q, 0., 0.)
    newFN.md = einstein_T(fn1.md ** q, fn2.md ** q) ** (1 / q)
    newFN.nmd = einstein_S(fn1.nmd ** q, fn2.nmd ** q) ** (1 / q)
    return newFN


def eins_plus(fn1: qrungfn, fn2: qrungfn):
    """
        Einstein addition of two FNs
    """
    assert fn1.qrung == fn2.qrung, 'ERROR:the two FNs are not the same FN'
    q = fn1.qrung
    newFN = qrungfn(q, 0., 0.)
    newFN.md = einstein_S(fn1.md ** q, fn2.md ** q) ** (1 / q)
    newFN.nmd = einstein_T(fn1.nmd ** q, fn2.nmd ** q) ** (1 / q)
    return newFN
