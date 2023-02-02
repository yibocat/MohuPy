#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/1 下午5:37
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzyKit
import re

import numpy as np
from .qrungivfn import qrungivfn


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


def str_to_ivfn(s, q):
    """
        Convert input data to interval-valued fuzzy number.
        Note: When the input data is 0, it should be set to 0.

        Q-rung Interval-valued fuzzy convert function accepts the form:
        [[x,x],[x,x]]

        Parameters
        ----------
        s : str
            Input data.
        q : int
            Q-rung

        Returns
        -------
        ivf : IVFNumbers
    """
    ivf = qrungivfn(q, [0., 0.], [0., 0.])
    t1 = re.findall(r'},\{|],\[|},\[|],\{', s)
    assert ('},{' not in t1) and ('],{' not in t1) and ('},[' not in t1) and (len(t1) == 1), 'ERROR: data format error.'
    t2 = re.findall(r'\[(\d.*?\d)]', s)
    assert len(t2) == 2, 'ERROR: data format error.'
    md = re.findall(r'\d.?\d*', t2[0])
    nmd = re.findall(r'\d.?\d*', t2[1])
    assert len(md) == 2 and len(nmd) == 2, 'ERROR: data format error.'

    ivf.md[0] = np.asarray(float(md[0]))
    ivf.md[1] = np.asarray(float(md[1]))
    ivf.nmd[0] = np.asarray(float(nmd[0]))
    ivf.nmd[1] = np.asarray(float(nmd[1]))
    assert ivf.isLegal(), 'Invalid data! Illegal Q-rung interval-valued fuzzy number.'
    return ivf


def one(q):
    return qrungivfn(q, [1., 1.], [0., 0.])


def zero(q):
    return qrungivfn(q, [0., 0.], [0., 0.])


def minusone(q):
    return qrungivfn(q, [0., 0.], [1., 1.])
