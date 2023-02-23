#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/21 上午4:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets

import copy
from ..Fuzzynum cimport Fuzzynum

import numpy as np
cimport numpy as np

cdef class qrungdhfe(Fuzzynum):
    cdef int __qrung
    cdef str __parent
    cdef double __score
    cdef double __accuracy
    cdef double __indeterminacy
    cdef np.ndarray __md
    cdef np.ndarray __nmd

    def __init__(self, int qrung, md, nmd):
        super().__init__()

        mds = np.asarray(md)
        nmds = np.asarray(nmd)

        if mds.size == 0 and nmds.size == 0:
            pass
        elif mds.size == 0:
            assert 0 <= nmds.all() <= 1, 'ERROR: Invalid data.'
        elif nmds.size == 0:
            assert 0 <= mds.all() <= 1, 'ERROR: Invalid data.'
        else:
            assert ( min(mds) >= 0 and min(nmds) >= 0) and (0 <= max(mds) ** qrung + max(nmds) ** qrung <= 1), \
                "ERROR:Construction failed! max(MD)^q+max(NMD)^q must be in interval[0,1]!"
        self.__md = mds
        self.__nmd = nmds
        self.__qrung = qrung

    def __repr__(self):
        if len(self.__md) > 50 or len(self.__nmd) > 50:
            return 'qrungdhfe(Q=%d)'%self.__qrung + \
                   '[%d,%d]:{' % (len(self.__md), len(self.__nmd)) + \
                '\n md :' + str(np.round(self.__md, 4)[:50]) + \
                ',\n nmd:' + str(np.round(self.__nmd, 4)[:50]) + ' }\n'
        else:
            return 'qrungdhfe(Q=%d)'%self.__qrung+ \
                   '[%d,%d]:{' % (len(self.__md), len(self.__nmd)) + \
                '\n md :' + str(np.round(self.__md, 4)) + \
                ',\n nmd:' + str(np.round(self.__nmd, 4)) + ' }\n'

    property qrung:
        def __get__(self):
            return self.__qrung

    property md:
        def __get__(self):
            return self.__md

        def __set__(self, value):
            m = np.asarray(value)
            om = self.__md
            self.__md = m
            if not self.isLegal():
                self.__md = om
                raise ValueError('ERROR: Invalid data.')
            assert 0 <= value.all() <= 1, 'ERROR: Invalid data.'

    property nmd:
        def __get__(self):
            return self.__nmd

        def __set__(self, value):
            nm = np.asarray(value)
            onm = self.__nmd
            self.__nmd = nm
            if not self.isLegal():
                self.__nmd = onm
                raise ValueError('ERROR: Invalid data.')
            assert 0 <= value.all() <= 1, 'ERROR: Invalid data.'

    property parent:
        def __get__(self):
            for base in self.__class__.__bases__:
                self.__parent = base.__name__
                return self.__parent

    property score:
        def __get__(self):
            mm = ((self.__md ** self.__qrung).sum()) / len(self.__md)
            nn = ((self.__nmd ** self.__qrung).sum()) / len(self.__nmd)
            self.__score =  mm - nn
            return self.__score

    property accuracy:
        def __get__(self):
            mm = ((self.__md ** self.__qrung).sum()) / len(self.__md)
            nn = ((self.__nmd ** self.__qrung).sum()) / len(self.__nmd)
            self.__accuracy =  mm + nn
            return self.__accuracy

    property indeterminacy:
        def __get__(self):
            mm = ((self.__md ** self.__qrung).sum()) / len(self.__md)
            nn = ((self.__nmd ** self.__qrung).sum()) / len(self.__nmd)
            if mm + nn == 1.:
                self.__indeterminacy = 0.
            else:
                self.__indeterminacy =  (1. - mm - nn) ** (1 / self.__qrung)
            return self.__indeterminacy

    cpdef set_md(self, value):
        # v = np.asarray(value)
        assert 0 <= value.all() <= 1, 'ERROR: Invalid data.'
        self.__md = value

    cpdef set_nmd(self, value):
        # v = np.asarray(value)
        assert 0 <= value.all() <= 1, 'ERROR: Invalid data.'
        self.__nmd = value

    cpdef bint isEmpty(self):
        if self.__md.size == 0 and self.__nmd.size == 0:
            return True
        else:
            return False

    cpdef bint isEmpty_half(self):
        if self.__md.size == 0 or self.__nmd.size == 0:
            return True
        else:
            return False

    cpdef bint isLegal(self):
        a1 = self.__md.size == 0 and self.__nmd.size == 0
        a2 = self.__md.size == 0 and 0 <= self.__nmd.all() <= 1
        a3 = self.__nmd.size == 0 and 0 <= self.__md.all() <= 1
        a4 = min(self.__md) >= 0 and min(self.__nmd) >= 0 and max(self.__md) ** self.__qrung + max(self.__nmd) ** self.__qrung <= 1
        if a1:
            # print('a1')
            return True
        elif a2:
            # print('a2')
            return True
        elif a3:
            # print('a3')
            return True
        elif a4:
            # print('a4')
            return True
        else:
            return False

    cpdef convert(self):
        cdef list m
        cdef list n
        m = np.round(self.__md ,4).tolist()
        n = np.round(self.__nmd,4).tolist()
        return m,n

    cpdef comp(self):
        newEle = copy.deepcopy(self)
        if self.__md.size == 0 and self.__nmd.size != 0:
            newEle.set_md(np.array([]))
            newEle.set_nmd(1. - self.__nmd)
        elif self.__md.size != 0 and self.__nmd.size == 0:
            newEle.set_nmd(np.array([]))
            newEle.set_md(1. - self.__md)
        else:
            newEle.set_md(self.__nmd)
            newEle.set_nmd(self.__md)
        return newEle

    cpdef qsort(self, rev=True):
        newEle = copy.deepcopy(self)
        if rev:
            newEle.md = np.sort(self.__md)
            newEle.nmd = np.sort(self.__nmd)
        else:
            newEle.md = np.abs(np.sort(-self.__md))
            newEle.nmd = np.abs(np.sort(-self.__nmd))
        return newEle

    cpdef algeb_power(self, double l):
        newEle = copy.deepcopy(self)
        newEle.set_md(self.__md ** l)
        newEle.set_nmd((1. - (1. - self.__nmd ** self.__qrung) ** l) ** (1 / self.__qrung))
        return newEle

    cpdef algeb_times(self, double l):
        newEle = copy.deepcopy(self)
        newEle.set_md((1. - (1. - self.__md ** self.__qrung) ** l) ** (1 / self.__qrung))
        newEle.set_nmd(self.__nmd ** l)
        return newEle

    cpdef eins_power(self, double l):
        newEle = copy.deepcopy(self)
        newEle.set_md(((2 * (self.__md ** self.__qrung) ** l) / (
                (2. - self.__md ** self.__qrung) ** l + (self.__md ** self.__qrung) ** l)) ** (1 / self.__qrung))
        newEle.set_nmd((((1. + self.__nmd ** self.__qrung) ** l - (1. - self.__nmd ** self.__qrung) ** l) /
                      ((1. + self.__nmd ** self.__qrung) ** l + (1. - self.__nmd ** self.__qrung) ** l)) ** (1 / self.__qrung))
        return newEle

    cpdef eins_times(self, double l):
        newEle = copy.deepcopy(self)
        newEle.set_md((((1. + self.__md ** self.__qrung) ** l - (1. - self.__md ** self.__qrung) ** l) /
                     ((1. + self.__md ** self.__qrung) ** l + (1. - self.__md ** self.__qrung) ** l)) ** (1 / self.__qrung))
        newEle.set_nmd(((2 * (self.__nmd ** self.__qrung) ** l) / (
                (2. - self.__nmd ** self.__qrung) ** l + (self.__nmd ** self.__qrung) ** l)) ** (1 / self.__qrung))
        return newEle
