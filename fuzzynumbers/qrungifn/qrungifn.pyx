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
        np.ndarray __md
        np.ndarray __nmd

    def __init__(self, int qrung, double md, double nmd):
        super().__init__()
        cdef np.ndarray mds
        cdef np.ndarray nmds
        mds = np.asarray(md)
        nmds = np.asarray(nmd)
        self.__qrung = qrung
        assert (( mds.size == 1 and nmds.size == 1)
                and 0. <= mds.all() <= 1. and 0. <= nmds.all() <= 1.) \
                and 0. <= mds.all() ** qrung + nmds.all() ** qrung <= 1., \
                'ERROR: Both of MD and NMD and MD^q+NMD^q must have be in the interval 0-1 ' \
                'and the number of MD or NMD must have be 1.'
        self.__md = mds[0]
        self.__nmd = nmds[0]

    def __repr__(self):
        return 'QRungFN(Q=%d):(' % self.__qrung + '\n' + '    md: ' + str(
            np.around(self.__md, 4)) + '\n' + '    nmd:' + str(
            np.around(self.__nmd, 4)) + ')'

    property qrung:
        def __get__(self):
            return self.__qrung

    property md:
        def __get__(self):
            return self.__md

        def __set__(self, double value):
            assert 0. <= value <= 1., 'ERROR: MD must be in the interval 0-1.'
            m = self.__md
            self.__md = value
            if not self.isLegal():
                self.__md = m
                raise ValueError('ERROR: Invalid data.')

    property nmd:
        def __get__(self):
            return self.__nmd

        def __set__(self, double value):
            assert 0. <= value <= 1., 'ERROR: NMD must be in the interval 0-1.'
            m = self.__nmd
            self.__nmd = value
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
            self.__indeterminacy = (1. - acc) ** (1. / self.__qrung)
            return self.__indeterminacy

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
        mds = np.asarray(self.__md)
        nmds = np.asarray(self.__nmd)
        if (mds.size == 1 and nmds.size == 1) and 0 <= mds <= 1 and 0 <= nmds <= 1 \
                and 0 <= mds ** self.__qrung + nmds ** self.__qrung <= 1:
            return True
        else:
            return False

    cpdef comp(self):
        newFN = copy.deepcopy(self)
        newFN.md = self.__nmd
        newFN.nmd = self.__md
        return newFN

    cpdef algeb_power(self, double l):
        newFN = copy.deepcopy(self)
        newFN.md = self.__md ** l
        newFN.nmd = (1. - (1. - self.__nmd ** self.__qrung) ** l) ** (1. / self.__qrung)
        return newFN

    cpdef algeb_times(self, double l):
        newFN = copy.deepcopy(self)
        newFN.md = (1. - (1. - self.__md ** self.__qrung) ** l) ** (1. / self.__qrung)
        newFN.nmd = self.__nmd ** l
        return newFN

    cpdef eins_power(self, double l):
        newFN = copy.deepcopy(self)
        newFN.md = ((2. * (self.__md ** self.__qrung) ** l) / (
                    (2. - self.__md ** self.__qrung) ** l + (self.__md ** self.__qrung) ** l)) ** (1. / self.__qrung)
        newFN.nmd = (((1. + self.__nmd ** self.__qrung) ** l - (1. - self.__nmd ** self.__qrung) ** l) / (
                    (1. + self.__nmd ** self.__qrung) ** l + (1. - self.__nmd ** self.__qrung) ** l)) ** (1. / self.__qrung)
        return newFN

    cpdef eins_times(self, double l):
        newFN = copy.deepcopy(self)
        newFN.md = (((1. + self.__md ** self.__qrung) ** l - (1. - self.__md ** self.__qrung) ** l) / (
                    (1. + self.__md ** self.__qrung) ** l + (1. - self.__md ** self.__qrung) ** l)) ** (1. / self.__qrung)
        newFN.nmd = ((2. * (self.__nmd ** self.__qrung) ** l) / (
                    (2. - self.__nmd ** self.__qrung) ** l + (self.__nmd ** self.__qrung) ** l)) ** (1. / self.__qrung)
        return newFN
