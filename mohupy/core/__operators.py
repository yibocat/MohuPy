#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/10/25 下午9:28
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
from typing import Union

import numpy as np

from .mohusets import mohuset
from .base import mohunum
from .__norms_operation import Algebraic


class Operation:
    def __call__(self, *args):
        return self.function(*args)

    def function(self, *args):
        raise NotImplementedError()


class Addition(Operation):
    def function(self, x, y):
        """
            1. 模糊数 + 模糊数
            2. 模糊数 + 模糊集合
            3. 模糊集合 + 模糊数
            4. 模糊集合 + 模糊集合
        """
        def __add(x0, x1):
            assert x0.mtype == x1.mtype, f"mtype does not match: ('{x.mtype}', '{x1.mtype}')."
            assert x0.qrung == x1.qrung, f"qrung does not match: ({x.qrung}, {x1.qrung})."
            
            operation = Algebraic(x0.qrung, x0.mtype)
            return operation.add(x0, x1)

        # 模糊数 + 模糊数
        if isinstance(x, mohunum) and isinstance(y, mohunum):
            return __add(x, y)

        # 模糊数 + 集合（广播）
        if isinstance(x, mohunum) and isinstance(y, mohuset):
            vec_func = np.vectorize(__add)
            newset = mohuset(x.qrung, x.mtype)
            newset.set = vec_func(x, y.set)
            return newset

        # 集合 + 模糊数（广播）
        if isinstance(x, mohuset) and isinstance(y, mohunum):
            vec_func = np.vectorize(__add)
            newset = mohuset(x.qrung, x.mtype)
            newset.set = vec_func(x.set, y)
            return newset

        # 集合 + 集合
        if isinstance(x, mohuset) and isinstance(y, mohuset):
            vec_func = np.vectorize(__add)
            newset = mohuset(x.qrung, x.mtype)
            newset.set = vec_func(x.set, y.set)
            return newset


