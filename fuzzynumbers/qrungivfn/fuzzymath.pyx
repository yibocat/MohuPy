from .qrungivfn import qrungivfn
from fuzzynumbers.archimedean import *

cpdef intersection(ivfn1: qrungivfn, ivfn2: qrungivfn):
    assert ivfn1.qrung == ivfn2.qrung, 'ERROR: The two QrungIVFNs are not the same qrungivfn!'
    q = ivfn1.qrung
    newIVFN = qrungivfn(q, [0., 0.], [0., 0.])
    newIVFN.md[0] = min(ivfn1.md[0], ivfn2.md[0])
    newIVFN.md[1] = min(ivfn1.md[1], ivfn2.md[1])
    newIVFN.nmd[0] = max(ivfn1.nmd[0], ivfn2.nmd[0])
    newIVFN.nmd[1] = max(ivfn1.nmd[1], ivfn2.nmd[1])
    return newIVFN

cpdef unions(ivfn1: qrungivfn, ivfn2: qrungivfn):
    assert ivfn1.qrung == ivfn2.qrung, 'ERROR: The two QrungIVFNs are not the same qrungivfn!'
    q = ivfn1.qrung
    newIVFN = qrungivfn(q, [0., 0.], [0., 0.])
    newIVFN.md[0] = max(ivfn1.md[0], ivfn2.md[0])
    newIVFN.md[1] = max(ivfn1.md[1], ivfn2.md[1])
    newIVFN.nmd[0] = min(ivfn1.nmd[0], ivfn2.nmd[0])
    newIVFN.nmd[1] = min(ivfn1.nmd[1], ivfn2.nmd[1])
    return newIVFN


cpdef algeb_multiply(ivfn1: qrungivfn, ivfn2: qrungivfn):
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


cpdef algeb_plus(ivfn1: qrungivfn, ivfn2: qrungivfn):
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


cpdef eins_multiply(ivfn1: qrungivfn, ivfn2: qrungivfn):
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


cpdef eins_plus(ivfn1: qrungivfn, ivfn2: qrungivfn):
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
