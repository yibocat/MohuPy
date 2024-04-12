#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/8 下午8:06
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from ..core import FuzzType


class Config:
    arch = 'algebraic'
    mtype = 'qrofn'
    enable_backprop = True

    mtype_dict = FuzzType


def set_mtype(mtype: str):
    if mtype not in Config.mtype_dict:
        raise ValueError(f'Fuzzy type \'{mtype}\' does not exist. Please choose from {Config.mtype_dict}')
    Config.mtype = mtype


def set_approx(approx):
    if approx <= 0:
        raise ValueError(f'Invalid approximation value: {approx}.')
    from ..core import Approx
    Approx.round = approx


