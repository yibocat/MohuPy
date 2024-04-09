#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/7 下午3:07
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import weakref

from .fuzztensor import Fuzztensor
# from .config import Config
from ..config import Config
from .utils import as_fuzztensor


class Operation:
    def __call__(self, *inputs):
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

    def forward(self, *xs):
        raise NotImplementedError()

    def backward(self, *gys):
        raise NotImplementedError()










