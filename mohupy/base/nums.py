#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/11/26 下午3:05
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
from typing import Union

from .base import mohunum
from .attributes import score, acc, ind, comp
from .function import initializeNum, transpose


class Fuzznum(mohunum):
    qrung = None
    mtype = None
    md = None
    nmd = None

    def __init__(self, qrung=None, md=None, nmd=None):
        self.ndim = 0
        self.size = 1
        self.shape = ()

        if qrung is not None and md is not None and nmd is not None:
            self.qrung = qrung
            self.mtype, self.md, self.nmd = initializeNum(qrung, md, nmd)

        self.init()

    def init(self):
        if self.qrung is not None and self.mtype is not None and self.md is not None and self.nmd is not None:
            self.score = score(self)
            self.acc = acc(self)
            self.ind = ind(self)
            self.comp = comp(self)
        else:
            self.score = None
            self.acc = None
            self.ind = None
            self.comp = None

    @property
    def T(self):
        return transpose(self)
