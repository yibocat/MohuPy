#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/1 下午5:37
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzyKit

import copy


class Fuzzynum(object):
    qrung = None
    md = None
    nmd = None

    def __init__(self):
        pass

    @property
    def score(self):
        return self.md ** self.qrung - self.nmd ** self.qrung

    @property
    def accuracy(self):
        return self.md ** self.qrung + self.nmd ** self.qrung

    @property
    def indeterminacy(self):
        return (1 - self.accuracy) ** (1 / self.qrung)

    def isEmpty(self):
        if self.md is None and self.nmd is None:
            return True
        else:
            return False

    def isEmpty_half(self):
        if self.md is None or self.nmd is None:
            return True
        else:
            return False

    def complement(self):
        newFN = copy.deepcopy(self)
        newFN.md = self.nmd
        newFN.nmd = self.md
        return newFN

    def algebraicPower(self, l):
        newFN = copy.deepcopy(self)
        newFN.md = self.md ** l
        newFN.nmd = (1 - (1 - self.nmd ** self.qrung) ** l) ** (1 / self.qrung)
        return newFN

    def algebraicTimes(self, l):
        newFN = copy.deepcopy(self)
        newFN.md = (1 - (1 - self.md ** self.qrung) ** l) ** (1 / self.qrung)
        newFN.nmd = self.nmd ** l
        return newFN

    def einsteinPower(self, l):
        newFn = copy.deepcopy(self)
        newFn.md = ((2 * (self.md ** self.qrung) ** l) / (
                    (2 - self.md ** self.qrung) ** l + (self.md ** self.qrung) ** l)) ** (1 / self.qrung)
        newFn.nmd = (((1 + self.nmd ** self.qrung) ** l - (1 - self.nmd ** self.qrung) ** l) / (
                    (1 + self.nmd ** self.qrung) ** l + (1 - self.nmd ** self.qrung) ** l)) ** (1 / self.qrung)
        return newFn

    def einsteinTimes(self, l):
        newFn = copy.deepcopy(self)
        newFn.md = (((1 + self.md ** self.qrung) ** l - (1 - self.md ** self.qrung) ** l) / (
                    (1 + self.md ** self.qrung) ** l + (1 - self.md ** self.qrung) ** l)) ** (1 / self.qrung)
        newFn.nmd = ((2 * (self.nmd ** self.qrung) ** l) / (
                    (2 - self.nmd ** self.qrung) ** l + (self.nmd ** self.qrung) ** l)) ** (1 / self.qrung)
        return newFn
