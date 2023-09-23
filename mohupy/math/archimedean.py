#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/9/21 下午8:25
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from ..config import import_cupy_lib
np = import_cupy_lib()


def algebraic_tau(x):
    return -np.log2(x)


def in_algebraic_tau(x):
    return 1 / (2 ** x)


def algebraic_s(x):
    return algebraic_tau(1. - x)


def in_algebraic_s(x):
    return 1 - in_algebraic_tau(x)


def algebraic_T(x, y):
    return x * y


def algebraic_S(x, y):
    return x + y - x * y


def einstein_tau(x):
    return np.log2((2 - x) / x)


def in_einstein_tau(x):
    return 2 / ((2 ** x) + 1)


def einstein_s(x):
    return np.log2((1 + x) / (1 - x))


def in_einstein_s(x):
    return (2 ** x - 1) / (2 ** x + 1)


def einstein_T(x, y):
    return (x * y) / (1 + (1 - x) * (1 - y))


def einstein_S(x, y):
    return (x + y) / (1 + x * y)
