#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/10 下午8:54
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import numpy as np

from .base import Operation
from .utils import as_fuzzarray
from .utils import as_fuzztensor

from ..core import Fuzzarray
# from ..corelib import poss_like, negs_like, zeros, dot, negs


class Add(Operation):
    def forward(self, x0, x1):
        self.x0_shape, self.x1_shape = x0.shape, x1.shape
        y = x0 + x1
        return (y,)

    def backward(self, grad):
        x1 = self.inputs[0].data
        x2 = self.inputs[1].data

        from ..corelib.lib.classConstruct import PossLikeConstruct
        y1 = PossLikeConstruct(x1)()
        y2 = PossLikeConstruct(x2)()

        y1 = as_fuzzarray(y1)
        y2 = as_fuzzarray(y2)

        if self.x0_shape != self.x1_shape:
            y1 = SumTo.sum_to(y1, self.x0_shape)
            y2 = SumTo.sum_to(y2, self.x1_shape)

        return as_fuzztensor(y1), as_fuzztensor(y2)


class Sub(Operation):
    def forward(self, x0, x1):
        self.x0_shape, self.x1_shape = x0.shape, x1.shape
        y = x0 - x1
        return y

    def backward(self, grad):
        x1 = self.inputs[0].data
        x2 = self.inputs[1].data

        from ..corelib.lib.classConstruct import PossLikeConstruct, NegsLikeConstruct
        y1 = PossLikeConstruct(x1)()
        y2 = NegsLikeConstruct(x2)()

        y1 = as_fuzzarray(y1)
        y2 = as_fuzzarray(y2)

        if self.x0_shape != self.x1_shape:
            y1 = SumTo.sum_to(y1, self.x0_shape)
            y2 = SumTo.sum_to(y2, self.x1_shape)
        return as_fuzztensor(y1), as_fuzztensor(y2)


class Mul(Operation):
    def forward(self, x0, x1):
        self.x0_shape, self.x1_shape = x0.shape, x1.shape
        y = x0 * x1
        return y

    def backward(self, grad):
        x1 = self.inputs[0].data
        x2 = self.inputs[1].data

        if isinstance(x1, Fuzzarray) and isinstance(x2, Fuzzarray):
            q = self.inputs[0].data.qrung

            def deriv(x, h):
                from ..corelib.lib.classConstruct import ZerosConstruct
                res = ZerosConstruct(qrung=q)()
                res.md = (1 + (h.md ** q - 1) / (1 - x.md ** q * h.md ** q)) ** (1 / q)
                res.nmd = (h.nmd ** q) / (x.nmd ** q + h.nmd ** q - x.nmd ** q * h.nmd ** q)
                return res

            newset1 = Fuzzarray(q)
            newset2 = Fuzzarray(q)

            vec_func = np.vectorize(deriv)
            y1 = vec_func(x1, x2)
            y2 = vec_func(x2, x1)

            newset1.array = y1
            newset2.array = y2

            n1 = as_fuzztensor(newset1)
            n2 = as_fuzztensor(newset2)

            gy0, gy1 = n2 * grad, n1 * grad

            if self.x0_shape != self.x1_shape:
                gy0 = SumTo.sum_to(gy0, self.x0_shape)
                gy1 = SumTo.sum_to(gy1, self.x1_shape)

            return gy0, gy1

        if isinstance(x1, Fuzzarray) and not isinstance(x2, Fuzzarray):
            x2 = np.array(x2)
            if np.all(x2 > 1):
                raise ValueError("The value must be less than 1.")

            def deriv(x, a):
                from ..corelib.lib.classConstruct import ZerosConstruct
                res = ZerosConstruct(qrung=q)()
                if a == 1 or a == 0:
                    res.md = a ** (1 / q)
                    res.nmd = (1 - a) ** (1 / q)
                else:
                    res.md = a ** (1 / q)
                    res.nmd = (1 - 1e-6 - a) ** (1 / q)
                return res

            q = self.inputs[0].data.qrung
            newset = Fuzzarray(q)

            vec_func = np.vectorize(deriv)
            y = vec_func(x1, x2)
            newset.array = y

            return newset * grad, x1 * grad

        if not isinstance(x1, Fuzzarray) and isinstance(x2, Fuzzarray):
            x1 = np.array(x1)
            if np.all(x1 > 1):
                raise ValueError("The value must be less than 1.")

            def deriv(x, a):
                from ..corelib.lib.classConstruct import ZerosConstruct
                res = ZerosConstruct(qrung=q)()
                if a == 1 or a == 0:
                    res.md = a ** (1 / q)
                    res.nmd = (1 - a) ** (1 / q)
                else:
                    res.md = a ** (1 / q)
                    res.nmd = (1 - 1e-6 - a) ** (1 / q)
                return res

            q = self.inputs[1].data.qrung
            newset = Fuzzarray(q)
            vec_func = np.vectorize(deriv)
            y = vec_func(x2, x1)
            newset.array = y

            return x2 * grad, newset * grad


