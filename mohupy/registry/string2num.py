#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/10/16 下午3:20
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import re

from ..core.base import fuzzNum

from .regedit import Register

fuzzString = Register()


@fuzzString('qrofn')
def str2qrofn(s: str, q) -> fuzzNum:
    """
        convert a string to a qrofn

        Parameters
        ----------
            s : str
            q : int
        Returns
        -------
            fuzzNum

        Notes: When the input data is 0, it should be set to 0.
        Q-rung fuzzy convert function accepts the form: [x,x]
    """
    from ..core.mohunum import mohunum
    newfn = mohunum(q, 0., 0.)
    t = re.findall(r'^\[(\d.*?\d)]$', s)
    assert len(t) == 1, \
        'data format error.'
    x = re.findall(r'\d.?\d*', t[0])
    assert len(x) == 2, \
        'data format error.'
    newfn.md = float(x[0])
    newfn.nmd = float(x[1])
    assert newfn.is_valid(), 'data format is correct, but the data is invalid.'
    return newfn


@fuzzString('ivfn')
def str2ivfn(s: str, q) -> fuzzNum:
    from ..core.mohunum import mohunum
    newfn = mohunum(q, [0., 0.], [0., 0.])
    newfn = mohunum(q, [0., 0.], [0., 0.])
    t2 = re.findall(r'\[(\d.*?\d)]', s)
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
    assert newfn.is_valid(), 'data format is correct, but the data is invalid.'
    return newfn


@fuzzString('qrohfn')
def str2qrohfn():
    pass






