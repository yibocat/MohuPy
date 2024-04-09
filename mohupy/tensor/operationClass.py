#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/7 下午3:44
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import numpy as np

from .operationBase import Operation
from ..core import Fuzzarray
from ..corelib import poss_like, negs_like, zeros, dot
from .utils import as_fuzzarray, as_fuzztensor
from ..config import Config


class Add(Operation):
    def forward(self, x0, x1):
        # self.x0_shape, self.x1_shape = x0.shape, x1.shape
        y = x0 + x1
        return (y,)

    def backward(self, grad):
        x1 = self.inputs[0].data
        x2 = self.inputs[1].data

        y1 = poss_like(x1)
        y2 = poss_like(x2)

        y1 = as_fuzzarray(y1)
        y2 = as_fuzzarray(y2)

        # if self.x0_shape != self.x1_shape:
        # y1 = sum_to(y1, self.x0_shape)
        # y2 = sum_to(y2, self.x1_shape)

        return as_fuzztensor(y1), as_fuzztensor(y2)


class Sub(Operation):
    def forward(self, x0, x1):
        # self.x0_shape, self.x1_shape = x0.shape, x1.shape
        y = x0 - x1
        return y

    def backward(self, grad):
        x1 = self.inputs[0].data
        x2 = self.inputs[1].data

        y1 = poss_like(x1)
        y2 = negs_like(x2)

        y1 = as_fuzzarray(y1)
        y2 = as_fuzzarray(y2)

        # if self.x0_shape != self.x1_shape:
        #     y1 = sum_to(y1, self.x0_shape)
        #     y2 = sum_to(y2, self.x1_shape)
        return as_fuzztensor(y1), as_fuzztensor(y2)


class Mul(Operation):
    def forward(self, x0, x1):
        # self.x0_shape, self.x1_shape = x0.shape, x1.shape
        y = x0 * x1
        return y

    def backward(self, grad):
        x1 = self.inputs[0].data
        x2 = self.inputs[1].data

        if isinstance(x1, Fuzzarray) and isinstance(x2, Fuzzarray):
            q = self.inputs[0].data.qrung

            def deriv(x, h):
                res = zeros(qrung=q)
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

            # if self.x0_shape != self.x1_shape:
            #     gy0 = sum_to(gy0, self.x0_shape)
            #     gy1 = sum_to(gy1, self.x1_shape)

            return gy0, gy1

        if isinstance(x1, Fuzzarray) and not isinstance(x2, Fuzzarray):
            x2 = np.array(x2)
            if np.all(x2 > 1):
                raise ValueError("The value must be less than 1.")

            def deriv(x, a):
                res = zeros(qrung=q)
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
                res = zeros(qrung=q)
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
                res = zeros(qrung=q)
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
            from ..corelib import poss
            res = poss(qrung=q)
            if f.md < 0.99 and f.nmd > 0.003:
                res.md = (((1 - f.md ** q) / (1 - f.md ** (l * q))) * l * f.md ** ((l - 1) * q)) ** (1 / q)
                res.nmd = (1 - (f.nmd ** q) / (1 - (1 - f.nmd ** q) ** l) * l * (1 - f.nmd ** q) ** (l - 1)) ** (1 / q)
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
        y = dot(x0, x1)
        return y

    def backward(self, grad):
        x1 = self.inputs[0].data
        x2 = self.inputs[1].data
        from .operation import matmul
        return matmul(grad, x2.T), matmul(x1.T, grad)


class Transpose(Operation):
    def forward(self, x):
        y = x.T
        return y

    def backward(self, grad):
        from .operation import transpose
        gx = transpose(grad)
        return gx
