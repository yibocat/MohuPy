#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/10/16 下午7:09
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import numpy as np

from .regedit import Register

fuzzRandom = Register()


@fuzzRandom('qrofn')
def random_qrofn(q):
    """
        Randomly generate a q-rung orthopair fuzzy number.

        Parameters
        ----------
            q:  int
                The q rung

        Returns
        -------
            mohunum
    """
    from ..core.mohunum import mohunum
    newfn = mohunum(q, 0., 0.)
    while True:
        newfn.md = np.random.rand()
        newfn.nmd = np.random.rand()
        if newfn.is_valid():
            break
    return newfn


@fuzzRandom('ivfn')
def random_ivfn(q):
    """
        Randomly generate a q-rung orthopair fuzzy number.

        Parameters
        ----------
            q:  int
                The q rung

        Returns
        -------
            mohunum
    """
    from ..core.mohunum import mohunum
    newfn = mohunum(q, [0., 0.], [0., 0.])
    while True:
        newfn.md = np.asarray([np.random.rand(), np.random.rand()])
        newfn.nmd = np.asarray([np.random.rand(), np.random.rand()])
        if newfn.is_valid():
            break
    return newfn


@fuzzRandom('qrohfn')
def random_qrohfn(q):
    pass



