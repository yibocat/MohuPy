#  Copyright (c) yibocat 2025 All Rights Reserved
#  Python: 3.10.9
#  Date: 2025/7/8 15:48
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import copy

import numpy as np

from .template import Template
from .base import fuzz_directory


@fuzz_directory('qrofn')
class qROFN(Template):

    mtype = 'qrofn'

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
        return self.md ** self.qrung - self.nmd ** self.qrung

    def accuracy(self):
        return self.md ** self.qrung + self.nmd ** self.qrung

    def indeterminacy(self):
        acc = self.md ** self.qrung + self.nmd ** self.qrung
        if acc == np.round(1., 6):
            return np.round(0., 6)
        else:
            return (1. - acc) ** (1. / self.qrung)

    def complement(self):
        newf = copy.deepcopy(self)
        newf.md = self.nmd
        newf.nmd = self.md
        return newf

    """
        模糊方法函数库
    """
    def initialize(self):
        if isinstance(self.md, (float, int, np.int_, np.float64)) and \
                isinstance(self.nmd, (float, int, np.int_, np.float64)):
            assert 0. <= self.md <= 1. and 0. <= self.nmd <= 1., \
                'ERROR: md and nmd must be betweenZERO and ONE'
            assert 0. <= self.md ** self.qrung + self.nmd ** self.qrung <= 1., \
                'ERROR: md ** qrung + nmd ** qrung must be between ZERO and ONE.'

            mtype = 'qrofn'
            memDegree = np.round(self.md, 6)
            nonMemDegree = np.round(self.nmd, 6)

            return mtype, memDegree, nonMemDegree
        else:
            raise TypeError(f'Unsupported data type or type error, md:{type(self.md)} and nmd:{type(self.nmd)}.')

    def validity(self):
        if 0. <= self.md <= 1. and 0. <= self.nmd <= 1. \
                and 0. <= self.md ** self.qrung + self.nmd ** self.qrung <= 1.:
            return True
        else:
            return False

    def empty(self):
        if self.md is None and self.nmd is None:
            return True
        else:
            return False

    def convert(self):
        return self.md, self.nmd

    def qsort(self):
        return self

    def unique(self):
        return self

    def normalize(self):
        return self

