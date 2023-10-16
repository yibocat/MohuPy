#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/9/29 上午10:36
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import abc


class MohuBase(abc.ABC):
    """
        Fuzzy base class is an abstract class, which is the base class of
        fuzzy numbers and fuzzy sets.
        The base class contains three attributes, basic operation rules
        (addition, subtraction, multiplication, division, exponentiation
        and intersection, comparison operations), and basic methods.
    """
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

    def max(self, axis=None):
        return self

    def min(self, axis=None):
        return self

    def mean(self, axis=None):
        return self

    def sum(self, axis=None):
        return self


class fuzzNum(MohuBase):
    """
        Fuzzy number base class, which inherits from the fuzzy base class.
        This class serves as the base class of fuzzy numbers and is intended
        to be distinguished from fuzzy set classes.

        TODO: This category will be adjusted later according to needs.
    """
    qrung = None
    md = None
    nmd = None
    mtype = None

    def __init__(self):
        super().__init__()
        pass

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def score(self):
        pass

    def acc(self):
        pass

    def ind(self):
        pass

    def comp(self):
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

    def is_valid(self):
        pass

    def isEmpty(self):
        pass

    def convert(self):
        pass
