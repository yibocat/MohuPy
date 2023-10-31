#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/9/29 上午10:37
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import copy
from typing import Union
import numpy as np

from .base import mohunum

from ..registry.regedit import Register
from ..config import Approx

fuzzType = Register()


@fuzzType('qrofn')
class MohuQROFN(mohunum):
    """
        MohuQROFN is a class of q-rung orthopair fuzzy numbers. The class
        contains the basic arithmetic rules, comparison rules and basic
        properties.
        q-rung orthopair fuzzy numbers(q-ROFNs) usually contains three main
        attributes: q-rung, membership and non-membership degree. In addition,
        there are score values, accuracy values, uncertainties and complements.
        In particular, it contains addition, subtraction, multiplication,
        division, exponentiation, intersection, union, greater than, less than,
        equal to, greater than or equal to, less than or equal to, and
        inequality operations.

        Attributes
        ----------
            qrung : int
                    The q-rung orthopair value.
            md: : float or int or np.float_ or np.int_
                    The membership degree.
            nmd: : float or int or np.float_ or np.int_
                    The non-membership degree.

        Examples
        --------
            Int [1]: import mohupy as mp
            Int [2]: mp.MohuQROFN(2, 0.5, 0.5)  # That means that the q-rung is 2 and the
                                                # membership degree is 0.5 and non-membership
                                                # degree is 0.5.
            Out [2]: <0.5,0.5>
    """
    qrung = None
    __md = None
    __nmd = None
    mtype = None

    def __init__(self, qrung: Union[int, np.int_] = None,
                 md: Union[float, int, np.int_, np.float_] = None,
                 nmd: Union[float, int, np.int_, np.float_] = None):
        super().__init__()
        if isinstance(md, (float, int, np.int_, np.float_)) and \
                isinstance(nmd, (float, int, np.int_, np.float_)):
            assert 0. <= md <= 1. and 0. <= nmd <= 1., \
                'ERROR: md and nmd must be between 0 and 1.'
            assert 0. <= md ** qrung + nmd ** qrung <= 1., \
                'ERROR: md ** qrung + nmd ** qrung must be between 0 and 1'

            self.qrung = qrung
            self.__md = np.round(md, Approx.round)
            self.__nmd = np.round(nmd, Approx.round)
            self.mtype = 'qrofn'
            self.size = 1
        pass

    def __repr__(self):
        return f'<{np.round(self.__md, 4)},{np.round(self.__nmd, 4)}>'

    def __str__(self):
        return f'<{np.round(self.__md, 4)},{np.round(self.__nmd, 4)}>'

    @property
    def md(self):
        return self.__md

    @md.setter
    def md(self, value):
        self.__md = np.round(value, Approx.round)

    @property
    def nmd(self):
        return self.__nmd

    @nmd.setter
    def nmd(self, value):
        self.__nmd = np.round(value, Approx.round)

    @property
    def score(self):
        return self.__md ** self.qrung - self.__nmd ** self.qrung

    @property
    def acc(self):
        return self.__md ** self.qrung + self.__nmd ** self.qrung

    @property
    def ind(self):
        acc = self.__md ** self.qrung + self.__nmd ** self.qrung
        if acc == 1.:
            return 0.
        else:
            return (1. - acc) ** (1. / self.qrung)

    @property
    def comp(self):
        newf = copy.deepcopy(self)
        newf.md = self.__nmd
        newf.nmd = self.__md
        return newf

    @property
    def T(self):
        t = copy.copy(self)
        return t

    # def __add__(self, other):
    #     q = self.qrung
    #
    #     def __add(oth: MohuQROFN):
    #         assert self.qrung == oth.qrung, \
    #             'ERROR: qrung must be equal.'
    #         assert self.mtype == oth.mtype, \
    #             'ERROR: mtype must be same.'
    #         from ._multi_func import fuzznum
    #         newfn = fuzznum(q, 0, 0)
    #         newfn.md = (self.__md ** q + oth.md ** q
    #                     - self.__md ** q * oth.md ** q) ** (1 / q)
    #         newfn.nmd = self.__nmd * oth.nmd
    #         return newfn
    #
    #     if isinstance(other, MohuQROFN):
    #         return __add(other)
    #
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         assert other.mtype == self.mtype, \
    #             'ERROR: The fuzzy number and set must be of the same type.'
    #         assert other.qrung == self.qrung, \
    #             'ERROR: The fuzzy number and set must be of the same Q-rung.'
    #
    #         vec_func = np.vectorize(__add)
    #         newset = mohuset(q, self.mtype)
    #         newset.set = vec_func(other.set)
    #         return newset
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __radd__(self, other):
    #     q = self.qrung
    #
    #     def __add(oth: MohuQROFN):
    #         assert self.qrung == oth.qrung, \
    #             'ERROR: qrung must be equal.'
    #         assert self.mtype == oth.mtype, \
    #             'ERROR: mtype must be same.'
    #         from ._multi_func import fuzznum
    #         newfn = fuzznum(q, 0, 0)
    #         newfn.md = (self.__md ** q + oth.md ** q
    #                     - self.__md ** q * oth.md ** q) ** (1 / q)
    #         newfn.nmd = self.__nmd * oth.nmd
    #         return newfn
    #
    #     if isinstance(other, MohuQROFN):
    #         return __add(other)
    #
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         assert other.mtype == self.mtype, \
    #             'ERROR: The fuzzy number and set must be of the same type.'
    #         assert other.qrung == self.qrung, \
    #             'ERROR: The fuzzy number and set must be of the same Q-rung.'
    #
    #         vec_func = np.vectorize(__add)
    #         newset = mohuset(q, self.mtype)
    #         newset.set = vec_func(other.set)
    #         return newset
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __sub__(self, other):
    #     q = self.qrung
    #
    #     def __sub(oth: MohuQROFN):
    #         assert self.qrung == oth.qrung, \
    #             'ERROR: qrung must be equal.'
    #         assert self.mtype == oth.mtype, \
    #             'ERROR: mtype must be same.'
    #         from ._multi_func import fuzznum
    #         newfn = fuzznum(q, 0, 1)
    #         if oth.nmd == 0. or oth.md == 1.:
    #             return newfn
    #         elif 0 <= self.__nmd / oth.nmd <= ((1 - self.__md ** q) / (1 - oth.md ** q)) ** (1 / q) <= 1:
    #             newfn.md = ((self.__md ** q - oth.md ** q) / (1 - oth.md ** q)) ** (1 / q)
    #             newfn.nmd = self.__nmd / oth.nmd
    #             return newfn
    #         else:
    #             return newfn
    #
    #     if isinstance(other, MohuQROFN):
    #         return __sub(other)
    #
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         assert other.mtype == self.mtype, \
    #             'ERROR: The fuzzy number and set must be of the same type.'
    #         assert other.qrung == self.qrung, \
    #             'ERROR: The fuzzy number and set must be of the same Q-rung.'
    #
    #         vec_func = np.vectorize(__sub)
    #         newset = mohuset(q, self.mtype)
    #         newset.set = vec_func(other.set)
    #         return newset
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __mul__(self, other):
    #     q = self.qrung
    #
    #     def __mul(oth: Union[MohuQROFN, float, int, np.int_, np.float_]):
    #         if isinstance(oth, MohuQROFN):
    #             assert self.qrung == oth.qrung, \
    #                 'ERROR: qrung must be equal.'
    #             assert self.mtype == oth.mtype, \
    #                 'ERROR: mtype must be same.'
    #             from ._multi_func import fuzznum
    #             newfn = fuzznum(q, 0, 0)
    #             newfn.md = self.__md * oth.md
    #             newfn.nmd = (self.__nmd ** q + oth.nmd ** q
    #                          - self.__nmd ** q * oth.nmd ** q) ** (1. / q)
    #             return newfn
    #         if isinstance(oth, Union[float, int, np.int_, np.float_]):
    #             assert oth > 0., 'ERROR: The value must be greater than 0.'
    #             from ._multi_func import fuzznum
    #             newfn = fuzznum(q, 0, 0)
    #             newfn.md = (1. - (1. - self.__md ** q) ** oth) ** (1. / q)
    #             newfn.nmd = self.__nmd ** oth
    #             return newfn
    #
    #     if isinstance(other, Union[MohuQROFN, float, int, np.int_, np.float_]):
    #         return __mul(other)
    #
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         assert other.mtype == self.mtype, \
    #             'ERROR: The fuzzy number and set must be of the same type.'
    #         assert other.qrung == self.qrung, \
    #             'ERROR: The fuzzy number and set must be of the same Q-rung.'
    #         vec_func = np.vectorize(__mul)
    #         newset = mohuset(q, self.mtype)
    #         newset.set = vec_func(other.set)
    #         return newset
    #     if isinstance(other, np.ndarray):
    #         assert np.all(other) > 0, 'ERROR: The value must be greater than 0.'
    #         vec_func = np.vectorize(__mul)
    #         newset = mohuset(q, self.mtype)
    #         newset.set = vec_func(other)
    #         return newset
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __rmul__(self, other):
    #     q = self.qrung
    #
    #     def __mul(oth: Union[MohuQROFN, float, int, np.int_, np.float_]):
    #         if isinstance(oth, MohuQROFN):
    #             assert self.qrung == oth.qrung, \
    #                 'ERROR: qrung must be equal.'
    #             assert self.mtype == oth.mtype, \
    #                 'ERROR: mtype must be same.'
    #             from ._multi_func import fuzznum
    #             newfn = fuzznum(q, 0, 0)
    #             newfn.md = self.__md * oth.md
    #             newfn.nmd = (self.__nmd ** q + oth.nmd ** q
    #                          - self.__nmd ** q * oth.nmd ** q) ** (1. / q)
    #             return newfn
    #         if isinstance(oth, Union[float, int, np.int_, np.float_]):
    #             assert oth >= 0., 'ERROR: The value must be greater than 0.'
    #             from ._multi_func import fuzznum
    #             newfn = fuzznum(q, 0, 0)
    #             newfn.md = (1. - (1. - self.__md ** q) ** oth) ** (1. / q)
    #             newfn.nmd = self.__nmd ** oth
    #             return newfn
    #
    #     if isinstance(other, Union[MohuQROFN, float, int, np.int_, np.float_]):
    #         return __mul(other)
    #
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         assert other.mtype == self.mtype, \
    #             'ERROR: The fuzzy number and set must be of the same type.'
    #         assert other.qrung == self.qrung, \
    #             'ERROR: The fuzzy number and set must be of the same Q-rung.'
    #         vec_func = np.vectorize(__mul)
    #         newset = mohuset(q, self.mtype)
    #         newset.set = vec_func(other.set)
    #         return newset
    #     if isinstance(other, np.ndarray):
    #         assert np.all(other) > 0, 'ERROR: The value must be greater than 0.'
    #         vec_func = np.vectorize(__mul)
    #         newset = mohuset(q, self.mtype)
    #         newset.set = vec_func(other)
    #         return newset
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __truediv__(self, other):
    #     q = self.qrung
    #
    #     def __truediv(oth: Union[MohuQROFN, float, int, np.int_, np.float_]):
    #         if isinstance(oth, MohuQROFN):
    #             from ._multi_func import fuzznum
    #             newfn = fuzznum(q, 1, 0)
    #             if self.__md == 0 and self.__nmd == 1:
    #                 return fuzznum(q, 0, 1)
    #             elif oth.md == 0 or oth.nmd == 1.:
    #                 return newfn
    #             elif 0 <= self.__md / oth.md <= \
    #                     ((1 - self.__nmd ** q) / (1 - oth.nmd ** q)) ** (1 / q) <= 1:
    #                 newfn.md = self.__md / oth.md
    #                 newfn.nmd = ((self.__nmd ** q - oth.nmd ** q) / (1 - oth.nmd ** q)) ** (1 / q)
    #                 return newfn
    #             else:
    #                 return newfn
    #         if isinstance(oth, Union[float, int, np.int_, np.float_]):
    #             assert oth >= 1., 'ERROR: The value must be greater than 1.'
    #             return self.__mul__(1. / oth)
    #
    #     if isinstance(other, Union[MohuQROFN, float, int, np.int_, np.float_]):
    #         return __truediv(other)
    #
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         assert other.mtype == self.mtype, \
    #             'ERROR: The fuzzy number and set must be of the same type.'
    #         assert other.qrung == self.qrung, \
    #             'ERROR: The fuzzy number and set must be of the same Q-rung.'
    #         vec_func = np.vectorize(__truediv)
    #         newset = mohuset(q, self.mtype)
    #         newset.set = vec_func(other.set)
    #         return newset
    #     if isinstance(other, np.ndarray):
    #         assert np.all(other) >= 1., 'ERROR: The value must be greater than'
    #         vec_func = np.vectorize(__truediv)
    #         newset = mohuset(q, self.mtype)
    #         newset.set = vec_func(other)
    #         return newset
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __pow__(self, power, modulo=None):
    #     q = self.qrung
    #
    #     def __pow(p: Union[float, int, np.int_, np.float_]):
    #         assert p > 0., 'ERROR: The power must be greater than 0.'
    #         from ._multi_func import fuzznum
    #         newfn = fuzznum(q, 0, 0)
    #         newfn.md = self.__md ** p
    #         newfn.nmd = (1. - (1. - self.__nmd ** q) ** p) ** (1. / q)
    #         return newfn
    #
    #     if isinstance(power, Union[float, int, np.int_, np.float_]):
    #         return __pow(power)
    #
    #     from .mohusets import mohuset
    #     if isinstance(power, np.ndarray):
    #         assert np.all(power) > 0., 'ERROR: The power must be greater than 0.'
    #         vec_func = np.vectorize(__pow)
    #         newset = mohuset(q, self.mtype)
    #         newset.set = vec_func(power)
    #         return newset
    #     raise TypeError(f'Invalid type: {type(power)}')
    #
    # def __and__(self, other):
    #     q = self.qrung
    #
    #     def __and(oth: MohuQROFN):
    #         assert self.mtype == oth.mtype, \
    #             'ERROR: mtype must be same.'
    #         assert self.qrung == oth.qrung, \
    #             'ERROR: The qrung must be equal.'
    #
    #         from ._multi_func import fuzznum
    #         newfn = fuzznum(q, 0, 0)
    #         newfn.md = (min(self.__md, oth.md))
    #         newfn.nmd = (max(self.__nmd, oth.nmd))
    #         return newfn
    #
    #     if isinstance(other, MohuQROFN):
    #         return __and(other)
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         newset = mohuset(q, self.mtype)
    #         vec_func = np.vectorize(__and)
    #         newset.set = vec_func(other.set)
    #         return newset
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __or__(self, other):
    #     q = self.qrung
    #
    #     def __or(oth: MohuQROFN):
    #         assert self.mtype == oth.mtype, \
    #             'ERROR: mtype must be same.'
    #         assert self.qrung == oth.qrung, \
    #             'ERROR: The qrung must be equal.'
    #         from ._multi_func import fuzznum
    #         newfn = fuzznum(q, 0, 0)
    #         newfn.md = (max(self.__md, oth.md))
    #         newfn.nmd = (min(self.__nmd, oth.nmd))
    #         return newfn
    #
    #     if isinstance(other, MohuQROFN):
    #         return __or(other)
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         newset = mohuset(q, self.mtype)
    #         vec_func = np.vectorize(__or)
    #         newset.set = vec_func(other.set)
    #         return newset
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __eq__(self, other):
    #     def __eq(oth: MohuQROFN):
    #         assert self.mtype == oth.mtype, \
    #             'ERROR: mtype must be same.'
    #         assert self.qrung == oth.qrung, \
    #             'ERROR: The qrung must be equal.'
    #         return self.__md == oth.md and self.__nmd == oth.nmd
    #
    #     if isinstance(other, MohuQROFN):
    #         return __eq(other)
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         vec_func = np.vectorize(__eq)
    #         res = vec_func(other.set)
    #         return res
    #
    # def __ne__(self, other):
    #     def __ne(oth: MohuQROFN):
    #         assert self.mtype == oth.mtype, \
    #             'ERROR: mtype must be same.'
    #         assert self.qrung == oth.qrung, \
    #             'ERROR: The qrung must be equal.'
    #         return self.__md != oth.md or self.__nmd != oth.nmd
    #
    #     if isinstance(other, MohuQROFN):
    #         return __ne(other)
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         vec_func = np.vectorize(__ne)
    #         res = vec_func(other.set)
    #         return res
    #
    # def __lt__(self, other):
    #     q = self.qrung
    #
    #     def __lt(oth: MohuQROFN):
    #         assert self.mtype == oth.mtype, \
    #             'ERROR: mtype must be same.'
    #         assert self.qrung == oth.qrung, \
    #             'ERROR: The qrung must be equal.'
    #         from ._multi_func import fuzznum
    #         if self - oth == fuzznum(q, 0, 1) and self != oth:
    #             return True
    #         else:
    #             return False
    #
    #     if isinstance(other, MohuQROFN):
    #         return __lt(other)
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         vec_func = np.vectorize(__lt)
    #         res = vec_func(other.set)
    #         return res
    #     if isinstance(other, np.ndarray):
    #         vec_func = np.vectorize(__lt)
    #         res = vec_func(other)
    #         return res
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __gt__(self, other):
    #     q = self.qrung
    #
    #     def __gt(oth: MohuQROFN):
    #         assert self.mtype == oth.mtype, \
    #             'ERROR: mtype must be same.'
    #         assert self.qrung == oth.qrung, \
    #             'ERROR: The qrung must be equal.'
    #         from ._multi_func import fuzznum
    #         if self - oth != fuzznum(q, 0., 1.) and self != oth:
    #             return True
    #         else:
    #             return False
    #
    #     if isinstance(other, MohuQROFN):
    #         return __gt(other)
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         vec_func = np.vectorize(__gt)
    #         res = vec_func(other.set)
    #         return res
    #     if isinstance(other, np.ndarray):
    #         vec_func = np.vectorize(__gt)
    #         res = vec_func(other)
    #         return res
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __le__(self, other):
    #     q = self.qrung
    #
    #     def __le(oth: MohuQROFN):
    #         assert self.mtype == oth.mtype, \
    #             'ERROR: mtype must be same.'
    #         assert self.qrung == oth.qrung, \
    #             'ERROR: The qrung must be equal.'
    #         from ._multi_func import fuzznum
    #         if self - oth == fuzznum(q, 0., 1.) or self == oth:
    #             return True
    #         else:
    #             return False
    #
    #     if isinstance(other, MohuQROFN):
    #         return __le(other)
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         vec_func = np.vectorize(__le)
    #         res = vec_func(other.set)
    #         return res
    #     if isinstance(other, np.ndarray):
    #         vec_func = np.vectorize(__le)
    #         res = vec_func(other)
    #         return res
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __ge__(self, other):
    #     q = self.qrung
    #
    #     def __ge(oth: MohuQROFN):
    #         assert self.mtype == oth.mtype, \
    #             'ERROR: mtype must be same.'
    #         assert self.qrung == oth.qrung, \
    #             'ERROR: The qrung must be equal.'
    #         from ._multi_func import fuzznum
    #         if self - oth != fuzznum(q, 0., 1.) or self == oth:
    #             return True
    #         else:
    #             return False
    #
    #     if isinstance(other, MohuQROFN):
    #         return __ge(other)
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         vec_func = np.vectorize(__ge)
    #         res = vec_func(other.set)
    #         return res
    #     if isinstance(other, np.ndarray):
    #         vec_func = np.vectorize(__ge)
    #         res = vec_func(other)
    #         return res
    #     raise TypeError(f'Invalid type: {type(other)}')

    def is_valid(self):
        mds = self.__md
        nmds = self.__nmd
        if 0. <= mds <= 1. and 0. <= nmds <= 1. \
                and 0. <= mds ** self.qrung + nmds ** self.qrung <= 1.:
            return True
        else:
            return False

    def isEmpty(self):
        if self.__md is None and self.__nmd is None:
            return True
        else:
            return False

    def convert(self):
        return self.__md, self.__nmd

    def flatten(self):
        from .mohusets import mohuset
        newset = mohuset(self.qrung, self.mtype)
        newset.append(self)
        return newset


