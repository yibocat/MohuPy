from typing import Union

import numpy as np
from matplotlib import pyplot as plt

from mohupy import asfuzzset
from mohupy.core.base import MohuBase


# @fuzzType('template')
class template(MohuBase):
    qrung = 1
    mtype = 'template'

    def __init__(self, ms):
        super().__init__()
        self.ms = ms

    def __repr__(self):
        return f'<{self.ms}>'

    def __str__(self):
        return f'<{self.ms}>'

    def score(self):
        pass

    def acc(self):
        pass

    def ind(self):
        pass

    def comp(self):
        pass

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
        raise ValueError(f'cannot reshape fuzznum of size {self.size} to {n}')

    def plot(self, other=None, color='red', alpha=0.3):
        """
            The following code is an example and can be completely replaced
            to suit your needs.
        """
        q = self.qrung

        x = np.linspace(0, 1, 1000)

        plt.gca().spines['top'].set_linewidth(False)
        plt.gca().spines['bottom'].set_linewidth(True)
        plt.gca().spines['left'].set_linewidth(True)
        plt.gca().spines['right'].set_linewidth(False)
        plt.axis((0, 1.1, 0, 1.1))
        plt.axhline(y=0)
        plt.axvline(x=0)

        if other is not None:
            assert other.qrung == q, 'ERROR: The qrungs are not equal'
            plt.scatter(other.md, other.nmd, color=color, marker='*')

        y = (1 - x ** q) ** (1 / q)
        #
        # n = (nmd ** q / (1 - md ** q) * (1 - x ** q)) ** (1 / q)
        # m = (md ** q / (1 - nmd ** q) * (1 - x ** q)) ** (1 / q)

        plt.plot(x, y)
        plt.show()
