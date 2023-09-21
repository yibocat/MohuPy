#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/21 上午4:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets

from .fuzzy_element import qrungivfn
from ..archimedean cimport einstein_T, einstein_S, algebraic_T, algebraic_S

cpdef intersection(ivfn1: qrungivfn, ivfn2: qrungivfn):
    assert ivfn1.qrung == ivfn2.qrung, 'ERROR: The two QrungIVFNs are not the same qrungivfn!'
    q = ivfn1.qrung
    newIVFN = qrungivfn(q, [0., 0.], [0., 0.])
    newIVFN.set_md([min(ivfn1.md[0], ivfn2.md[0]),
                    min(ivfn1.md[1], ivfn2.md[1])])
    newIVFN.set_nmd([max(ivfn1.nmd[0], ivfn2.nmd[0]),
                     max(ivfn1.nmd[1], ivfn2.nmd[1])])
    assert newIVFN.isLegal(),'The data calculation result is invalid'
    # newIVFN.md[0] = min(ivfn1.md[0], ivfn2.md[0])
    # newIVFN.md[1] = min(ivfn1.md[1], ivfn2.md[1])
    # newIVFN.nmd[0] = max(ivfn1.nmd[0], ivfn2.nmd[0])
    # newIVFN.nmd[1] = max(ivfn1.nmd[1], ivfn2.nmd[1])
    return newIVFN

cpdef unions(ivfn1: qrungivfn, ivfn2: qrungivfn):
    assert ivfn1.qrung == ivfn2.qrung, 'ERROR: The two QrungIVFNs are not the same qrungivfn!'
    q = ivfn1.qrung
    newIVFN = qrungivfn(q, [0., 0.], [0., 0.])
    newIVFN.set_md([max(ivfn1.md[0], ivfn2.md[0]),
                    max(ivfn1.md[1], ivfn2.md[1])])
    newIVFN.set_nmd([min(ivfn1.nmd[0], ivfn2.nmd[0]),
                     min(ivfn1.nmd[1], ivfn2.nmd[1])])
    assert newIVFN.isLegal(),'The data calculation result is invalid'
    # newIVFN.md[0] = max(ivfn1.md[0], ivfn2.md[0])
    # newIVFN.md[1] = max(ivfn1.md[1], ivfn2.md[1])
    # newIVFN.nmd[0] = min(ivfn1.nmd[0], ivfn2.nmd[0])
    # newIVFN.nmd[1] = min(ivfn1.nmd[1], ivfn2.nmd[1])
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
    newIVFN.set_md([algebraic_T(ivfn1.md[0] ** q, ivfn2.md[0] ** q) ** (1 / q),
                    algebraic_T(ivfn1.md[1] ** q, ivfn2.md[1] ** q) ** (1 / q)])
    newIVFN.set_nmd([algebraic_S(ivfn1.nmd[0] ** q, ivfn2.nmd[0] ** q) ** (1 / q),
                     algebraic_S(ivfn1.nmd[1] ** q, ivfn2.nmd[1] ** q) ** (1 / q)])
    assert newIVFN.isLegal(),'The data calculation result is invalid'
    # newIVFN.md[0] = algebraic_T(ivfn1.md[0] ** q, ivfn2.md[0] ** q) ** (1 / q)
    # newIVFN.md[1] = algebraic_T(ivfn1.md[1] ** q, ivfn2.md[1] ** q) ** (1 / q)
    # newIVFN.nmd[0] = algebraic_S(ivfn1.nmd[0] ** q, ivfn2.nmd[0] ** q) ** (1 / q)
    # newIVFN.nmd[1] = algebraic_S(ivfn1.nmd[1] ** q, ivfn2.nmd[1] ** q) ** (1 / q)
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
    newIVFN.set_md([algebraic_S(ivfn1.md[0] ** q, ivfn2.md[0] ** q) ** (1 / q),
                    algebraic_S(ivfn1.md[1] ** q, ivfn2.md[1] ** q) ** (1 / q)])
    newIVFN.set_nmd([algebraic_T(ivfn1.nmd[0] ** q, ivfn2.nmd[0] ** q) ** (1 / q),
                     algebraic_T(ivfn1.nmd[1] ** q, ivfn2.nmd[1] ** q) ** (1 / q)])
    assert newIVFN.isLegal(),'The data calculation result is invalid'
    # newIVFN.md[0] = algebraic_S(ivfn1.md[0] ** q, ivfn2.md[0] ** q) ** (1 / q)
    # newIVFN.md[1] = algebraic_S(ivfn1.md[1] ** q, ivfn2.md[1] ** q) ** (1 / q)
    # newIVFN.nmd[0] = algebraic_T(ivfn1.nmd[0] ** q, ivfn2.nmd[0] ** q) ** (1 / q)
    # newIVFN.nmd[1] = algebraic_T(ivfn1.nmd[1] ** q, ivfn2.nmd[1] ** q) ** (1 / q)
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
    newIVFN.set_md([einstein_T(ivfn1.md[0] ** q, ivfn2.md[0] ** q) ** (1 / q),
                    einstein_T(ivfn1.md[1] ** q, ivfn2.md[1] ** q) ** (1 / q)])
    newIVFN.set_nmd([einstein_S(ivfn1.nmd[0] ** q, ivfn2.nmd[0] ** q) ** (1 / q),
                     einstein_S(ivfn1.nmd[1] ** q, ivfn2.nmd[1] ** q) ** (1 / q)])
    assert newIVFN.isLegal(),'The data calculation result is invalid'
    # newIVFN.md[0] = einstein_T(ivfn1.md[0] ** q, ivfn2.md[0] ** q) ** (1 / q)
    # newIVFN.md[1] = einstein_T(ivfn1.md[1] ** q, ivfn2.md[1] ** q) ** (1 / q)
    # newIVFN.nmd[0] = einstein_S(ivfn1.nmd[0] ** q, ivfn2.nmd[0] ** q) ** (1 / q)
    # newIVFN.nmd[1] = einstein_S(ivfn1.nmd[1] ** q, ivfn2.nmd[1] ** q) ** (1 / q)
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
    newIVFN.set_md([einstein_S(ivfn1.md[0] ** q, ivfn2.md[0] ** q) ** (1 / q),
                    einstein_S(ivfn1.md[1] ** q, ivfn2.md[1] ** q) ** (1 / q)])
    newIVFN.set_nmd([einstein_T(ivfn1.nmd[0] ** q, ivfn2.nmd[0] ** q) ** (1 / q),
                     einstein_T(ivfn1.nmd[1] ** q, ivfn2.nmd[1] ** q) ** (1 / q)])
    assert newIVFN.isLegal(),'The data calculation result is invalid'
    # newIVFN.md[0] = einstein_S(ivfn1.md[0] ** q, ivfn2.md[0] ** q) ** (1 / q)
    # newIVFN.md[1] = einstein_S(ivfn1.md[1] ** q, ivfn2.md[1] ** q) ** (1 / q)
    # newIVFN.nmd[0] = einstein_T(ivfn1.nmd[0] ** q, ivfn2.nmd[0] ** q) ** (1 / q)
    # newIVFN.nmd[1] = einstein_T(ivfn1.nmd[1] ** q, ivfn2.nmd[1] ** q) ** (1 / q)
    return newIVFN
