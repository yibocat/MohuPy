#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/11/27 下午7:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

# from ..regedit.algebraic_operation import (algebAdd, algebSub,
#                                            algebMul, algebDiv,
#                                            algebPow, algebTim)

from ..regedit import archimedeanDict
from ..config import Norms


class BasicOperation:

    def __init__(self, qrung, mtype):
        self.qrung = qrung
        self.mtype = mtype

    def add(self, x, y):
        from .nums import Fuzznum
        newfn = Fuzznum()
        newfn.mtype = self.mtype
        newfn.qrung = self.qrung
        newfn.md = archimedeanDict[Norms.arch]['add'][self.mtype](x.md, x.nmd, y.md, y.nmd, self.qrung)[0]
        newfn.nmd = archimedeanDict[Norms.arch]['add'][self.mtype](x.md, x.nmd, y.md, y.nmd, self.qrung)[1]
        return newfn

    def sub(self, x, y):
        from .nums import Fuzznum
        newfn = Fuzznum()
        newfn.mtype = self.mtype
        newfn.qrung = self.qrung
        newfn.md = archimedeanDict[Norms.arch]['sub'][self.mtype](x.md, x.nmd, y.md, y.nmd, self.qrung)[0]
        newfn.nmd = archimedeanDict[Norms.arch]['sub'][self.mtype](x.md, x.nmd, y.md, y.nmd, self.qrung)[1]
        return newfn

    def mul(self, x, y):
        from .nums import Fuzznum
        newfn = Fuzznum()
        newfn.mtype = self.mtype
        newfn.qrung = self.qrung
        newfn.md = archimedeanDict[Norms.arch]['mul'][self.mtype](x.md, x.nmd, y.md, y.nmd, self.qrung)[0]
        newfn.nmd = archimedeanDict[Norms.arch]['mul'][self.mtype](x.md, x.nmd, y.md, y.nmd, self.qrung)[1]
        return newfn

    def div(self, x, y):
        from .nums import Fuzznum
        newfn = Fuzznum()
        newfn.mtype = self.mtype
        newfn.qrung = self.qrung
        newfn.md = archimedeanDict[Norms.arch]['div'][self.mtype](x.md, x.nmd, y.md, y.nmd, self.qrung)[0]
        newfn.nmd = archimedeanDict[Norms.arch]['div'][self.mtype](x.md, x.nmd, y.md, y.nmd, self.qrung)[1]
        return newfn

    def power(self, l, x):
        from .nums import Fuzznum
        newfn = Fuzznum()
        newfn.mtype = self.mtype
        newfn.qrung = self.qrung
        newfn.md = archimedeanDict[Norms.arch]['pow'][self.mtype](l, x.md, x.nmd, self.qrung)[0]
        newfn.nmd = archimedeanDict[Norms.arch]['pow'][self.mtype](l, x.md, x.nmd, self.qrung)[1]
        return newfn

    def times(self, l, x):
        from .nums import Fuzznum
        newfn = Fuzznum()
        newfn.mtype = self.mtype
        newfn.qrung = self.qrung
        newfn.md = archimedeanDict[Norms.arch]['tim'][self.mtype](l, x.md, x.nmd, self.qrung)[0]
        newfn.nmd = archimedeanDict[Norms.arch]['tim'][self.mtype](l, x.md, x.nmd, self.qrung)[1]
        return newfn

