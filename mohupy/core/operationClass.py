#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/6 下午2:55
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from .operationLib import archimedeanDict


class BasicOperation:
    norms = 'algebraic'

    def __init__(self, qrung, mtype):
        self.qrung = qrung
        self.mtype = mtype

    def add(self, x, y):
        from .fuzznums import Fuzznum
        newfn = Fuzznum()
        newfn.mtype = self.mtype
        newfn.qrung = self.qrung
        newfn.md = archimedeanDict[self.norms]['add'][self.mtype](x.md, x.nmd, y.md, y.nmd, self.qrung)[0]
        newfn.nmd = archimedeanDict[self.norms]['add'][self.mtype](x.md, x.nmd, y.md, y.nmd, self.qrung)[1]
        return newfn

    def sub(self, x, y):
        from .fuzznums import Fuzznum
        newfn = Fuzznum()
        newfn.mtype = self.mtype
        newfn.qrung = self.qrung
        newfn.md = archimedeanDict[self.norms]['sub'][self.mtype](x.md, x.nmd, y.md, y.nmd, self.qrung)[0]
        newfn.nmd = archimedeanDict[self.norms]['sub'][self.mtype](x.md, x.nmd, y.md, y.nmd, self.qrung)[1]
        return newfn

    def mul(self, x, y):
        from .fuzznums import Fuzznum
        newfn = Fuzznum()
        newfn.mtype = self.mtype
        newfn.qrung = self.qrung
        newfn.md = archimedeanDict[self.norms]['mul'][self.mtype](x.md, x.nmd, y.md, y.nmd, self.qrung)[0]
        newfn.nmd = archimedeanDict[self.norms]['mul'][self.mtype](x.md, x.nmd, y.md, y.nmd, self.qrung)[1]
        return newfn

    def div(self, x, y):
        from .fuzznums import Fuzznum
        newfn = Fuzznum()
        newfn.mtype = self.mtype
        newfn.qrung = self.qrung
        newfn.md = archimedeanDict[self.norms]['div'][self.mtype](x.md, x.nmd, y.md, y.nmd, self.qrung)[0]
        newfn.nmd = archimedeanDict[self.norms]['div'][self.mtype](x.md, x.nmd, y.md, y.nmd, self.qrung)[1]
        return newfn

    def power(self, l, x):
        from .fuzznums import Fuzznum
        newfn = Fuzznum()
        newfn.mtype = self.mtype
        newfn.qrung = self.qrung
        newfn.md = archimedeanDict[self.norms]['pow'][self.mtype](l, x.md, x.nmd, self.qrung)[0]
        newfn.nmd = archimedeanDict[self.norms]['pow'][self.mtype](l, x.md, x.nmd, self.qrung)[1]
        return newfn

    def times(self, l, x):
        from .fuzznums import Fuzznum
        newfn = Fuzznum()
        newfn.mtype = self.mtype
        newfn.qrung = self.qrung
        newfn.md = archimedeanDict[self.norms]['tim'][self.mtype](l, x.md, x.nmd, self.qrung)[0]
        newfn.nmd = archimedeanDict[self.norms]['tim'][self.mtype](l, x.md, x.nmd, self.qrung)[1]
        return newfn
