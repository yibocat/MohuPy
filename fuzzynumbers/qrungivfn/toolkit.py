import re

import numpy as np

from .qrungivfn import qrungivfn


def random(q):
    """
        Generate a randomQHF Q-rung interval-valued fuzzy number
        Parameters:
            q : int
                The Q-rung number

        Returns:
            IVFNumbers
    """
    newf = qrungivfn(q, [0., 0.], [0., 0.])
    newf.md[0], newf.md[1] = np.random.rand(1)[0], np.random.rand(1)[0]
    newf.nmd[0], newf.nmd[1] = np.random.rand(1)[0], np.random.rand(1)[0]
    while not newf.isLegal():
        newf.md[0], newf.md[1] = np.random.rand(1)[0], np.random.rand(1)[0]
        newf.nmd[0], newf.nmd[1] = np.random.rand(1)[0], np.random.rand(1)[0]
    return newf


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


def pos(q):
    return qrungivfn(q, [1., 1.], [0., 0.])


def neg(q):
    return qrungivfn(q, [0., 0.], [1., 1.])


def zero(q):
    return qrungivfn(q, [0., 0.], [0., 0.])
