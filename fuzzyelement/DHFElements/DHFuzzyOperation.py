from .qrunghfe import qrunghfe
from .archimedean import *
import numpy as np


def intersection(dh1: qrunghfe, dh2: qrunghfe):
    """
        intersection of two DHFEs
        :param dh1: DHFE 1
        :param dh2: DHFE 2
        :return: DHFE
    """
    assert dh1.qrung == dh2.qrung, 'ERROR! The two DHFEs are not the same DHFE !'
    q = dh1.qrung
    newDHFE = qrunghfe(q, [], [])
    md_min = min(max(dh1.md), max(dh2.md))
    nmd_max = max(min(dh1.nmd), min(dh2.nmd))

    md1 = dh1.md[dh1.md <= md_min]
    md2 = dh2.md[dh2.md <= md_min]
    newDHFE.md = np.unique(np.concatenate((md1, md2)))

    nmd1 = dh1.nmd[dh1.nmd >= nmd_max]
    nmd2 = dh2.nmd[dh2.nmd >= nmd_max]
    newDHFE.nmd = np.unique(np.concatenate((nmd1, nmd2)))

    return newDHFE


def unions(dh1: qrunghfe, dh2: qrunghfe):
    """
        unions of two DHFEs
        :param dh1: DHFE 1
        :param dh2: DHFE 2
        :return: DHFE
    """
    assert dh1.qrung == dh2.qrung, 'ERROR! The two DHFEs are not the same DHFE!'
    q = dh1.qrung
    newDHFE = qrunghfe(q, [], [])
    md_max = max(min(dh1.md), min(dh2.md))
    nmd_min = min(max(dh1.nmd), max(dh2.nmd))

    md1 = dh1.md[dh1.md >= md_max]
    md2 = dh2.md[dh2.md >= md_max]
    newDHFE.md = np.unique(np.concatenate((md1, md2)))

    nmd1 = dh1.nmd[dh1.nmd <= nmd_min]
    nmd2 = dh2.nmd[dh2.nmd <= nmd_min]
    newDHFE.nmd = np.unique(np.concatenate((nmd1, nmd2)))

    return newDHFE


def algebraicmultiplication(dh1: qrunghfe, dh2: qrunghfe):
    """
        Algebraic multiplication of two DHFEs
        :param dh1: DHFE 1
        :param dh2: DHFE 2
        :return: DHFE
    """
    assert dh1.qrung == dh2.qrung, 'ERROR! The two DHFEs are not the same DHFE!'
    q = dh1.qrung
    newDHFE = qrunghfe(q, [], [])

    mds = np.array(np.meshgrid(dh1.md, dh2.md)).T.reshape(-1, 2)
    nmds = np.array(np.meshgrid(dh1.nmd, dh2.nmd)).T.reshape(-1, 2)

    for i in range(len(mds)):
        newDHFE.md = np.append(newDHFE.md, algebraic_T(mds[i, 0] ** q, mds[i, 1] ** q) ** (1 / q))
    for i in range(len(nmds)):
        newDHFE.nmd = np.append(newDHFE.nmd, algebraic_S(nmds[i, 0] ** q, nmds[i, 1] ** q) ** (1 / q))

    return newDHFE


def algebraicplus(dh1: qrunghfe, dh2: qrunghfe):
    """
        Algebraic addition of two DHFEs
        :param dh1: DHFE 1
        :param dh2: DHFE 2
        :return: DHFE
    """
    assert dh1.qrung == dh2.qrung, 'ERROR! The two DHFEs are not the same DHFE!'
    q = dh1.qrung
    newDHFE = qrunghfe(q, [], [])

    mds = np.array(np.meshgrid(dh1.md, dh2.md)).T.reshape(-1, 2)
    nmds = np.array(np.meshgrid(dh1.nmd, dh2.nmd)).T.reshape(-1, 2)

    for i in range(len(mds)):
        newDHFE.md = np.append(newDHFE.md, algebraic_S(mds[i, 0] ** q, mds[i, 1] ** q) ** (1 / q))
    for i in range(len(nmds)):
        newDHFE.nmd = np.append(newDHFE.nmd, algebraic_T(nmds[i, 0] ** q, nmds[i, 1] ** q) ** (1 / q))

    return newDHFE


def einsteinmultiplication(dh1: qrunghfe, dh2: qrunghfe):
    """
        Einstein multiplication of two DHFEs
        :param dh1: DHFE 1
        :param dh2: DHFE 2
        :return: DHFE
    """
    assert dh1.qrung == dh2.qrung, 'ERROR! The two DHFEs are not the same DHFE!'
    q = dh1.qrung
    newDHFE = qrunghfe(q, [], [])

    mds = np.array(np.meshgrid(dh1.md, dh2.md)).T.reshape(-1, 2)
    nmds = np.array(np.meshgrid(dh1.nmd, dh2.nmd)).T.reshape(-1, 2)

    for i in range(len(mds)):
        newDHFE.md = np.append(newDHFE.md, einstein_T(mds[i, 0] ** q, mds[i, 1] ** q) ** (1 / q))
    for i in range(len(nmds)):
        newDHFE.nmd = np.append(newDHFE.nmd, einstein_S(nmds[i, 0] ** q, nmds[i, 1] ** q) ** (1 / q))

    return newDHFE


def einsteinplus(dh1: qrunghfe, dh2: qrunghfe):
    """
        Einstein addition of two DHFEs
        :param dh1: DHFE 1
        :param dh2: DHFE 2
        :return: DHFE
    """
    assert dh1.qrung == dh2.qrung, 'ERROR! The two DHFEs are not the same DHFE!'
    q = dh1.qrung
    newDHFE = qrunghfe(q, [], [])

    mds = np.array(np.meshgrid(dh1.md, dh2.md)).T.reshape(-1, 2)
    nmds = np.array(np.meshgrid(dh1.nmd, dh2.nmd)).T.reshape(-1, 2)

    for i in range(len(mds)):
        newDHFE.md = np.append(newDHFE.md, einstein_S(mds[i, 0] ** q, mds[i, 1] ** q) ** (1 / q))
    for i in range(len(nmds)):
        newDHFE.nmd = np.append(newDHFE.nmd, einstein_T(nmds[i, 0] ** q, nmds[i, 1] ** q) ** (1 / q))

    return newDHFE
