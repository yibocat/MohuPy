#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/1 下午5:37
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzyKit

from .qrungivfn import qrungivfn
from .archimedean import *


def algebraicmultiplication(ivfn1: qrungivfn, ivfn2: qrungivfn):
    """
        Multiplies two QrungIVFNs by the algebraic T and S functions.

        Parameters
        ----------
        ivfn1 : qrungivfn
            The first QrungIVFN.
        ivfn2 : qrungivfn
            The second QrungIVFN.
    """
    assert ivfn1.qrung == ivfn2.qrung, 'ERROR: The two QrungIVFNs are not the same qrungivfn!'
    q = ivfn1.qrung
    newIVFN = qrungivfn(q, [0., 0.], [0., 0.])
    newIVFN.md[0] = algebraic_T(ivfn1.md[0] ** q, ivfn2.md[0] ** q) ** (1 / q)
    newIVFN.md[1] = algebraic_T(ivfn1.md[1] ** q, ivfn2.md[1] ** q) ** (1 / q)
    newIVFN.nmd[0] = algebraic_S(ivfn1.nmd[0] ** q, ivfn2.nmd[0] ** q) ** (1 / q)
    newIVFN.nmd[1] = algebraic_S(ivfn1.nmd[1] ** q, ivfn2.nmd[1] ** q) ** (1 / q)
    return newIVFN


def algebraicplus(ivfn1: qrungivfn, ivfn2: qrungivfn):
    """
        Adds two QrungIVFNs by the algebraic T and S functions.

        Parameters
        ----------
        ivfn1 : qrungivfn
            The first QrungIVFN.
        ivfn2 : qrungivfn
            The second QrungIVFN.
    """
    assert ivfn1.qrung == ivfn2.qrung, 'ERROR: The two QrungIVFNs are not the same qrungivfn!'
    q = ivfn1.qrung
    newIVFN = qrungivfn(q, [0., 0.], [0., 0.])
    newIVFN.md[0] = algebraic_S(ivfn1.md[0] ** q, ivfn2.md[0] ** q) ** (1 / q)
    newIVFN.md[1] = algebraic_S(ivfn1.md[1] ** q, ivfn2.md[1] ** q) ** (1 / q)
    newIVFN.nmd[0] = algebraic_T(ivfn1.nmd[0] ** q, ivfn2.nmd[0] ** q) ** (1 / q)
    newIVFN.nmd[1] = algebraic_T(ivfn1.nmd[1] ** q, ivfn2.nmd[1] ** q) ** (1 / q)
    return newIVFN


def einsteinmultiplication(ivfn1: qrungivfn, ivfn2: qrungivfn):
    """
        Multiplies two QrungIVFNs by the einstein T and S functions.

        Parameters
        ----------
        ivfn1 : qrungivfn
            The first QrungIVFN.
        ivfn2 : qrungivfn
            The second QrungIVFN.
    """
    assert ivfn1.qrung == ivfn2.qrung, 'ERROR: The two QrungIVFNs are not the same qrungivfn!'
    q = ivfn1.qrung
    newIVFN = qrungivfn(q, [0., 0.], [0., 0.])
    newIVFN.md[0] = einstein_T(ivfn1.md[0] ** q, ivfn2.md[0] ** q) ** (1 / q)
    newIVFN.md[1] = einstein_T(ivfn1.md[1] ** q, ivfn2.md[1] ** q) ** (1 / q)
    newIVFN.nmd[0] = einstein_S(ivfn1.nmd[0] ** q, ivfn2.nmd[0] ** q) ** (1 / q)
    newIVFN.nmd[1] = einstein_S(ivfn1.nmd[1] ** q, ivfn2.nmd[1] ** q) ** (1 / q)
    return newIVFN


def einsteinplus(ivfn1: qrungivfn, ivfn2: qrungivfn):
    """
        Adds two QrungIVFNs by the einstein T and S functions.

        Parameters
        ----------
        ivfn1 : qrungivfn
            The first QrungIVFN.
        ivfn2 : qrungivfn
            The second QrungIVFN.
    """
    assert ivfn1.qrung == ivfn2.qrung, 'ERROR: The two QrungIVFNs are not the same qrungivfn!'
    q = ivfn1.qrung
    newIVFN = qrungivfn(q, [0., 0.], [0., 0.])
    newIVFN.md[0] = einstein_S(ivfn1.md[0] ** q, ivfn2.md[0] ** q) ** (1 / q)
    newIVFN.md[1] = einstein_S(ivfn1.md[1] ** q, ivfn2.md[1] ** q) ** (1 / q)
    newIVFN.nmd[0] = einstein_T(ivfn1.nmd[0] ** q, ivfn2.nmd[0] ** q) ** (1 / q)
    newIVFN.nmd[1] = einstein_T(ivfn1.nmd[1] ** q, ivfn2.nmd[1] ** q) ** (1 / q)
    return newIVFN