@fuzzType('ivfn')
class MohuQROIVFN(mohunum):
    qrung = None
    __md = np.array([])
    __nmd = np.array([])
    mtype = None

    def __init__(self, qrung: Union[int, np.int_] = None,
                 md: Union[tuple, list, np.ndarray] = None,
                 nmd: Union[tuple, list, np.ndarray] = None):
        super().__init__()
        if isinstance(md, Union[tuple, list, np.ndarray]) and isinstance(nmd, Union[tuple, list, np.ndarray]):
            assert len(md) == 2 and len(nmd) == 2, \
                'ERROR: The data format contains at least upper and lower bounds.'
            assert md[0] <= md[1] and nmd[0] <= nmd[1], \
                'ERROR: The upper of membership and non-membership must be greater than the lower.'
            assert 0 <= md[0] <= 1 and 0 <= md[1] <= 1, \
                'ERROR: The upper and lower of membership degree must be between 0 and 1.'
            assert 0 <= nmd[0] <= 1 and 0 <= nmd[1] <= 1, \
                'ERROR: The upper and lower of non-membership degree must be between 0 and 1.'
            assert 0 <= md[0] ** qrung + nmd[0] ** qrung <= 1 and 0 <= md[1] ** qrung + nmd[1] ** qrung <= 1, \
                'ERROR: The q powers sum of membership degree and non-membership degree must be between 0 and 1.'

            self.qrung = qrung
            self.__md = np.round(md, Approx.round)
            self.__nmd = np.round(nmd, Approx.round)
            self.mtype = 'ivfn'
            self.size = 1

    def __repr__(self):
        return f'<{np.round(self.__md, 4)},{np.round(self.__nmd, 4)}>'

    def __str__(self):
        return f'<{np.round(self.__md, 4)},{np.round(self.__nmd, 4)}>'

    @property
    def md(self):
        return self.__md

    @md.setter
    def md(self, value):
        self.__md = np.round(value, Approx.round)

    @property
    def nmd(self):
        return self.__nmd

    @nmd.setter
    def nmd(self, value):
        self.__nmd = np.round(value, Approx.round)

    @property
    def score(self):
        m = self.__md[0] ** self.qrung + self.__md[1] ** self.qrung
        n = self.__nmd[0] ** self.qrung + self.__nmd[1] ** self.qrung
        return (m - n) / 2

    @property
    def acc(self):
        m = self.__md[0] ** self.qrung + self.__md[1] ** self.qrung
        n = self.__nmd[0] ** self.qrung + self.__nmd[1] ** self.qrung
        return (m + n) / 2

    @property
    def ind(self):
        m = self.__md[0] ** self.qrung + self.__md[1] ** self.qrung
        n = self.__nmd[0] ** self.qrung + self.__nmd[1] ** self.qrung
        if m + n:
            return 0.
        else:
            return (1. - (m + n) / 2) ** (1. / self.qrung)

    @property
    def comp(self):
        newf = copy.deepcopy(self)
        newf.md = self.__nmd
        newf.nmd = self.__md
        return newf

    @property
    def T(self):
        t = copy.copy(self)
        return t

    # def __add__(self, other):
    #     q = self.qrung
    #
    #     def __add(oth: MohuQROIVFN):
    #         assert self.qrung == oth.qrung, \
    #             'ERROR: qrung must be equal.'
    #         assert self.mtype == oth.mtype, \
    #             'ERROR: mtype must be same.'
    #         from ._multi_func import fuzznum
    #         newfn = fuzznum(q, (0., 0.), (0., 0.))
    #         newfn.md = (self.__md ** q + oth.md ** q - self.__md ** q * oth.md ** q) ** (1. / q)
    #         newfn.nmd = self.__nmd * oth.nmd
    #         return newfn
    #
    #     if isinstance(other, MohuQROIVFN):
    #         return __add(other)
    #
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         assert other.mtype == self.mtype, \
    #             'ERROR: The fuzzy number and set must be of the same type.'
    #         assert other.qrung == self.qrung, \
    #             'ERROR: The fuzzy number and set must be of the same Q-rung.'
    #
    #         vec_func = np.vectorize(__add)
    #         newset = mohuset(q, self.mtype)
    #         newset.set = vec_func(other.set)
    #         return newset
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __radd__(self, other):
    #     q = self.qrung
    #
    #     def __add(oth: MohuQROIVFN):
    #         assert self.qrung == oth.qrung, \
    #             'ERROR: qrung must be equal.'
    #         assert self.mtype == oth.mtype, \
    #             'ERROR: mtype must be same.'
    #         from ._multi_func import fuzznum
    #         newfn = fuzznum(q, (0., 0.), (0., 0.))
    #         newfn.md = (self.__md ** q + oth.md ** q - self.__md ** q * oth.md ** q) ** (1. / q)
    #         newfn.nmd = self.__nmd * oth.nmd
    #         return newfn
    #
    #     if isinstance(other, MohuQROIVFN):
    #         return __add(other)
    #
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         assert other.mtype == self.mtype, \
    #             'ERROR: The fuzzy number and set must be of the same type.'
    #         assert other.qrung == self.qrung, \
    #             'ERROR: The fuzzy number and set must be of the same Q-rung.'
    #
    #         vec_func = np.vectorize(__add)
    #         newset = mohuset(q, self.mtype)
    #         newset.set = vec_func(other.set)
    #         return newset
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __sub__(self, other):
    #     # TODO: The subtraction of MohuQROIVFN is not supported.
    #     raise TypeError('interval-valued fuzzy subtraction operation is not supported for the time being.')
    #
    # def __mul__(self, other):
    #     q = self.qrung
    #
    #     def __mul(oth: Union[MohuQROIVFN, float, int, np.int_, np.float_]):
    #         if isinstance(oth, MohuQROIVFN):
    #             assert self.qrung == oth.qrung, \
    #                 'ERROR: qrung must be equal.'
    #             assert self.mtype == oth.mtype, \
    #                 'ERROR: mtype must be same.'
    #             from ._multi_func import fuzznum
    #             newfn = fuzznum(q, (0., 0.), (0., 0.))
    #             newfn.md = self.__md * oth.md
    #             newfn.nmd = (self.__nmd ** q + oth.nmd ** q - self.__nmd ** q * oth.nmd ** q) ** (1. / q)
    #             return newfn
    #         if isinstance(oth, Union[float, int, np.int_, np.float_]):
    #             assert oth >= 0., 'ERROR: The value must be greater than 0.'
    #             from ._multi_func import fuzznum
    #             newfn = fuzznum(q, (0., 0.), (0., 0.))
    #             newfn.md = (1. - (1 - self.__md ** q) ** oth) ** (1. / q)
    #             newfn.nmd = self.__nmd ** oth
    #             return newfn
    #         raise TypeError('ERROR: Unsupported type.')
    #
    #     if isinstance(other, Union[MohuQROIVFN, float, int, np.int_, np.float_]):
    #         return __mul(other)
    #
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         assert other.mtype == self.mtype, \
    #             'ERROR: The fuzzy number and set must be of the same type.'
    #         assert other.qrung == self.qrung, \
    #             'ERROR: The fuzzy number and set must be of the same Q-rung.'
    #         vec_func = np.vectorize(__mul)
    #         newset = mohuset(q, self.mtype)
    #         newset.set = vec_func(other.set)
    #         return newset
    #
    #     if isinstance(other, np.ndarray):
    #         assert np.all(other) > 0, 'ERROR: The value must be greater than 0.'
    #         vec_func = np.vectorize(__mul)
    #         newset = mohuset(q, self.mtype)
    #         newset.set = vec_func(other)
    #         return newset
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __rmul__(self, other):
    #     q = self.qrung
    #
    #     def __mul(oth: Union[MohuQROIVFN, float, int, np.int_, np.float_]):
    #         if isinstance(oth, MohuQROIVFN):
    #             assert self.qrung == oth.qrung, \
    #                 'ERROR: qrung must be equal.'
    #             assert self.mtype == oth.mtype, \
    #                 'ERROR: mtype must be same.'
    #             from ._multi_func import fuzznum
    #             newfn = fuzznum(q, (0., 0.), (0., 0.))
    #             newfn.md = self.__md * oth.md
    #             newfn.nmd = (self.__nmd ** q + oth.nmd ** q - self.__nmd ** q * oth.nmd ** q) ** (1. / q)
    #             return newfn
    #         if isinstance(oth, Union[float, int, np.int_, np.float_]):
    #             assert oth >= 0., 'ERROR: The value must be greater than 0.'
    #             from ._multi_func import fuzznum
    #             newfn = fuzznum(q, (0., 0.), (0., 0.))
    #             newfn.md = (1. - (1 - self.__md ** q) ** oth) ** (1. / q)
    #             newfn.nmd = self.__nmd ** oth
    #             return newfn
    #         raise TypeError('ERROR: Unsupported type.')
    #
    #     if isinstance(other, Union[MohuQROIVFN, float, int, np.int_, np.float_]):
    #         return __mul(other)
    #
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         assert other.mtype == self.mtype, \
    #             'ERROR: The fuzzy number and set must be of the same type.'
    #         assert other.qrung == self.qrung, \
    #             'ERROR: The fuzzy number and set must be of the same Q-rung.'
    #         vec_func = np.vectorize(__mul)
    #         newset = mohuset(q, self.mtype)
    #         newset.set = vec_func(other.set)
    #         return newset
    #     if isinstance(other, np.ndarray):
    #         assert np.all(other) > 0, 'ERROR: The value must be greater than 0.'
    #         vec_func = np.vectorize(__mul)
    #         newset = mohuset(q, self.mtype)
    #         newset.set = vec_func(other)
    #         return newset
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __truediv__(self, other):
    #     # TODO: The division of MohuQROIVFN is not supported.
    #     raise TypeError('Interval-valued fuzzy division operation is not supported for the time being.')
    #
    # def __pow__(self, power, modulo=None):
    #     q = self.qrung
    #
    #     def __pow(p: Union[float, int, np.int_, np.float_]):
    #         assert p > 0., 'ERROR: The power must be greater than 0.'
    #         from ._multi_func import fuzznum
    #         newfn = fuzznum(q, (0., 0.), (0., 0.))
    #         newfn.md = self.__md ** p
    #         newfn.nmd = (1. - (1. - self.__nmd ** q) ** p) ** (1. / q)
    #         return newfn
    #
    #     if isinstance(power, Union[float, int, np.int_, np.float_]):
    #         return __pow(power)
    #
    #     from .mohusets import mohuset
    #     if isinstance(power, np.ndarray):
    #         assert np.all(power) > 0., 'ERROR: The power must be greater than 0.'
    #         vec_func = np.vectorize(__pow)
    #         newset = mohuset(q, self.mtype)
    #         newset.set = vec_func(power)
    #         return newset
    #     raise TypeError(f'Invalid type: {type(power)}')
    #
    # def __and__(self, other):
    #     q = self.qrung
    #
    #     def __and(oth: MohuQROIVFN):
    #         assert self.mtype == oth.mtype, \
    #             'ERROR: mtype must be same.'
    #         assert self.qrung == oth.qrung, \
    #             'ERROR: The qrung must be equal.'
    #         from ._multi_func import fuzznum
    #         newfn = fuzznum(q, (0., 0.), (0., 0.))
    #         newfn.md = [min(self.__md[0], oth.md[0]), min(self.__md[1], oth.md[1])]
    #         newfn.nmd = [max(self.__nmd[0], oth.nmd[0]), max(self.__nmd[1], oth.nmd[1])]
    #         return newfn
    #
    #     if isinstance(other, MohuQROIVFN):
    #         return __and(other)
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         newset = mohuset(q, self.mtype)
    #         vec_func = np.vectorize(__and)
    #         newset.set = vec_func(other.set)
    #         return newset
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __or__(self, other):
    #     q = self.qrung
    #
    #     def __or(oth: MohuQROIVFN):
    #         assert self.mtype == oth.mtype, \
    #             'ERROR: mtype must be same.'
    #         assert self.qrung == oth.qrung, \
    #             'ERROR: The qrung must be equal.'
    #         from ._multi_func import fuzznum
    #         newfn = fuzznum(q, (0., 0.), (0., 0.))
    #         newfn.md = [max(self.__md[0], oth.md[0]), max(self.__md[1], oth.md[1])]
    #         newfn.nmd = [min(self.__nmd[0], oth.nmd[0]), min(self.__nmd[1], oth.nmd[1])]
    #         return newfn
    #
    #     if isinstance(other, MohuQROIVFN):
    #         return __or(other)
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         newset = mohuset(q, self.mtype)
    #         vec_func = np.vectorize(__or)
    #         newset.set = vec_func(other.set)
    #         return newset
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __eq__(self, other):
    #
    #     def __eq(oth: MohuQROIVFN):
    #         assert self.qrung == oth.qrung, \
    #             'ERROR: The qrung must be equal.'
    #         assert self.mtype == oth.mtype, \
    #             'ERROR: The mtype must be same.'
    #         return np.array_equal(self.__md, oth.md) and np.array_equal(self.__nmd, oth.nmd)
    #
    #     if isinstance(other, MohuQROIVFN):
    #         return __eq(other)
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         vec_func = np.vectorize(__eq)
    #         res = vec_func(other.set)
    #         return res
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __ne__(self, other):
    #
    #     def __ne(oth: MohuQROIVFN):
    #         assert self.mtype == oth.mtype, \
    #             'ERROR: The mtype must be same.'
    #         assert self.qrung == other.qrung, \
    #             'ERROR: The qrung must be equal.'
    #         return not np.array_equal(self.__md, other.md) or not np.array_equal(self.__nmd, other.nmd)
    #
    #     if isinstance(other, MohuQROIVFN):
    #         return __ne(other)
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         vec_func = np.vectorize(__ne)
    #         res = vec_func(other.set)
    #         return res
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __lt__(self, other):
    #     # TODO: The comparison of MohuQROIVFN is not supported.
    #     # Temporarily adopt the score value comparison method
    #
    #     def __lt(oth: MohuQROIVFN):
    #         assert self.qrung == oth.qrung, \
    #             'ERROR: The qrung must be equal.'
    #         assert self.mtype == oth.mtype, \
    #             'ERROR: The mtype must be same.'
    #         return self.score < oth.score
    #
    #     if isinstance(other, MohuQROIVFN):
    #         return __lt(other)
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         vec_func = np.vectorize(__lt)
    #         res = vec_func(other.set)
    #         return res
    #     if isinstance(other, np.ndarray):
    #         vec_func = np.vectorize(__lt)
    #         res = vec_func(other)
    #         return res
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __gt__(self, other):
    #     # TODO: The comparison of MohuQROIVFN is not supported.
    #     # Temporarily adopt the score value comparison method
    #
    #     def __gt(oth: MohuQROIVFN):
    #         assert self.qrung == oth.qrung, \
    #             'ERROR: The qrung must be equal.'
    #         assert self.mtype == oth.mtype, \
    #             'ERROR: The mtype must be same.'
    #         return self.score > oth.score
    #
    #     if isinstance(other, MohuQROIVFN):
    #         return __gt(other)
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         vec_func = np.vectorize(__gt)
    #         res = vec_func(other.set)
    #         return res
    #     if isinstance(other, np.ndarray):
    #         vec_func = np.vectorize(__gt)
    #         res = vec_func(other)
    #         return res
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __le__(self, other):
    #     # TODO: The comparison of MohuQROIVFN is not supported.
    #     # Temporarily adopt the score value comparison method
    #
    #     def __le(oth: MohuQROIVFN):
    #         assert self.qrung == oth.qrung, \
    #             'ERROR: The qrung must be equal.'
    #         assert self.mtype == oth.mtype, \
    #             'ERROR: The mtype must be same.'
    #         return self.score <= oth.score
    #
    #     if isinstance(other, MohuQROIVFN):
    #         return __le(other)
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         vec_func = np.vectorize(__le)
    #         res = vec_func(other.set)
    #         return res
    #     if isinstance(other, np.ndarray):
    #         vec_func = np.vectorize(__le)
    #         res = vec_func(other)
    #         return res
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __ge__(self, other):
    #     # TODO: The comparison of MohuQROIVFN is not supported.
    #     # Temporarily adopt the score value comparison method
    #
    #     def __ge(oth: MohuQROIVFN):
    #         assert self.qrung == oth.qrung, \
    #             'ERROR: The qrung must be equal.'
    #         assert self.mtype == oth.mtype, \
    #             'ERROR: The mtype must be same.'
    #         return self.score >= oth.score
    #
    #     if isinstance(other, MohuQROIVFN):
    #         return __ge(other)
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         vec_func = np.vectorize(__ge)
    #         res = vec_func(other.set)
    #         return res
    #     if isinstance(other, np.ndarray):
    #         vec_func = np.vectorize(__ge)
    #         res = vec_func(other)
    #         return res
    #     raise TypeError(f'Invalid type: {type(other)}')

    def is_valid(self):
        if not len(self.__md) == 2 and len(self.__nmd) == 2:
            return False
        elif not 0. <= np.all(self.__md) <= 1. and 0. <= np.all(self.__md) <= 1.:
            return False
        elif not (self.__md[0] <= self.__md[1] and self.__nmd[0] <= self.__nmd[1]):
            return False
        elif not 0 <= self.__md[1] ** self.qrung + self.__nmd[1] ** self.qrung <= 1:
            return False
        else:
            return True

    def isEmpty(self):
        if self.__md is None and self.__nmd is None:
            return True
        else:
            return False

    def convert(self):
        return self.__md.tolist(), self.__nmd.tolist()

    def flatten(self):
        from .mohusets import mohuset
        newset = mohuset(self.qrung, self.mtype)
        newset.append(self)
        return newset


