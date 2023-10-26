#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/10/26 下午12:21
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from .__algebraic import (algebAdd, algebSub, algebMul, algebDiv, algebPow, algebTim)


class Algebraic:

    def __init__(self, qrung, mtype):
        self.qrung = qrung
        self.mtype = mtype

    def add(self, x, y):
        from .mohu import fuzzType
        newfn = fuzzType[self.mtype]()
        newfn.mtype = self.mtype
        newfn.qrung = self.qrung
        newfn.md = algebAdd[self.mtype](x.md, x.nmd, y.md, y.nmd, self.qrung)[0]
        newfn.nmd = algebAdd[self.mtype](x.md, x.nmd, y.md, y.nmd, self.qrung)[1]
        return newfn

    def sub(self, x, y):
        from .mohu import fuzzType
        newfn = fuzzType[self.mtype]()
        newfn.mtype = self.mtype
        newfn.qrung = self.qrung
        newfn.md = algebSub[self.mtype](x.md, x.nmd, y.md, y.nmd, self.qrung)[0]
        newfn.nmd = algebSub[self.mtype](x.md, x.nmd, y.md, y.nmd, self.qrung)[1]
        return newfn

    def mul(self, x, y):
        from .mohu import fuzzType
        newfn = fuzzType[self.mtype]()
        newfn.mtype = self.mtype
        newfn.qrung = self.qrung
        newfn.md = algebMul[self.mtype](x.md, x.nmd, y.md, y.nmd, self.qrung)[0]
        newfn.nmd = algebMul[self.mtype](x.md, x.nmd, y.md, y.nmd, self.qrung)[1]
        return newfn

    def div(self, x, y):
        from .mohu import fuzzType
        newfn = fuzzType[self.mtype]()
        newfn.mtype = self.mtype
        newfn.qrung = self.qrung
        newfn.md = algebDiv[self.mtype](x.md, x.nmd, y.md, y.nmd, self.qrung)[0]
        newfn.nmd = algebDiv[self.mtype](x.md, x.nmd, y.md, y.nmd, self.qrung)[1]
        return newfn

    def power(self, l, x):
        from .mohu import fuzzType
        newfn = fuzzType[self.mtype]()
        newfn.mtype = self.mtype
        newfn.qrung = self.qrung
        newfn.md = algebPow[self.mtype](l, x.md, x.nmd, self.qrung)[0]
        newfn.nmd = algebPow[self.mtype](l, x.md, x.nmd, self.qrung)[1]
        return newfn

    def times(self, l, x):
        from .mohu import fuzzType
        newfn = fuzzType[self.mtype]()
        newfn.mtype = self.mtype
        newfn.qrung = self.qrung
        newfn.md = algebTim[self.mtype](l, x.md, x.nmd, self.qrung)[0]
        newfn.nmd = algebTim[self.mtype](l, x.md, x.nmd, self.qrung)[1]
        return newfn


class Einstein:

    def __init__(self, mtype):
        self.mtype = mtype

    def add(self): pass

    def sub(self): pass

    def mul(self): pass

    def div(self): pass

    def power(self): pass

    def times(self): pass
