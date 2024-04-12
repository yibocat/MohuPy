#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/11 下午9:09
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
from typing import Union

from .base import Library

from ...core import Fuzznum, Fuzzarray
from ...tensor import Fuzztensor


class TensorDistance(Library):
    def __init__(self, para_l, para_t, indeterminacy):
        self.para_l = para_l
        self.para_t = para_t
        self.indeterminacy = indeterminacy

    # def function(self, f1: Union[Fuzznum, Fuzzarray, Fuzztensor], f2: Union[Fuzznum, Fuzzarray, Fuzztensor]):
    #     from ...corelib.lib.classMeasure import Distance
    #     if isinstance(f1, Fuzztensor) and isinstance(f2, Fuzztensor):
    #         return Distance()(f1.data, f2.data, self.para_l, self.para_t, self.indeterminacy)
    #     if isinstance(f1, Fuzztensor) and isinstance(f2, Union[Fuzznum, Fuzzarray]):
    #         return Distance()(f1.data, f2, self.para_l, self.para_t, self.indeterminacy)
    #     if isinstance(f1, Union[Fuzznum, Fuzzarray]) and isinstance(f2, Fuzztensor):
    #         return Distance()(f1, f2.data, self.para_l, self.para_t, self.indeterminacy)
    #     raise TypeError(f'Unsupported type for {type(f1)} and {type(f2)}')

    def function(self, f1: Fuzztensor, f2: Fuzztensor):
        from ...corelib.lib.classMeasure import Distance
        return Distance()(f1.data, f2.data, self.para_l, self.para_t, self.indeterminacy)
