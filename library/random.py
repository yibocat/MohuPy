#  Copyright (c) yibocat 2023 All Rights Reserved
#  Date: 2023/1/30 下午12:54
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzyKit
import numpy as np
from fuzzyelement.FNumbers import qrungfn
from fuzzyelement.DHFElements import qrunghfe
from fuzzyelement.IVFNumbers import qrungivfn


def randomFN(q):
    """
        Generate a randomQHF Q-rung fuzzy number.

        Args:
            q (float): the q-rung number.
        Returns:
            FNumbers
    """
    md = np.random.rand(1)[0]
    nmd = np.random.rand(1)[0]
    newFN = qrungfn(q, 0., 0.)
    newFN.md = md
    newFN.nmd = nmd
    if newFN.isLegal():
        return newFN
    else:
        return randomFN(q)


def randomIVFN(q):
    """
        Generate a randomQHF Q-rung interval-valued fuzzy number
        Parameters:
            q : int
                The Q-rung number

        Returns:
            IVFNumbers
    """
    mdl, mdu = np.random.rand(1)[0], np.random.rand(1)[0]
    nmdl, nmdu = np.random.rand(1)[0], np.random.rand(1)[0]
    newIVFN = qrungivfn(q, [0., 0.], [0., 0.])
    newIVFN.md[0], newIVFN.md[1] = mdl, mdu
    newIVFN.nmd[0], newIVFN.nmd[1] = nmdl, nmdu
    if newIVFN.isLegal():
        return newIVFN
    else:
        return randomIVFN(q)


def randomQHF(q, n=5):
    """
        Generate a randomQHF Q-rung hesitant fuzzy element
        Parameters:
            q : int
                The Q-rung number
            n : int
                n represents the maximum randomQHF number of generated numbers, the default is 5.
        Returns:
            DHFElements
    """
    md = np.random.rand(np.random.randint(1, n))
    nmd = np.random.rand(np.random.randint(1, n))
    newHFE = qrunghfe(q, [], [])
    newHFE.md = md
    newHFE.nmd = nmd
    if newHFE.isLegal():
        return newHFE
    else:
        return randomQHF(q, n)