@fuzzType('qrohfn')
class MohuQROHFN(mohunum):
    qrung = None
    __md = []
    __nmd = []
    mtype = None

    def __init__(self, qrung: Union[int, np.int_] = None,
                 md: Union[list, np.ndarray] = None,
                 nmd: Union[list, np.ndarray] = None):
        super().__init__()
        if isinstance(md, Union[list, np.ndarray]) and isinstance(nmd, Union[list, np.ndarray]):
            mds = np.asarray(md)
            nmds = np.asarray(nmd)
            if mds.size == 0 and nmds.size == 0:
                pass
            if mds.size == 0 and nmds.size != 0:
                assert np.max(nmds) <= 1 and np.min(nmds) >= 0, \
                    'non-membership degrees must be in the interval [0,1].'
            if mds.size != 0 and nmds.size == 0:
                assert np.max(mds) <= 1 and np.min(mds) >= 0, \
                    'membership degrees must be in the interval [0,1].'
            if mds.size > 0 and nmds.size > 0:
                assert np.max(mds) <= 1 and np.max(nmds) <= 1 and \
                       np.min(mds) >= 0 and np.min(nmds) >= 0, 'ERROR: must be in [0,1].'
                assert 0 <= np.max(mds) ** qrung + np.max(nmds) ** qrung <= 1, 'ERROR'

            self.qrung = qrung
            self.__md = np.round(mds, Approx.round)
            self.__nmd = np.round(nmds, Approx.round)
            self.mtype = 'qrohfn'
            self.size = 1

    def __repr__(self):
        if len(self.__md) > 8 >= len(self.__nmd):
            return f'<{np.round(self.__md[:8], 4)}..., {np.round(self.__nmd, 4)}>'
        if len(self.__nmd) > 8 >= len(self.__md):
            return f'<{np.round(self.__md, 4)}, {np.round(self.__nmd[:8], 4)}...>'
        if len(self.__md) > 8 and len(self.__nmd) > 8:
            return f'<{np.round(self.__md[:8], 4)}..., {np.round(self.__nmd[:8], 4)}...>'
        else:
            return f'<{np.round(self.__md, 4)}, {np.round(self.__nmd, 4)}>'

    def __str__(self):
        if len(self.__md) > 8 >= len(self.__nmd):
            return f'<{np.round(self.__md[:8], 4)}..., {np.round(self.__nmd, 4)}>'
        if len(self.__nmd) > 8 >= len(self.__md):
            return f'<{np.round(self.__md, 4)}, {np.round(self.__nmd[:8], 4)}...>'
        if len(self.__md) > 8 and len(self.__nmd) > 8:
            return f'<{np.round(self.__md[:8], 4)}..., {np.round(self.__nmd[:8], 4)}...>'
        else:
            return f'<{np.round(self.__md, 4)}, {np.round(self.__nmd, 4)}>'

    @property
    def md(self):
        return self.__md

    @md.setter
    def md(self, value):
        self.__md = np.round(value, Approx.round)

    @property
    def nmd(self):
        return self.__nmd

    @nmd.setter
    def nmd(self, value):
        self.__nmd = np.round(value, Approx.round)

    @property
    def info(self):
        print(f'<({len(self.__md)},{len(self.__nmd)}), qrung={self.qrung}>, mtype={self.mtype}>')
        return None

    @property
    def score(self):
        mm = ((self.__md ** self.qrung).sum()) / len(self.__md)
        nn = ((self.__nmd ** self.qrung).sum()) / len(self.__nmd)
        return mm - nn

    @property
    def acc(self):
        mm = ((self.__md ** self.qrung).sum()) / len(self.__md)
        nn = ((self.__nmd ** self.qrung).sum()) / len(self.__nmd)
        return mm + nn

    @property
    def ind(self):
        mm = ((self.__md ** self.qrung).sum()) / len(self.__md)
        nn = ((self.__nmd ** self.qrung).sum()) / len(self.__nmd)
        if mm + nn == 1.:
            return 0.
        else:
            return (1. - mm - nn) ** (1 / self.qrung)

    @property
    def comp(self):
        newfn = copy.deepcopy(self)
        if self.__md.size == 0 and self.__nmd.size != 0:
            newfn.md = np.array([])
            newfn.nmd = 1. - self.__nmd
        elif self.__md.size != 0 and self.__nmd.size == 0:
            newfn.md = 1. - self.__md
            newfn.nmd = np.array([])
        else:
            newfn.md = self.__nmd
            newfn.nmd = self.__md
        return newfn

    @property
    def T(self):
        t = copy.copy(self)
        return t

    # def __add__(self, other):
    #     q = self.qrung
    #
    #     def __add(oth: MohuQROHFN):
    #         assert self.qrung == oth.qrung, \
    #             'ERROR: qrung must be equal.'
    #         assert self.mtype == oth.mtype, \
    #             'ERROR: mtype must be same.'
    #         from ._multi_func import fuzznum
    #         newfn = fuzznum(q, [], [])
    #
    #         mds = np.array(np.meshgrid(self.__md, oth.md)).T.reshape(-1, 2)
    #         nmds = np.array(np.meshgrid(self.__nmd, oth.nmd)).T.reshape(-1, 2)
    #
    #         from ..math.archimedean import algebraic_S, algebraic_T
    #         for i in range(len(mds)):
    #             newfn.md = np.append(newfn.md, algebraic_S(mds[i, 0] ** q, mds[i, 1] ** q) ** (1 / q))
    #         for i in range(len(nmds)):
    #             newfn.nmd = np.append(newfn.nmd, algebraic_T(nmds[i, 0] ** q, nmds[i, 1] ** q) ** (1 / q))
    #
    #         return newfn.unique(4)
    #
    #     if isinstance(other, MohuQROHFN):
    #         return __add(other)
    #
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         assert other.mtype == self.mtype, \
    #             'ERROR: The fuzzy number and set must be of the same type.'
    #         assert other.qrung == self.qrung, \
    #             'ERROR: The fuzzy number and set must be of the same Q-rung.'
    #
    #         vec_func = np.vectorize(__add)
    #         newset = mohuset(q, self.mtype)
    #         newset.set = vec_func(other.set)
    #         return newset
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __radd__(self, other):
    #     q = self.qrung
    #
    #     def __add(oth: MohuQROHFN):
    #         assert self.qrung == oth.qrung, \
    #             'ERROR: qrung must be equal.'
    #         assert self.mtype == oth.mtype, \
    #             'ERROR: mtype must be same.'
    #         from ._multi_func import fuzznum
    #         newfn = fuzznum(q, [], [])
    #
    #         mds = np.array(np.meshgrid(self.__md, oth.md)).T.reshape(-1, 2)
    #         nmds = np.array(np.meshgrid(self.__nmd, oth.nmd)).T.reshape(-1, 2)
    #
    #         from ..math.archimedean import algebraic_S, algebraic_T
    #         for i in range(len(mds)):
    #             newfn.md = np.append(newfn.md, algebraic_S(mds[i, 0] ** q, mds[i, 1] ** q) ** (1 / q))
    #         for i in range(len(nmds)):
    #             newfn.nmd = np.append(newfn.nmd, algebraic_T(nmds[i, 0] ** q, nmds[i, 1] ** q) ** (1 / q))
    #
    #         return newfn.unique(4)
    #
    #     if isinstance(other, MohuQROHFN):
    #         return __add(other)
    #
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         assert other.mtype == self.mtype, \
    #             'ERROR: The fuzzy number and set must be of the same type.'
    #         assert other.qrung == self.qrung, \
    #             'ERROR: The fuzzy number and set must be of the same Q-rung.'
    #
    #         vec_func = np.vectorize(__add)
    #         newset = mohuset(q, self.mtype)
    #         newset.set = vec_func(other.set)
    #         return newset
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __sub__(self, other):
    #     # TODO: The subtraction of MohuQROHFN is not supported.
    #     raise TypeError('q-rung orthopair fuzzy subtraction operation is not supported for the time being.')
    #
    # def __mul__(self, other):
    #     q = self.qrung
    #
    #     def __mul(oth: Union[MohuQROHFN, float, int, np.int_, np.float_]):
    #         if isinstance(oth, MohuQROHFN):
    #             assert self.qrung == oth.qrung, \
    #                 'ERROR: qrung must be equal.'
    #             assert self.mtype == oth.mtype, \
    #                 'ERROR: mtype must be same.'
    #             from ._multi_func import fuzznum
    #             newfn = fuzznum(q, [], [])
    #
    #             mds = np.array(np.meshgrid(self.__md, oth.md)).T.reshape(-1, 2)
    #             nmds = np.array(np.meshgrid(self.__nmd, oth.nmd)).T.reshape(-1, 2)
    #
    #             from ..math.archimedean import algebraic_S, algebraic_T
    #             for i in range(len(mds)):
    #                 newfn.md = np.append(newfn.md, algebraic_T(mds[i, 0] ** q, mds[i, 1] ** q) ** (1 / q))
    #             for i in range(len(nmds)):
    #                 newfn.nmd = np.append(newfn.nmd, algebraic_S(nmds[i, 0] ** q, nmds[i, 1] ** q) ** (1 / q))
    #
    #             return newfn.unique(4)
    #
    #         if isinstance(oth, Union[float, int, np.int_, np.float_]):
    #             assert oth >= 0., 'ERROR: The value must be greater than 0.'
    #             from ._multi_func import fuzznum
    #             newfn = fuzznum(q, [], [])
    #             newfn.md = (1. - (1. - self.__md ** self.qrung) ** oth) ** (1 / self.qrung)
    #             newfn.nmd = self.__nmd ** oth
    #             return newfn.unique(4)
    #
    #     if isinstance(other, Union[MohuQROHFN, float, int, np.int_, np.float_]):
    #         return __mul(other)
    #
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         # assert other.mtype == self.mtype, \
    #         #     'ERROR: The fuzzy number and set must be of the same type.'
    #         # assert other.qrung == self.qrung, \
    #         #     'ERROR: The fuzzy number and set must be of the same Q-rung.'
    #         vec_func = np.vectorize(__mul)
    #         newset = mohuset(q, self.mtype)
    #         newset.set = vec_func(other.set)
    #         return newset
    #
    #     if isinstance(other, np.ndarray):
    #         # assert np.all(other) > 0, 'ERROR: The value must be greater than 0.'
    #         vec_func = np.vectorize(__mul)
    #         newset = mohuset(q, self.mtype)
    #         newset.set = vec_func(other)
    #         return newset
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __rmul__(self, other):
    #     q = self.qrung
    #
    #     def __mul(oth: Union[MohuQROHFN, float, int, np.int_, np.float_]):
    #         if isinstance(oth, MohuQROHFN):
    #             assert self.qrung == oth.qrung, \
    #                 'ERROR: qrung must be equal.'
    #             assert self.mtype == oth.mtype, \
    #                 'ERROR: mtype must be same.'
    #             from ._multi_func import fuzznum
    #             newfn = fuzznum(q, [], [])
    #
    #             mds = np.array(np.meshgrid(self.__md, oth.md)).T.reshape(-1, 2)
    #             nmds = np.array(np.meshgrid(self.__nmd, oth.nmd)).T.reshape(-1, 2)
    #
    #             from ..math.archimedean import algebraic_S, algebraic_T
    #             for i in range(len(mds)):
    #                 newfn.md = np.append(newfn.md, algebraic_T(mds[i, 0] ** q, mds[i, 1] ** q) ** (1 / q))
    #             for i in range(len(nmds)):
    #                 newfn.nmd = np.append(newfn.nmd, algebraic_S(nmds[i, 0] ** q, nmds[i, 1] ** q) ** (1 / q))
    #
    #             return newfn.unique(4)
    #
    #         if isinstance(oth, Union[float, int, np.int_, np.float_]):
    #             assert oth >= 0., 'ERROR: The value must be greater than 0.'
    #             from ._multi_func import fuzznum
    #             newfn = fuzznum(q, [], [])
    #             newfn.md = (1. - (1. - self.__md ** self.qrung) ** oth) ** (1 / self.qrung)
    #             newfn.nmd = self.__nmd ** oth
    #             return newfn.unique(4)
    #
    #     if isinstance(other, Union[MohuQROHFN, float, int, np.int_, np.float_]):
    #         return __mul(other)
    #
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         # assert other.mtype == self.mtype, \
    #         #     'ERROR: The fuzzy number and set must be of the same type.'
    #         # assert other.qrung == self.qrung, \
    #         #     'ERROR: The fuzzy number and set must be of the same Q-rung.'
    #         vec_func = np.vectorize(__mul)
    #         newset = mohuset(q, self.mtype)
    #         newset.set = vec_func(other.set)
    #         return newset
    #
    #     if isinstance(other, np.ndarray):
    #         # assert np.all(other) > 0, 'ERROR: The value must be greater than 0.'
    #         vec_func = np.vectorize(__mul)
    #         newset = mohuset(q, self.mtype)
    #         newset.set = vec_func(other)
    #         return newset
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __truediv__(self, other):
    #     # TODO: The division of MohuQROHFN is not supported.
    #     raise TypeError('q-rung orthopair fuzzy division operation is not supported for the time being.')
    #
    # def __pow__(self, power, modulo=None):
    #     q = self.qrung
    #
    #     def __pow(p: Union[float, int, np.int_, np.float_]):
    #         assert p > 0., 'ERROR: The power must be greater than 0.'
    #         from ._multi_func import fuzznum
    #         newfn = fuzznum(q, [], [])
    #         newfn.md = self.__md ** p
    #         newfn.nmd = (1. - (1. - self.__nmd ** self.qrung) ** p) ** (1 / self.qrung)
    #         return newfn.unique(4)
    #
    #     if isinstance(power, Union[float, int, np.int_, np.float_]):
    #         return __pow(power)
    #
    #     from .mohusets import mohuset
    #     if isinstance(power, np.ndarray):
    #         assert np.all(power) > 0., 'ERROR: The power must be greater than 0.'
    #         vec_func = np.vectorize(__pow)
    #         newset = mohuset(q, self.mtype)
    #         newset.set = vec_func(power)
    #         return newset
    #     raise TypeError(f'Invalid type: {type(power)}')
    #
    # def __and__(self, other):
    #     # TODO: The and of MohuQROHFN is not supported.
    #     raise TypeError('q-rung orthopair hesitant fuzzy add operation is not supported for the time being.')
    #
    # def __or__(self, other):
    #     # TODO: The or of MohuQROHFN is not supported.
    #     raise TypeError('q-rung orthopair hesitant fuzzy or operation is not supported for the time being.')
    #
    # def __eq__(self, other):
    #     def __eq(oth: MohuQROHFN):
    #         assert self.qrung == oth.qrung, \
    #             'ERROR: The qrung must be equal.'
    #         assert self.mtype == oth.mtype, \
    #             'ERROR: The mtype must be same.'
    #         return np.array_equal(self.__md, oth.md) and np.array_equal(self.__nmd, oth.nmd)
    #
    #     if isinstance(other, MohuQROHFN):
    #         return __eq(other)
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         vec_func = np.vectorize(__eq)
    #         res = vec_func(other.set)
    #         return res
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __ne__(self, other):
    #     def __ne(oth: MohuQROHFN):
    #         assert self.mtype == oth.mtype, \
    #             'ERROR: The mtype must be same.'
    #         assert self.qrung == other.qrung, \
    #             'ERROR: The qrung must be equal.'
    #         return not np.array_equal(self.__md, other.md) or not np.array_equal(self.__nmd, other.nmd)
    #
    #     if isinstance(other, MohuQROHFN):
    #         return __ne(other)
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         vec_func = np.vectorize(__ne)
    #         res = vec_func(other.set)
    #         return res
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __lt__(self, other):
    #     # TODO: The comparison of MohuQROHFN is not supported.
    #     # Temporarily adopt the score value comparison method
    #
    #     def __lt(oth: MohuQROHFN):
    #         assert self.qrung == oth.qrung, \
    #             'ERROR: The qrung must be equal.'
    #         assert self.mtype == oth.mtype, \
    #             'ERROR: The mtype must be same.'
    #         return self.score < oth.score
    #
    #     if isinstance(other, MohuQROHFN):
    #         return __lt(other)
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         vec_func = np.vectorize(__lt)
    #         res = vec_func(other.set)
    #         return res
    #     if isinstance(other, np.ndarray):
    #         vec_func = np.vectorize(__lt)
    #         res = vec_func(other)
    #         return res
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __gt__(self, other):
    #     # TODO: The comparison of MohuQROHFN is not supported.
    #     # Temporarily adopt the score value comparison method
    #
    #     def __gt(oth: MohuQROHFN):
    #         assert self.qrung == oth.qrung, \
    #             'ERROR: The qrung must be equal.'
    #         assert self.mtype == oth.mtype, \
    #             'ERROR: The mtype must be same.'
    #         return self.score > oth.score
    #
    #     if isinstance(other, MohuQROHFN):
    #         return __gt(other)
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         vec_func = np.vectorize(__gt)
    #         res = vec_func(other.set)
    #         return res
    #     if isinstance(other, np.ndarray):
    #         vec_func = np.vectorize(__gt)
    #         res = vec_func(other)
    #         return res
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __le__(self, other):
    #     # TODO: The comparison of MohuQROHFN is not supported.
    #     # Temporarily adopt the score value comparison method
    #
    #     def __le(oth: MohuQROHFN):
    #         assert self.qrung == oth.qrung, \
    #             'ERROR: The qrung must be equal.'
    #         assert self.mtype == oth.mtype, \
    #             'ERROR: The mtype must be same.'
    #         return self.score <= oth.score
    #
    #     if isinstance(other, MohuQROHFN):
    #         return __le(other)
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         vec_func = np.vectorize(__le)
    #         res = vec_func(other.set)
    #         return res
    #     if isinstance(other, np.ndarray):
    #         vec_func = np.vectorize(__le)
    #         res = vec_func(other)
    #         return res
    #     raise TypeError(f'Invalid type: {type(other)}')
    #
    # def __ge__(self, other):
    #     # TODO: The comparison of MohuQROHFN is not supported.
    #     # Temporarily adopt the score value comparison method
    #
    #     def __ge(oth: MohuQROHFN):
    #         assert self.qrung == oth.qrung, \
    #             'ERROR: The qrung must be equal.'
    #         assert self.mtype == oth.mtype, \
    #             'ERROR: The mtype must be same.'
    #         return self.score >= oth.score
    #
    #     if isinstance(other, MohuQROHFN):
    #         return __ge(other)
    #     from .mohusets import mohuset
    #     if isinstance(other, mohuset):
    #         vec_func = np.vectorize(__ge)
    #         res = vec_func(other.set)
    #         return res
    #     if isinstance(other, np.ndarray):
    #         vec_func = np.vectorize(__ge)
    #         res = vec_func(other)
    #         return res
    #     raise TypeError(f'Invalid type: {type(other)}')

    def is_valid(self):
        a1 = self.__md.size == 0 and self.__nmd.size == 0
        a2 = self.__md.size == 0 and 0 <= self.__nmd.all() <= 1
        a3 = self.__nmd.size == 0 and 0 <= self.__md.all() <= 1
        a4 = min(self.__md) >= 0 and min(self.__nmd) >= 0 and max(self.__md) ** self.qrung + max(
            self.__nmd) ** self.qrung <= 1
        if a1:
            # print('a1')
            return True
        elif a2:
            # print('a2')
            return True
        elif a3:
            # print('a3')
            return True
        elif a4:
            # print('a4')
            return True
        else:
            return False

    def isEmpty(self):
        if self.__md.size == 0 and self.__nmd.size == 0:
            return True
        else:
            return False

    def convert(self):
        m = self.__md.tolist()
        n = self.__nmd.tolist()
        return m, n

    def qsort(self, rev=True):
        newEle = copy.deepcopy(self)
        if rev:
            newEle.md = np.sort(self.__md)
            newEle.nmd = np.sort(self.__nmd)
        else:
            newEle.md = np.abs(np.sort(-self.__md))
            newEle.nmd = np.abs(np.sort(-self.__nmd))
        return newEle

    def unique(self):
        """
            Simplify the membership and non-membership degrees with x precision
        """
        # assert ac >= 1, "x must be greater than 1"
        self.__md = np.unique(self.__md, Approx.round)
        self.__nmd = np.unique(self.__nmd, Approx.round)
        return self

    def flatten(self):
        from .mohusets import mohuset
        newset = mohuset(self.qrung, self.mtype)
        newset.append(self)
        return newset
