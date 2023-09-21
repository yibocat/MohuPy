#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/21 上午4:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets

import re

import numpy as np
from .fuzzy_element import qrungdhfe


def random(q, n):
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
    newf = qrungdhfe(q, [], [])
    newf.set_md(np.random.rand(np.random.randint(1, n)))
    newf.set_nmd(np.random.rand(np.random.randint(1, n)))
    while not newf.isLegal():
        newf.set_md(np.random.rand(np.random.randint(1, n)))
        newf.set_nmd(np.random.rand(np.random.randint(1, n)))
    return newf


def str_to_hfe(s, q):
    """
        Convert input data to Q-rung hesitant fuzzy element.
        Note: When the input data is '0', it should be set to '0.'.

        Q-rung Hesitant Fuzzy convert function accepts three forms
        of input data:
        {[x,x,x,x],[x,x,x,x]};
        [[x,x,x,x],[x,x,x,x]].

        Parameters
        ----------
            s : str
                Input data.
            q : int
                Q-rung.
        Returns
        -------
            dhf : DHFElements
    """
    dhf = qrungdhfe(q, [], [])

    # t1 = re.findall(r'},\{|],\[|},\[|],\{', s)
    # assert ('},{' not in t1) and ('],{' not in t1) and ('},[' not in t1) and (len(t1) == 1), 'ERROR: data format error.'
    t2 = re.findall(r'\[(\d.*?\d)]', s)
    assert len(t2) == 2, 'ERROR: data format error.'
    md = re.findall(r'\d.?\d*', t2[0])
    nmd = re.findall(r'\d.?\d*', t2[1])

    for i in range(len(md)):
        dhf.set_md(np.append(dhf.md, float(md[i])))
    for j in range(len(nmd)):
        dhf.set_nmd(np.append(dhf.nmd, float(nmd[j])))

    assert dhf.isLegal(), 'ERROR: The data format is correct, but the data is invalid.'
    return dhf


def pos(q):
    return qrungdhfe(q, [1.], [0.])


def neg(q):
    return qrungdhfe(q, [0.], [1.])


def zero(q):
    return qrungdhfe(q, [0.], [0.])
