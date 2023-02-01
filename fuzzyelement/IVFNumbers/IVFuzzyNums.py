#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/1 下午5:37
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzyKit

import copy
from .archimedean import *


class IVFuzzynum(object):
    qrung = None
    md = None
    nmd = None

    def __init__(self):
        pass

    @property
    def score(self):
        md = self.md[0] ** self.qrung + self.md[1] ** self.qrung
        nmd = self.nmd[0] ** self.qrung + self.nmd[1] ** self.qrung
        return (md - nmd) / 2

    def isEmpty(self):
        if not (self.md[0] and self.md[1] and self.nmd[0] and self.nmd[1]):
            return True
        else:
            return False

    def isEmpty_half(self):
        if not (self.md[0] or self.md[1] or self.nmd[0] or self.nmd[1]):
            return True
        else:
            return False

    def complement(self):
        pass

    def algebraicPower(self, l):
        newIVFN = copy.deepcopy(self)
        newIVFN.md[0] = in_algebraic_tau(l * algebraic_tau(self.md[0] ** self.qrung)) ** (1 / self.qrung)
        newIVFN.md[1] = in_algebraic_tau(l * algebraic_tau(self.md[1] ** self.qrung)) ** (1 / self.qrung)
        newIVFN.nmd[0] = in_algebraic_s(l * algebraic_s(self.nmd[0] ** self.qrung)) ** (1 / self.qrung)
        newIVFN.nmd[1] = in_algebraic_s(l * algebraic_s(self.nmd[1] ** self.qrung)) ** (1 / self.qrung)
        return newIVFN

    def algebraicTimes(self, l):
        newIVFN = copy.deepcopy(self)
        newIVFN.md[0] = in_algebraic_s(l * algebraic_s(self.md[0] ** self.qrung)) ** (1 / self.qrung)
        newIVFN.md[1] = in_algebraic_s(l * algebraic_s(self.md[1] ** self.qrung)) ** (1 / self.qrung)
        newIVFN.nmd[0] = in_algebraic_tau(l * algebraic_tau(self.nmd[0] ** self.qrung)) ** (1 / self.qrung)
        newIVFN.nmd[1] = in_algebraic_tau(l * algebraic_tau(self.nmd[1] ** self.qrung)) ** (1 / self.qrung)
        return newIVFN

    def einsteinPower(self, l):
        newIVFN = copy.deepcopy(self)
        newIVFN.md[0] = in_einstein_tau(l * einstein_tau(self.md[0] ** self.qrung)) ** (1 / self.qrung)
        newIVFN.md[1] = in_einstein_tau(l * einstein_tau(self.md[1] ** self.qrung)) ** (1 / self.qrung)
        newIVFN.nmd[0] = in_einstein_s(l * einstein_s(self.nmd[0] ** self.qrung)) ** (1 / self.qrung)
        newIVFN.nmd[1] = in_einstein_s(l * einstein_s(self.nmd[1] ** self.qrung)) ** (1 / self.qrung)
        return newIVFN

    def einsteinTimes(self, l):
        newIVFN = copy.deepcopy(self)
        newIVFN.md[0] = in_einstein_s(l * einstein_s(self.md[0] ** self.qrung)) ** (1 / self.qrung)
        newIVFN.md[1] = in_einstein_s(l * einstein_s(self.md[1] ** self.qrung)) ** (1 / self.qrung)
        newIVFN.nmd[0] = in_einstein_tau(l * einstein_tau(self.nmd[0] ** self.qrung)) ** (1/self.qrung)
        newIVFN.nmd[1] = in_einstein_tau(l * einstein_tau(self.nmd[1] ** self.qrung)) ** (1/self.qrung)
        return newIVFN
