#  Copyright (c) yibocat 2023 All Rights Reserved
#  Date: 2023/1/30 下午12:54
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzyKit
import numpy as np
from FNumbers import qrungfn


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
    newFN = qrungfn(q, 0, 0)
    newFN.md = md
    newFN.nmd = nmd
    if newFN.isLegal():
        return newFN
    else:
        return randomFN(q)
