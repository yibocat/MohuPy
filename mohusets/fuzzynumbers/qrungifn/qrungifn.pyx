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

cdef class qrungifn(Fuzzynum):

    cdef:
        int __qrung
        str __parent
        double __score
        double __accuracy
        double __indeterminacy
        float __md
        float __nmd

    def __init__(self, int qrung, float md, float nmd):
        super().__init__()
        cdef float mds
        cdef float nmds
        mds = np.float_(md)
        nmds = np.float_(nmd)

        assert 0. <= md <= 1. and 0. <= nmd <= 1., 'md and nmd must be between 0 and 1.'
        assert 0. <= md ** qrung + nmd ** qrung <= 1., 'md ** qrung + nmd ** qrung must be between 0 and 1'

        self.__qrung = qrung
        self.__md = mds
        self.__nmd = nmds

    def __repr__(self):
        return 'qrungifn(Q=%d):(' % self.__qrung + '\n' + '    md: ' + str(
            np.around(self.__md, 4)) + '\n' + '    nmd:' + str(
            np.around(self.__nmd, 4)) + ')'

    property qrung:
        def __get__(self):
            return self.__qrung

    property md:
        def __get__(self):
            return self.__md

        def __set__(self, float value):
            assert 0. <= value <= 1., 'ERROR: MD must be in the interval 0-1.'
            v = np.float_(value)
            m = self.__md
            self.__md = v
            if not self.isLegal():
                self.__md = m
                raise ValueError('ERROR: Invalid data.')

    property nmd:
        def __get__(self):
            return self.__nmd

        def __set__(self, float value):
            assert 0. <= value <= 1., 'ERROR: NMD must be in the interval 0-1.'
            v = np.float_(value)
            m = self.__nmd
            self.__nmd = v
            if not self.isLegal():
                self.__nmd = m
                raise ValueError('ERROR: Invalid data.')

    property parent:
        def __get__(self):
            for base in self.__class__.__bases__:
                self.__parent = base.__name__
                return self.__parent
    property score:
        def __get__(self):
            self.__score = self.md ** self.__qrung - self.nmd ** self.__qrung
            return self.__score

    property accuracy:
        def __get__(self):
            self.__accuracy = self.md ** self.__qrung + self.nmd ** self.__qrung
            return self.__accuracy

    property indeterminacy:
        def __get__(self):
            acc = self.md ** self.__qrung + self.nmd ** self.__qrung
            if acc == 1.:
                self.__indeterminacy = 0.
            else:
                self.__indeterminacy = (1. - acc) ** (1. / self.__qrung)
            return self.__indeterminacy

    cpdef set_md(self, value):
        v = np.float_(value)
        assert 0 <= v.all() <= 1, 'ERROR: Invalid data.'
        self.__md = v

    cpdef set_nmd(self, value):
        v = np.float_(value)
        assert 0 <= v.all() <= 1, 'ERROR: Invalid data.'
        self.__nmd = v

    cpdef bint isEmpty(self):
        if self.__md is None and self.__nmd is None:
            return True
        else:
            return False

    cpdef bint isEmpty_half(self):
        if self.__md is None or self.__nmd is None:
            return True
        else:
            return False

    cpdef bint isLegal(self):
        mds = self.__md
        nmds = self.__nmd
        if 0. <= mds <= 1. and 0. <= nmds <= 1. \
                and 0. <= mds ** self.__qrung + nmds ** self.__qrung <= 1.:
            return True
        else:
            return False

    cpdef convert(self):
        m = np.round(self.__md ,4)
        n = np.round(self.__nmd,4)
        return m,n

    cpdef comp(self):
        newFN = copy.deepcopy(self)
        newFN.set_md(self.__nmd)
        newFN.set_nmd(self.__md)
        return newFN

    cpdef algeb_power(self, float l):
        newFN = copy.deepcopy(self)
        newFN.set_md(self.__md ** l)
        newFN.set_nmd((1. - (1. - self.__nmd ** self.__qrung) ** l) ** (1. / self.__qrung))
        return newFN

    cpdef algeb_times(self, float l):
        newFN = copy.deepcopy(self)
        newFN.set_md((1. - (1. - self.__md ** self.__qrung) ** l) ** (1. / self.__qrung))
        newFN.set_nmd(self.__nmd ** l)
        return newFN

    cpdef eins_power(self, float l):
        newFN = copy.deepcopy(self)
        newFN.set_md(((2. * (self.__md ** self.__qrung) ** l) / (
                    (2. - self.__md ** self.__qrung) ** l + (self.__md ** self.__qrung) ** l)) ** (1. / self.__qrung))
        newFN.set_nmd((((1. + self.__nmd ** self.__qrung) ** l - (1. - self.__nmd ** self.__qrung) ** l) / (
                    (1. + self.__nmd ** self.__qrung) ** l + (1. - self.__nmd ** self.__qrung) ** l)) ** (1. / self.__qrung))
        return newFN

    cpdef eins_times(self, float l):
        newFN = copy.deepcopy(self)
        newFN.set_md((((1. + self.__md ** self.__qrung) ** l - (1. - self.__md ** self.__qrung) ** l) / (
                    (1. + self.__md ** self.__qrung) ** l + (1. - self.__md ** self.__qrung) ** l)) ** (1. / self.__qrung))
        newFN.set_nmd(((2. * (self.__nmd ** self.__qrung) ** l) / (
                    (2. - self.__nmd ** self.__qrung) ** l + (self.__nmd ** self.__qrung) ** l)) ** (1. / self.__qrung))
        return newFN
