#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/7 下午1:29
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import re
import numpy as np

from ...core import Fuzznum, Registry

fuzzString = Registry()


@fuzzString('qrofn')
def str2qrofn(s: str, q) -> Fuzznum:
    """
        convert a string to a qrofn

        Parameters
        ----------
            s : str
            q : int
        Returns
        -------
            Fuzznum

        Notes: When the input data is 0, it should be set to ZERO
        Q-rung fuzzy convert function accepts the form: [x,x]
    """
    from ...core import fuzznum
    newfn = fuzznum(q, 0., 0.)
    t = re.findall(r'^<(\d.*?\d)>$', s)
    assert len(t) == 1, \
        'data format error.'
    x = re.findall(r'\d.?\d*', t[0])
    assert len(x) == 2, \
        'data format error.'
    newfn.md = float(x[0])
    newfn.nmd = float(x[1])
    assert newfn.valid(), f'data format is correct, but the data is invalid: {s}'
    return newfn


@fuzzString('ivfn')
def str2ivfn(s: str, q) -> Fuzznum:
    from ...core import fuzznum
    newfn = fuzznum(q, (0., 0.), (0., 0.))
    t2 = re.findall(r'\[(\d.*?\d)\s?]', s)
    assert len(t2) == 2, \
        'data format error.'
    md = re.findall(r'\d.?\d*', t2[0])
    nmd = re.findall(r'\d.?\d*', t2[1])
    assert len(md) == 2 and len(nmd) == 2, \
        'data format error.'

    m = [float(md[0]), float(md[1])]
    n = [float(nmd[0]), float(nmd[1])]
    newfn.md = m
    newfn.nmd = n
    assert newfn.valid(), f'data format is correct, but the data is invalid: {s}'
    return newfn


@fuzzString('qrohfn')
def str2qrohfn(s: str, q) -> Fuzznum:
    """
        Convert input data to Q-rung orthopair hesitant fuzzy element.
        Note: When the input data is '0', it should be set to 'ZERO'.

        Q-rung Hesitant Fuzzy convert function accepts three forms
        of input data:
        {[x,x,x,x],[x,x,x,x]};
        [[x,x,x,x],[x,x,x,x]].

        Parameters
        ----------
            s : str
                Input data.
            q : int
                q-rung.
        Returns
        -------
            MohuQROHFN
    """
    from ...core import fuzznum
    newfn = fuzznum(q, [], [])
    t2 = re.findall(r'\[(\d.*?\d)\s*?]', s)
    assert len(t2) == 2, f'data format error:{t2}'
    md = re.findall(r'\d.?\d*', t2[0])
    nmd = re.findall(r'\d.?\d*', t2[1])

    for i in range(len(md)):
        newfn.md = np.append(newfn.md, np.float_(md[i]))
    for j in range(len(nmd)):
        newfn.nmd = np.append(newfn.nmd, np.float_(nmd[j]))

    assert newfn.valid(), f'data format is correct, but the data is invalid: {s}'
    return newfn