class Subtraction(Operation):
    def function(self, x, y):
        """
            1. 模糊数 - 模糊数
            2. 模糊数 - 模糊集合
            3. 模糊集合 - 模糊数
            4. 模糊集合 - 模糊集合
        """
        def __sub(x0, x1):
            assert x0.mtype == x1.mtype, f"mtype does not match: ('{x.mtype}', '{x1.mtype}')."
            assert x0.qrung == x1.qrung, f"qrung does not match: ({x.qrung}, {x1.qrung})."
            operation = Algebraic(x0.qrung, x0.mtype)
            return operation.sub(x0, x1)

        # 模糊数 - 模糊数
        if isinstance(x, mohunum) and isinstance(y, mohunum):
            return __sub(x, y)

        # 模糊数 - 集合（广播）
        if isinstance(x, mohunum) and isinstance(y, mohuset):
            vec_func = np.vectorize(__sub)
            newset = mohuset(x.qrung, x.mtype)
            newset.set = vec_func(x, y.set)
            return newset

        # 集合 - 模糊数（广播）
        if isinstance(x, mohuset) and isinstance(y, mohunum):
            vec_func = np.vectorize(__sub)
            newset = mohuset(x.qrung, x.mtype)
            newset.set = vec_func(x.set, y)
            return newset

        # 集合 - 集合
        if isinstance(x, mohuset) and isinstance(y, mohuset):
            vec_func = np.vectorize(__sub)
            newset = mohuset(x.qrung, x.mtype)
            newset.set = vec_func(x.set, y.set)
            return newset


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
            if isinstance(x0, mohunum) and isinstance(x1, mohunum):
                assert x0.mtype == x1.mtype, f"mtype does not match: ('{x0.mtype}', '{x1.mtype}')."
                assert x0.qrung == x1.qrung, f"qrung does not match: ({x0.qrung}, {x1.qrung})."
                operation = Algebraic(x0.qrung, x0.mtype)
                return operation.mul(x0, x1)

            if isinstance(x0, mohunum) and isinstance(x1, Union[int, float, np.float_, np.int_]):
                assert x1 > 0, f"value must be greater than 0: ({x1} <= 0)."
                operation = Algebraic(x0.qrung, x0.mtype)
                return operation.times(x1, x0)

            if isinstance(x0, Union[int, float, np.float_, np.int_]) and isinstance(x1, mohunum):
                assert x0 > 0, f"value must be greater than 0: ({x0} <= 0)."
                operation = Algebraic(x1.qrung, x1.mtype)
                return operation.times(x0, x1)

        if isinstance(x, mohunum) and isinstance(y, mohunum):
            return __mul(x, y)

        if isinstance(x, mohunum) and isinstance(y, Union[int, float, np.float_, np.int_]):
            return __mul(x, y)

        if isinstance(x, mohunum) and isinstance(y, mohuset):
            vec_func = np.vectorize(__mul)
            newset = mohuset(x.qrung, x.mtype)
            newset.set = vec_func(x, y.set)
            return newset

        if isinstance(x, mohunum) and isinstance(y, np.ndarray):
            vec_func = np.vectorize(__mul)
            newset = mohuset(x.qrung, x.mtype)
            newset.set = vec_func(x, y)
            return newset

        if isinstance(x, mohuset) and isinstance(y, mohuset):
            vec_func = np.vectorize(__mul)
            newset = mohuset(x.qrung, x.mtype)
            newset.set = vec_func(x.set, y.set)
            return newset

        if isinstance(x, mohuset) and isinstance(y, mohunum):
            vec_func = np.vectorize(__mul)
            newset = mohuset(x.qrung, x.mtype)
            newset.set = vec_func(x.set, y)
            return newset

        if isinstance(x, mohuset) and isinstance(y, np.ndarray):
            vec_func = np.vectorize(__mul)
            newset = mohuset(x.qrung, x.mtype)
            newset.set = vec_func(x.set, y)
            return newset

        if isinstance(x, mohuset) and isinstance(y, Union[int, float, np.float_, np.int_]):
            vec_func = np.vectorize(__mul)
            newset = mohuset(x.qrung, x.mtype)
            newset.set = vec_func(x.set, y)
            return newset

        ### TODO: 数在前的都有点问题，因为不能直接让其等于 mohuset.__mul__，需要在低下的函数 mul() 调整
        if isinstance(x, Union[int, float, np.float_, np.int_]) and isinstance(y, mohunum):
            return __mul(x, y)

        if isinstance(x, Union[int, float, np.float_, np.int_]) and isinstance(y, mohuset):
            vec_func = np.vectorize(__mul)
            newset = mohuset(y.qrung, y.mtype)
            newset.set = vec_func(x, y.set)
            return newset

        if isinstance(x, np.ndarray) and isinstance(y, mohunum):
            vec_func = np.vectorize(__mul)
            newset = mohuset(y.qrung, y.mtype)
            newset.set = vec_func(x, y)
            return newset

        if isinstance(x, np.ndarray) and isinstance(y, mohuset):
            vec_func = np.vectorize(__mul)
            newset = mohuset(y.qrung, y.mtype)
            newset.set = vec_func(x, y.set)
            return newset


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
            if isinstance(x0, mohunum) and isinstance(x1, mohunum):
                assert x0.mtype == x1.mtype, f"mtype does not match: ('{x0.mtype}', '{x1.mtype}')."
                assert x0.qrung == x1.qrung, f"qrung does not match: ({x0.qrung}, {x1.qrung})."
                operation = Algebraic(x0.qrung, x.mtype)
                return operation.div(x0, x1)
            if isinstance(x0, mohunum) and isinstance(x1, Union[int, float, np.float_, np.int_]):
                assert x1 > 0, f"value must be greater than 0: ({x1} <= 0)."
                operation = Algebraic(x0.qrung, x0.mtype)
                return operation.times((1/x1), x0)

        if isinstance(x, mohunum) and isinstance(y, mohunum):
            return __div(x, y)

        if isinstance(x, mohunum) and isinstance(y, Union[int, float, np.float_, np.int_]):
            return __div(x, y)

        if isinstance(x, mohunum) and isinstance(y, mohuset):
            vec_func = np.vectorize(__div)
            newset = mohuset(x.qrung, x.mtype)
            newset.set = vec_func(x, y.set)
            return newset

        if isinstance(x, mohunum) and isinstance(y, np.ndarray):
            vec_func = np.vectorize(__div)
            newset = mohuset(x.qrung, x.mtype)
            newset.set = vec_func(x, y)
            return newset

        if isinstance(x, mohuset) and isinstance(y, mohuset):
            vec_func = np.vectorize(__div)
            newset = mohuset(x.qrung, x.mtype)
            newset.set = vec_func(x.set, y.set)
            return newset

        if isinstance(x, mohuset) and isinstance(y, mohunum):
            vec_func = np.vectorize(__div)
            newset = mohuset(x.qrung, x.mtype)
            newset.set = vec_func(x.set, y)
            return newset

        if isinstance(x, mohuset) and isinstance(y, np.ndarray):
            vec_func = np.vectorize(__div)
            newset = mohuset(x.qrung, x.mtype)
            newset.set = vec_func(x.set, y)
            return newset

        if isinstance(x, mohuset) and isinstance(y, Union[int, float, np.float_, np.int_]):
            vec_func = np.vectorize(__div)
            newset = mohuset(x.qrung, x.mtype)
            newset.set = vec_func(x.set, y)
            return newset


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
            operation = Algebraic(x0.qrung, x0.mtype)
            return operation.power(p, x0)

        if isinstance(x, mohunum) and isinstance(self.p, Union[int, float, np.float_, np.int_]):
            return __pow(x, self.p)

        if isinstance(x, mohunum) and isinstance(self.p, np.ndarray):
            vec_func = np.vectorize(__pow)
            newset = mohuset(x.qrung, x.mtype)
            newset.set = vec_func(x, self.p)
            return newset

        if isinstance(x, mohuset) and isinstance(self.p, Union[int, float, np.float_, np.int_]):
            vec_func = np.vectorize(__pow)
            newset = mohuset(x.qrung, x.mtype)
            newset.set = vec_func(x.set, self.p)
            return newset

        if isinstance(x, mohuset) and isinstance(self.p, np.ndarray):
            vec_func = np.vectorize(__pow)
            newset = mohuset(x.qrung, x.mtype)
            newset.set = vec_func(x.set, self.p)
            return newset


