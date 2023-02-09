from .qrungifn import qrungifn
from fuzzpy_c.fuzzynumbers.archimedean import *

cpdef intersection(fn1:qrungifn, fn2:qrungifn):
    assert fn1.qrung == fn2.qrung, 'ERROR:the two FNs are not the same FN'
    q = fn1.qrung
    newFN = qrungifn(q, 0., 0.)
    newFN.md = min(fn1.md, fn2.md)
    newFN.nmd = max(fn1.nmd, fn2.nmd)
    return newFN


cpdef unions(fn1:qrungifn, fn2:qrungifn):
    assert fn1.qrung == fn2.qrung, 'ERROR:the two FNs are not the same FN'
    q = fn1.qrung
    newFN = qrungifn(q, 0., 0.)
    newFN.md = max(fn1.md, fn2.md)
    newFN.nmd = min(fn1.nmd, fn2.nmd)
    return newFN


cpdef algeb_multiply(fn1: qrungifn, fn2: qrungifn):
    assert fn1.qrung == fn2.qrung, 'ERROR:the two FNs are not the same FN'
    q = fn1.qrung
    newFN = qrungifn(q, 0., 0.)
    newFN.md = algebraic_T(fn1.md ** q, fn2.md ** q) ** (1 / q)
    newFN.nmd = algebraic_S(fn1.nmd ** q, fn2.nmd ** q) ** (1 / q)
    return newFN


cpdef algeb_plus(fn1: qrungifn, fn2: qrungifn):
    assert fn1.qrung == fn2.qrung, 'ERROR:the two FNs are not the same FN'
    q = fn1.qrung
    newFN = qrungifn(q, 0., 0.)
    newFN.md = algebraic_S(fn1.md ** q, fn2.md ** q) ** (1 / q)
    newFN.nmd = algebraic_T(fn1.nmd ** q, fn2.nmd ** q) ** (1 / q)
    return newFN


cpdef eins_multiply(fn1: qrungifn, fn2: qrungifn):
    assert fn1.qrung == fn2.qrung, 'ERROR:the two FNs are not the same FN'
    q = fn1.qrung
    newFN = qrungifn(q, 0., 0.)
    newFN.md = einstein_T(fn1.md ** q, fn2.md ** q) ** (1 / q)
    newFN.nmd = einstein_S(fn1.nmd ** q, fn2.nmd ** q) ** (1 / q)
    return newFN


cpdef eins_plus(fn1: qrungifn, fn2: qrungifn):
    assert fn1.qrung == fn2.qrung, 'ERROR:the two FNs are not the same FN'
    q = fn1.qrung
    newFN = qrungifn(q, 0., 0.)
    newFN.md = einstein_S(fn1.md ** q, fn2.md ** q) ** (1 / q)
    newFN.nmd = einstein_T(fn1.nmd ** q, fn2.nmd ** q) ** (1 / q)
    return newFN
