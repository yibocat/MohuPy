#  Copyright (c) yibocat 2023 All Rights Reserved
#  Date: 2023/1/31 下午5:06
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzyKit
import re

import numpy as np
from .qrunghfe import qrunghfe


def randomQHF(q, n):
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


def str_to_hfe(s, q: float):
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
    dhf = qrunghfe(q, [], [])

    t1 = re.findall(r'},\{|],\[|},\[|],\{', s)
    assert ('},{' not in t1) and ('],{' not in t1) and ('},[' not in t1) and (len(t1) == 1), 'ERROR: data format error.'
    t2 = re.findall(r'\[(\d.*?\d)]', s)
    assert len(t2) == 2, 'ERROR: data format error.'
    md = re.findall(r'\d.?\d*', t2[0])
    nmd = re.findall(r'\d.?\d*', t2[1])

    for i in range(len(md)):
        dhf.md = np.append(dhf.md, float(md[i]))
    for j in range(len(nmd)):
        dhf.nmd = np.append(dhf.nmd, float(nmd[j]))

    assert dhf.isLegal(), 'ERROR: The data format is correct, but the data is invalid.'
    return dhf
