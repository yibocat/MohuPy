#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/6 下午3:01
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import numpy as np

from .base import Operation
from .fuzznums import Fuzznum
from .fuzzarray import Fuzzarray
from .operationClass import BasicOperation


class Addition(Operation):
    def function(self, x, y):
        """
            1. 模糊数 + 模糊数
            2. 模糊数 + 模糊集合
            3. 模糊集合 + 模糊数
            4. 模糊集合 + 模糊集合
        """

        def __add(x0, x1):
            assert x0.mtype == x1.mtype, f"mtype does not match('{x.mtype}' and '{x1.mtype}')."
            assert x0.qrung == x1.qrung, f"qrung does not match({x.qrung} and {x1.qrung})."

            operation = BasicOperation(x0.qrung, x0.mtype)
            return operation.add(x0, x1)

        # 模糊数 + 模糊数
        if isinstance(x, Fuzznum) and isinstance(y, Fuzznum):
            return __add(x, y)

        # 模糊数 + 集合（广播）
        if isinstance(x, Fuzznum) and isinstance(y, Fuzzarray):
            vec_func = np.vectorize(__add)
            newset = Fuzzarray(x.qrung)
            newset.array = vec_func(x, y.array)
            return newset

        # 集合 + 模糊数（广播）
        if isinstance(x, Fuzzarray) and isinstance(y, Fuzznum):
            vec_func = np.vectorize(__add)
            newset = Fuzzarray(x.qrung)
            newset.array = vec_func(x.array, y)
            return newset

        # 集合 + 集合
        if isinstance(x, Fuzzarray) and isinstance(y, Fuzzarray):
            vec_func = np.vectorize(__add)
            newset = Fuzzarray(x.qrung)
            newset.array = vec_func(x.array, y.array)
            return newset

        return NotImplemented


def add(x, y):
    return Addition()(x, y)


class Subtraction(Operation):
    def function(self, x, y):
        """
            1. 模糊数 - 模糊数
            2. 模糊数 - 模糊集合
            3. 模糊集合 - 模糊数
            4. 模糊集合 - 模糊集合
        """

        def __sub(x0, x1):
            assert x0.mtype == x1.mtype, f"mtype does not match('{x.mtype}' and '{x1.mtype}')."
            assert x0.qrung == x1.qrung, f"qrung does not match({x.qrung} and {x1.qrung})."
            operation = BasicOperation(x0.qrung, x0.mtype)
            return operation.sub(x0, x1)

        # 模糊数 - 模糊数
        if isinstance(x, Fuzznum) and isinstance(y, Fuzznum):
            return __sub(x, y)

        # 模糊数 - 集合（广播）
        if isinstance(x, Fuzznum) and isinstance(y, Fuzzarray):
            vec_func = np.vectorize(__sub)
            newset = Fuzzarray(x.qrung)
            newset.array = vec_func(x, y.array)
            return newset

        # 集合 - 模糊数（广播）
        if isinstance(x, Fuzzarray) and isinstance(y, Fuzznum):
            vec_func = np.vectorize(__sub)
            newset = Fuzzarray(x.qrung)
            newset.array = vec_func(x.array, y)
            return newset

        # 集合 - 集合
        if isinstance(x, Fuzzarray) and isinstance(y, Fuzzarray):
            vec_func = np.vectorize(__sub)
            newset = Fuzzarray(x.qrung)
            newset.array = vec_func(x.array, y.array)
            return newset

        return NotImplemented


def sub(x, y):
    return Subtraction()(x, y)


