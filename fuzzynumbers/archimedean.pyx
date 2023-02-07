import numpy as np
cimport numpy as np

cpdef algebraic_tau(double x):
    return -np.log2(x)

cpdef in_algebraic_tau(double x):
    return 1 / (2 ** x)

cpdef algebraic_s(double x):
    return algebraic_tau(1 - x)

cpdef in_algebraic_s(double x):
    return 1 - in_algebraic_tau(x)

cpdef algebraic_T(double x, double y):
    return x * y

cpdef algebraic_S(double x, double y):
    return x + y - x * y

cpdef einstein_tau(double x):
    return np.log2((2 - x) / x)

cpdef in_einstein_tau(double x):
    return 2 / ((2 ** x) + 1)

cpdef einstein_s(double x):
    return np.log2((1 + x) / (1 - x))

cpdef in_einstein_s(double x):
    return (2 ** x - 1) / (2 ** x + 1)

cpdef einstein_T(double x, double y):
    return (x * y) / (1 + (1 - x) * (1 - y))

cpdef einstein_S(double x, double y):
    return (x + y) / (1 + x * y)

