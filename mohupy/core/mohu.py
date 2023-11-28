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
                'ERROR: md and nmd must be betweenZERO and ONE'
            assert 0. <= md ** qrung + nmd ** qrung <= 1., \
                'ERROR: md ** qrung + nmd ** qrung must be between ZERO and ONE'

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
        if acc == np.round(1., Approx.round):
            return np.round(0., Approx.round)
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
                 md: tuple = None,
                 nmd: tuple = None):
        super().__init__()
        if isinstance(md, tuple) and isinstance(nmd, tuple):
            assert len(md) == 2 and len(nmd) == 2, \
                'ERROR: The data format contains at least upper and lower bounds.'
            assert md[0] <= md[1] and nmd[0] <= nmd[1], \
                'ERROR: The upper of membership and non-membership must be greater than the lower.'
            assert 0. <= md[0] <= 1. and 0. <= md[1] <= 1., \
                'ERROR: The upper and lower of membership degree must be between 0 and 1.'
            assert 0. <= nmd[0] <= 1. and 0. <= nmd[1] <= 1., \
                'ERROR: The upper and lower of non-membership degree must be between 0 and 1.'
            assert 0. <= md[0] ** qrung + nmd[0] ** qrung <= 1. and 0. <= md[1] ** qrung + nmd[1] ** qrung <= 1., \
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
            return np.round(0., Approx.round)
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

    def is_valid(self):
        if not len(self.__md) == 2 and len(self.__nmd) == 2:
            return False
        elif not 0. <= np.all(self.__md) <= 1. and 0. <= np.all(self.__md) <= 1.:
            return False
        elif not (self.__md[0] <= self.__md[1] and self.__nmd[0] <= self.__nmd[1]):
            return False
        elif not 0. <= self.__md[1] ** self.qrung + self.__nmd[1] ** self.qrung <= 1.:
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
            return np.round(0., Approx.round)
        else:
            return (1. - mm - nn) ** (1. / self.qrung)

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

    def is_valid(self):
        a1 = self.__md.size == 0 and self.__nmd.size == 0
        a2 = self.__md.size == 0 and 0. <= self.__nmd.all() <= 1.
        a3 = self.__nmd.size == 0 and 0. <= self.__md.all() <= 1.
        a4 = min(self.__md) >= 0. and min(self.__nmd) >= 0. and max(self.__md) ** self.qrung + max(
            self.__nmd) ** self.qrung <= 1.
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
