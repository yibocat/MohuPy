#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/12 下午2:41
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import warnings

import numpy as np

from typing import Callable

from ...core import Fuzznum, Fuzzarray


def fuzz_isscalar(x: Fuzznum | Fuzzarray) -> bool:
    """
    检查输入是否是模糊标量。
    :param x:
    :return:
    """
    from ..lib import Isscalar
    return Isscalar()(x)


def fuzz_func4fuzz(x: Fuzznum | Fuzzarray, func: Callable, *params) -> Fuzznum | Fuzzarray:
    """
    对输入模糊数进行任意函数 func 的计算转换
    :param x:       输入的模糊数或模糊集合
    :param func:    函数 func
    :param params:  函数的参数
    :return:        Fuzznum 或 Fuzzarray
    """
    from ..lib import FuncForFuzz
    return FuncForFuzz(func, *params)(x)


def asfuzzyarray(x: Fuzznum | Fuzzarray | np.ndarray | list, copy=False) -> Fuzzarray:
    """
    将一个模糊数或列表转换成一个 Fuzzarray。
    需要注意：该方法在未来版本可能弃用，函数名称换成 asfuzzarray
    :param x:       输入模糊数、模糊集合、np.ndarray，和列表
    :param copy:    是否拷贝
    :return:        Fuzzarray
    """
    warnings.warn(
        f'The method will be deprecated and will be removed in future versions, please use \'asfuzzarray\' instead.',
        DeprecationWarning)
    from ..lib import AsFuzzarray
    return AsFuzzarray()(x, copy)


def asfuzzarray(x: Fuzznum | Fuzzarray | np.ndarray, copy=False) -> Fuzzarray:
    """
    将一个模糊数或列表转换成一个 Fuzzarray。
    :param x:       输入模糊数、模糊集合、np.ndarray，和列表
    :param copy:    是否拷贝
    :return:        Fuzzarray
    """
    from ..lib import AsFuzzarray
    return AsFuzzarray()(x, copy)


def fuzz_absolute(x: Fuzznum | Fuzzarray, y: Fuzznum | Fuzzarray) -> Fuzznum | Fuzzarray:
    """
    计算两个模糊数或模糊集的绝对值
    :param x:   第一个模糊数或模糊集
    :param y:   第二个模糊数或模糊集
    :return:    返回绝对值
    """
    from ..lib import Absolute
    return Absolute()(x, y)


def fuzz_relu(fuzz: Fuzznum | Fuzzarray, op: Fuzznum = None) -> Fuzznum | Fuzzarray:
    """
    模糊Relu函数，op 表示想要设置的对比基准模糊数，默认为 <0.5,0.5>，目前仅适用于 mtype='qrofn'
    :param fuzz:
    :param op:
    :return:
    """
    from ..lib import Relu
    return Relu()(fuzz, op)
