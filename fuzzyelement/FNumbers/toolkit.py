#  Copyright (c) yibocat 2023 All Rights Reserved
#  Date: 2023/1/31 下午5:09
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzyKit
import re

import numpy as np
from .qrungfn import qrungfn


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


def str_to_fn(s, q):
    """
        Convert input data to fuzzy number.
        Note: When the input data is 0, it should be set to 0.

        Q-rung fuzzy convert function accepts the form:
        [x,x]

        Parameters
        ----------
            s : str
                Input data.
            q : int
                Q-rung

        Returns
        -------
            fnf : FNumbers
    """
    fnf = qrungfn(q, 0., 0.)
    t = re.findall(r'^\[(\d.*?\d)]$', s)
    assert len(t) == 1, 'ERROR: data format error.'
    x = re.findall(r'\d.?\d*', t[0])
    assert len(x) == 2, 'ERROR: data format error.'
    fnf.md = np.asarray(float(x[0]))
    fnf.nmd = np.asarray(float(x[1]))
    assert fnf.isLegal(), 'ERROR: The data format is correct, but the data is invalid.'
    return fnf
