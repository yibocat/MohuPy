#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/21 上午4:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets

from .fuzzy_element import qrungifn
from ..archimedean cimport algebraic_T, algebraic_S, einstein_T, einstein_S

cpdef intersection(fn1:qrungifn, fn2:qrungifn):
    assert fn1.qrung == fn2.qrung, 'ERROR:the two FNs are not the same FN'
    q = fn1.qrung
    newFN = qrungifn(q, 0., 0.)
    newFN.set_md(min(fn1.md, fn2.md))
    newFN.set_nmd(max(fn1.nmd, fn2.nmd))
    return newFN


cpdef unions(fn1:qrungifn, fn2:qrungifn):
    assert fn1.qrung == fn2.qrung, 'ERROR:the two FNs are not the same FN'
    q = fn1.qrung
    newFN = qrungifn(q, 0., 0.)
    newFN.set_md(max(fn1.md, fn2.md))
    newFN.set_nmd(min(fn1.nmd, fn2.nmd))
    return newFN


cpdef algeb_multiply(fn1: qrungifn, fn2: qrungifn):
    assert fn1.qrung == fn2.qrung, 'ERROR:the two FNs are not the same FN'
    q = fn1.qrung
    newFN = qrungifn(q, 0., 0.)
    newFN.set_md(algebraic_T(fn1.md ** q, fn2.md ** q) ** (1 / q))
    newFN.set_nmd(algebraic_S(fn1.nmd ** q, fn2.nmd ** q) ** (1 / q))
    return newFN


cpdef algeb_plus(fn1: qrungifn, fn2: qrungifn):
    assert fn1.qrung == fn2.qrung, 'ERROR:the two FNs are not the same FN'
    q = fn1.qrung
    newFN = qrungifn(q, 0., 0.)
    newFN.set_md(algebraic_S(fn1.md ** q, fn2.md ** q) ** (1 / q))
    newFN.set_nmd(algebraic_T(fn1.nmd ** q, fn2.nmd ** q) ** (1 / q))
    return newFN


cpdef eins_multiply(fn1: qrungifn, fn2: qrungifn):
    assert fn1.qrung == fn2.qrung, 'ERROR:the two FNs are not the same FN'
    q = fn1.qrung
    newFN = qrungifn(q, 0., 0.)
    newFN.set_md(einstein_T(fn1.md ** q, fn2.md ** q) ** (1 / q))
    newFN.set_nmd(einstein_S(fn1.nmd ** q, fn2.nmd ** q) ** (1 / q))
    return newFN


cpdef eins_plus(fn1: qrungifn, fn2: qrungifn):
    assert fn1.qrung == fn2.qrung, 'ERROR:the two FNs are not the same FN'
    q = fn1.qrung
    newFN = qrungifn(q, 0., 0.)
    newFN.set_md(einstein_S(fn1.md ** q, fn2.md ** q) ** (1 / q))
    newFN.set_nmd(einstein_T(fn1.nmd ** q, fn2.nmd ** q) ** (1 / q))
    return newFN
