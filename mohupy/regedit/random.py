#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/11/28 下午3:12
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import numpy as np

from ..core.regedit import Registry
from ..constant import Approx

fuzzRandom = Registry()


@fuzzRandom('qrofn')
def random_qrofn(q, minnum=None, maxnum=None):
    """
        Randomly generate a q-rung orthopair fuzzy number.

        Parameters
        ----------
            q:  int
                The q rung
            minnum: int
                Minimum number of generated
            maxnum: int
                Maximum number of generated

        Returns
        -------
            Fuzznum
    """
    from ..core import fuzznum
    newfn = fuzznum(q, 0., 0.)
    while True:
        newfn.md = np.round(np.random.rand(), Approx.round)
        newfn.nmd = np.round(np.random.rand(), Approx.round)
        if newfn.isValid():
            break
    return newfn


@fuzzRandom('ivfn')
def random_ivfn(q, minnum=None, maxnum=None):
    """
        Randomly generate a interval-valued q-rung orthopair fuzzy number.

        Parameters
        ----------
            q:  int
                The q rung
            minnum: int
                Minimum number of generated
            maxnum: int
                Maximum number of generated

        Returns
        -------
            fuzznum
    """
    from ..core import fuzznum
    newfn = fuzznum(q, (0., 0.), (0., 0.))
    while True:
        newfn.md = np.round(np.asarray([np.random.rand(), np.random.rand()]), Approx.round)
        newfn.nmd = np.round(np.asarray([np.random.rand(), np.random.rand()]), Approx.round)
        if newfn.isValid():
            break
    return newfn


@fuzzRandom('qrohfn')
def random_qrohfn(q, minnum, maxnum):
    """
        Randomly generate a q-rung orthopair hesitant fuzzy number.
        Parameters
        ----------
            q:  int
                The q rung
            minnum: int
                Minimum number of generated
            maxnum: int
                Maximum number of generated

        Returns
        -------
            fuzznum
    """
    from ..core import fuzznum
    newfn = fuzznum(q, [], [])
    newfn.md = np.round(np.random.rand(np.random.randint(minnum, maxnum)), Approx.round)
    newfn.nmd = np.round(np.random.rand(np.random.randint(minnum, maxnum)), Approx.round)
    while True:
        newfn.md = np.round(np.random.rand(np.random.randint(minnum, maxnum)), Approx.round)
        newfn.nmd = np.round(np.random.rand(np.random.randint(minnum, maxnum)), Approx.round)
        if newfn.isValid():
            break
    return newfn