class Multiplication(Operation):
    def function(self, x, y):
        """
            1. 模糊数 * 模糊数
            2. 模糊数 * 数
            3. 模糊数 * 模糊集合
            4. 模糊数 * 数集合

            5. 模糊集合 * 模糊集合
            6. 模糊集合 * 模糊数
            7. 模糊集合 * 数集合
            8. 模糊集合 * 数

            9. 数 * 模糊数
            10.数 * 模糊集合
            11.数集合 * 模糊数
            12.数集合 * 模糊集合
        """

        def __mul(x0, x1):
            if isinstance(x0, Fuzznum) and isinstance(x1, Fuzznum):
                assert x0.mtype == x1.mtype, f"mtype does not match('{x0.mtype}' and '{x1.mtype}')."
                assert x0.qrung == x1.qrung, f"qrung does not match({x0.qrung} and {x1.qrung})."
                operation = BasicOperation(x0.qrung, x0.mtype)
                return operation.mul(x0, x1)

            if isinstance(x0, Fuzznum) and isinstance(x1, (int, float, np.float_, np.int_)):
                assert x1 > 0, f"value must be greater than 0: ({x1} <= 0)."
                operation = BasicOperation(x0.qrung, x0.mtype)
                return operation.times(x1, x0)

            if isinstance(x0, (int, float, np.float_, np.int_)) and isinstance(x1, Fuzznum):
                assert x0 > 0, f"value must be greater than 0: ({x0} <= 0)."
                operation = BasicOperation(x1.qrung, x1.mtype)
                return operation.times(x0, x1)

        if isinstance(x, Fuzznum) and isinstance(y, Fuzznum):
            return __mul(x, y)

        if isinstance(x, Fuzznum) and isinstance(y, (int, float, np.float_, np.int_)):
            return __mul(x, y)

        if isinstance(x, Fuzznum) and isinstance(y, Fuzzarray):
            vec_func = np.vectorize(__mul)
            newset = Fuzzarray(x.qrung)
            newset.array = vec_func(x, y.array)
            return newset

        if isinstance(x, Fuzznum) and isinstance(y, np.ndarray):
            vec_func = np.vectorize(__mul)
            newset = Fuzzarray(x.qrung)
            newset.array = vec_func(x, y)
            return newset

        if isinstance(x, Fuzzarray) and isinstance(y, Fuzzarray):
            vec_func = np.vectorize(__mul)
            newset = Fuzzarray(x.qrung)
            newset.array = vec_func(x.array, y.array)
            return newset

        if isinstance(x, Fuzzarray) and isinstance(y, Fuzznum):
            vec_func = np.vectorize(__mul)
            newset = Fuzzarray(x.qrung)
            newset.array = vec_func(x.array, y)
            return newset

        if isinstance(x, Fuzzarray) and isinstance(y, np.ndarray):
            vec_func = np.vectorize(__mul)
            newset = Fuzzarray(x.qrung)
            newset.array = vec_func(x.array, y)
            return newset

        if isinstance(x, Fuzzarray) and isinstance(y, (int, float, np.float_, np.int_)):
            vec_func = np.vectorize(__mul)
            newset = Fuzzarray(x.qrung)
            newset.array = vec_func(x.array, y)
            return newset

        ### TODO: 数在前的都有点问题，因为不能直接让其等于 Fuzzarray.__mul__，需要在低下的函数 mul() 调整
        if isinstance(x, (int, float, np.float_, np.int_)) and isinstance(y, Fuzznum):
            return __mul(x, y)

        if isinstance(x, (int, float, np.float_, np.int_)) and isinstance(y, Fuzzarray):
            vec_func = np.vectorize(__mul)
            newset = Fuzzarray(y.qrung)
            newset.array = vec_func(x, y.array)
            return newset

        if isinstance(x, np.ndarray) and isinstance(y, Fuzznum):
            vec_func = np.vectorize(__mul)
            newset = Fuzzarray(y.qrung)
            newset.array = vec_func(x, y)
            return newset

        if isinstance(x, np.ndarray) and isinstance(y, Fuzzarray):
            vec_func = np.vectorize(__mul)
            newset = Fuzzarray(y.qrung)
            newset.array = vec_func(x, y.array)
            return newset

        return NotImplemented


def mul(x, y):
    return Multiplication()(x, y)


