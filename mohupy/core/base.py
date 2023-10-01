#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/9/29 上午10:36
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import abc


class MohuBase(abc.ABC):
    __shape = ()
    __ndim = 0
    size = 0

    def __init__(self):
        pass

    def __add__(self, other):
        pass

    def __radd__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __rmul__(self, other):
        pass

    def __truediv__(self, other):
        pass

    def __pow__(self, power, modulo=None):
        pass

    def __and__(self, other):
        pass

    def __or__(self, other):
        pass

    def __eq__(self, other):
        pass

    def __ne__(self, other):
        pass

    def __lt__(self, other):
        pass

    def __gt__(self, other):
        pass

    def __le__(self, other):
        pass

    def __ge__(self, other):
        pass

    @property
    def shape(self):
        return self.__shape

    @property
    def ndim(self):
        return self.__ndim

    def is_valid(self):
        pass

    def isEmpty(self):
        pass

    def convert(self):
        pass

    def plot(self):
        pass

    def max(self):
        return self

    def min(self):
        return self

    def mean(self):
        return self

    def sum(self):
        return self
