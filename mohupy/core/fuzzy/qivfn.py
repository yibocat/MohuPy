#  Copyright (c) yibocat 2025 All Rights Reserved
#  Python: 3.10.9
#  Date: 2025/7/8 18:25
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import copy

import numpy as np

from .template import Template
from .base import fuzz_directory


@fuzz_directory('qivfn')
class qIVFN(Template):

    mtype = 'qivfn'

    def __init__(self, qrung=None, md=None, nmd=None):
        super().__init__(qrung, md, nmd)
        self.qrung = qrung
        self.md = md
        self.nmd = nmd

    def report(self):
        return f'<{np.round(self.md, 4)},{np.round(self.nmd, 4)}>'

    def str(self):
        return f'<{np.round(self.md, 4)},{np.round(self.nmd, 4)}>'

    def score(self):
        m = self.md[0] ** self.qrung + self.md[1] ** self.qrung
        n = self.nmd[0] ** self.qrung + self.nmd[1] ** self.qrung
        return (m - n) / 2

    def accuracy(self):
        m = self.md[0] ** self.qrung + self.md[1] ** self.qrung
        n = self.nmd[0] ** self.qrung + self.nmd[1] ** self.qrung
        return (m + n) / 2

    def indeterminacy(self):
        m = self.md[0] ** self.qrung + self.md[1] ** self.qrung
        n = self.nmd[0] ** self.qrung + self.nmd[1] ** self.qrung
        if m + n:
            return np.round(0., 6)
        else:
            return (1. - (m + n) / 2) ** (1. / self.qrung)

    def complement(self):
        newf = copy.deepcopy(self)
        newf.md = self.nmd
        newf.nmd = self.md
        return newf

    def initialize(self):
        if isinstance(self.md, tuple) and isinstance(self.nmd, tuple):
            assert len(self.md) == 2 and len(self.nmd) == 2, \
                'ERROR: The data format contains at least upper and lower bounds.'
            assert self.md[0] <= self.md[1] and self.nmd[0] <= self.nmd[1], \
                'ERROR: The upper of membership and non-membership must be greater than the lower.'
            assert 0. <= self.md[0] <= 1. and 0. <= self.md[1] <= 1., \
                'ERROR: The upper and lower of membership degree must be between 0 and 1.'
            assert 0. <= self.nmd[0] <= 1. and 0. <= self.nmd[1] <= 1., \
                'ERROR: The upper and lower of non-membership degree must be between 0 and 1.'
            assert 0. <= self.md[0] ** self.qrung + self.nmd[0] ** self.qrung <= 1. and 0. <= self.md[1] ** self.qrung + self.nmd[1] ** self.qrung <= 1., \
                'ERROR: The q powers sum of membership degree and non-membership degree must be between 0 and 1.'

            mtype = 'qivfn'
            memDegree = np.round(self.md, 6)
            nonMemDegree = np.round(self.nmd, 6)

            return mtype, memDegree, nonMemDegree
        else:
            raise TypeError(f'Unsupported data type or type error, md:{type(self.md)} and nmd:{type(self.nmd)}.')

    def validity(self):
        if not len(self.md) == 2 and len(self.nmd) == 2:
            return False
        elif not 0. <= np.all(self.md) <= 1. and 0. <= np.all(self.md) <= 1.:
            return False
        elif not (self.md[0] <= self.md[1] and self.nmd[0] <= self.nmd[1]):
            return False
        elif not 0. <= self.md[1] ** self.qrung + self.nmd[1] ** self.qrung <= 1.:
            return False
        else:
            return True

    def empty(self):
        if self.md is None and self.nmd is None:
            return True
        else:
            return False

    def convert(self):
        return self.md.tolist(), self.nmd.tolist()

    def qsort(self):
        return self

    def unique(self):
        return self

    def normalize(self):
        return self

