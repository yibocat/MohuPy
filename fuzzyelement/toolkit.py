#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/4 下午8:33
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzPy

from fuzzyelement.DHFElements import qrunghfe
from fuzzyelement.FNumbers import qrungfn
from fuzzyelement.IVFNumbers import qrungivfn


# ----------------------------------------------------------------
# Convert Qrung Hesitant Fuzzy element to Q-rung fuzzy number,
# according to the method of membership degree maximum, minimum and mean.
def dh_fn_max(dhf: qrunghfe):
    """
        Convert Q-rung hesitant fuzzy element to Q-rung fuzzy number by max value
        Parameters
        ----------
            dhf : DHFElements

        Returns
        -------
            newfn : FNumbers
    """
    newfn = qrungfn(dhf.qrung, 0, 0)
    newfn.md = dhf.md.max()
    newfn.nmd = dhf.nmd.max()
    return newfn


def dh_fn_min(dhf: qrunghfe):
    """
        Convert Q-rung hesitant fuzzy element to Q-rung fuzzy number by min value
        Parameters
        ----------
            dhf : DHFElements

        Returns
        -------
            newfn : FNumbers
    """
    newfn = qrungfn(dhf.qrung, 0, 0)
    newfn.md = dhf.md.min()
    newfn.nmd = dhf.nmd.min()
    return newfn


def dh_fn_mean(dhf: qrunghfe):
    """
        Convert Q-rung hesitant fuzzy element to Q-rung fuzzy number by mean value.
        Parameters
        ----------
            dhf : DHFElements

        Returns
        -------
            newfn : FNumbers
    """
    newfn = qrungfn(dhf.qrung, 0, 0)
    newfn.md = dhf.md.mean()
    newfn.nmd = dhf.nmd.mean()
    return newfn