class Division(Operation):
    def function(self, x, y):
        """
            1. 模糊数 / 模糊数
            2. 模糊数 / 数
            3. 模糊数 / 模糊集合
            4. 模糊数 / 数集合

            5. 模糊集合 / 模糊集合
            6. 模糊集合 / 模糊数
            7. 模糊集合 / 数集合
            8. 模糊集合 / 数
        """

        def __div(x0, x1):
            if isinstance(x0, Fuzznum) and isinstance(x1, Fuzznum):
                assert x0.mtype == x1.mtype, f"mtype does not match: ('{x0.mtype}', '{x1.mtype}')."
                assert x0.qrung == x1.qrung, f"qrung does not match: ({x0.qrung}, {x1.qrung})."
                operation = BasicOperation(x0.qrung, x.mtype)
                return operation.div(x0, x1)
            if isinstance(x0, Fuzznum) and isinstance(x1, (int, float, np.float_, np.int_)):
                assert x1 > 0, f"value must be greater than 0: ({x1} <= 0)."
                operation = BasicOperation(x0.qrung, x0.mtype)
                return operation.times((1 / x1), x0)

        if isinstance(x, Fuzznum) and isinstance(y, Fuzznum):
            return __div(x, y)

        if isinstance(x, Fuzznum) and isinstance(y, (int, float, np.float_, np.int_)):
            return __div(x, y)

        if isinstance(x, Fuzznum) and isinstance(y, Fuzzarray):
            vec_func = np.vectorize(__div)
            newset = Fuzzarray(x.qrung)
            newset.array = vec_func(x, y.array)
            return newset

        if isinstance(x, Fuzznum) and isinstance(y, np.ndarray):
            vec_func = np.vectorize(__div)
            newset = Fuzzarray(x.qrung)
            newset.array = vec_func(x, y)
            return newset

        if isinstance(x, Fuzzarray) and isinstance(y, Fuzzarray):
            vec_func = np.vectorize(__div)
            newset = Fuzzarray(x.qrung)
            newset.array = vec_func(x.array, y.array)
            return newset

        if isinstance(x, Fuzzarray) and isinstance(y, Fuzznum):
            vec_func = np.vectorize(__div)
            newset = Fuzzarray(x.qrung)
            newset.array = vec_func(x.array, y)
            return newset

        if isinstance(x, Fuzzarray) and isinstance(y, np.ndarray):
            vec_func = np.vectorize(__div)
            newset = Fuzzarray(x.qrung)
            newset.array = vec_func(x.array, y)
            return newset

        if isinstance(x, Fuzzarray) and isinstance(y, (int, float, np.float_, np.int_)):
            vec_func = np.vectorize(__div)
            newset = Fuzzarray(x.qrung)
            newset.array = vec_func(x.array, y)
            return newset

        return NotImplemented


def div(x, y):
    return Division()(x, y)


class Power(Operation):
    def __init__(self, p):
        self.p = p

    def function(self, x):
        """
            1. 模糊数 ** 数
            2. 模糊数 ** 数集合
            3. 模糊集合 ** 数
            4. 模糊集合 ** 数集合
        """

        def __pow(x0, p):
            assert p > 0, f"value must be greater than 0: ({self.p} <= 0)."
            operation = BasicOperation(x0.qrung, x0.mtype)
            return operation.power(p, x0)

        if isinstance(x, Fuzznum) and isinstance(self.p, (int, float, np.float_, np.int_)):
            return __pow(x, self.p)

        if isinstance(x, Fuzznum) and isinstance(self.p, np.ndarray):
            vec_func = np.vectorize(__pow)
            newset = Fuzzarray(x.qrung)
            newset.array = vec_func(x, self.p)
            return newset

        if isinstance(x, Fuzzarray) and isinstance(self.p, (int, float, np.float_, np.int_)):
            vec_func = np.vectorize(__pow)
            newset = Fuzzarray(x.qrung)
            newset.array = vec_func(x.array, self.p)
            return newset

        if isinstance(x, Fuzzarray) and isinstance(self.p, np.ndarray):
            vec_func = np.vectorize(__pow)
            newset = Fuzzarray(x.qrung)
            newset.array = vec_func(x.array, self.p)
            return newset

        return NotImplemented


def pow(x, p):
    return Power(p)(x)


class MatrixMul(Operation):
    def function(self, x: Fuzzarray, y: Fuzzarray):
        assert x.ndim > 0, f"input operand 0 does not have enough dimensions."
        assert y.ndim > 0, f"input operand 1 does not have enough dimensions."

        newset = Fuzzarray(x.qrung)
        newset.array = x.array @ y.array
        return newset


def matmul(x, y):
    return MatrixMul()(x, y)


