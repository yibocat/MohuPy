#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/11/27 下午7:49
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
from .nums import Fuzznum
from .array import Fuzzarray
from .attributes import report, string
from .operation import (add, sub, mul, div,
                        pow, equal, inequal,
                        lt, gt, le, ge, matmul, getitem)

Fuzznum.__repr__ = report
Fuzznum.__str__ = string
Fuzznum.__add__ = add
Fuzznum.__radd__ = add
Fuzznum.__sub__ = sub
Fuzznum.__mul__ = mul
Fuzznum.__rmul__ = mul
Fuzznum.__truediv__ = div
Fuzznum.__pow__ = pow
Fuzznum.__eq__ = equal
Fuzznum.__ne__ = inequal
Fuzznum.__lt__ = lt
Fuzznum.__gt__ = gt
Fuzznum.__le__ = le
Fuzznum.__ge__ = ge

Fuzzarray.__repr__ = report
Fuzzarray.__str__ = string
Fuzzarray.__add__ = add
Fuzzarray.__radd__ = add
Fuzzarray.__sub__ = sub
Fuzzarray.__mul__ = mul
Fuzzarray.__rmul__ = mul
Fuzzarray.__truediv__ = div
Fuzzarray.__pow__ = pow
Fuzzarray.__eq__ = equal
Fuzzarray.__ne__ = inequal
Fuzzarray.__lt__ = lt
Fuzzarray.__gt__ = gt
Fuzzarray.__le__ = le
Fuzzarray.__ge__ = ge
Fuzzarray.__matmul__ = matmul
Fuzzarray.__getitem__ = getitem
