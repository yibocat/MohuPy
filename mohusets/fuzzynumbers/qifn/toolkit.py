#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/21 上午4:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets

import re

import numpy as np
from .fuzzy_element import qrungifn


def random(q: int):
    """
        Generate a randomQHF Q-rung fuzzy number.

        Args:
            q (float): the q-rung number.
        Returns:
            FNumbers
    """
    newf = qrungifn(q, 0., 0.)
    newf.set_md(np.random.rand(1))
    newf.set_nmd(np.random.rand(1))
    while not newf.isLegal():
        newf.set_md(np.random.rand(1))
        newf.set_nmd(np.random.rand(1))
    return newf


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
    fnf = qrungifn(q, 0., 0.)
    t = re.findall(r'^\[(\d.*?\d)]$', s)
    assert len(t) == 1, 'ERROR: data format error.'
    x = re.findall(r'\d.?\d*', t[0])
    assert len(x) == 2, 'ERROR: data format error.'
    fnf.set_md(np.asarray(float(x[0])))
    fnf.set_nmd(np.asarray(float(x[1])))
    assert fnf.isLegal(), 'ERROR: The data format is correct, but the data is invalid.'
    return fnf


def pos(q):
    return qrungifn(q, 1., 0.)


def neg(q):
    return qrungifn(q, 0., 1.)


def zero(q):
    return qrungifn(q, 0., 0.)
