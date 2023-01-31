import numpy as np
import copy


class DhFuzzy(object):
    # noinspection PyUnresolvedReferences
    """
        DhFuzzy is a class to represent the dual hesitant fuzzy sets model.

        Attributes
        ----------
            md : numpy.ndarray, shape = (n_numbers), indicates the number of membership degrees
            nmd : numpy.ndarray, shape = (n_numbers), indicates the number of non-membership degrees
            qrung : numpy.ndarray, shape = (n_numbers), indicates the Q rung of the elements

        Function
        ----------
            __init__(self, md, nmd): Initializes a dual hesitant fuzzy element

            isEmpty(self) : bool, judging that a dual hesitant fuzzy element is empty
            isEmpty_half(self) : bool, judging whether the membership degree or non-membership degree of
                a dual hesitant fuzzy element is empty

            complement(self) : DhFuzzy, complement set of the dual hesitated fuzzy element

            qSort(self, rev) : DhFuzzy, Sort the dual hesitated fuzzy element
                rev: : bool, indicate whether the sort is in reverse

            algebraicPower(self,l) : Algebraic power operation, l indicates the operation parameter
            algebraicTimes(self,l) : Algebraic times operation, l indicates the operation parameter
            einsteinPower(self,l) : Einstein power operation, l indicates the operation parameter
            einsteinTimes(self,l) : Einstein times operation, l indicates the operation parameter

        """
    md = None
    nmd = None
    qrung = None

    def __init__(self):
        pass

    @property
    def score(self):
        return ((self.md ** self.qrung).sum()) / len(self.md) - ((self.nmd ** self.qrung).sum()) / len(self.nmd)

    def isEmpty(self):
        ## 判断隶属度和非隶属度是否为空
        if self.md.size == 0 and self.nmd.size == 0:
            return True
        else:
            return False

    def isEmpty_half(self):
        ## 判断隶属度和非隶属度是否有空
        if self.md.size == 0 or self.nmd.size == 0:
            return True
        else:
            return False

    def complement(self):
        newEle = copy.copy(self)
        if self.md.size == 0 and self.nmd.size != 0:
            newEle.md = np.array([])
            newEle.nmd = 1 - self.nmd
        elif self.md.size != 0 and self.nmd.size == 0:
            newEle.nmd = np.array([])
            newEle.md = 1 - self.md
        else:
            newEle.md = self.nmd
            newEle.nmd = self.md
        return newEle

    def qSort(self, rev=True):
        newEle = copy.copy(self)
        if rev:
            newEle.md = np.sort(self.md)
            newEle.nmd = np.sort(self.nmd)
        else:
            newEle.md = np.abs(np.sort(-self.md))
            newEle.nmd = np.abs(np.sort(-self.nmd))
        return newEle

    def algebraicPower(self, l):
        newEle = copy.copy(self)
        newEle.md = self.md ** l
        newEle.nmd = (1 - (1 - self.nmd ** self.qrung) ** l) ** (1 / self.qrung)
        return newEle

    def algebraicTimes(self, l):
        newEle = copy.copy(self)
        newEle.md = (1 - (1 - self.md ** self.qrung) ** l) ** (1 / self.qrung)
        newEle.nmd = self.nmd ** l
        return newEle

    def einsteinPower(self, l):
        newEle = copy.copy(self)
        newEle.md = ((2 * (self.md ** self.qrung) ** l) / (
                (2 - self.md ** self.qrung) ** l + (self.md ** self.qrung) ** l)) ** (1 / self.qrung)
        newEle.nmd = (((1 + self.nmd ** self.qrung) ** l - (1 - self.nmd ** self.qrung) ** l) /
                      ((1 + self.nmd ** self.qrung) ** l + (1 - self.nmd ** self.qrung) ** l)) ** (1 / self.qrung)
        return newEle

    def einsteinTimes(self, l):
        newEle = copy.copy(self)
        newEle.md = (((1 + self.md ** self.qrung) ** l - (1 - self.md ** self.qrung) ** l) /
                     ((1 + self.md ** self.qrung) ** l + (1 - self.md ** self.qrung) ** l)) ** (1 / self.qrung)
        newEle.nmd = ((2 * (self.nmd ** self.qrung) ** l) / (
                (2 - self.nmd ** self.qrung) ** l + (self.nmd ** self.qrung) ** l)) ** (1 / self.qrung)
        return newEle
