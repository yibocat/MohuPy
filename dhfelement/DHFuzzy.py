import numpy as np
import copy


class DhFuzzy(object):
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

    def __init__(self, md, nmd):
        self.md = md
        self.nmd = nmd

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


class HQrungF(DhFuzzy):
    """
    HQrungF is a class representing the Q-Rung hesitant fuzzy sets model. It is inherited from the DHFuzzy class.

    Attributes
    ----------
        md : numpy.ndarray, shape = (n_numbers), indicates the number of membership degrees
        nmd : numpy.ndarray, shape = (n_numbers), indicates the number of non-membership degrees
        qrung : numpy.ndarray, shape = (n_numbers), indicates the Q rung of the elements

    Function
    ---------
        __init__(self, md, nmd): Initializes a Q-Rung dual hesitant fuzzy element
        __repr__(self): Returns a string representation of the Q-Rung dual hesitant fuzzy element
    """
    def __init__(self, qrung, md, nmd):
        md = np.asarray(md)
        nmd = np.asarray(nmd)
        self.qrung = qrung
        assert (md.size == 0 or nmd.size == 0) or (
                max(md) <= 1 and max(nmd) <= 1 and min(md) >= 0 and min(nmd) >= 0) and (
                       0 <= max(md) ** self.qrung + max(nmd) ** self.qrung <= 1), \
            "ERROR:Construction failed! max(MD)^q+max(NMD)^q and min(MD)^q+min(NMD)^q must be in interval[0,1]!"
        DhFuzzy.__init__(self, md, nmd)

    def __repr__(self):
        if len(self.md) > 50 or len(self.nmd) > 50:
            return 'HQrungF(Q=%d)[%d,%d]:{' % (self.qrung, len(self.md), len(self.nmd)) + \
                '\n md :' + str(np.round(self.md, 4)[:50]) + \
                ',\n nmd:' + str(np.round(self.nmd, 4)[:50]) + ' }\n'
        else:
            return 'HQrungF(Q=%d)[%d,%d]:{' % (self.qrung, len(self.md), len(self.nmd)) + \
                '\n md :' + str(np.round(self.md, 4)) + \
                ',\n nmd:' + str(np.round(self.nmd, 4)) + ' }\n'


# class HIntuiF(_DhFuzzy):
#     qrung = 1
#
#     def __init__(self, md, nmd):
#         md = np.asarray(md)
#         nmd = np.asarray(nmd)
#         assert (md.size == 0 or nmd.size == 0) or (
#                 max(md) <= 1 and max(nmd) <= 1 and min(md) >= 0 and min(nmd) >= 0) and (
#                        0 <= max(md) ** self.qrung + max(nmd) ** self.qrung <= 1), \
#             "ERROR:Construction failed! max(MD)+max(NMD) and min(MD)+min(NMD) must be in interval[0,1]!"
#         _DhFuzzy.__init__(self, md, nmd)
#
#     def __repr__(self):
#         if len(self.md) > 50 or len(self.nmd) > 50:
#             return 'DHFE(%d,%d):{' % (len(self.md), len(self.nmd)) + \
#                 '\n md :' + str(np.round(self.md, 4)[:50]) + \
#                 ',\n nmd:' + str(np.round(self.nmd, 4)[:50]) + ' }\n'
#         else:
#             return 'DHFE(%d,%d):{' % (len(self.md), len(self.nmd)) + \
#                 '\n md :' + str(np.round(self.md, 4)) + \
#                 ',\n nmd:' + str(np.round(self.nmd, 4)) + ' }\n'
#
#
# class HPythF(_DhFuzzy):
#     qrung = 2
#
#     def __init__(self, md, nmd):
#         md = np.asarray(md)
#         nmd = np.asarray(nmd)
#         assert (md.size == 0 or nmd.size == 0) or (
#                 max(md) <= 1 and max(nmd) <= 1 and min(md) >= 0 and min(nmd) >= 0) and (
#                        0 <= max(md) ** self.qrung + max(nmd) ** self.qrung <= 1), \
#             "ERROR:Construction failed! max(MD)^2+max(NMD)^2 and min(MD)^2+min(NMD)^2 must be in interval[0,1]!"
#         _DhFuzzy.__init__(self, md, nmd)
#
#     def __repr__(self):
#         if len(self.md) > 50 or len(self.nmd) > 50:
#             return 'HPFE(%d,%d):{' % (len(self.md), len(self.nmd)) + \
#                 '\n md :' + str(np.round(self.md, 4)[:50]) + \
#                 ',\n nmd:' + str(np.round(self.nmd, 4)[:50]) + ' }\n'
#         else:
#             return 'HPFE(%d,%d):{' % (len(self.md), len(self.nmd)) + \
#                 '\n md :' + str(np.round(self.md, 4)) + \
#                 ',\n nmd:' + str(np.round(self.nmd, 4)) + ' }\n'
#
#
# class HFermatF(_DhFuzzy):
#     qrung = 3
#
#     def __init__(self, md, nmd):
#         md = np.asarray(md)
#         nmd = np.asarray(nmd)
#         assert (md.size == 0 or nmd.size == 0) or (
#                 max(md) <= 1 and max(nmd) <= 1 and min(md) >= 0 and min(nmd) >= 0) and (
#                        0 <= max(md) ** self.qrung + max(nmd) ** self.qrung <= 1), \
#             "ERROR:Construction failed! max(MD)^3+max(NMD)^3 and min(MD)^3+min(NMD)^3 must be in interval[0,1]!"
#         _DhFuzzy.__init__(self, md, nmd)
#
#     def __repr__(self):
#         if len(self.md) > 50 or len(self.nmd) > 50:
#             return 'HFFE(%d,%d):{' % (len(self.md), len(self.nmd)) + \
#                 '\n md :' + str(np.round(self.md, 4)[:50]) + \
#                 ',\n nmd:' + str(np.round(self.nmd, 4)[:50]) + ' }\n'
#         else:
#             return 'HFFE(%d,%d):{' % (len(self.md), len(self.nmd)) + \
#                 '\n md :' + str(np.round(self.md, 4)) + \
#                 ',\n nmd:' + str(np.round(self.nmd, 4)) + ' }\n'
