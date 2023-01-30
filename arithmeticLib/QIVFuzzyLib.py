#  Copyright (c) yibocat 2023 All Rights Reserved
#  Date: 2023/1/30 下午12:54
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzyKit
import numpy as np
from IVFNumbers import qrungivfn


def randomIVFN(q):
    """
        Generate a randomQHF Q-rung interval-valued fuzzy number
        Parameters
        ----------
            q : int
                The Q-rung number

        Returns
        -------
            IVFNumbers
    """
    mdl = np.random.rand(1)[0]
    mdu = np.random.rand(1)[0]
    nmdl = np.random.rand(1)[0]
    nmdu = np.random.rand(1)[0]
    newIVFN = qrungivfn(q, 0, 0, 0, 0)
    newIVFN.mdl, newIVFN.mdu = mdl, mdu
    newIVFN.nmdl, newIVFN.nmdu = nmdl, nmdu
    if newIVFN.isLegal():
        return newIVFN
    else:
        return randomIVFN(q)
