#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/21 上午4:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets

from .qdhfe.fuzzy_element import qrungdhfe
from .qifn.fuzzy_element import qrungifn


def dh_fn_max(dhf: qrungdhfe):
    newfn = qrungifn(dhf.qrung, 0, 0)
    newfn.md = dhf.md.max()
    newfn.nmd = dhf.nmd.max()
    return newfn


def dh_fn_min(dhf: qrungdhfe):
    newfn = qrungifn(dhf.qrung, 0, 0)
    newfn.md = dhf.md.min()
    newfn.nmd = dhf.nmd.min()
    return newfn


def dh_fn_mean(dhf: qrungdhfe):
    newfn = qrungifn(dhf.qrung, 0, 0)
    newfn.md = dhf.md.mean()
    newfn.nmd = dhf.nmd.mean()
    return newfn
