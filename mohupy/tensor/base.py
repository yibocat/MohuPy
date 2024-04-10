#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/7 下午3:04
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import abc
import weakref

from ..config import Config


class FuzzTensorBase(abc.ABC):
    """
        FuzzTensorBase is a tensor base based on Fuzzarray
    """


class FuzzTensorFunctionBase:
    """
    模糊张量方法的基本类，即可当作 Fuzztensor 的运算类基类，也可作为一般方法的基类
    需要注意的是，当作为 Fuzztensor 的基本运算类的父类时，需要重载函数 __call__。
    """
    def __call__(self, *inputs):
        return self.forward(*inputs)

    def forward(self, *xs):
        raise NotImplementedError()

    def backward(self, *gys):
        raise NotImplementedError()


class Operation(FuzzTensorFunctionBase):
    """
    Fuzztensor 的基本运算类，父类继承自Fuzztensor的基本方法类 FuzzTensorFunctionBase，
    其主要差别在于其 __call__ 参与了自动微分，执行一些特殊的方法。
    """
    def __call__(self, *inputs):

        from .utils import as_fuzztensor
        from .fuzztensor import Fuzztensor
        inputs = [as_fuzztensor(x) for x in inputs]
        xs = [x.data for x in inputs]
        ys = self.forward(*xs)
        if not isinstance(ys, tuple):
            ys = (ys,)
        outputs = [Fuzztensor(y) for y in ys]

        if Config.enable_backprop:
            self.generation = max([x.generation for x in inputs])
            for output in outputs:
                output.set_creator(self)

            self.inputs = inputs  # 保存输入变量
            self.outputs = [weakref.ref(output) for output in outputs]  # 保存输出变量

        return outputs if len(outputs) > 1 else outputs[0]


class Function(FuzzTensorFunctionBase):
    ...

