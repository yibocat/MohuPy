#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/9/29 上午10:37
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import copy
from typing import Union

from matplotlib import pyplot as plt
from .base import MohuBase
from ..init import fuzzType

import numpy as np


@fuzzType('MohuQROFN')
class MohuQROFN(MohuBase):
    qrung = None
    md = None
    nmd = None
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
            self.md = np.float_(md)
            self.nmd = np.float_(nmd)
            self.mtype = 'qrofn'
            self.size = 1
        pass

    def __repr__(self):
        return '[' + \
            str(np.round(self.md, 4)) + ',' + \
            str(np.round(self.nmd, 4)) + ']'

    def __str__(self):
        return '[' + \
            str(np.round(self.md, 4)) + ',' + \
            str(np.round(self.nmd, 4)) + ']'

    def score(self):
        return self.md ** self.qrung - self.nmd ** self.qrung

    def acc(self):
        return self.md ** self.qrung + self.nmd ** self.qrung

    def ind(self):
        acc = self.md ** self.qrung + self.nmd ** self.qrung
        if acc == 1.:
            return 0.
        else:
            return (1. - acc) ** (1. / self.qrung)

    def comp(self):
        newf = copy.deepcopy(self)
        newf.md = self.nmd
        newf.nmd = self.md
        return newf

    def __add__(self, other):
        q = self.qrung

        def __add(oth: MohuQROFN):
            assert self.qrung == oth.qrung, \
                'ERROR: qrung must be equal.'
            assert self.mtype == oth.mtype, \
                'ERROR: mtype must be same.'
            from .mohunum import mohunum
            newfn = mohunum(q, 0, 0)
            newfn.md = (self.md ** q + oth.md ** q
                        - self.md ** q * oth.md ** q) ** (1 / q)
            newfn.nmd = self.nmd * oth.nmd
            return newfn

        if isinstance(other, MohuQROFN):
            return __add(other)

        from .mohusets import mohuset
        if isinstance(other, mohuset):
            assert other.mtype == self.mtype, \
                'ERROR: The fuzzy number and set must be of the same type.'
            assert other.qrung == self.qrung, \
                'ERROR: The fuzzy number and set must be of the same Q-rung.'

            vec_func = np.vectorize(__add)
            newset = mohuset(q, self.mtype)
            newset.set = vec_func(other.set)
            return newset
        raise TypeError(f'Invalid type: {type(other)}')

    def __radd__(self, other):
        q = self.qrung

        def __add(oth: MohuQROFN):
            assert self.qrung == oth.qrung, \
                'ERROR: qrung must be equal.'
            assert self.mtype == oth.mtype, \
                'ERROR: mtype must be same.'
            from .mohunum import mohunum
            newfn = mohunum(q, 0, 0)
            newfn.md = (self.md ** q + oth.md ** q
                        - self.md ** q * oth.md ** q) ** (1 / q)
            newfn.nmd = self.nmd * oth.nmd
            return newfn

        if isinstance(other, MohuQROFN):
            return __add(other)

        from .mohusets import mohuset
        if isinstance(other, mohuset):
            assert other.mtype == self.mtype, \
                'ERROR: The fuzzy number and set must be of the same type.'
            assert other.qrung == self.qrung, \
                'ERROR: The fuzzy number and set must be of the same Q-rung.'

            vec_func = np.vectorize(__add)
            newset = mohuset(q, self.mtype)
            newset.set = vec_func(other.set)
            return newset
        raise TypeError(f'Invalid type: {type(other)}')

    def __sub__(self, other):
        q = self.qrung

        def __sub(oth: MohuQROFN):
            assert self.qrung == oth.qrung, \
                'ERROR: qrung must be equal.'
            assert self.mtype == oth.mtype, \
                'ERROR: mtype must be same.'
            from .mohunum import mohunum
            newfn = mohunum(q, 0, 1)
            if oth.nmd == 0. or oth.md == 1.:
                return newfn
            elif 0 <= self.nmd / oth.nmd <= ((1 - self.md ** q) / (1 - oth.md ** q)) ** (1 / q) <= 1:
                newfn.md = ((self.md ** q - oth.md ** q) / (1 - oth.md ** q)) ** (1 / q)
                newfn.nmd = self.nmd / oth.nmd
                return newfn
            else:
                return newfn

        if isinstance(other, MohuQROFN):
            return __sub(other)

        from .mohusets import mohuset
        if isinstance(other, mohuset):
            assert other.mtype == self.mtype, \
                'ERROR: The fuzzy number and set must be of the same type.'
            assert other.qrung == self.qrung, \
                'ERROR: The fuzzy number and set must be of the same Q-rung.'

            vec_func = np.vectorize(__sub)
            newset = mohuset(q, self.mtype)
            newset.set = vec_func(other.set)
            return newset
        raise TypeError(f'Invalid type: {type(other)}')

    def __mul__(self, other):
        q = self.qrung

        def __mul(oth: Union[MohuQROFN, float, int, np.int_, np.float_]):
            if isinstance(oth, MohuQROFN):
                assert self.qrung == oth.qrung, \
                    'ERROR: qrung must be equal.'
                assert self.mtype == oth.mtype, \
                    'ERROR: mtype must be same.'
                from .mohunum import mohunum
                newfn = mohunum(q, 0, 0)
                newfn.md = self.md * oth.md
                newfn.nmd = (self.nmd ** q + oth.nmd ** q
                             - self.nmd ** q * oth.nmd ** q) ** (1. / q)
                return newfn
            if isinstance(oth, Union[float, int, np.int_, np.float_]):
                assert oth > 0., 'ERROR: The value must be greater than 0.'
                from .mohunum import mohunum
                newfn = mohunum(q, 0, 0)
                newfn.md = (1. - (1. - self.md ** q) ** oth) ** (1. / q)
                newfn.nmd = self.nmd ** oth
                return newfn

        if isinstance(other, Union[MohuQROFN, float, int, np.int_, np.float_]):
            return __mul(other)

        from .mohusets import mohuset
        if isinstance(other, mohuset):
            assert other.mtype == self.mtype, \
                'ERROR: The fuzzy number and set must be of the same type.'
            assert other.qrung == self.qrung, \
                'ERROR: The fuzzy number and set must be of the same Q-rung.'
            vec_func = np.vectorize(__mul)
            newset = mohuset(q, self.mtype)
            newset.set = vec_func(other.set)
            return newset
        if isinstance(other, np.ndarray):
            assert np.all(other) > 0, 'ERROR: The value must be greater than 0.'
            vec_func = np.vectorize(__mul)
            newset = mohuset(q, self.mtype)
            newset.set = vec_func(other)
            return newset
        raise TypeError(f'Invalid type: {type(other)}')

    def __rmul__(self, other):
        q = self.qrung

        def __mul(oth: Union[MohuQROFN, float, int, np.int_, np.float_]):
            if isinstance(oth, MohuQROFN):
                assert self.qrung == oth.qrung, \
                    'ERROR: qrung must be equal.'
                assert self.mtype == oth.mtype, \
                    'ERROR: mtype must be same.'
                from .mohunum import mohunum
                newfn = mohunum(q, 0, 0)
                newfn.md = self.md * oth.md
                newfn.nmd = (self.nmd ** q + oth.nmd ** q
                             - self.nmd ** q * oth.nmd ** q) ** (1. / q)
                return newfn
            if isinstance(oth, Union[float, int, np.int_, np.float_]):
                assert oth >= 0., 'ERROR: The value must be greater than 0.'
                from .mohunum import mohunum
                newfn = mohunum(q, 0, 0)
                newfn.md = (1. - (1. - self.md ** q) ** oth) ** (1. / q)
                newfn.nmd = self.nmd ** oth
                return newfn

        if isinstance(other, Union[MohuQROFN, float, int, np.int_, np.float_]):
            return __mul(other)

        from .mohusets import mohuset
        if isinstance(other, mohuset):
            assert other.mtype == self.mtype, \
                'ERROR: The fuzzy number and set must be of the same type.'
            assert other.qrung == self.qrung, \
                'ERROR: The fuzzy number and set must be of the same Q-rung.'
            vec_func = np.vectorize(__mul)
            newset = mohuset(q, self.mtype)
            newset.set = vec_func(other.set)
            return newset
        if isinstance(other, np.ndarray):
            assert np.all(other) > 0, 'ERROR: The value must be greater than 0.'
            vec_func = np.vectorize(__mul)
            newset = mohuset(q, self.mtype)
            newset.set = vec_func(other)
            return newset
        raise TypeError(f'Invalid type: {type(other)}')

    def __truediv__(self, other):
        q = self.qrung

        def __truediv(oth: Union[MohuQROFN, float, int, np.int_, np.float_]):
            if isinstance(oth, MohuQROFN):
                from .mohunum import mohunum
                newfn = mohunum(q, 1, 0)
                if oth.md == 0 or oth.nmd == 1.:
                    return newfn
                elif 0 <= self.md / oth.md <= \
                        ((1 - self.nmd ** q) / (1 - oth.nmd ** q)) ** (1 / q) <= 1:
                    newfn.md = self.md / oth.md
                    newfn.nmd = ((self.nmd ** q - oth.nmd ** q) / (1 - oth.nmd ** q)) ** (1 / q)
                    return newfn
                else:
                    return newfn
            if isinstance(oth, Union[float, int, np.int_, np.float_]):
                assert oth >= 1., 'ERROR: The value must be greater than 1.'
                return self.__mul__(1. / oth)

        if isinstance(other, Union[MohuQROFN, float, int, np.int_, np.float_]):
            return __truediv(other)

        from .mohusets import mohuset
        if isinstance(other, mohuset):
            assert other.mtype == self.mtype, \
                'ERROR: The fuzzy number and set must be of the same type.'
            assert other.qrung == self.qrung, \
                'ERROR: The fuzzy number and set must be of the same Q-rung.'
            vec_func = np.vectorize(__truediv)
            newset = mohuset(q, self.mtype)
            newset.set = vec_func(other.set)
            return newset
        if isinstance(other, np.ndarray):
            assert np.all(other) >= 1., 'ERROR: The value must be greater than'
            vec_func = np.vectorize(__truediv)
            newset = mohuset(q, self.mtype)
            newset.set = vec_func(other)
            return newset
        raise TypeError(f'Invalid type: {type(other)}')

    def __pow__(self, power, modulo=None):
        q = self.qrung

        def __pow(p: Union[float, int, np.int_, np.float_]):
            assert p > 0., 'ERROR: The power must be greater than 0.'
            from .mohunum import mohunum
            newfn = mohunum(q, 0, 0)
            newfn.md = self.md ** p
            newfn.nmd = (1. - (1. - self.nmd ** q) ** p) ** (1. / q)
            return newfn

        if isinstance(power, Union[float, int, np.int_, np.float_]):
            return __pow(power)

        from .mohusets import mohuset
        if isinstance(power, np.ndarray):
            assert np.all(power) > 0., 'ERROR: The power must be greater than 0.'
            vec_func = np.vectorize(__pow)
            newset = mohuset(q, self.mtype)
            newset.set = vec_func(power)
            return newset
        raise TypeError(f'Invalid type: {type(power)}')

    def __and__(self, other):
        assert isinstance(other, MohuQROFN), \
            'ERROR: other must be a MohuQROFN.'
        assert self.mtype == other.mtype, \
            'ERROR: mtype must be same.'
        assert self.qrung == other.qrung, \
            'ERROR: The qrung must be equal.'

        q = self.qrung
        from .mohunum import mohunum
        newfn = mohunum(q, 0, 0)
        newfn.md = (min(self.md, other.md))
        newfn.nmd = (max(self.nmd, other.nmd))
        return newfn

    def __or__(self, other):
        assert isinstance(other, MohuQROFN), \
            'ERROR: other must be a MohuQROFN.'
        assert self.mtype == other.mtype, \
            'ERROR: mtype must be same.'
        assert self.qrung == other.qrung, \
            'ERROR: The qrung must be equal.'
        q = self.qrung
        from .mohunum import mohunum
        newfn = mohunum(q, 0, 0)
        newfn.md = (max(self.md, other.md))
        newfn.nmd = (min(self.nmd, other.nmd))
        return newfn

    def __eq__(self, other):
        assert isinstance(other, MohuQROFN), \
            'ERROR: other must be a MohuQROFN.'
        assert self.mtype == other.mtype, \
            'ERROR: mtype must be same.'
        assert self.qrung == other.qrung, \
            'ERROR: The qrung must be equal.'
        return self.md == other.md and self.nmd == other.nmd

    def __ne__(self, other):
        assert isinstance(other, MohuQROFN), \
            'ERROR: other must be a MohuQROFN.'
        assert self.mtype == other.mtype, \
            'ERROR: mtype must be same.'
        assert self.qrung == other.qrung, \
            'ERROR: The qrung must be equal.'
        return self.md != other.md or self.nmd != other.nmd

    def __lt__(self, other):
        assert isinstance(other, MohuQROFN), \
            'ERROR: other must be a MohuQROFN.'
        assert self.mtype == other.mtype, \
            'ERROR: mtype must be same.'
        assert self.qrung == other.qrung, \
            'ERROR: The qrung must be equal.'
        q = self.qrung
        from .mohunum import mohunum
        if self - other == mohunum(q, 0, 1) and self != other:
            return True
        else:
            return False

    def __gt__(self, other):
        assert isinstance(other, MohuQROFN), \
            'ERROR: other must be a MohuQROFN.'
        assert self.mtype == other.mtype, \
            'ERROR: mtype must be same.'
        assert self.qrung == other.qrung, \
            'ERROR: The qrung must be equal.'
        q = self.qrung
        from .mohunum import mohunum
        if self - other != mohunum(q, 0., 1.) and self != other:
            return True
        else:
            return False

    def __le__(self, other):
        assert isinstance(other, MohuQROFN), \
            'ERROR: other must be a MohuQROFN.'
        assert self.mtype == other.mtype, \
            'ERROR: mtype must be same.'
        assert self.qrung == other.qrung, \
            'ERROR: The qrung must be equal.'
        q = self.qrung
        from .mohunum import mohunum
        if self - other == mohunum(q, 0., 1.) or self == other:
            return True
        else:
            return False

    def __ge__(self, other):
        assert isinstance(other, MohuQROFN), \
            'ERROR: other must be a MohuQROFN.'
        assert self.mtype == other.mtype, \
            'ERROR: mtype must be same.'
        assert self.qrung == other.qrung, \
            'ERROR: The qrung must be equal.'
        q = self.qrung
        from .mohunum import mohunum
        if self - other != mohunum(q, 0., 1.) or self == other:
            return True
        else:
            return False

    def is_valid(self):
        mds = self.md
        nmds = self.nmd
        if 0. <= mds <= 1. and 0. <= nmds <= 1. \
                and 0. <= mds ** self.qrung + nmds ** self.qrung <= 1.:
            return True
        else:
            return False

    def isEmpty(self):
        if self.md is None and self.nmd is None:
            return True
        else:
            return False

    def convert(self):
        return np.round(self.md, 4), np.round(self.nmd, 4)

    def plot(self, other=None, area=None, color='red', color_area=None, alpha=0.3):

        if area is None:
            area = [False, False, False, False]
        if color_area is None:
            color_area = ['red', 'green', 'blue', 'yellow']

        md = self.md
        nmd = self.nmd
        q = self.qrung

        x = np.linspace(0, 1, 1000)

        plt.gca().spines['top'].set_linewidth(False)
        plt.gca().spines['bottom'].set_linewidth(True)
        plt.gca().spines['left'].set_linewidth(True)
        plt.gca().spines['right'].set_linewidth(False)
        plt.axis((0, 1.1, 0, 1.1))
        plt.axhline(y=0)
        plt.axvline(x=0)
        plt.scatter(md, nmd, color=color, marker='.')

        if other is not None:
            assert other.qrung == q, 'ERROR: The qrungs are not equal'
            plt.scatter(other.md, other.nmd, color=color, marker='*')

        y = (1 - x ** q) ** (1 / q)

        n = (nmd ** q / (1 - md ** q) * (1 - x ** q)) ** (1 / q)
        m = (md ** q / (1 - nmd ** q) * (1 - x ** q)) ** (1 / q)

        if area[0]:
            # Q-ROFN f addition region
            plt.fill_between(x, n, color=color_area[0], alpha=alpha, where=x > md)
        if area[1]:
            # Q-ROFN f subtraction region
            plt.fill_between(x, n, y, color=color_area[1], alpha=alpha, where=x < md)
        if area[2]:
            # Q-ROFN f multiplication region
            plt.fill_betweenx(x, m, color=color_area[2], alpha=alpha, where=x > nmd)
        if area[3]:
            # Q-ROFN f division region
            plt.fill_betweenx(x, m, y, color=color_area[3], alpha=alpha, where=x < nmd)

        plt.plot(x, y)
        plt.show()