class MatrixMul(Operation):
    def function(self, x: mohuset, y: mohuset):
        assert x.ndim > 0, f"input operand 0 does not have enough dimensions."
        assert y.ndim > 0, f"input operand 1 does not have enough dimensions."

        newset = mohuset(x.qrung, x.mtype)
        newset.set = x.set @ y.set
        return newset


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

        if isinstance(x, mohunum) and isinstance(y, mohunum):
            return __eq(x, y)

        if isinstance(x, mohunum) and isinstance(y, mohuset):
            vec_func = np.vectorize(__eq)
            return vec_func(x, y.set)

        if isinstance(x, mohuset) and isinstance(y, mohunum):
            vec_func = np.vectorize(__eq)
            return vec_func(x.set, y)

        if isinstance(x, mohuset) and isinstance(y, mohuset):
            vec_func = np.vectorize(__eq)
            return vec_func(x.set, y.set)


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

        if isinstance(x, mohunum) and isinstance(y, mohunum):
            return __ne(x, y)

        if isinstance(x, mohunum) and isinstance(y, mohuset):
            vec_func = np.vectorize(__ne)
            return vec_func(x, y.set)

        if isinstance(x, mohuset) and isinstance(y, mohunum):
            vec_func = np.vectorize(__ne)
            return vec_func(x.set, y)

        if isinstance(x, mohuset) and isinstance(y, mohuset):
            vec_func = np.vectorize(__ne)
            return vec_func(x.set, y.set)


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
            if x0.mtype == 'ivfn' or x0.mtype == 'qrohfn':
                return x0.score < x1.score
            else:
                from .. import fuzznum
                if Equal()(Subtraction()(x0, x1), fuzznum(x0.qrung, 0., 1.)) and Inequality()(x0, x1):
                    return True
                else:
                    return False

        if isinstance(x, mohunum) and isinstance(y, mohunum):
            return __lt(x, y)

        if isinstance(x, mohunum) and isinstance(y, mohuset):
            vec_func = np.vectorize(__lt)
            return vec_func(x, y.set)

        if isinstance(x, mohuset) and isinstance(y, mohunum):
            vec_func = np.vectorize(__lt)
            return vec_func(x.set, y)

        if isinstance(x, mohuset) and isinstance(y, mohuset):
            vec_func = np.vectorize(__lt)
            return vec_func(x.set, y.set)


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
            if x0.mtype == 'ivfn' or x0.mtype == 'qrohfn':
                return x0.score > x1.score
            else:
                from .. import fuzznum
                if Inequality()(Subtraction()(x0, x1), fuzznum(x0.qrung, 0., 1.)) and Inequality()(x0, x1):
                    return True
                else:
                    return False

        if isinstance(x, mohunum) and isinstance(y, mohunum):
            return __gt(x, y)

        if isinstance(x, mohunum) and isinstance(y, mohuset):
            vec_func = np.vectorize(__gt)
            return vec_func(x, y.set)

        if isinstance(x, mohuset) and isinstance(y, mohunum):
            vec_func = np.vectorize(__gt)
            return vec_func(x.set, y)

        if isinstance(x, mohuset) and isinstance(y, mohuset):
            vec_func = np.vectorize(__gt)
            return vec_func(x.set, y.set)


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
            if x0.mtype == 'ivfn' or x0.mtype == 'qrohfn':
                return x0.score <= x1.score
            else:
                from .. import fuzznum
                if Equal()(Subtraction()(x0, x1), fuzznum(x0.qrung, 0., 1.)) or Equal()(x0, x1):
                    return True
                else:
                    return False

        if isinstance(x, mohunum) and isinstance(y, mohunum):
            return __le(x, y)

        if isinstance(x, mohunum) and isinstance(y, mohuset):
            vec_func = np.vectorize(__le)
            return vec_func(x, y.set)

        if isinstance(x, mohuset) and isinstance(y, mohunum):
            vec_func = np.vectorize(__le)
            return vec_func(x.set, y)

        if isinstance(x, mohuset) and isinstance(y, mohuset):
            vec_func = np.vectorize(__le)
            return vec_func(x.set, y.set)


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
            if x0.mtype == 'ivfn' or x0.mtype == 'qrohfn':
                return x0.score >= x1.score
            else:
                from .. import fuzznum
                if Inequality()(Subtraction()(x0, x1), fuzznum(x0.qrung, 0., 1.)) or Equal()(x0, x1):
                    return True
                else:
                    return False

        if isinstance(x, mohunum) and isinstance(y, mohunum):
            return __ge(x, y)

        if isinstance(x, mohunum) and isinstance(y, mohuset):
            vec_func = np.vectorize(__ge)
            return vec_func(x, y.set)

        if isinstance(x, mohuset) and isinstance(y, mohunum):
            vec_func = np.vectorize(__ge)
            return vec_func(x.set, y)

        if isinstance(x, mohuset) and isinstance(y, mohuset):
            vec_func = np.vectorize(__ge)
            return vec_func(x.set, y.set)


def add(x, y):
    return Addition()(x, y)


def sub(x, y):
    return Subtraction()(x, y)


def mul(x, y):
    return Multiplication()(x, y)


def div(x, y):
    return Division()(x, y)


def pow(x, p):
    return Power(p)(x)


def matmul(x, y):
    return MatrixMul()(x, y)


def equal(x, y):
    return Equal()(x, y)


def inequal(x, y):
    return Inequality()(x, y)


def lt(x, y):
    return Lt()(x, y)


def gt(x, y):
    return Gt()(x, y)


def le(x, y):
    return Le()(x, y)


def ge(x, y):
    return Ge()(x, y)