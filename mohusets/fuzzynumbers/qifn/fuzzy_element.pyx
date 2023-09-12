#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/21 上午4:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets

import copy

from matplotlib import pyplot as plt

from ..Fuzzynum cimport Fuzzynum
from ..archimedean cimport algebraic_T, algebraic_S, einstein_T, einstein_S

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

    def __add__(self, other):
        assert other.__class__.__name__ == self.__class__.__name__, 'ERROR: the two fuzzy elements are not same'
        assert self.qrung == other.qrung, 'ERROR:the two FNs are not the same FN'
        q = self.qrung
        newFN = qrungifn(q, 0., 0.)
        newFN.set_md(algebraic_S(self.md ** q, other.md ** q) ** (1 / q))
        newFN.set_nmd(algebraic_T(self.nmd ** q, other.nmd ** q) ** (1 / q))
        return newFN

    def __pow__(self, power, modulo):
        q = self.qrung
        newFN = qrungifn(q, 0., 0.)
        newFN.set_md(self.__md ** power)
        newFN.set_nmd((1. - (1. - self.__nmd ** self.__qrung) ** power) ** (1. / self.__qrung))
        return newFN

    def __mul__(self, other):
        q = self.qrung
        newFN = qrungifn(q, 0., 0.)
        if other.__class__.__name__ == self.__class__.__name__:
            assert other.qrung == q, 'ERROR: the two ifns are not the ifn with the same q'
            newFN.set_md(algebraic_T(self.md ** q, other.md ** q) ** (1 / q))
            newFN.set_nmd(algebraic_S(self.nmd ** q, other.nmd ** q) ** (1 / q))
        else:
            newFN.set_md((1. - (1. - self.__md ** self.__qrung) ** other) ** (1. / self.__qrung))
            newFN.set_nmd(self.__nmd ** other)
        return newFN

    def __rmul__(self, other):
        q = self.qrung
        newFN = qrungifn(q, 0., 0.)
        if other.__class__.__name__ == self.__class__.__name__:
            assert other.qrung == q, 'ERROR: the two ifns are not the ifn with the same q'
            newFN.set_md(algebraic_T(self.md ** q, other.md ** q) ** (1 / q))
            newFN.set_nmd(algebraic_S(self.nmd ** q, other.nmd ** q) ** (1 / q))
        else:
            newFN.set_md((1. - (1. - self.__md ** self.__qrung) ** other) ** (1. / self.__qrung))
            newFN.set_nmd(self.__nmd ** other)
        return newFN

    def __sub__(self, other:qrungifn):
        """
             Subtraction of Q-Rung orthopair fuzzy numbers
        """
        q = self.qrung
        newFN = qrungifn(q, 0., 0.)
        if other.nmd == 0 or other.md == 1:
            newFN.set_md(0)
            newFN.set_nmd(1)
        elif 0<=self.nmd/other.nmd<=((1-self.md**q)/(1-other.md**q))**(1/q)<=1:
            newFN.set_md(((self.md ** q - other.md ** q)/(1 - other.md**q))**(1/q))
            newFN.set_nmd(self.nmd/other.nmd)
        else:
            newFN.set_md(0)
            newFN.set_nmd(1)
        return newFN

    def __truediv__(self, other):
        """
             Division of Q-Rung orthopair fuzzy numbers
        """
        q = self.qrung
        newFN = qrungifn(q, 0., 0.)
        if other.md == 0 or other.nmd == 1:
            newFN.set_md(1)
            newFN.set_nmd(0)
        elif 0<=self.md/other.md<=((1-self.nmd**q)/(1-other.nmd**q))**(1/q)<=1:
            newFN.set_md(self.md/other.md)
            newFN.set_nmd(((self.nmd ** q - other.nmd ** q)/(1 - other.nmd**q))**(1/q))
        else:
            newFN.set_md(1)
            newFN.set_nmd(0)
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

    cpdef plot(self, region='None'):
        """
            Plots the fuzzynumber distribution for a given fuzzynumber.

            Parameters
            ----------
            region : str
                The region of operations.
                optional: 'all','addition','subtraction','multiplication' or 'division'

            Returns
            -------
        """
        md = self.__md
        nmd = self.__nmd
        q = self.__qrung

        x = np.linspace(0, 1, 1000)

        plt.gca().spines['top'].set_linewidth(False)
        plt.gca().spines['bottom'].set_linewidth(True)
        plt.gca().spines['left'].set_linewidth(True)
        plt.gca().spines['right'].set_linewidth(False)
        plt.axis([0,1.1,0,1.1])
        plt.axhline(y=0)
        plt.axvline(x=0)
        plt.scatter(md, nmd, color='red', marker='o')

        y = (1 - x**q)**(1/q)

        n = (nmd**q/(1-md**q)*(1-x**q))**(1/q)
        m = (md**q/(1-nmd**q)*(1-x**q))**(1/q)

        if region == 'addition':
            # Q-ROFN f addition region
            plt.fill_between(x,n,color='blue', alpha=0.1, where=x>md)
        elif region =='subtraction':
            # Q-ROFN f subtraction region
            plt.fill_between(x,n,y,color='red', alpha=0.1, where=x<md)
        elif region =='multiplication':
            # Q-ROFN f multiplication region
            plt.fill_betweenx(x, m, color='blue', alpha=0.1,where=x>nmd)
        elif region == 'division':
            # Q-ROFN f division region
            plt.fill_betweenx(x,m,y, color='red', alpha=0.1, where=x<nmd)
        elif region == 'all':
            plt.fill_between(x,n,color='blue', alpha=0.1, where=x>md)
            plt.fill_between(x,n,y,color='red', alpha=0.1, where=x<md)
            plt.fill_betweenx(x, m, color='blue', alpha=0.1,where=x>nmd)
            plt.fill_betweenx(x,m,y, color='red', alpha=0.1, where=x<nmd)
        else:
            pass

        plt.plot(x,y)
        # plt.plot(x,n,linestyle='--')
        # plt.plot(m,x,linestyle='--')
        plt.show()