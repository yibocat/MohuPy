#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/11/28 下午3:12
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import numpy as np

from ..base.regedit import Registry
from ..lib.approximate import Approx

fuzzRandom = Registry()


def random_qrofn(q, num=0):
    """
        Randomly generate a q-rung orthopair fuzzy number.

        Parameters
        ----------
            q:  int
                The q rung
            num:  int
                default 1

        Returns
        -------
            Fuzznum
    """
    from ..base import fuzznum
    newfn = fuzznum(q, 0., 0.)
    while True:
        newfn.md = np.round(np.random.rand(), Approx.round)
        newfn.nmd = np.round(np.random.rand(), Approx.round)
        if newfn.isValid():
            break
    return newfn



