class Equal(Operation):
    def function(self, x, y):
        """
            1. 模糊数 == 模糊数
            2. 模糊数 == 模糊集合
            3. 模糊集合 == 模糊数
            4. 模糊集合 == 模糊集合
        """

        def __eq(x0, x1):
            assert x0.mtype == x1.mtype, f"mtype does not match: ('{x0.mtype}', '{x1.mtype}')."
            assert x0.qrung == x1.qrung, f"qrung does not match: ({x0.qrung}, {x1.qrung})."
            return x0.md == x1.md and x0.nmd == x1.nmd

        if isinstance(x, Fuzznum) and isinstance(y, Fuzznum):
            return __eq(x, y)

        if isinstance(x, Fuzznum) and isinstance(y, Fuzzarray):
            vec_func = np.vectorize(__eq)
            return vec_func(x, y.array)

        if isinstance(x, Fuzzarray) and isinstance(y, Fuzznum):
            vec_func = np.vectorize(__eq)
            return vec_func(x.array, y)

        if isinstance(x, Fuzzarray) and isinstance(y, Fuzzarray):
            vec_func = np.vectorize(__eq)
            return vec_func(x.array, y.array)

        return NotImplemented


def equal(x, y):
    return Equal()(x, y)


class Inequality(Operation):
    def function(self, x, y):
        """
            1. 模糊数 != 模糊数
            2. 模糊数 != 模糊集合
            3. 模糊集合 != 模糊数
            4. 模糊集合 != 模糊集合
        """

        def __ne(x0, x1):
            assert x0.mtype == x1.mtype, f"mtype does not match: ('{x0.mtype}', '{x1.mtype}')."
            assert x0.qrung == x1.qrung, f"qrung does not match: ({x0.qrung}, {x1.qrung})."
            return x0.md != x1.md or x0.nmd != x1.nmd

        if isinstance(x, Fuzznum) and isinstance(y, Fuzznum):
            return __ne(x, y)

        if isinstance(x, Fuzznum) and isinstance(y, Fuzzarray):
            vec_func = np.vectorize(__ne)
            return vec_func(x, y.array)

        if isinstance(x, Fuzzarray) and isinstance(y, Fuzznum):
            vec_func = np.vectorize(__ne)
            return vec_func(x.array, y)

        if isinstance(x, Fuzzarray) and isinstance(y, Fuzzarray):
            vec_func = np.vectorize(__ne)
            return vec_func(x.array, y.array)

        return NotImplemented


def inequal(x, y):
    return Inequality()(x, y)


class Lt(Operation):
    def function(self, x, y):
        """
            1. 模糊数 < 模糊数
            2. 模糊数 < 模糊集合
            3. 模糊集合 < 模糊数
            4. 模糊集合 < 模糊集合
        """

        def __lt(x0, x1):
            assert x0.mtype == x1.mtype, f"mtype does not match: ('{x0.mtype}', '{x1.mtype}')."
            assert x0.qrung == x1.qrung, f"qrung does not match: ({x0.qrung}, {x1.qrung})."
            # if x0.mtype == 'ivfn' or x0.mtype == 'qrohfn':
            #     return x0.score < x1.score
            # else:
            #     from .. import fuzznum
            #     if Equal()(Subtraction()(x0, x1), fuzznum(x0.qrung, 0., 1.)) and Inequality()(x0, x1):
            #         return True
            #     else:
            #         return False
            return x0.score < x1.score

        if isinstance(x, Fuzznum) and isinstance(y, Fuzznum):
            return __lt(x, y)

        if isinstance(x, Fuzznum) and isinstance(y, Fuzzarray):
            vec_func = np.vectorize(__lt)
            return vec_func(x, y.array)

        if isinstance(x, Fuzzarray) and isinstance(y, Fuzznum):
            vec_func = np.vectorize(__lt)
            return vec_func(x.array, y)

        if isinstance(x, Fuzzarray) and isinstance(y, Fuzzarray):
            vec_func = np.vectorize(__lt)
            return vec_func(x.array, y.array)

        return NotImplemented


def lt(x, y):
    return Lt()(x, y)


