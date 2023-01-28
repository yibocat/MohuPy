from .QrungIVFNs import QrungIVFN
from .archimedean import *


def algebraicMultiply(ivfn1: QrungIVFN, ivfn2: QrungIVFN):
    """
        Multiplies two QrungIVFNs by the algebraic T and S functions.

        Parameters
        ----------
        ivfn1 : QrungIVFN
            The first QrungIVFN.
        ivfn2 : QrungIVFN
            The second QrungIVFN.
    """
    assert ivfn1.qrung == ivfn2.qrung, 'ERROR: The two QrungIVFNs are not the same QrungIVFN!'
    q = ivfn1.qrung
    newIVFN = QrungIVFN(q, 0, 0, 0, 0)
    newIVFN.mdl = algebraic_T(ivfn1.mdl ** q, ivfn2.mdl ** q) ** (1 / q)
    newIVFN.mdu = algebraic_T(ivfn1.mdu ** q, ivfn2.mdu ** q) ** (1 / q)
    newIVFN.nmdl = algebraic_S(ivfn1.nmdl ** q, ivfn2.nmdl ** q) ** (1 / q)
    newIVFN.nmdu = algebraic_S(ivfn1.nmdu ** q, ivfn2.nmdu ** q) ** (1 / q)
    return newIVFN


def algebraicPlus(ivfn1: QrungIVFN, ivfn2: QrungIVFN):
    """
        Adds two QrungIVFNs by the algebraic T and S functions.

        Parameters
        ----------
        ivfn1 : QrungIVFN
            The first QrungIVFN.
        ivfn2 : QrungIVFN
            The second QrungIVFN.
    """
    assert ivfn1.qrung == ivfn2.qrung, 'ERROR: The two QrungIVFNs are not the same QrungIVFN!'
    q = ivfn1.qrung
    newIVFN = QrungIVFN(q, 0, 0, 0, 0)
    newIVFN.mdl = algebraic_S(ivfn1.mdl ** q, ivfn2.mdl ** q) ** (1 / q)
    newIVFN.mdu = algebraic_S(ivfn1.mdu ** q, ivfn2.mdu ** q) ** (1 / q)
    newIVFN.nmdl = algebraic_T(ivfn1.nmdl ** q, ivfn2.nmdl ** q) ** (1 / q)
    newIVFN.nmdu = algebraic_T(ivfn1.nmdu ** q, ivfn2.nmdu ** q) ** (1 / q)
    return newIVFN


def einsteinMultiply(ivfn1: QrungIVFN, ivfn2: QrungIVFN):
    """
        Multiplies two QrungIVFNs by the einstein T and S functions.

        Parameters
        ----------
        ivfn1 : QrungIVFN
            The first QrungIVFN.
        ivfn2 : QrungIVFN
            The second QrungIVFN.
    """
    assert ivfn1.qrung == ivfn2.qrung, 'ERROR: The two QrungIVFNs are not the same QrungIVFN!'
    q = ivfn1.qrung
    newIVFN = QrungIVFN(q, 0, 0, 0, 0)
    newIVFN.mdl = einstein_T(ivfn1.mdl ** q, ivfn2.mdl ** q) ** (1 / q)
    newIVFN.mdu = einstein_T(ivfn1.mdu ** q, ivfn2.mdu ** q) ** (1 / q)
    newIVFN.nmdl = einstein_S(ivfn1.nmdl ** q, ivfn2.nmdl ** q) ** (1 / q)
    newIVFN.nmdu = einstein_S(ivfn1.nmdu ** q, ivfn2.nmdu ** q) ** (1 / q)
    return newIVFN


def einsteinPlus(ivfn1: QrungIVFN, ivfn2: QrungIVFN):
    """
        Adds two QrungIVFNs by the einstein T and S functions.

        Parameters
        ----------
        ivfn1 : QrungIVFN
            The first QrungIVFN.
        ivfn2 : QrungIVFN
            The second QrungIVFN.
    """
    assert ivfn1.qrung == ivfn2.qrung, 'ERROR: The two QrungIVFNs are not the same QrungIVFN!'
    q = ivfn1.qrung
    newIVFN = QrungIVFN(q, 0, 0, 0, 0)
    newIVFN.mdl = einstein_S(ivfn1.mdl ** q, ivfn2.mdl ** q) ** (1 / q)
    newIVFN.mdu = einstein_S(ivfn1.mdu ** q, ivfn2.mdu ** q) ** (1 / q)
    newIVFN.nmdl = einstein_T(ivfn1.nmdl ** q, ivfn2.nmdl ** q) ** (1 / q)
    newIVFN.nmdu = einstein_T(ivfn1.nmdu ** q, ivfn2.nmdu ** q) ** (1 / q)
    return newIVFN