@fuzzType('MohuQROIVFN')
class MohuQROIVFN(MohuBase):
    qrung = None
    md = None
    nmd = None
    mtype = None

    def __init__(self, qrung: Union[int, np.int_] = None,
                 md: Union[list, tuple, np.ndarray] = None,
                 nmd: Union[list, tuple, np.ndarray] = None):
        super().__init__()
        if isinstance(md, (list, tuple, np.ndarray)) and isinstance(nmd, (list, tuple, np.ndarray)):
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
            self.md = np.asarray(md)
            self.nmd = np.asarray(nmd)
            self.mtype = 'ivfn'
            self.size = 1

    def __repr__(self):
        return '[[' + \
            str(np.round(self.md[0], 4)) + ',' + \
            str(np.round(self.md[1], 4)) + '],[' + \
            str(np.round(self.nmd[0], 4)) + ',' + \
            str(np.round(self.nmd[1], 4)) + ']]'

    def __str__(self):
        return '[[' + \
            str(np.round(self.md[0], 4)) + ',' + \
            str(np.round(self.md[1], 4)) + '],[' + \
            str(np.round(self.nmd[0], 4)) + ',' + \
            str(np.round(self.nmd[1], 4)) + ']]'

    def score(self):
        m = self.md[0] ** self.qrung + self.md[1] ** self.qrung
        n = self.nmd[0] ** self.qrung + self.nmd[1] ** self.qrung
        return (m - n) / 2

    def acc(self):
        m = self.md[0] ** self.qrung + self.md[1] ** self.qrung
        n = self.nmd[0] ** self.qrung + self.nmd[1] ** self.qrung
        return (m + n) / 2

    def ind(self):
        m = self.md[0] ** self.qrung + self.md[1] ** self.qrung
        n = self.nmd[0] ** self.qrung + self.nmd[1] ** self.qrung
        if m + n:
            return 0.
        else:
            return (1. - (m + n) / 2) ** (1. / self.qrung)

    def comp(self):
        newf = copy.deepcopy(self)
        newf.md = self.nmd
        newf.nmd = self.md
        return newf

    def __add__(self, other):
        q = self.qrung

        def __add(oth: MohuQROIVFN):
            assert self.qrung == oth.qrung, \
                'ERROR: qrung must be equal.'
            assert self.mtype == oth.mtype, \
                'ERROR: mtype must be same.'
            from .mohunum import mohunum
            newfn = mohunum(q, [0., 0.], [0., 0.])
            newfn.md = (self.md ** q + oth.md ** q - self.md ** q * oth.md ** q) ** (1. / q)
            newfn.nmd = self.nmd * oth.nmd
            return newfn

        if isinstance(other, MohuQROIVFN):
            return __add(other)

        from .mohusets import mohuset
        if isinstance(other, mohuset):
            assert other.mtype == self.mtype, \
                'ERROR: The fuzzy number and set must be of the same type.'
            assert other.qrung == self.qrung, \
                'ERROR: The fuzzy number and set must be of the same Q-rung.'

            vec_func = np.vectorize(__add)
            newset = mohuset(q, self.mtype)
            newset.set = vec_func(other.set)
            return newset
        raise TypeError(f'Invalid type: {type(other)}')

    def __radd__(self, other):
        q = self.qrung

        def __add(oth: MohuQROIVFN):
            assert self.qrung == oth.qrung, \
                'ERROR: qrung must be equal.'
            assert self.mtype == oth.mtype, \
                'ERROR: mtype must be same.'
            from .mohunum import mohunum
            newfn = mohunum(q, [0., 0.], [0., 0.])
            newfn.md = (self.md ** q + oth.md ** q - self.md ** q * oth.md ** q) ** (1. / q)
            newfn.nmd = self.nmd * oth.nmd
            return newfn

        if isinstance(other, MohuQROIVFN):
            return __add(other)

        from .mohusets import mohuset
        if isinstance(other, mohuset):
            assert other.mtype == self.mtype, \
                'ERROR: The fuzzy number and set must be of the same type.'
            assert other.qrung == self.qrung, \
                'ERROR: The fuzzy number and set must be of the same Q-rung.'

            vec_func = np.vectorize(__add)
            newset = mohuset(q, self.mtype)
            newset.set = vec_func(other.set)
            return newset
        raise TypeError(f'Invalid type: {type(other)}')

    def __sub__(self, other):
        # TODO: The subtraction of MohuQROIVFN is not supported.
        pass

    def __mul__(self, other):
        q = self.qrung

        def __mul(oth: Union[MohuQROIVFN, float, int, np.int_, np.float_]):
            if isinstance(oth, MohuQROIVFN):
                assert self.qrung == oth.qrung, \
                    'ERROR: qrung must be equal.'
                assert self.mtype == oth.mtype, \
                    'ERROR: mtype must be same.'
                from .mohunum import mohunum
                newfn = mohunum(q, [0., 0.], [0., 0.])
                newfn.md = self.md * oth.md
                newfn.nmd = (self.nmd ** q + oth.nmd ** q - self.nmd ** q * oth.nmd ** q) ** (1. / q)
                return newfn
            if isinstance(oth, Union[float, int, np.int_, np.float_]):
                assert oth >= 0., 'ERROR: The value must be greater than 0.'
                from .mohunum import mohunum
                newfn = mohunum(q, [0., 0.], [0., 0.])
                newfn.md = (1. - (1 - self.md ** q) ** oth) ** (1. / q)
                newfn.nmd = self.nmd ** oth
                return newfn
            raise TypeError('ERROR: Unsupported type.')

        if isinstance(other, Union[MohuQROIVFN, float, int, np.int_, np.float_]):
            return __mul(other)

        from .mohusets import mohuset
        if isinstance(other, mohuset):
            assert other.mtype == self.mtype, \
                'ERROR: The fuzzy number and set must be of the same type.'
            assert other.qrung == self.qrung, \
                'ERROR: The fuzzy number and set must be of the same Q-rung.'
            vec_func = np.vectorize(__mul)
            newset = mohuset(q, self.mtype)
            newset.set = vec_func(other.set)
            return newset
        if isinstance(other, np.ndarray):
            assert np.all(other) > 0, 'ERROR: The value must be greater than 0.'
            vec_func = np.vectorize(__mul)
            newset = mohuset(q, self.mtype)
            newset.set = vec_func(other)
            return newset
        raise TypeError(f'Invalid type: {type(other)}')

    def __rmul__(self, other):
        q = self.qrung

        def __mul(oth: Union[MohuQROIVFN, float, int, np.int_, np.float_]):
            if isinstance(oth, MohuQROIVFN):
                assert self.qrung == oth.qrung, \
                    'ERROR: qrung must be equal.'
                assert self.mtype == oth.mtype, \
                    'ERROR: mtype must be same.'
                from .mohunum import mohunum
                newfn = mohunum(q, [0., 0.], [0., 0.])
                newfn.md = self.md * oth.md
                newfn.nmd = (self.nmd ** q + oth.nmd ** q - self.nmd ** q * oth.nmd ** q) ** (1. / q)
                return newfn
            if isinstance(oth, Union[float, int, np.int_, np.float_]):
                assert oth >= 0., 'ERROR: The value must be greater than 0.'
                from .mohunum import mohunum
                newfn = mohunum(q, [0., 0.], [0., 0.])
                newfn.md = (1. - (1 - self.md ** q) ** oth) ** (1. / q)
                newfn.nmd = self.nmd ** oth
                return newfn
            raise TypeError('ERROR: Unsupported type.')

        if isinstance(other, Union[MohuQROIVFN, float, int, np.int_, np.float_]):
            return __mul(other)

        from .mohusets import mohuset
        if isinstance(other, mohuset):
            assert other.mtype == self.mtype, \
                'ERROR: The fuzzy number and set must be of the same type.'
            assert other.qrung == self.qrung, \
                'ERROR: The fuzzy number and set must be of the same Q-rung.'
            vec_func = np.vectorize(__mul)
            newset = mohuset(q, self.mtype)
            newset.set = vec_func(other.set)
            return newset
        if isinstance(other, np.ndarray):
            assert np.all(other) > 0, 'ERROR: The value must be greater than 0.'
            vec_func = np.vectorize(__mul)
            newset = mohuset(q, self.mtype)
            newset.set = vec_func(other)
            return newset
        raise TypeError(f'Invalid type: {type(other)}')

    def __truediv__(self, other):
        # TODO: The division of MohuQROIVFN is not supported.
        pass

    def __pow__(self, power, modulo=None):
        q = self.qrung

        def __pow(p: Union[float, int, np.int_, np.float_]):
            assert p > 0., 'ERROR: The power must be greater than 0.'
            from .mohunum import mohunum
            newfn = mohunum(q, [0., 0.], [0., 0.])
            newfn.md = self.md ** p
            newfn.nmd = (1. - (1. - self.nmd ** q) ** p) ** (1. / q)
            return newfn

        if isinstance(power, Union[float, int, np.int_, np.float_]):
            return __pow(power)

        from .mohusets import mohuset
        if isinstance(power, np.ndarray):
            assert np.all(power) > 0., 'ERROR: The power must be greater than 0.'
            vec_func = np.vectorize(__pow)
            newset = mohuset(q, self.mtype)
            newset.set = vec_func(power)
            return newset
        raise TypeError(f'Invalid type: {type(power)}')

    def __and__(self, other):
        assert isinstance(other, MohuQROIVFN), \
            'ERROR: other must be a MohuQROIVFN.'
        assert self.mtype == other.mtype, \
            'ERROR: mtype must be same.'
        assert self.qrung == other.qrung, \
            'ERROR: The qrung must be equal.'
        q = self.qrung
        from .mohunum import mohunum
        newfn = mohunum(q, [0., 0.], [0., 0.])
        newfn.md = [min(self.md[0], other.md[0]), min(self.md[1], other.md[1])]
        newfn.nmd = [max(self.nmd[0], other.nmd[0]), max(self.nmd[1], other.nmd[1])]
        return newfn

    def __or__(self, other):
        assert isinstance(other, MohuQROIVFN), \
            'ERROR: other must be a MohuQROIVFN.'
        assert self.mtype == other.mtype, \
            'ERROR: mtype must be same.'
        assert self.qrung == other.qrung, \
            'ERROR: The qrung must be equal.'
        q = self.qrung
        from .mohunum import mohunum
        newfn = mohunum(q, [0., 0.], [0., 0.])
        newfn.md = [max(self.md[0], other.md[0]), max(self.md[1], other.md[1])]
        newfn.nmd = [min(self.nmd[0], other.nmd[0]), min(self.nmd[1], other.nmd[1])]
        return newfn

    def __eq__(self, other):
        assert isinstance(other, MohuQROIVFN), \
            'ERROR: other must be a MohuQROIVFN.'
        assert self.qrung == other.qrung, \
            'ERROR: The qrung must be equal.'
        return np.array_equal(self.md, other.md) and np.array_equal(self.nmd, other.nmd)

    def __ne__(self, other):
        assert isinstance(other, MohuQROIVFN), \
            'ERROR: other must be a MohuQROIVFN.'
        assert self.qrung == other.qrung, \
            'ERROR: The qrung must be equal.'
        return not np.array_equal(self.md, other.md) or not np.array_equal(self.nmd, other.nmd)

    def __lt__(self, other):
        # TODO: The comparison of MohuQROIVFN is not supported.
        assert isinstance(other, MohuQROIVFN), \
            'ERROR: other must be a MohuQROIVFN.'
        assert self.qrung == other.qrung, \
            'ERROR: The qrung must be equal.'
        raise TypeError('MohuQROIVFN does not support comparison.')

    def __gt__(self, other):
        # TODO: The comparison of MohuQROIVFN is not supported.
        assert isinstance(other, MohuQROIVFN), \
            'ERROR: other must be a MohuQROIVFN.'
        assert self.qrung == other.qrung, \
            'ERROR: The qrung must be equal.'
        raise TypeError('MohuQROIVFN does not support comparison.')

    def __le__(self, other):
        # TODO: The comparison of MohuQROIVFN is not supported.
        assert isinstance(other, MohuQROIVFN), \
            'ERROR: other must be a MohuQROIVFN.'
        assert self.qrung == other.qrung, \
            'ERROR: The qrung must be equal.'
        raise TypeError('MohuQROIVFN does not support comparison.')

    def __ge__(self, other):
        # TODO: The comparison of MohuQROIVFN is not supported.
        assert isinstance(other, MohuQROIVFN), \
            'ERROR: other must be a MohuQROIVFN.'
        assert self.qrung == other.qrung, \
            'ERROR: The qrung must be equal.'
        raise TypeError('MohuQROIVFN does not support comparison.')

    def is_valid(self):
        if not len(self.md) == 2 and len(self.nmd) == 2:
            return False
        elif not 0. <= np.all(self.md) <= 1. and 0. <= np.all(self.md) <= 1.:
            return False
        elif not (self.md[0] <= self.md[1] and self.nmd[0] <= self.nmd[1]):
            return False
        elif not 0 <= self.md[1] ** self.qrung + self.nmd[1] ** self.qrung <= 1:
            return False
        else:
            return True

    def isEmpty(self):
        if self.md is None and self.nmd is None:
            return True
        else:
            return False

    def convert(self):
        return np.round(self.md, 4).tolist(), np.round(self.nmd, 4).tolist()

    def plot(self, other=None, color='red', alpha=0.3):
        md = self.md
        nmd = self.nmd
        q = self.qrung

        x = np.linspace(0, 1, 1000)

        plt.gca().spines['top'].set_linewidth(False)
        plt.gca().spines['bottom'].set_linewidth(True)
        plt.gca().spines['left'].set_linewidth(True)
        plt.gca().spines['right'].set_linewidth(False)
        plt.axis((0, 1.1, 0, 1.1))
        plt.axhline(y=0)
        plt.axvline(x=0)

        plt.fill([md[0], md[1], md[1], md[0]],
                 [nmd[1], nmd[1], nmd[0], nmd[0]],
                 color=color, alpha=alpha)

        if other is not None:
            assert isinstance(other, MohuQROIVFN), \
                'ERROR: other must be a mohunum object.'
            assert other.qrung == q, \
                'ERROR: The qrungs are not equal'
            assert self.mtype == other.mtype, \
                'ERROR: The type of two fuzzy numbers must be same.'
            plt.fill([other.md[0], other.md[1], other.md[1], other.md[0]],
                     [other.nmd[1], other.nmd[1], other.nmd[0], other.nmd[0]],
                     color=color, alpha=alpha)

        y = (1 - x ** q) ** (1 / q)
        plt.plot(x, y)
        plt.show()
