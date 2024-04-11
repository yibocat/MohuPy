#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/7 下午3:04
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import numpy as np

from typing import Union

from ..core import Fuzzarray, Fuzznum
from ..config import Config

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

    mtype = None
    qrung = None

    """
        构造函数，值得注意的是，data可以设置为Fuzzarray，也可以是ndarray，只不过ndarray只参与运算，不进行求导
        另外，目前仅支持 ‘qrofn’ 类型的模糊数，其余暂不支持。原因在于 区间值模糊数和犹豫模糊数的微分理论尚不完善
    """

    def __init__(self, data=None):
        if data is not None:
            if isinstance(data, np.ndarray):
                self.__data = data
                self.mtype = None
                self.qrung = None
                self.shape = data.shape
                self.ndim = data.ndim
                self.size = data.size
            elif isinstance(data, Union[Fuzznum, Fuzzarray]):
                if Config.mtype != 'qrofn':
                    raise NotImplementedError(f'Fuzztensor currently only supports the qrofn fuzzy number type.')
                from .utils import as_fuzzarray
                self.__data = as_fuzzarray(data)
                self.mtype = data.mtype
                self.qrung = data.qrung
                self.shape = data.shape
                self.ndim = data.ndim
                self.size = data.size
            else:
                raise NotImplementedError(f'{type(data).__name__} is not supported.')

    """
        类的特别方法，包括基本打印输出，字符类型，基本运算等等
    """

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
        from .operationFunc import tensor_add
        return tensor_add(self, other)

    def __radd__(self, other):
        from .operationFunc import tensor_add
        return tensor_add(other, self)

    def __sub__(self, other):
        from .operationFunc import tensor_sub
        return tensor_sub(self, other)

    def __mul__(self, other):
        from .operationFunc import tensor_mul
        return tensor_mul(self, other)

    def __rmul__(self, other):
        from .operationFunc import tensor_mul
        return tensor_mul(other, self)

    def __truediv__(self, other):
        from .operationFunc import tensor_div
        return tensor_div(self, other)

    def __pow__(self, p, modulo=None):
        from .operationFunc import tensor_powers
        return tensor_powers(self, p)

    def __matmul__(self, other):
        from .operationFunc import tensor_matmul
        return tensor_matmul(self, other)

    def __rmatmul__(self, other):
        from .operationFunc import tensor_matmul
        return tensor_matmul(other, self)

    """
        Fuzztensor 的特殊方法，包括Fuzzarray的一些特别性质，包括得分，隶属度和非隶属度
        不确定度，补，和转置
    """

    @property
    def score(self):
        if isinstance(self.__data, Fuzzarray):
            return self.__data.score
        else:
            return None

    @property
    def md(self):
        if self.__data is None:
            return None
        if not isinstance(self.__data, Fuzzarray):
            return None
        return self.__data.md

    @property
    def nmd(self):
        if self.__data is None:
            return None
        if not isinstance(self.__data, Fuzzarray):
            return None
        return self.__data.nmd

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
        from .operationFunc import tensor_transpose
        return tensor_transpose(self)

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, fdata):
        if Config.mtype != 'qrofn': raise NotImplementedError(f'Currently only available for fuzzy type \'qrofn\'.')
        if isinstance(fdata, Union[Fuzzarray, Fuzznum]):
            if fdata.qrung is None or fdata.md is None and fdata.nmd is None:
                from .utils import as_fuzzarray
                self.__data = None if isinstance(fdata, Fuzzarray) else as_fuzzarray(fdata)
                self.mtype = Config.mtype
                self.qrung = None if isinstance(fdata, Fuzzarray) else fdata.qrung
                self.shape = ()
                self.ndim = None
                self.size = None if isinstance(fdata, Fuzzarray) else 1
                self.grad = None
                self.creator = None
                self.generation = 0
            else:
                from .utils import as_fuzzarray
                self.__data = as_fuzzarray(fdata)

                self.mtype = self.__data.mtype
                self.qrung = self.__data.qrung
                self.shape = self.__data.shape
                self.ndim = self.__data.ndim
                self.size = self.__data.size if isinstance(fdata, Fuzzarray) else 1
                self.grad = None
                self.creator = None
                self.generation = 0
        elif isinstance(fdata, Union[np.ndarray, int, float, np.int_, np.float_]):
            from .utils import as_array
            self.__data = as_array(fdata)

            self.shape = self.__data.shape
            self.ndim = self.__data.ndim
            self.size = self.__data.size
            self.grad = None
            self.creator = None
            self.generation = 0
            self.qrung = None
            self.mtype = None
        elif fdata is None:
            self.__data = None
            self.shape = ()
            self.ndim = None
            self.size = None
            self.grad = None
            self.creator = None
            self.generation = 0
        else:
            raise TypeError(f'{type(fdata)} is not supported.')

    ## Fuzztensor 的反向微分和特别方法。backward 和set_creator和clear_grad用于自动微分计算
    def set_creator(self, func):
        self.creator = func
        self.generation = func.generation + 1

    def clear_grad(self):
        self.grad = None

    def backward(self, retain_grad=False):
        if self.grad is None:
            if isinstance(self.__data, Fuzzarray):
                # from ..corelib import poss_like
                from ..corelib.lib.classConstruct import PossLikeConstruct
                self.grad = PossLikeConstruct(self.__data)()
            elif isinstance(self.__data, np.ndarray):
                self.grad = np.ones_like(self.__data)
            else:
                raise NotImplementedError(f'{type(self.__data)} is not supported.')

        from .utils import as_fuzzarray
        self.grad = Fuzztensor(as_fuzzarray(self.grad))

        funcs = []
        seen_set = set()

        def add_func(fun):
            if fun not in seen_set:
                funcs.append(fun)
                seen_set.add(fun)
                funcs.sort(key=lambda func: func.generation)

        if self.creator is not None:
            add_func(self.creator)
        else:
            self.creator = self

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

    """
        Fuzztensor 的一些一般方法，包括求和，求积等等张量方法
    """

    def empty(self, onlyfn: bool = False) -> bool:
        """
        Checks if the fuzzy tensor is empty
        onlyfn:  All fuzzy numbers in the fuzzy set are judged
        """
        from .function import TensorEmpty
        return TensorEmpty(onlyfn)(self)

    def valid(self) -> bool:
        """
        Checks if the fuzzy tensor is valid
        """
        from .function import TensorValidity
        return TensorValidity()(self)

    def init(self) -> bool:
        from .function import TensorInit
        return TensorInit()(self)

    # TODO: 排序方法暂不支持
    # def sort(self) -> 'Fuzztensor':
    #     from .functionClass import TensorSort
    #     self = TensorSort()(self)
    #     return self

    def unique(self) -> 'Fuzztensor':
        from .function import TensorUnique
        return TensorUnique()(self)

    def append(self, e) -> 'Fuzztensor':
        from .function import TensorAppend
        return TensorAppend(e)(self)

    def remove(self, e) -> 'Fuzztensor':
        from .function import TensorRemove
        return TensorRemove(e)(self)

    def pop(self, i) -> 'Fuzztensor':
        from .function import TensorPop
        return TensorPop(i)(self)

    def squeeze(self, axis=None) -> 'Fuzztensor':
        from .function import TensorSqueeze
        return TensorSqueeze(axis)(self)

    def clear(self, to_none=False) -> 'Fuzztensor':
        from .function import TensorClear
        return TensorClear(to_none)(self)

    def initialize(self) -> 'Fuzztensor':
        from .function import TensorInitialize
        return TensorInitialize()(self)

    def flatten(self) -> 'Fuzztensor':
        from .function import TensorFlatten
        return TensorFlatten()(self)

    def ravel(self) -> 'Fuzztensor':
        from .function import TensorRavel
        return TensorRavel()(self)

    def max(self, show=False, axis=None) -> 'Fuzztensor':
        from .function import TensorGetMax
        return TensorGetMax(show, axis)(self)

    def min(self, show=False, axis=None) -> 'Fuzztensor':
        from .function import TensorGetMin
        return TensorGetMin(show, axis)(self)

    def fmax(self, func, *params, show=False, axis=None) -> 'Fuzztensor':
        from .function import TensorGetFmax
        return TensorGetFmax(show, axis, func, *params)(self)

    def fmin(self, func, *params, show=False, axis=None) -> 'Fuzztensor':
        from .function import TensorGetFmin
        return TensorGetFmin(show, axis, func, *params)(self)

    """
        带有自动微分的方法，这些都包含计算相关，在深度学习框架中可以很好地发挥
    """
    ##
    def reshape(self, *shape):
        from .operationFunc import tensor_reshape
        return tensor_reshape(self, *shape)

    def broadcast(self, *shape):
        from .operationFunc import tensor_broadcast_to
        return tensor_broadcast_to(self, shape)

    def sum(self, axis=None, keepdims=False):
        from .operationFunc import tensor_sum
        return tensor_sum(self, axis, keepdims)

    def __getitem__(self, item):
        from .operationFunc import tensor_getitem
        return tensor_getitem(self, item)

    def prod(self, axis=None, keepdims=False):
        from .operationFunc import tensor_prod
        return tensor_prod(self, axis, keepdims)

    def mean(self, axis=None):
        from .operationFunc import tensor_mean
        return tensor_mean(self, axis)