class Div(Operation):
    def forward(self, x0, x1):
        y = x0 / x1
        return y

    def backward(self, grad):
        x1 = self.inputs[0].data
        x2 = 1 / self.inputs[1].data

        if isinstance(x1, Fuzzarray) and not isinstance(x2, Fuzzarray):
            x2 = np.array(x2)
            if np.all(x2 > 1):
                raise ValueError("The value must be less than 1.")

            def deriv(x, a):
                from ..corelib.lib.classConstruct import ZerosConstruct
                res = ZerosConstruct(qrung=q)()
                if a == 1 or a == 0:
                    res.md = a ** (1 / q)
                    res.nmd = (1 - a) ** (1 / q)
                else:
                    res.md = a ** (1 / q)
                    res.nmd = (1 - 1e-6 - a) ** (1 / q)
                return res

            q = self.inputs[0].data.qrung
            newset = Fuzzarray(q)

            vec_func = np.vectorize(deriv)
            y = vec_func(x1, x2)
            newset.array = y

            return newset * grad, x1 * grad


class Power(Operation):
    def __init__(self, p):
        self.power = p

    def forward(self, x):
        y = x ** self.power
        return y

    def backward(self, grad):
        q = self.inputs[0].data.qrung
        x = self.inputs[0].data

        l = self.power

        def deriv(f):
            # from ..corelib import poss
            from ..corelib.lib.classConstruct import PossConstruct
            res = PossConstruct(qrung=q)()
            if f.md < 0.99 and f.nmd > 0.003:
                res.md = (((1 - f.md ** q) / (1 - f.md ** (l * q)))
                          * l * f.md ** ((l - 1) * q)) ** (1 / q)
                res.nmd = (1 - (f.nmd ** q) / (1 - (1 - f.nmd ** q) ** l)
                           * l * (1 - f.nmd ** q) ** (l - 1)) ** (1 / q)
            else:
                pass
            return res

        newset = Fuzzarray(q)
        vec_func = np.vectorize(deriv)
        y = vec_func(x)
        newset.array = y
        n = as_fuzztensor(newset)
        return n * grad


class Matmul(Operation):
    def forward(self, x0, x1):
        from ..corelib.math.classProduct import Dot
        y = Dot()(x0, x1)
        return y

    def backward(self, grad):
        x1 = self.inputs[0].data
        x2 = self.inputs[1].data

        from .operationFunc import tensor_matmul
        return tensor_matmul(grad, x2.T), tensor_matmul(x1.T, grad)


class Transpose(Operation):
    def forward(self, x):
        y = x.T
        return y

    def backward(self, grad):
        from .operationFunc import tensor_transpose
        gx = tensor_transpose(grad)
        return gx


class Reshape(Operation):

    def __init__(self, shape):
        self.shape = shape

    def forward(self, x):
        self.x_shape = x.shape
        y = x.reshape(*self.shape)
        return y

    def backward(self, grad):
        from .operationFunc import tensor_reshape
        return tensor_reshape(grad, self.x_shape)


class Sum(Operation):
    def __init__(self, axis, keepdims):
        self.axis = axis
        self.keepdims = keepdims

    def forward(self, x):
        self.x_shape = x.shape
        y = x.sum(axis=self.axis, keepdims=self.keepdims)
        return y

    def backward(self, grad):
        from .utils import reshape_sum_backward
        gy = reshape_sum_backward(grad, self.x_shape, self.axis, self.keepdims)
        from .operationFunc import tensor_broadcast_to
        gx = tensor_broadcast_to(gy, self.x_shape)
        return gx


class Mean(Operation):
    def __init__(self, axis):
        self.axis = axis

    # TODO: 平均数的正向函数和反向微分


class Prod(Operation):
    def __init__(self, axis, keepdims):
        self.axis = axis
        self.keepdims = keepdims

    # TODO: 连乘的正向函数和反向微分


class BroadcastTo(Operation):
    def __init__(self, shape):
        self.shape = shape

    def forward(self, x):
        self.x_shape = x.shape
        from ..core.funcitonClass import FuzzBroadcast

        y = FuzzBroadcast(*self.shape)(x)
        return y

    def backward(self, grad):
        gx = SumTo.sum_to(grad, self.x_shape)
        return gx


class SumTo(Operation):
    def __init__(self, shape):
        self.shape = shape

    def forward(self, x):
        self.x_shape = x.shape
        from .utils import sumto
        y = sumto(x, self.shape)
        return y

    def backward(self, grad):
        from .operationFunc import tensor_broadcast_to
        gx = tensor_broadcast_to(grad, self.x_shape)
        return gx

    @staticmethod
    def sum_to(x, shape):
        if x.shape == shape:
            return as_fuzztensor(x)
        return SumTo(shape)(x)


class GetItem(Operation):
    def __init__(self, slices):
        self.slices = slices

    def forward(self, x):
        return x[self.slices]

    def backward(self, grad):
        x, = self.inputs
        f = GetItemGrad(self.slices, x.shape)
        return f(grad)


class GetItemGrad(Operation):
    def __init__(self, slices, in_shape):
        self.slices = slices
        self.in_shape = in_shape

    def forward(self, x):
        from ..corelib.lib.classConstruct import NegsConstruct
        gx = NegsConstruct(x.qrung)(*self.in_shape)
        np.add.at(gx.array, self.slices, x.array)
        return gx

    def backward(self, grad):
        return GetItem(self.slices)(grad)
