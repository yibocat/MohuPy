from .QrungFN import QrungFN
from .archimedean import *


def Intersection(fn1: QrungFN, fn2: QrungFN):
    """
        Intersection of two FNs
    """
    assert fn1.qrung == fn2.qrung, 'ERROR:the two FNs are not the same FN'
    q = fn1.qrung
    newFN = QrungFN(q, 0, 0)
    newFN.md = min(fn1.md, fn2.md)
    newFN.nmd = max(fn1.nmd, fn2.nmd)
    return newFN


def Union(fn1: QrungFN, fn2: QrungFN):
    """
        Union of two FNs
    """
    assert fn1.qrung == fn2.qrung, 'ERROR:the two FNs are not the same FN'
    q = fn1.qrung
    newFN = QrungFN(q, 0, 0)
    newFN.md = max(fn1.md, fn2.md)
    newFN.nmd = min(fn1.nmd, fn2.nmd)
    return newFN


def algebraicMultiply(fn1: QrungFN, fn2: QrungFN):
    """
        Algebraic multiplication of two FNs
    """
    assert fn1.qrung == fn2.qrung, 'ERROR:the two FNs are not the same FN'
    q = fn1.qrung
    newFN = QrungFN(q, 0, 0)
    newFN.md = algebraic_T(fn1.md ** q, fn2.md ** q) ** (1 / q)
    newFN.nmd = algebraic_S(fn1.nmd ** q, fn2.nmd ** q) ** (1 / q)
    return newFN


def algebraicPlus(fn1: QrungFN, fn2: QrungFN):
    """
        Algebraic addition of two FNs
    """
    assert fn1.qrung == fn2.qrung, 'ERROR:the two FNs are not the same FN'
    q = fn1.qrung
    newFN = QrungFN(q, 0, 0)
    newFN.md = algebraic_S(fn1.md ** q, fn2.md ** q) ** (1 / q)
    newFN.nmd = algebraic_T(fn1.nmd ** q, fn2.nmd ** q) ** (1 / q)
    return newFN


def einsteinMultiply(fn1: QrungFN, fn2: QrungFN):
    """
        Einstein multiplication of two FNs
    """
    assert fn1.qrung == fn2.qrung, 'ERROR:the two FNs are not the same FN'
    q = fn1.qrung
    newFN = QrungFN(q, 0, 0)
    newFN.md = einstein_T(fn1.md ** q, fn2.md ** q) ** (1 / q)
    newFN.nmd = einstein_S(fn1.nmd ** q, fn2.nmd ** q) ** (1 / q)
    return newFN


def einsteinPlus(fn1: QrungFN, fn2: QrungFN):
    """
        Einstein addition of two FNs
    """
    assert fn1.qrung == fn2.qrung, 'ERROR:the two FNs are not the same FN'
    q = fn1.qrung
    newFN = QrungFN(q, 0, 0)
    newFN.md = einstein_S(fn1.md ** q, fn2.md ** q) ** (1 / q)
    newFN.nmd = einstein_T(fn1.nmd ** q, fn2.nmd ** q) ** (1 / q)
    return newFN
