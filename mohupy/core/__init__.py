#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/9/29 上午10:34
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

__all__ = []

from .__multi_func import fuzznum, fuzzset
from .mohusets import mohuset
from .base import mohunum

from .interface import download_template

__all__ += [
    'fuzznum', 'fuzzset', 'mohuset', 'mohunum', 'download_template'
]

from .mohu import MohuQROFN, MohuQROIVFN, MohuQROHFN
from .__operators import (add, sub, mul, div,
                          pow, equal, inequal,
                          lt, gt, le, ge, matmul, getitem)

MohuQROFN.__add__ = add
MohuQROFN.__radd__ = add
MohuQROFN.__sub__ = sub
MohuQROFN.__mul__ = mul
MohuQROFN.__rmul__ = mul
MohuQROFN.__truediv__ = div
MohuQROFN.__pow__ = pow
MohuQROFN.__eq__ = equal
MohuQROFN.__ne__ = inequal
MohuQROFN.__lt__ = lt
MohuQROFN.__gt__ = gt
MohuQROFN.__le__ = le
MohuQROFN.__ge__ = ge

MohuQROIVFN.__add__ = add
MohuQROIVFN.__radd__ = add
MohuQROIVFN.__sub__ = sub
MohuQROIVFN.__mul__ = mul
MohuQROIVFN.__rmul__ = mul
MohuQROIVFN.__truediv__ = div
MohuQROIVFN.__pow__ = pow
MohuQROIVFN.__eq__ = equal
MohuQROIVFN.__ne__ = inequal
MohuQROIVFN.__lt__ = lt
MohuQROIVFN.__gt__ = gt
MohuQROIVFN.__le__ = le
MohuQROIVFN.__ge__ = ge

MohuQROHFN.__add__ = add
MohuQROHFN.__radd__ = add
MohuQROHFN.__sub__ = sub
MohuQROHFN.__mul__ = mul
MohuQROHFN.__rmul__ = mul
MohuQROHFN.__truediv__ = div
MohuQROHFN.__pow__ = pow
MohuQROHFN.__eq__ = equal
MohuQROHFN.__ne__ = inequal
MohuQROHFN.__lt__ = lt
MohuQROHFN.__gt__ = gt
MohuQROHFN.__le__ = le
MohuQROHFN.__ge__ = ge

mohuset.__add__ = add
mohuset.__radd__ = add
mohuset.__sub__ = sub
mohuset.__mul__ = mul
mohuset.__rmul__ = mul
mohuset.__truediv__ = div
mohuset.__pow__ = pow
mohuset.__eq__ = equal
mohuset.__ne__ = inequal
mohuset.__lt__ = lt
mohuset.__gt__ = gt
mohuset.__le__ = le
mohuset.__ge__ = ge
mohuset.__matmul__ = matmul
mohuset.__getitem__ = getitem
