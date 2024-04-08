#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/6 下午8:20
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

class Config:
    enable_backprop = True
    mtype = 'qrofn'

    from ..core import FuzzType
    mtype_dict = FuzzType


def set_mtype(mtype: str):
    if mtype not in Config.mtype_dict:
        raise ValueError(f'Fuzzy type \'{mtype}\' does not exist. Please choose from {Config.mtype_dict}')
    Config.mtype = mtype

