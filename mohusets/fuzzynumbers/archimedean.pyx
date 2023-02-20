#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/21 上午4:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets

import numpy as np
cimport numpy as np

cpdef double algebraic_tau(double x):
    return -np.log2(x)

cpdef double in_algebraic_tau(double x):
    return 1 / (2 ** x)

cpdef double algebraic_s(double x):
    return algebraic_tau(1. - x)

cpdef double in_algebraic_s(double x):
    return 1 - in_algebraic_tau(x)

cpdef double algebraic_T(double x, double y):
    return x * y

cpdef double algebraic_S(double x, double y):
    return x + y - x * y

cpdef double einstein_tau(double x):
    return np.log2((2 - x) / x)

cpdef double in_einstein_tau(double x):
    return 2 / ((2 ** x) + 1)

cpdef double einstein_s(double x):
    return np.log2((1 + x) / (1 - x))

cpdef double in_einstein_s(double x):
    return (2 ** x - 1) / (2 ** x + 1)

cpdef double einstein_T(double x, double y):
    return (x * y) / (1 + (1 - x) * (1 - y))

cpdef double einstein_S(double x, double y):
    return (x + y) / (1 + x * y)

