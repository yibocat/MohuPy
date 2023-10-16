from typing import Union

import numpy as np
from matplotlib import pyplot as plt

from mohupy import asfuzzset
from mohupy.core.base import fuzzNum


# from .mohu import fuzzType
#
# @fuzzType('template')
class template(fuzzNum):
    """
        This class is a template class used to create new fuzzy numbers
        (hesitant fuzzy numbers, etc.). It contains basic algorithms.
        To use this class, run the mp.download_template(path) function,
        where path means downloading the template to the specified location.
    """
    qrung = None
    mtype = None

    def __init__(self):
        super().__init__()
        pass

    def __repr__(self):
        pass

    def __str__(self):
        pass

    @property
    def score(self):
        return None

    @property
    def acc(self):
        return None

    @property
    def ind(self):
        return None

    @property
    def comp(self):
        return None

    def __add__(self, other):
        q = self.qrung

        def __add(oth: template):
            pass

        if isinstance(other, template):
            return __add(other)

        from mohupy.core.mohusets import mohuset
        if isinstance(other, mohuset):
            # Judgment syntax

            vec_func = np.vectorize(__add)
            newset = mohuset(q, self.mtype)
            newset.set = vec_func(other.set)
            return newset
        raise TypeError(f'Invalid type: {type(other)}')

    def __radd__(self, other):
        q = self.qrung

        def __add(oth: template):
            pass

        if isinstance(other, template):
            return __add(other)

        from mohupy.core.mohusets import mohuset
        if isinstance(other, mohuset):
            # Judgment syntax

            vec_func = np.vectorize(__add)
            newset = mohuset(q, self.mtype)
            newset.set = vec_func(other.set)
            return newset
        raise TypeError(f'Invalid type: {type(other)}')

    def __sub__(self, other):
        q = self.qrung

        def __sub(oth: template):
            pass

        if isinstance(other, template):
            return __sub(other)

        from mohupy.core.mohusets import mohuset
        if isinstance(other, mohuset):
            # Judgment syntax

            vec_func = np.vectorize(__sub)
            newset = mohuset(q, self.mtype)
            newset.set = vec_func(other.set)
            return newset
        raise TypeError(f'Invalid type: {type(other)}')

    def __mul__(self, other):
        q = self.qrung

        def __mul(oth: Union[template, float, int, np.int_, np.float_]):
            if isinstance(oth, template):
                pass
            if isinstance(oth, Union[float, int, np.int_, np.float_]):
                pass

        if isinstance(other, Union[template, float, int, np.int_, np.float_]):
            return __mul(other)

        from mohupy.core.mohusets import mohuset
        if isinstance(other, mohuset):
            # Judgment syntax

            vec_func = np.vectorize(__mul)
            newset = mohuset(q, self.mtype)
            newset.set = vec_func(other.set)
            return newset
        if isinstance(other, np.ndarray):
            # Judgment syntax

            vec_func = np.vectorize(__mul)
            newset = mohuset(q, self.mtype)
            newset.set = vec_func(other)
            return newset
        raise TypeError(f'Invalid type: {type(other)}')

    def __rmul__(self, other):
        q = self.qrung

        def __mul(oth: Union[template, float, int, np.int_, np.float_]):
            if isinstance(oth, template):
                pass
            if isinstance(oth, Union[float, int, np.int_, np.float_]):
                pass

        if isinstance(other, Union[template, float, int, np.int_, np.float_]):
            return __mul(other)

        from mohupy.core.mohusets import mohuset
        if isinstance(other, mohuset):
            # Judgment syntax

            vec_func = np.vectorize(__mul)
            newset = mohuset(q, self.mtype)
            newset.set = vec_func(other.set)
            return newset
        if isinstance(other, np.ndarray):
            # Judgment syntax

            vec_func = np.vectorize(__mul)
            newset = mohuset(q, self.mtype)
            newset.set = vec_func(other)
            return newset
        raise TypeError(f'Invalid type: {type(other)}')

    def __truediv__(self, other):
        q = self.qrung

        def __truediv(oth: Union[template, float, int, np.int_, np.float_]):
            if isinstance(oth, template):
                pass
            if isinstance(oth, Union[float, int, np.int_, np.float_]):
                pass

        if isinstance(other, Union[template, float, int, np.int_, np.float_]):
            return __truediv(other)

        from mohupy.core.mohusets import mohuset
        if isinstance(other, mohuset):
            # Judgment syntax

            vec_func = np.vectorize(__truediv)
            newset = mohuset(q, self.mtype)
            newset.set = vec_func(other.set)
            return newset
        if isinstance(other, np.ndarray):
            # Judgment syntax

            vec_func = np.vectorize(__truediv)
            newset = mohuset(q, self.mtype)
            newset.set = vec_func(other)
            return newset
        raise TypeError(f'Invalid type: {type(other)}')

    def __pow__(self, power, modulo=None):
        q = self.qrung

        def __pow(p: Union[float, int, np.int_, np.float_]):
            pass

        if isinstance(power, Union[float, int, np.int_, np.float_]):
            return __pow(power)

        from mohupy.core.mohusets import mohuset
        if isinstance(power, np.ndarray):
            # Judgment syntax

            vec_func = np.vectorize(__pow)
            newset = mohuset(q, self.mtype)
            newset.set = vec_func(power)
            return newset
        raise TypeError(f'Invalid type: {type(power)}')

    def __and__(self, other):
        q = self.qrung

        def __and(oth: template):
            pass

        if isinstance(other, template):
            return __and(other)
        from mohupy.core.mohusets import mohuset
        if isinstance(other, mohuset):
            newset = mohuset(q, self.mtype)
            vec_func = np.vectorize(__and)
            newset.set = vec_func(other.set)
            return newset
        raise TypeError(f'Invalid type: {type(other)}')

    def __or__(self, other):
        q = self.qrung

        def __or(oth: template):
            pass

        if isinstance(other, template):
            return __or(other)
        from mohupy.core.mohusets import mohuset
        if isinstance(other, mohuset):
            newset = mohuset(q, self.mtype)
            vec_func = np.vectorize(__or)
            newset.set = vec_func(other.set)
            return newset
        raise TypeError(f'Invalid type: {type(other)}')

    def __eq__(self, other):
        def __eq(oth: template):
            pass

        if isinstance(other, template):
            return __eq(other)
        from mohupy.core.mohusets import mohuset
        if isinstance(other, mohuset):
            vec_func = np.vectorize(__eq)
            res = vec_func(other.set)
            return res

    def __ne__(self, other):
        def __ne(oth: template):
            pass

        if isinstance(other, template):
            return __ne(other)
        from mohupy.core.mohusets import mohuset
        if isinstance(other, mohuset):
            vec_func = np.vectorize(__ne)
            res = vec_func(other.set)
            return res

    def __lt__(self, other):
        q = self.qrung

        def __lt(oth: template):
            pass

        if isinstance(other, template):
            return __lt(other)
        from mohupy.core.mohusets import mohuset
        if isinstance(other, mohuset):
            vec_func = np.vectorize(__lt)
            res = vec_func(other.set)
            return res
        if isinstance(other, np.ndarray):
            vec_func = np.vectorize(__lt)
            res = vec_func(other)
            return res
        raise TypeError(f'Invalid type: {type(other)}')

    def __gt__(self, other):
        q = self.qrung

        def __gt(oth: template):
            pass

        if isinstance(other, template):
            return __gt(other)
        from mohupy.core.mohusets import mohuset
        if isinstance(other, mohuset):
            vec_func = np.vectorize(__gt)
            res = vec_func(other.set)
            return res
        if isinstance(other, np.ndarray):
            vec_func = np.vectorize(__gt)
            res = vec_func(other)
            return res
        raise TypeError(f'Invalid type: {type(other)}')

    def __le__(self, other):
        q = self.qrung

        def __le(oth: template):
            pass

        if isinstance(other, template):
            return __le(other)
        from mohupy.core.mohusets import mohuset
        if isinstance(other, mohuset):
            vec_func = np.vectorize(__le)
            res = vec_func(other.set)
            return res
        if isinstance(other, np.ndarray):
            vec_func = np.vectorize(__le)
            res = vec_func(other)
            return res
        raise TypeError(f'Invalid type: {type(other)}')

    def __ge__(self, other):
        q = self.qrung

        def __ge(oth: template):
            pass

        if isinstance(other, template):
            return __ge(other)
        from mohupy.core.mohusets import mohuset
        if isinstance(other, mohuset):
            vec_func = np.vectorize(__ge)
            res = vec_func(other.set)
            return res
        if isinstance(other, np.ndarray):
            vec_func = np.vectorize(__ge)
            res = vec_func(other)
            return res
        raise TypeError(f'Invalid type: {type(other)}')

    def is_valid(self):
        pass

    def isEmpty(self):
        pass

    def convert(self):
        pass

    def reshape(self, *n):
        if n == (1,):
            return asfuzzset([self])
        raise ValueError(f'cannot reshape mohunum of size {self.size} to {n}')

