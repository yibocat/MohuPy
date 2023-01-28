import copy
from .archimedean import *


class IVFuzzynum(object):
    qrung = None
    mdl = None
    mdu = None
    nmdl = None
    nmdu = None

    def __init__(self):
        pass

    def score(self):
        md = self.mdl ** self.qrung + self.mdu ** self.qrung
        nmd = self.nmdl ** self.qrung + self.nmdu ** self.qrung
        return (md - nmd) / 2

    def isEmpty(self):
        if not (self.mdl and self.mdu and self.nmdl and self.nmdu):
            return True
        else:
            return False

    def isEmpty_half(self):
        if not (self.mdl or self.mdu or self.nmdl or self.nmdu):
            return True
        else:
            return False

    def complement(self):
        pass

    def algebraicPower(self, l):
        newIVFN = copy.copy(self)
        newIVFN.mdl = in_algebraic_tau(l * algebraic_tau(self.mdl ** self.qrung)) ** (1 / self.qrung)
        newIVFN.mdu = in_algebraic_tau(l * algebraic_tau(self.mdu ** self.qrung)) ** (1 / self.qrung)
        newIVFN.nmdl = in_algebraic_s(l * algebraic_s(self.nmdl ** self.qrung)) ** (1 / self.qrung)
        newIVFN.nmdu = in_algebraic_s(l * algebraic_s(self.nmdu ** self.qrung)) ** (1 / self.qrung)
        return newIVFN

    def algebraicTimes(self,l):
        newIVFN = copy.copy(self)
        newIVFN.mdl = in_algebraic_s(l*algebraic_s(self.mdl ** self.qrung))**(1/self.qrung)
        newIVFN.mdu = in_algebraic_s(l*algebraic_s(self.mdu ** self.qrung))**(1/self.qrung)
        newIVFN.nmdl = in_algebraic_tau(l*algebraic_tau(self.nmdl**self.qrung))**(1/self.qrung)
        newIVFN.nmdu = in_algebraic_tau(l*algebraic_tau(self.nmdu**self.qrung))**(1/self.qrung)
        return newIVFN

    def einsteinPower(self,l):
        newIVFN = copy.copy(self)
        newIVFN.mdl = in_einstein_tau(l*einstein_tau(self.mdl**self.qrung)) ** (1 / self.qrung)
        newIVFN.mdu = in_einstein_tau(l*einstein_tau(self.mdu**self.qrung)) ** (1 / self.qrung)
        newIVFN.nmdl = in_einstein_s(l*einstein_s(self.nmdl**self.qrung))**(1/self.qrung)
        newIVFN.nmdu = in_einstein_s(l*einstein_s(self.nmdu**self.qrung))**(1/self.qrung)
        return newIVFN

    



























