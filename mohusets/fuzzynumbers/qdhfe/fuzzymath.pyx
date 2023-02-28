#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/21 上午4:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets

import numpy as np

from .fuzzy_element import qrungdhfe
from ..archimedean cimport algebraic_T, algebraic_S, einstein_S, einstein_T

cpdef intersection(dh1: qrungdhfe, dh2: qrungdhfe):
    assert dh1.qrung == dh2.qrung, 'ERROR! The two DHFEs are not the same DHFE !'
    q = dh1.qrung
    newDHFE = qrungdhfe(q, [], [])
    md_min = min(max(dh1.md), max(dh2.md))
    nmd_max = max(min(dh1.nmd), min(dh2.nmd))

    md1 = dh1.md[dh1.md <= md_min]
    md2 = dh2.md[dh2.md <= md_min]
    newDHFE.set_md(np.unique(np.concatenate((md1, md2))))

    nmd1 = dh1.nmd[dh1.nmd >= nmd_max]
    nmd2 = dh2.nmd[dh2.nmd >= nmd_max]
    newDHFE.set_nmd(np.unique(np.concatenate((nmd1, nmd2))))

    return newDHFE


cpdef unions(dh1: qrungdhfe, dh2: qrungdhfe):
    """
        unions of two DHFEs
        :param dh1: DHFE 1
        :param dh2: DHFE 2
        :return: DHFE
    """
    assert dh1.qrung == dh2.qrung, 'ERROR! The two DHFEs are not the same DHFE!'
    q = dh1.qrung
    newDHFE = qrungdhfe(q, [], [])
    md_max = max(min(dh1.md), min(dh2.md))
    nmd_min = min(max(dh1.nmd), max(dh2.nmd))

    md1 = dh1.md[dh1.md >= md_max]
    md2 = dh2.md[dh2.md >= md_max]
    newDHFE.set_md(np.unique(np.concatenate((md1, md2))))

    nmd1 = dh1.nmd[dh1.nmd <= nmd_min]
    nmd2 = dh2.nmd[dh2.nmd <= nmd_min]
    newDHFE.set_nmd(np.unique(np.concatenate((nmd1, nmd2))))

    return newDHFE


cpdef algeb_multiply(dh1: qrungdhfe, dh2: qrungdhfe):
    """
        Algebraic multiplication of two DHFEs
        :param dh1: DHFE 1
        :param dh2: DHFE 2
        :return: DHFE
    """
    assert dh1.qrung == dh2.qrung, 'ERROR! The two DHFEs are not the same DHFE!'
    q = dh1.qrung
    newDHFE = qrungdhfe(q, [], [])

    mds = np.array(np.meshgrid(dh1.md, dh2.md)).T.reshape(-1, 2)
    nmds = np.array(np.meshgrid(dh1.nmd, dh2.nmd)).T.reshape(-1, 2)

    for i in range(len(mds)):
        newDHFE.set_md(np.append(newDHFE.md, algebraic_T(mds[i, 0] ** q, mds[i, 1] ** q) ** (1 / q)))
    for i in range(len(nmds)):
        newDHFE.set_nmd(np.append(newDHFE.nmd, algebraic_S(nmds[i, 0] ** q, nmds[i, 1] ** q) ** (1 / q)))

    return newDHFE


cpdef algeb_plus(dh1: qrungdhfe, dh2: qrungdhfe):
    """
        Algebraic addition of two DHFEs
        :param dh1: DHFE 1
        :param dh2: DHFE 2
        :return: DHFE
    """
    assert dh1.qrung == dh2.qrung, 'ERROR! The two DHFEs are not the same DHFE!'
    q = dh1.qrung
    newDHFE = qrungdhfe(q, [], [])

    mds = np.array(np.meshgrid(dh1.md, dh2.md)).T.reshape(-1, 2)
    nmds = np.array(np.meshgrid(dh1.nmd, dh2.nmd)).T.reshape(-1, 2)

    for i in range(len(mds)):
        newDHFE.set_md(np.append(newDHFE.md, algebraic_S(mds[i, 0] ** q, mds[i, 1] ** q) ** (1 / q)))
    for i in range(len(nmds)):
        newDHFE.set_nmd(np.append(newDHFE.nmd, algebraic_T(nmds[i, 0] ** q, nmds[i, 1] ** q) ** (1 / q)))

    return newDHFE


cpdef eins_multiply(dh1: qrungdhfe, dh2: qrungdhfe):
    """
        Einstein multiplication of two DHFEs
        :param dh1: DHFE 1
        :param dh2: DHFE 2
        :return: DHFE
    """
    assert dh1.qrung == dh2.qrung, 'ERROR! The two DHFEs are not the same DHFE!'
    q = dh1.qrung
    newDHFE = qrungdhfe(q, [], [])

    mds = np.array(np.meshgrid(dh1.md, dh2.md)).T.reshape(-1, 2)
    nmds = np.array(np.meshgrid(dh1.nmd, dh2.nmd)).T.reshape(-1, 2)

    for i in range(len(mds)):
        newDHFE.set_md(np.append(newDHFE.md, einstein_T(mds[i, 0] ** q, mds[i, 1] ** q) ** (1 / q)))
    for i in range(len(nmds)):
        newDHFE.set_nmd(np.append(newDHFE.nmd, einstein_S(nmds[i, 0] ** q, nmds[i, 1] ** q) ** (1 / q)))

    return newDHFE


cpdef eins_plus(dh1: qrungdhfe, dh2: qrungdhfe):
    """
        Einstein addition of two DHFEs
        :param dh1: DHFE 1
        :param dh2: DHFE 2
        :return: DHFE
    """
    assert dh1.qrung == dh2.qrung, 'ERROR! The two DHFEs are not the same DHFE!'
    q = dh1.qrung
    newDHFE = qrungdhfe(q, [], [])

    mds = np.array(np.meshgrid(dh1.md, dh2.md)).T.reshape(-1, 2)
    nmds = np.array(np.meshgrid(dh1.nmd, dh2.nmd)).T.reshape(-1, 2)

    for i in range(len(mds)):
        newDHFE.set_md(np.append(newDHFE.md, einstein_S(mds[i, 0] ** q, mds[i, 1] ** q) ** (1 / q)))
    for i in range(len(nmds)):
        newDHFE.set_nmd(np.append(newDHFE.nmd, einstein_T(nmds[i, 0] ** q, nmds[i, 1] ** q) ** (1 / q)))

    return newDHFE