class Gt(Operation):
    def function(self, x, y):
        """
            1. 模糊数 > 模糊数
            2. 模糊数 > 模糊集合
            3. 模糊集合 > 模糊数
            4. 模糊集合 > 模糊集合
        """

        def __gt(x0, x1):
            assert x0.mtype == x1.mtype, f"mtype does not match: ('{x0.mtype}', '{x1.mtype}')."
            assert x0.qrung == x1.qrung, f"qrung does not match: ({x0.qrung}, {x1.qrung})."
            # if x0.mtype == 'ivfn' or x0.mtype == 'qrohfn':
            #     return x0.score > x1.score
            # else:
            #     from .. import fuzznum
            #     if Inequality()(Subtraction()(x0, x1), fuzznum(x0.qrung, 0., 1.)) and Inequality()(x0, x1):
            #         return True
            #     else:
            #         return False
            return x0.score > x1.score

        if isinstance(x, Fuzznum) and isinstance(y, Fuzznum):
            return __gt(x, y)

        if isinstance(x, Fuzznum) and isinstance(y, Fuzzarray):
            vec_func = np.vectorize(__gt)
            return vec_func(x, y.array)

        if isinstance(x, Fuzzarray) and isinstance(y, Fuzznum):
            vec_func = np.vectorize(__gt)
            return vec_func(x.array, y)

        if isinstance(x, Fuzzarray) and isinstance(y, Fuzzarray):
            vec_func = np.vectorize(__gt)
            return vec_func(x.array, y.array)

        return NotImplemented


def gt(x, y):
    return Gt()(x, y)


class Le(Operation):
    def function(self, x, y):
        """
            1. 模糊数 <= 模糊数
            2. 模糊数 <= 模糊集合
            3. 模糊集合 <= 模糊数
            4. 模糊集合 <= 模糊集合
        """

        def __le(x0, x1):
            assert x0.mtype == x1.mtype, f"mtype does not match: ('{x0.mtype}', '{x1.mtype}')."
            assert x0.qrung == x1.qrung, f"qrung does not match: ({x0.qrung}, {x1.qrung})."
            # if x0.mtype == 'ivfn' or x0.mtype == 'qrohfn':
            #     return x0.score <= x1.score
            # else:
            #     from .. import fuzznum
            #     if Equal()(Subtraction()(x0, x1), fuzznum(x0.qrung, 0., 1.)) or Equal()(x0, x1):
            #         return True
            #     else:
            #         return False
            return x0.score <= x1.score

        if isinstance(x, Fuzznum) and isinstance(y, Fuzznum):
            return __le(x, y)

        if isinstance(x, Fuzznum) and isinstance(y, Fuzzarray):
            vec_func = np.vectorize(__le)
            return vec_func(x, y.array)

        if isinstance(x, Fuzzarray) and isinstance(y, Fuzznum):
            vec_func = np.vectorize(__le)
            return vec_func(x.array, y)

        if isinstance(x, Fuzzarray) and isinstance(y, Fuzzarray):
            vec_func = np.vectorize(__le)
            return vec_func(x.array, y.array)

        return NotImplemented


def le(x, y):
    return Le()(x, y)


class Ge(Operation):
    def function(self, x, y):
        """
            1. 模糊数 >= 模糊数
            2. 模糊数 >= 模糊集合
            3. 模糊集合 >= 模糊数
            4. 模糊集合 >= 模糊集合
        """

        def __ge(x0, x1):
            assert x0.mtype == x1.mtype, f"mtype does not match: ('{x0.mtype}', '{x1.mtype}')."
            assert x0.qrung == x1.qrung, f"qrung does not match: ({x0.qrung}, {x1.qrung})."
            # if x0.mtype == 'ivfn' or x0.mtype == 'qrohfn':
            #     return x0.score >= x1.score
            # else:
            #     from .. import fuzznum
            #     if Inequality()(Subtraction()(x0, x1), fuzznum(x0.qrung, 0., 1.)) or Equal()(x0, x1):
            #         return True
            #     else:
            #         return False
            return x0.score >= x1.score

        if isinstance(x, Fuzznum) and isinstance(y, Fuzznum):
            return __ge(x, y)

        if isinstance(x, Fuzznum) and isinstance(y, Fuzzarray):
            vec_func = np.vectorize(__ge)
            return vec_func(x, y.array)

        if isinstance(x, Fuzzarray) and isinstance(y, Fuzznum):
            vec_func = np.vectorize(__ge)
            return vec_func(x.array, y)

        if isinstance(x, Fuzzarray) and isinstance(y, Fuzzarray):
            vec_func = np.vectorize(__ge)
            return vec_func(x.array, y.array)

        return NotImplemented


def ge(x, y):
    return Ge()(x, y)


class GetItem(Operation):
    def __init__(self, slices):
        self.slices = slices

    def function(self, x):
        from .construct import fuzzset
        y = x.array[self.slices]
        if isinstance(y, np.ndarray):
            return fuzzset(y)
        else:
            return y


def getitem(x, slices):
    return GetItem(slices)(x)
