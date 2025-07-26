#  Copyright (c) yibocat 2025 All Rights Reserved
#  Python: 3.10.9
#  Date: 2025/7/8 18:43
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import copy

import numpy as np

from .template import Template
from .base import fuzz_directory


@fuzz_directory('qrohfn')
class qROHFN(Template):

    mtype = 'qrohfn'

    def __init__(self, qrung=None, md=None, nmd=None):
        super().__init__(qrung, md, nmd)
        self.qrung = qrung
        self.md = md
        self.nmd = nmd

    def report(self):
        if len(self.md) > 8 >= len(self.nmd):
            return f'<{np.round(self.md[:8], 4)}..., {np.round(self.nmd, 4)}>'
        if len(self.nmd) > 8 >= len(self.md):
            return f'<{np.round(self.md, 4)}, {np.round(self.nmd[:8], 4)}...>'
        if len(self.md) > 8 and len(self.nmd) > 8:
            return f'<{np.round(self.md[:8], 4)}..., {np.round(self.nmd[:8], 4)}...>'
        else:
            return f'<{np.round(self.md, 4)}, {np.round(self.nmd, 4)}>'

    def str(self):
        if len(self.md) > 8 >= len(self.nmd):
            return f'<{np.round(self.md[:8], 4)}..., {np.round(self.nmd, 4)}>'
        if len(self.nmd) > 8 >= len(self.md):
            return f'<{np.round(self.md, 4)}, {np.round(self.nmd[:8], 4)}...>'
        if len(self.md) > 8 and len(self.nmd) > 8:
            return f'<{np.round(self.md[:8], 4)}..., {np.round(self.nmd[:8], 4)}...>'
        else:
            return f'<{np.round(self.md, 4)}, {np.round(self.nmd, 4)}>'

    def score(self):
        if len(self.md) == 0 or len(self.nmd) == 0:
            return None
        else:
            mm = ((self.md ** self.qrung).sum()) / len(self.md)
            nn = ((self.nmd ** self.qrung).sum()) / len(self.nmd)
            return mm - nn

    def accuracy(self):
        if len(self.md) == 0 or len(self.nmd) == 0:
            return None
        else:
            mm = ((self.md ** self.qrung).sum()) / len(self.md)
            nn = ((self.nmd ** self.qrung).sum()) / len(self.nmd)
            return mm + nn

    def indeterminacy(self):
        if len(self.md) == 0 or len(self.nmd) == 0:
            return None
        else:
            mm = ((self.md ** self.qrung).sum()) / len(self.md)
            nn = ((self.nmd ** self.qrung).sum()) / len(self.nmd)
            if mm + nn == 1.:
                return np.round(0., 6)
            else:
                return (1. - mm - nn) ** (1. / self.qrung)

    def complement(self):
        newfn = copy.deepcopy(self)
        if len(self.md) == 0 and len(self.nmd) != 0:
            newfn.md = np.array([])
            newfn.nmd = 1. - np.array(self.nmd)
        elif len(self.md) != 0 and len(self.nmd) == 0:
            newfn.md = 1. - np.array(self.md)
            newfn.nmd = np.array([])
        else:
            newfn.md = self.nmd
            newfn.nmd = self.md
        return newfn

    def initialize(self):
        if isinstance(self.md, (list, np.ndarray)) and isinstance(self.nmd, (list, np.ndarray)):
            mds = np.asarray(self.md)
            nmds = np.asarray(self.nmd)
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
                assert 0 <= np.max(mds) ** self.qrung + np.max(nmds) ** self.qrung <= 1, 'ERROR'

            mtype = 'qrohfn'
            memDegree = np.round(self.md, 6)
            nonMemDegree = np.round(self.nmd, 6)

            return mtype, memDegree, nonMemDegree
        else:
            raise TypeError(f'Unsupported data type or type error, md:{type(self.md)} and nmd:{type(self.nmd)}.')

    def validity(self):
        a1 = self.md.size == 0 and self.nmd.size == 0
        a2 = self.md.size == 0 and 0. <= self.nmd.all() <= 1.
        a3 = self.nmd.size == 0 and 0. <= self.md.all() <= 1.
        a4 = min(self.md) >= 0. and min(self.nmd) >= 0. and max(self.md) ** self.qrung + max(
            self.nmd) ** self.qrung <= 1.
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

    def empty(self):
        if self.md.size == 0 and self.nmd.size == 0:
            return True
        else:
            return False

    def convert(self):
        return self.md.tolist(), self.nmd.tolist()

    def qsort(self, ascending):
        newfn = copy.deepcopy(self)
        if ascending:
            newfn.md = np.sort(self.md)
            newfn.nmd = np.sort(self.nmd)
        else:
            newfn.md = np.abs(np.sort(-self.md))
            newfn.nmd = np.abs(np.sort(-self.nmd))
        return newfn

    def unique(self):
        t = copy.deepcopy(self)
        t.md = np.unique(self.md)
        t.nmd = np.unique(self.nmd)
        return t

    @staticmethod
    def normalize(d1, d2, tao):
        def __adj(d, tm):
            return tm * d.max() + (1. - tm) * d.min()

        d_1 = copy.deepcopy(d1)
        d_2 = copy.deepcopy(d2)

        md_len = len(d_1.md) - len(d_2.md)
        nmd_len = len(d_1.nmd) - len(d_2.nmd)

        if md_len > 0:
            # Explain that the number of membership elements in d1 is greater than d2,
            # and it is necessary to add elements of d2 membership.
            i = 0.
            m = d_2.md
            while i < md_len:
                d_2.md = np.append(d_2.md, __adj(m, tao))
                i += 1
        else:
            # Explain that the number of membership elements in d1 is less than d2,
            # and it is necessary to increase the elements of d1 membership.
            i = 0.
            m = d_1.md
            while i < (-md_len):
                d_1.md = np.append(d_1.md, __adj(m, tao))
                i += 1

        if nmd_len > 0:
            # Explain that the number of membership elements in d1 is greater than d2,
            # and it is necessary to add elements of d2 membership.
            i = 0.
            u = d_2.nmd
            while i < nmd_len:
                d_2.nmd = np.append(d_2.nmd, __adj(u, tao))
                i += 1
        else:
            i = 0.
            u = d_1.nmd
            while i < (-nmd_len):
                d_1.nmd = np.append(d_1.nmd, __adj(u, tao))
                i += 1
        return d_1.qsort(), d_2.qsort()
