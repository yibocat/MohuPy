#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/7 下午3:04
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import numpy as np

from typing import Union

from ..core import Fuzzarray, Fuzznum
from .base import FuzzTensorBase


class Fuzztensor(FuzzTensorBase):
    """
        模糊张量类，不同于 Fuzzarray 和 Fuzznum，Fuzztensor 可以进行函数的正向传播运算和反向传播
        运算，也就是说，Fuzztensor 可以进行复杂模糊函数的微分与高阶微分运算。

        # Attribute
        ---------
        - shape:          形状
        - ndim:           维度
        - size:           大小
        - grad:           梯度
        - creator:        创造者，这个属性其实就表示当前 Fuzztensor 由哪个函数计算而来
        - generation:     梯度代数，在计算图模型中，每个运算都有一个优先级，而 generation 则表示当前 Fuzztensor 的优先级代数
        - data:           存储数据
        # Note
        ---------
        Fuzztensor 不能单独存在，其存储数据格式为 Fuzzarray，此外，ndarray 参与运算。注意：Fuzznum
        也可以设置为其数据格式，但是会转换成 Fuzzarray 的形式。
    """
    __array_priority__ = 200
    shape = ()
    ndim = None
    size = None
    __data = None
    grad = None
    creator = None
    generation = 0

    ## 构造函数，值得注意的是，data可以设置为Fuzzarray，也可以是ndarray，只不过ndarray只参与运算，不进行求导
    ## 另外，目前仅支持 ‘qrofn’ 类型的模糊数，其余暂不支持。原因在于 区间值模糊数和犹豫模糊数的微分理论尚不完善

    def __init__(self, data=None):
        if data is not None:
            if isinstance(data, Union[Fuzznum, Fuzzarray]):
                # TODO: 目前仅适用于qrofn，需要适配 ivfn 和 qrohfn
                if data.mtype == 'ivfn' or data.mtype == 'qrohfn':
                    raise NotImplementedError(f'{data.mtype} is not implemented yet. Please use qrofn.')

                from .utils import as_fuzzarray
                self.__data = as_fuzzarray(data)

                self.mtype = self.__data.mtype
                self.qrung = self.__data.qrung

                self.shape = self.__data.shape
                self.ndim = self.__data.ndim
                self.size = self.__data.size
            elif isinstance(data, np.ndarray):
                self.__data = data

                self.shape = self.__data.shape
                self.ndim = self.__data.ndim
                self.size = self.__data.size
            else:
                raise TypeError(f'{type(data).__name__} is not supported.')

    ## 类的特别方法，保罗基本的打印输出，字符类型，基本运算等等

    def __repr__(self):
        if self.__data is None:
            return 'Fuzztensor(None)'
        p = str(self.__data).replace('\n', '\n' + ' ' * 11)
        if isinstance(self.__data, Fuzzarray):
            return f'Fuzztensor({p}, qrung={self.__data.qrung}, mtype={self.__data.mtype})'
        if isinstance(self.__data, Union[np.ndarray, np.int_, np.float_, float, int]):
            return f'Fuzztensor({p}, mtype=ndarray:{self.__data.dtype})'

    def __len__(self):
        return len(self.__data)

    def __str__(self):
        return str(self.__data)

    def __add__(self, other):
        from .operation import add
        return add(self, other)

    def __radd__(self, other):
        from .operation import add
        return add(other, self)

    def __sub__(self, other):
        from .operation import sub
        return sub(self, other)

    def __mul__(self, other):
        from .operation import mul
        return mul(self, other)

    def __rmul__(self, other):
        from .operation import mul
        return mul(other, self)

    def __truediv__(self, other):
        from .operation import div
        return div(self, other)

    def __pow__(self, p, modulo=None):
        from .operation import powers
        return powers(self, p)

    def __matmul__(self, other):
        from .operation import matmul
        return matmul(self, other)

    def __rmatmul__(self, other):
        from .operation import matmul
        return matmul(other, self)

    ## Fuzztensor 的特殊方法，包括Fuzzarray的一些特别性质，包括得分，隶属度和非隶属度
    ## 不确定度，补，和转置

    @property
    def score(self):
        if isinstance(self.__data, Fuzzarray):
            return self.__data.score
        else:
            return None

    @property
    def md(self):
        if isinstance(self.__data, Fuzzarray):
            return self.__data.md
        else:
            return None

    @property
    def nmd(self):
        if isinstance(self.__data, Fuzzarray):
            return self.__data.nmd
        else:
            return None

    @property
    def ind(self):
        if isinstance(self.__data, Fuzzarray):
            return self.__data.ind
        else:
            return None

    @property
    def comp(self):
        if isinstance(self.__data, Fuzzarray):
            return self.__data.comp
        else:
            return None

    @property
    def T(self):
        # TODO: 添加转置，这个转置方法需要特别函数
        return None

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, fdata):
        if isinstance(fdata, Union[Fuzzarray, Fuzznum]):
            if fdata.mtype == 'qrofn':
                from .utils import as_fuzzarray
                self.__data = as_fuzzarray(fdata)

                self.mtype = self.__data.mtype
                self.qrung = self.__data.qrung

                self.shape = self.__data.shape
                self.ndim = self.__data.ndim
                self.size = self.__data.size
            elif fdata.mtype is None and fdata.qrung is None:
                self.__data = None
                self.mtype = None
                self.qrung = None
                self.shape = ()
                self.ndim = None
                self.size = None
            else:
                raise TypeError(f'The mtype must be \'qrofn\'.')
        elif isinstance(fdata, Union[np.ndarray, int, float, np.int_, np.float_]):
            from .utils import as_array
            self.__data = as_array(fdata)

            self.shape = self.__data.shape
            self.ndim = self.__data.ndim
            self.size = self.__data.size
        else:
            raise TypeError(f'{type(fdata).__name__} is not supported.')

    ## Fuzztensor 的反向微分和特别方法。backward 和set_creator和clear_grad用于自动微分计算

    def set_creator(self, func):
        self.creator = func
        self.generation = func.generation + 1

    def clear_grad(self):
        self.grad = None

    def backward(self, retain_grad=False):
        if self.grad is None:
            if isinstance(self.__data, Fuzzarray):
                from ..corelib import poss_like
                self.grad = poss_like(self.__data)
            elif isinstance(self.__data, np.ndarray):
                self.grad = np.ones_like(self.__data)
            else:
                raise NotImplemented

        from .utils import as_fuzzarray
        self.grad = Fuzztensor(as_fuzzarray(self.grad))

        funcs = []
        seen_set = set()

        def add_func(fun):
            if fun not in seen_set:
                funcs.append(fun)
                seen_set.add(fun)
                funcs.sort(key=lambda func: func.generation)

        add_func(self.creator)

        while funcs:
            f = funcs.pop()
            gys = [output().grad for output in f.outputs]
            gxs = f.backward(*gys)

            if not isinstance(gxs, tuple):
                gxs = (gxs,)
            for x, gx in zip(f.inputs, gxs):
                if x.grad is None:
                    x.grad = gx
                else:
                    x.grad = x.grad + gx

                if x.creator is not None:
                    add_func(x.creator)

            if not retain_grad:
                for y in f.outputs:
                    y().clear_grad()

    ## Fuzztensor 的一些一般方法，包括求和，求积等等张量方法
    def empty(self, only_data=False):
        from .functionClass import TensorEmpty
        return TensorEmpty(only_data)(self)

    def valid(self):
        from .functionClass import TensorValidity
        return TensorValidity()(self)

    def initial(self):
        from .functionClass import TensorInitial
        return TensorInitial()(self)

    def sort(self) -> 'Fuzztensor':
        from .functionClass import TensorSort
        return TensorSort()(self)

    def unique(self) -> 'Fuzztensor':
        from .functionClass import TensorUnique
        return TensorUnique()(self)

    def append(self, e) -> 'Fuzztensor':
        from .functionClass import TensorAppend
        return TensorAppend()(self, e)

    def remove(self, e) -> 'Fuzztensor':
        from .functionClass import TensorRemove
        return TensorRemove()(self, e)

    def pop(self, i) -> 'Fuzztensor':
        from .functionClass import TensorPop
        return TensorPop()(self, i)

    def reshape(self, *n) -> 'Fuzztensor':
        # TODO: reshape 需要特别的反向微分求导方法
        ...

    def squeeze(self, axis=None) -> 'Fuzztensor':
        from .functionClass import TensorSqueeze
        return TensorSqueeze()(self, axis)

    def clear(self) -> 'Fuzztensor':
        from .functionClass import TensorClear
        return TensorClear()(self)

    def broadcast_to(self, *tensors) -> 'Fuzztensor':
        from .functionClass import TensorBroadcast
        return TensorBroadcast()(self, tensors)

    def max(self, show=False, axis=None) -> 'Fuzztensor':
        from .functionClass import TensorGetMax
        return TensorGetMax()(self, show, axis)

    def min(self, show=False, axis=None) -> 'Fuzztensor':
        from .functionClass import TensorGetMin
        return TensorGetMin()(self, show, axis)

    def fmax(self, func, *args, show=False, axis=None) -> 'Fuzztensor':
        from .functionClass import TensorGetFmax
        return TensorGetFmax()(self, func, *args, show, axis)

    def fmin(self, func, *args, show=False, axis=None) -> 'Fuzztensor':
        from .functionClass import TensorGetFmin
        return TensorGetFmin()(self, func, *args, show, axis)

    def sum(self, axis=None, keepdims=False) -> 'Fuzztensor':
        from .functionClass import TensorGetSum
        return TensorGetSum()(self, axis, keepdims)

    def prod(self, axis=None, keepdims=False) -> 'Fuzztensor':
        from .functionClass import TensorGetProd
        return TensorGetProd()(self, axis, keepdims)

    def mean(self, axis=None) -> 'Fuzztensor':
        from .functionClass import TensorGetMean
        return TensorGetMean()(self, axis)















