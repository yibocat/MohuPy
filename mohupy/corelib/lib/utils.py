#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/7 下午2:07
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import warnings

from typing import Union
from ...core import Fuzznum, Fuzzarray

#
# def isscalar(x) -> bool:
#     from .classUtils import Isscalar
#     return Isscalar()(x)
#
#
# def func4fuzz(x, func, *params) -> Union[Fuzznum, Fuzzarray]:
#     from .classUtils import FuncForFuzz
#     return FuncForFuzz(func, *params)(x)
#
#
# def asfuzzyarray(x, copy=False) -> Fuzzarray:
#     # TODO: asfuzzyarray 将替换为 asfuzzarray，该方法将抛弃
#     warnings.warn(f'The method will be deprecated and will be removed in future versions, please use \'asfuzzarray\' instead.', DeprecationWarning)
#     from .classUtils import AsFuzzarray
#     return AsFuzzarray()(x, copy)
#
#
# def asfuzzarray(x, copy=False) -> Fuzzarray:
#     from .classUtils import AsFuzzarray
#     return AsFuzzarray()(x, copy)
#
#
# def absolute(a, b) -> Union[Fuzznum, Fuzzarray]:
#     warnings.warn(f'This function calculates the difference between the two fuzzy numbers, but it is not reasonable. '
#                   f'It is recommended to use the \'abs()\'.')
#     from .classUtils import Absolute
#     return Absolute()(a, b)
#
#
# def relu(x, op=None) -> Union[Fuzznum, Fuzzarray]:
#     from .classUtils import Relu
#     return Relu()(x, op)
#

