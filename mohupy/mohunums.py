#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/9/21 下午8:25
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import copy

from .config import import_cupy_lib, import_cudf_lib
from matplotlib import pyplot as plt

np = import_cupy_lib()
pd = import_cudf_lib()

class mohunum(object):
    """
        Mohunum(mohu number, fuzzy number) is a class of fuzzy numbers. This class
        contains two types of fuzzy numbers (currently): q-rung orthopair fuzzy number
        and q-rung orthopair interval-valued fuzzy number. The main content includes
        the membership degree, non-membership degree, basic operation rules, and score
        values of fuzzy numbers. Commonly used fuzzy number functions such as exact values.

        Private Attributes
        ------------------
            __qrung:        The q rung of fuzzy number
            __md:           The membership degree of fuzzy number
            __nmd:          The non-membership degree of fuzzy number
            __mtype:        The type of fuzzy number
                            Currently only contains q-rung orthopair fuzzy number,
                            q-rung orthopair interval-valued fuzzy numbers
            __MEMSHIP_KEY:  Constant. Not accessible externally and cannot be modified.
                            The switch of membership and non-membership degree.
                            Membership and non-membership degree of a fuzzy number is
                            generally unmodifiable. This constant enables the code to
                            modify membership and non-membership degrees. But not
                            accessible externally and cannot be modified.

        Public Attributes
        -----------------
            qrung:          int
                    The q rung of fuzzy number
            md:             numpy.float_ or numpy.ndarray
                    The membership degree of fuzzy number
            nmd:            numpy.float_ or numpy.ndarray
                    The non-membership degree of fuzzy number
            mtype:          str
                    The type of fuzzy number
            score:          numpy.float_
                    The score value of fuzzy number
            accuracy:       numpy.float_
                    The accuracy value of fuzzy number
            indeterminacy:  numpy.float_
                    The indeterminacy of fuzzy number
            comp:           mohunum
                    The complement of fuzzy number

        Methods
        -------
            __init__(qrung, md, nmd):
                The constructor of fuzzy number.
            __str__(self):
                The representation of fuzzy number.
            __repr__(self):
                The detail representation of fuzzy number.
            __add__:
                The addition of fuzzy number.
            __radd__:
                The addition of fuzzy number.
            __sub__:
                The subtraction of fuzzy number.
            __mul__:
                The multiplication of fuzzy number.
            __rmul__:
                The multiplication of fuzzy number.
            __truediv__:
                The division of fuzzy number.
            __pow__:
                The power of fuzzy number.
            __and__:
                Intersection operation of fuzzy numbers
            __or__:
                Union operation of fuzzy numbers
            __eq__:
                Comparison operators for equality.
            __ne__:
                Inequality between price comparison operators
            __lt__:
                Comparison operators for less than.
            __gt__:
                Comparison operators for greater than.
            __le__:
                Comparison operators for less than or equal to.
            __ge__:
                Comparison operators for greater than or equal to.
            is_valid:
                The validity of fuzzy number.
            isEmpty:
                Determine whether the fuzzy number is empty
            convert:
                Simple conversion of fuzzy number formats
            plot:
                Draw a plot of the fuzzy number and visually check the position
                of the fuzzy number in the fuzzy range. It is noting that the q-rung
                orthopair fuzzy number can be compared from the plot, while the q-rung
                orthopair interval-valued fuzzy number cannot be compared from the
                range plot.
    """
    __qrung = None
    __md = None
    __nmd = None
    __mtype = None

    __MEMSHIP_KEY = True

    def __init__(self, qrung, md, nmd):
        """
            The constructor of fuzzy number.

            Parameters
            ----------
                qrung:      int
                            The q rung of fuzzy number
                md:         The membership degree of fuzzy number
                nmd:        The non-membership degree of fuzzy number

            Notes
            -----
                 The constructor automatically constructs a fuzzy number based
                 on inputs of different membership and non-membership degrees.

            Examples
            --------
                >> x = mohunum(3, 0.5, 0.3)
                >> print(x)
                [0.5, 0.3]
                >> y = mohunum(3, [0.2, 0.7], [0.4, 0.5])
                >> print(y)
                [[0.2, 0.7], [0.4, 0.5]]
        """
        if isinstance(md, (float, int, np.int_, np.float_)) and isinstance(nmd, (float, int, np.int_, np.float_)):
            assert 0. <= md <= 1. and 0. <= nmd <= 1., \
                'ERROR: md and nmd must be between 0 and 1.'
            assert 0. <= md ** qrung + nmd ** qrung <= 1., \
                'ERROR: md ** qrung + nmd ** qrung must be between 0 and 1'

            self.__qrung = np.int_(qrung)
            self.__md = np.float_(md)
            self.__nmd = np.float_(nmd)
            self.__mtype = 'fn'
        elif isinstance(md, (list, tuple, np.ndarray)) and isinstance(nmd, (list, tuple, np.ndarray)):
            assert len(md) == 2 and len(nmd) == 2, \
                'ERROR: The data format contains at least upper and lower bounds.'
            assert md[0] <= md[1] and nmd[0] <= nmd[1], \
                'ERROR: The upper of membership and non-membership must be greater than the lower.'
            assert 0 <= md[0] <= 1 and 0 <= md[1] <= 1, \
                'ERROR: The upper and lower of membership degree must be between 0 and 1.'
            assert 0 <= nmd[0] <= 1 and 0 <= nmd[1] <= 1, \
                'ERROR: The upper and lower of non-membership degree must be between 0 and 1.'
            assert 0 <= md[0] ** qrung + nmd[0] ** qrung <= 1 and 0 <= md[1] ** qrung + nmd[1] ** qrung <= 1, \
                'ERROR: The q powers sum of membership degree and non-membership degree must be between 0 and 1.'

            self.__qrung = np.int_(qrung)
            self.__md = np.asarray(md)
            self.__nmd = np.asarray(nmd)
            self.__mtype = 'ivfn'

    def __repr__(self):
        # if self.__mtype == 'fn':
        #     return '<md:' + \
        #         str(np.round(self.__md, 4)) + ', nmd:' + \
        #         str(np.round(self.__nmd, 4)) + ', q-rung=' + \
        #         str(self.__qrung) + ', mtype=' + \
        #         str(self.__mtype) + '>'
        # if self.__mtype == 'ivfn':
        #     return '<md:[' + \
        #         str(np.round(self.__md[0], 4)) + ',' + \
        #         str(np.round(self.__md[1], 4)) + '], nmd:[' + \
        #         str(np.round(self.__nmd[0], 4)) + ',' + \
        #         str(np.round(self.__nmd[1], 4)) + '], q-rung=' + \
        #         str(self.__qrung) + ', mtype=' + \
        #         str(self.__mtype) + '>'
        if self.__mtype == 'fn':
            return '[' + \
                str(np.round(self.__md, 4)) + ',' + \
                str(np.round(self.__nmd, 4)) + ']'

        if self.__mtype == 'ivfn':
            return '[[' + \
                str(np.round(self.__md[0], 4)) + ',' + \
                str(np.round(self.__md[1], 4)) + '],[' + \
                str(np.round(self.__nmd[0], 4)) + ',' + \
                str(np.round(self.__nmd[1], 4)) + ']]'

    def __str__(self):
        if self.__mtype == 'fn':
            return '[' + \
                str(np.round(self.__md, 4)) + ',' + \
                str(np.round(self.__nmd, 4)) + ']'

        if self.__mtype == 'ivfn':
            return '[[' + \
                str(np.round(self.__md[0], 4)) + ',' + \
                str(np.round(self.__md[1], 4)) + '],[' + \
                str(np.round(self.__nmd[0], 4)) + ',' + \
                str(np.round(self.__nmd[1], 4)) + ']]'

    ### Set the constants of the class. The constants are not accessible from the outside and cannot be modified.
    @classmethod
    def get_constant(cls):
        return cls.__MEMSHIP_KEY

    @classmethod
    def set_constant(cls, value):
        raise ValueError('ERROR: The constant value cannot be set.')

    @property
    def qrung(self):
        return self.__qrung

    @property
    def md(self):
        return self.__md

    @md.setter
    def md(self, value):
        if self.__mtype == 'fn':
            if self.__MEMSHIP_KEY:
                raise ValueError('ERROR: Membership degree cannot be set.')
            assert 0. <= value <= 1., \
                'ERROR: md must be between 0 and 1.'
            self.__md = np.round(value,6)
        if self.__mtype == 'ivfn':
            if self.__MEMSHIP_KEY:
                raise ValueError('ERROR: Membership degree cannot be set.')
            assert 0 <= value[0] <= 1 and 0 <= value[1] <= 1, \
                'ERROR: The upper and lower of membership degree must be between 0 and 1.'
            self.__md = np.round(np.asarray(value),6)

    @property
    def nmd(self):
        return self.__nmd

    @nmd.setter
    def nmd(self, value):
        if self.__mtype == 'fn':
            if self.__MEMSHIP_KEY:
                raise ValueError('ERROR: Non-membership degree cannot be set.')
            assert 0. <= value <= 1., \
                'ERROR: nmd must be between 0 and 1.'
            self.__nmd = np.round(value,6)
        if self.__mtype == 'ivfn':
            if self.__MEMSHIP_KEY:
                raise ValueError('ERROR: Non-membership degree cannot be set.')
            assert 0 <= value[0] <= 1 and 0 <= value[1] <= 1, \
                'ERROR: The upper and lower of non-membership degree must be between 0 and 1.'
            self.__nmd = np.round(np.asarray(value),6)

    @property
    def mtype(self):
        return self.__mtype

    @property
    def score(self):
        if self.__mtype == 'fn':
            return self.md ** self.__qrung - self.nmd ** self.__qrung
        if self.__mtype == 'ivfn':
            m = self.__md[0] ** self.__qrung + self.__md[1] ** self.__qrung
            n = self.__nmd[0] ** self.__qrung + self.__nmd[1] ** self.__qrung
            return (m - n) / 2

    @property
    def accuracy(self):
        if self.__mtype == 'fn':
            return self.md ** self.__qrung + self.nmd ** self.__qrung
        if self.__mtype == 'ivfn':
            m = self.__md[0] ** self.__qrung + self.__md[1] ** self.__qrung
            n = self.__nmd[0] ** self.__qrung + self.__nmd[1] ** self.__qrung
            return (m + n) / 2

    @property
    def indeterminacy(self):
        if self.__mtype == 'fn':
            acc = self.md ** self.__qrung + self.nmd ** self.__qrung
            if acc == 1.:
                return 0.
            else:
                return (1. - acc) ** (1. / self.__qrung)
        if self.__mtype == 'ivfn':
            m = self.__md[0] ** self.__qrung + self.__md[1] ** self.__qrung
            n = self.__nmd[0] ** self.__qrung + self.__nmd[1] ** self.__qrung
            if m + n:
                return 0.
            else:
                return (1. - (m + n) / 2) ** (1. / self.__qrung)

    @property
    def comp(self):
        newfn = copy.deepcopy(self)
        newfn.__MEMSHIP_KEY = False
        newfn.md = self.nmd
        newfn.nmd = self.md
        newfn.__MEMSHIP_KEY = True
        return newfn

    def __add__(self, other):

        q = self.__qrung

        def __mul(ms: mohunum):
            if self.__mtype == 'fn':
                newfn = mohunum(q, 0., 0.)
                newfn.__MEMSHIP_KEY = False
                newfn.md = (self.__md ** q + ms.md ** q
                            - self.__md ** q * ms.md ** q) ** (1. / q)
                newfn.nmd = self.__nmd * ms.nmd
                newfn.__MEMSHIP_KEY = True
                return newfn
            if self.__mtype == 'ivfn':
                newfn = mohunum(q, [0., 0.], [0., 0.])
                newfn.__MEMSHIP_KEY = False
                newfn.md = [(1 - (1 - self.__md[0] ** q) * (1 - ms.md[0] ** q)) ** (1 / q),
                            (1 - (1 - self.__md[1] ** q) * (1 - ms.md[1] ** q)) ** (1 / q)]
                newfn.nmd = [self.__nmd[0] * ms.nmd[0], self.__nmd[1] * ms.nmd[1]]
                newfn.__MEMSHIP_KEY = True
                return newfn
            raise ValueError('ERROR: Unsupported type.')

        if isinstance(other, mohunum):
            assert self.__qrung == other.qrung, \
                'ERROR: The qrung must be equal.'
            assert self.__mtype == other.__mtype, \
                'ERROR: The type of two fuzzy numbers must be equal.'
            q = self.__qrung
            return __mul(other)

        from .mohusets import mohuset
        if isinstance(other, mohuset):
            assert other.mtype == self.__mtype, \
                'ERROR: The fuzzy number and set must be of the same type.'
            assert other.qrung == self.__qrung, \
                'ERROR: The fuzzy number and set must be of the same Q-rung.'

            vec_func = np.vectorize(__mul)
            newset = mohuset(q, self.__mtype)
            newset._mohuset__set = vec_func(other.set)
            newset._mohuset__shape = other.shape
            newset._mohuset__size = other.size
            newset._mohuset__ndim = other.ndim
            return newset

    def __radd__(self, other):
        q = self.__qrung

        def __mul(ms: mohunum):
            if self.__mtype == 'fn':
                newfn = mohunum(q, 0., 0.)
                newfn.__MEMSHIP_KEY = False
                newfn.md = (self.__md ** q + ms.md ** q
                            - self.__md ** q * ms.md ** q) ** (1. / q)
                newfn.nmd = self.__nmd * ms.nmd
                newfn.__MEMSHIP_KEY = True
                return newfn
            if self.__mtype == 'ivfn':
                newfn = mohunum(q, [0., 0.], [0., 0.])
                newfn.__MEMSHIP_KEY = False
                newfn.md = [(1 - (1 - self.__md[0] ** q) * (1 - ms.md[0] ** q)) ** (1 / q),
                            (1 - (1 - self.__md[1] ** q) * (1 - ms.md[1] ** q)) ** (1 / q)]
                newfn.nmd = [self.__nmd[0] * ms.nmd[0], self.__nmd[1] * ms.nmd[1]]
                newfn.__MEMSHIP_KEY = True
                return newfn
            raise ValueError('ERROR: Unsupported type.')

        if isinstance(other, mohunum):
            assert self.__qrung == other.qrung, \
                'ERROR: The qrung must be equal.'
            assert self.__mtype == other.__mtype, \
                'ERROR: The type of two fuzzy numbers must be equal.'
            return __mul(other)

        from .mohusets import mohuset
        if isinstance(other, mohuset):
            assert other.mtype == self.__mtype, \
                'ERROR: The fuzzy number and set must be of the same type.'
            assert other.qrung == self.__qrung, \
                'ERROR: The fuzzy number and set must be of the same Q-rung.'

            vec_func = np.vectorize(__mul)
            newset = mohuset(q, self.__mtype)
            newset._mohuset__set = vec_func(other.set)
            newset._mohuset__shape = other.shape
            newset._mohuset__size = other.size
            newset._mohuset__ndim = other.ndim
            return newset

    def __sub__(self, other):

        q = self.__qrung

        def __sub(ms: mohunum):
            if self.__mtype == 'fn':
                newfn = mohunum(q, 0., 1.)
                if ms.nmd == 0. or ms.md == 1:
                    return newfn
                elif 0 <= self.__nmd / ms.nmd <= \
                        ((1 - self.__md ** q) / (1 - ms.md ** q)) ** (1 / q) <= 1:
                    newfn.__MEMSHIP_KEY = False
                    newfn.md = ((self.__md ** q - ms.md ** q) / (1 - ms.md ** q)) ** (1 / q)
                    newfn.nmd = self.__nmd / ms.nmd
                    newfn.__MEMSHIP_KEY = True
                    return newfn
                else:
                    return newfn
            if self.__mtype == 'ivfn':
                raise ValueError('ERROR: Fuzzy numbers of \'ivfn\' '
                                 'do not currently support subtraction.')

        if isinstance(other, mohunum):
            assert self.__qrung == other.qrung, \
                'ERROR: The qrung must be equal.'
            assert self.__mtype == other.__mtype, \
                'ERROR: The type of two fuzzy numbers must be equal.'
            return __sub(other)

        from .mohusets import mohuset
        if isinstance(other, mohuset):
            assert other.mtype == self.__mtype, \
                'ERROR: The fuzzy number and set must be of the same type.'
            assert other.qrung == self.__qrung, \
                'ERROR: The fuzzy number and set must be of the same Q-rung.'

            vec_func = np.vectorize(__sub)
            newset = mohuset(q, self.__mtype)
            newset._mohuset__set = vec_func(other.set)
            newset._mohuset__shape = other.shape
            newset._mohuset__size = other.size
            newset._mohuset__ndim = other.ndim
            return newset

    def __mul__(self, other):
        q = self.__qrung

        def __mul(mn: mohunum):
            if self.__mtype == 'fn':
                newf = mohunum(q, 0., 0.)
                newf.__MEMSHIP_KEY = False
                newf.md = self.__md * mn.md
                newf.nmd = (self.__nmd ** q + mn.nmd ** q
                            - self.__nmd ** q * mn.nmd ** q) ** (1. / q)
                newf.__MEMSHIP_KEY = True
                return newf

            if self.__mtype == 'ivfn':
                newf = mohunum(q, [0., 0.], [0., 0.])
                newf.__MEMSHIP_KEY = False
                newf.md = self.__md * mn.md
                newf.nmd = (self.__nmd ** q + mn.nmd ** q
                            - self.__nmd ** q * mn.nmd ** q) ** (1. / q)
                newf.__MEMSHIP_KEY = True
                return newf
            raise ValueError('ERROR: Unsupported type.')

        if isinstance(other, mohunum):
            assert self.__qrung == other.qrung, \
                'ERROR: The qrung must be equal.'
            assert self.__mtype == other.__mtype, \
                'ERROR: The type of two fuzzy numbers must be equal.'
            return __mul(other)

        if isinstance(other, (float, np.float_)):
            assert 0. <= other <= 1., \
                'ERROR: The value must be between to 0 and 1.'
            if self.__mtype == 'fn':
                newfn = mohunum(q, 0., 0.)
                newfn.__MEMSHIP_KEY = False
                newfn.md = (1. - (1. - self.__md ** q) ** other) ** (1. / q)
                newfn.nmd = self.__nmd ** other
                newfn.__MEMSHIP_KEY = True
                return newfn
            if self.__mtype == 'ivfn':
                newfn = mohunum(q, [0., 0.], [0., 0.])
                newfn.__MEMSHIP_KEY = False
                newfn.md = (1. - (1. - self.__md ** q) ** other) ** (1. / q)
                newfn.nmd = self.__nmd ** other
                newfn.__MEMSHIP_KEY = True
                return newfn
            raise ValueError('ERROR: Unsupported type.')

        from .mohusets import mohuset
        if isinstance(other, mohuset):
            assert other.mtype == self.__mtype, \
                'ERROR: The fuzzy number and set must be of the same type.'
            assert other.qrung == self.__qrung, \
                'ERROR: The fuzzy number and set must be of the same Q-rung.'
            vec_func = np.vectorize(__mul)
            newset = mohuset(q, self.__mtype)
            newset._mohuset__set = vec_func(other.set)
            newset._mohuset__shape = other.shape
            newset._mohuset__size = other.size
            newset._mohuset__ndim = other.ndim
            return newset
        raise ValueError('ERROR: Unsupported type.')

    def __rmul__(self, other):
        q = self.__qrung

        def __mul(mn: mohunum):
            if self.__mtype == 'fn':
                newf = mohunum(q, 0., 0.)
                newf.__MEMSHIP_KEY = False
                newf.md = self.__md * mn.md
                newf.nmd = (self.__nmd ** q + mn.nmd ** q
                            - self.__nmd ** q * mn.nmd ** q) ** (1. / q)
                newf.__MEMSHIP_KEY = True
                return newf

            if self.__mtype == 'ivfn':
                newf = mohunum(q, [0., 0.], [0., 0.])
                newf.__MEMSHIP_KEY = False
                newf.md = self.__md * mn.md
                newf.nmd = (self.__nmd ** q + mn.nmd ** q
                            - self.__nmd ** q * mn.nmd ** q) ** (1. / q)
                newf.__MEMSHIP_KEY = True
                return newf
            raise ValueError('ERROR: Unsupported type.')

        if isinstance(other, mohunum):
            assert self.__qrung == other.qrung, \
                'ERROR: The qrung must be equal.'
            assert self.__mtype == other.__mtype, \
                'ERROR: The type of two fuzzy numbers must be equal.'
            return __mul(other)

        if isinstance(other, (float, np.float_)):
            assert 0. <= other <= 1., \
                'ERROR: The value must be between to 0 and 1.'
            if self.__mtype == 'fn':
                newfn = mohunum(q, 0., 0.)
                newfn.__MEMSHIP_KEY = False
                newfn.md = (1. - (1. - self.__md ** q) ** other) ** (1. / q)
                newfn.nmd = self.__nmd ** other
                newfn.__MEMSHIP_KEY = True
                return newfn
            if self.__mtype == 'ivfn':
                newfn = mohunum(q, [0., 0.], [0., 0.])
                newfn.__MEMSHIP_KEY = False
                newfn.md = (1. - (1. - self.__md ** q) ** other) ** (1. / q)
                newfn.nmd = self.__nmd ** other
                newfn.__MEMSHIP_KEY = True
                return newfn
            raise ValueError('ERROR: Unsupported type.')

        from .mohusets import mohuset
        if isinstance(other, mohuset):
            assert other.mtype == self.__mtype, \
                'ERROR: The fuzzy number and set must be of the same type.'
            assert other.qrung == self.__qrung, \
                'ERROR: The fuzzy number and set must be of the same Q-rung.'
            vec_func = np.vectorize(__mul)
            newset = mohuset(q, self.__mtype)
            newset._mohuset__set = vec_func(other.set)
            newset._mohuset__shape = other.shape
            newset._mohuset__size = other.size
            newset._mohuset__ndim = other.ndim
            return newset
        raise ValueError('ERROR: Unsupported type.')

    def __truediv__(self, other):
        q = self.__qrung

        def __truediv(mn: mohunum):
            if self.__mtype == 'fn':
                newfn = mohunum(q, 1., 0.)
                if mn.md == 0. or mn.nmd == 1.:
                    return newfn
                elif 0 <= self.__md / mn.md <= \
                        ((1 - self.__nmd ** q) / (1 - mn.nmd ** q)) ** (1 / q) <= 1:
                    newfn.__MEMSHIP_KEY = False
                    newfn.md = self.__md / mn.md
                    newfn.nmd = ((self.__nmd ** q - mn.nmd ** q) / (1 - mn.nmd ** q)) ** (1 / q)
                    newfn.__MEMSHIP_KEY = True
                    return newfn
                else:
                    return newfn

            if self.__mtype == 'ivfn':
                raise ValueError('ERROR: Fuzzy numbers of \'ivfn\' do not currently support division.')

        if isinstance(other, mohunum):
            assert self.__qrung == other.qrung, \
                'ERROR: The qrung must be equal.'
            assert self.__mtype == other.__mtype, \
                'ERROR: The type of two fuzzy numbers must be equal.'
            return __truediv(other)

        if isinstance(other, (float, int, np.int_, np.float_)):
            assert 1. < other, \
                'ERROR: The value must be greater than 1.'
            return self.__mul__(1. / other)

        from .mohusets import mohuset
        if isinstance(other, mohuset):
            assert other.mtype == self.__mtype, \
                'ERROR: The fuzzy number and set must be of the same type.'
            assert other.qrung == self.__qrung, \
                'ERROR: The fuzzy number and set must be of the same Q-rung.'

            vec_func = np.vectorize(__truediv)
            newset = mohuset(q, self.__mtype)
            newset._mohuset__set = vec_func(other.set)
            newset._mohuset__shape = other.shape
            newset._mohuset__size = other.size
            newset._mohuset__ndim = other.ndim
            return newset

    def __pow__(self, other, modulo=None):
        q = self.__qrung
        assert isinstance(other, (float, np.float_)), \
            'ERROR: The power value must be a float.'
        assert 0 < other <= 1., \
            'ERROR: The power value must be between 0 and 1.'
        if self.__mtype == 'fn':
            newfn = mohunum(q, 0., 0.)
            newfn.__MEMSHIP_KEY = False
            newfn.md = self.__md ** other
            newfn.nmd = (1. - (1. - self.__nmd ** q) ** other) ** (1. / q)
            newfn.__MEMSHIP_KEY = True
            return newfn
        if self.__mtype == 'ivfn':
            newfn = mohunum(q, [0., 0.], [0., 0.])
            newfn.__MEMSHIP_KEY = False
            newfn.md = self.__md ** other
            newfn.nmd = (1. - (1. - self.__nmd ** q) ** other) ** (1. / q)
            newfn.__MEMSHIP_KEY = True
            return newfn

    def __and__(self, other):
        assert isinstance(other, mohunum), \
            'ERROR: other must be a mohunum object.'
        assert self.__mtype == other.mtype, \
            'ERROR: The type of two fuzzy numbers must be same.'
        assert self.__qrung == other.qrung, \
            'ERROR: The qrung must be equal.'
        q = self.__qrung

        if self.__mtype == 'fn':
            newfn = mohunum(q, 0., 0.)
            newfn.__MEMSHIP_KEY = False
            newfn.md = (min(self.__md, other.md))
            newfn.nmd = (max(self.__nmd, other.nmd))
            newfn.__MEMSHIP_KEY = True
            return newfn
        if self.__mtype == 'ivfn':
            newfn = mohunum(q, [0., 0.], [0., 0.])
            newfn.__MEMSHIP_KEY = False
            newfn.md = [min(self.__md[0], other.md[0]), min(self.__md[1], other.md[1])]
            newfn.nmd = [max(self.__nmd[0], other.nmd[0]), max(self.__nmd[1], other.nmd[1])]
            newfn.__MEMSHIP_KEY = True
            return newfn

    def __or__(self, other):
        assert isinstance(other, mohunum), \
            'ERROR: other must be a mohunum object.'
        assert self.__mtype == other.mtype, \
            'ERROR: The type of two fuzzy numbers must be same.'
        assert self.__qrung == other.qrung, \
            'ERROR: The qrung must be equal.'
        q = self.__qrung

        if self.__mtype == 'fn':
            newfn = mohunum(q, 0., 0.)
            newfn.__MEMSHIP_KEY = False
            newfn.md = (max(self.__md, other.md))
            newfn.nmd = (min(self.__nmd, other.nmd))
            newfn.__MEMSHIP_KEY = True
            return newfn
        if self.__mtype == 'ivfn':
            newfn = mohunum(q, [0., 0.], [0., 0.])
            newfn.__MEMSHIP_KEY = False
            newfn.md = [max(self.__md[0], other.md[0]), max(self.__md[1], other.md[1])]
            newfn.nmd = [min(self.__nmd[0], other.nmd[0]), min(self.__nmd[1], other.nmd[1])]
            newfn.__MEMSHIP_KEY = True
            return newfn

    def __eq__(self, other):
        assert isinstance(other, mohunum), \
            'ERROR: other must be a mohunum object.'
        assert self.__qrung == other.qrung, \
            'ERROR: The qrung must be equal.'
        if self.__mtype == 'fn':
            return self.__md == other.md and self.__nmd == other.nmd
        if self.__mtype == 'ivfn':
            return np.array_equal(self.__md, other.md) and np.array_equal(self.__nmd, other.nmd)

    def __ne__(self, other):
        assert isinstance(other, mohunum), \
            'ERROR: other must be a mohunum object.'
        assert self.__qrung == other.qrung, \
            'ERROR: The qrung must be equal.'
        if self.__mtype == 'fn':
            return self.__md != other.md or self.__nmd != other.nmd
        if self.__mtype == 'ivfn':
            return np.array_equal(self.__md, other.md) or not np.array_equal(self.__nmd, other.nmd)

    def __lt__(self, other):
        assert isinstance(other, mohunum), \
            'ERROR: other must be a mohunum object.'
        assert self.__qrung == other.qrung, \
            'ERROR: The qrung must be equal.'
        assert self.__mtype == other.mtype, \
            'ERROR: The type of two fuzzy numbers must be same.'
        q = self.__qrung
        if self.__mtype == 'fn':
            if self - other == mohunum(q, 0., 1.) and self != other:
                return True
            else:
                return False
        if self.__mtype == 'ivfn':
            raise ValueError('ERROR: Fuzzy numbers of \'ivfn\' do not currently support comparison.')

    def __gt__(self, other):
        assert isinstance(other, mohunum), \
            'ERROR: other must be a mohunum object.'
        assert self.__qrung == other.qrung, \
            'ERROR: The qrung must be equal.'
        assert self.__mtype == other.mtype, \
            'ERROR: The type of two fuzzy numbers must be same.'
        q = self.__qrung
        if self.__mtype == 'fn':
            if self - other != mohunum(q, 0., 1.) and self != other:
                return True
            else:
                return False
        if self.__mtype == 'ivfn':
            raise ValueError('ERROR: Fuzzy numbers of \'ivfn\' do not currently support comparison.')

    def __le__(self, other):
        assert isinstance(other, mohunum), \
            'ERROR: other must be a mohunum object.'
        assert self.__qrung == other.qrung, \
            'ERROR: The qrung must be equal.'
        assert self.__mtype == other.mtype, \
            'ERROR: The type of two fuzzy numbers must be same.'
        q = self.__qrung
        if self.__mtype == 'fn':
            if self - other == mohunum(q, 0., 1.) or self == other:
                return True
            else:
                return False
        if self.__mtype == 'ivfn':
            raise ValueError('ERROR: Fuzzy numbers of \'ivfn\' do not currently support comparison.')

    def __ge__(self, other):
        assert isinstance(other, mohunum), \
            'ERROR: other must be a mohunum object.'
        assert self.__qrung == other.qrung, \
            'ERROR: The qrung must be equal.'
        assert self.__mtype == other.mtype, \
            'ERROR: The type of two fuzzy numbers must be same.'
        q = self.__qrung
        if self.__mtype == 'fn':
            if self - other != mohunum(q, 0., 1.) or self == other:
                return True
            else:
                return False

    def is_valid(self):
        if self.__mtype == 'fn':
            mds = self.__md
            nmds = self.__nmd
            if 0. <= mds <= 1. and 0. <= nmds <= 1. \
                    and 0. <= mds ** self.__qrung + nmds ** self.__qrung <= 1.:
                return True
            else:
                return False
        if self.__mtype == 'ivfn':
            if not len(self.__md) == 2 and len(self.__nmd) == 2:
                return False
            elif not 0. <= np.all(self.__md) <= 1. and 0. <= np.all(self.__md) <= 1.:
                return False
            elif not (self.__md[0] <= self.__md[1] and self.__nmd[0] <= self.__nmd[1]):
                return False
            elif not 0 <= self.__md[1] ** self.__qrung + self.__nmd[1] ** self.__qrung <= 1:
                return False
            else:
                return True

    def isEmpty(self):
        if self.__md is None and self.__nmd is None:
            return True
        else:
            return False

    def convert(self):
        if self.__mtype == 'fn':
            return np.round(self.__md, 4), np.round(self.__nmd, 4)
        if self.__mtype == 'ivfn':
            return np.round(self.__md, 4).tolist(), np.round(self.__nmd, 4).tolist()

    def plot(self, other=None, area=None, color='red', color_area=None, alpha=0.3):
        if area is None:
            area = [False, False, False, False]
        if color_area is None:
            color_area = ['red', 'green', 'blue', 'yellow']
        if self.__mtype == 'fn':
            md = self.__md
            nmd = self.__nmd
            q = self.__qrung

            x = np.linspace(0, 1, 1000)

            plt.gca().spines['top'].set_linewidth(False)
            plt.gca().spines['bottom'].set_linewidth(True)
            plt.gca().spines['left'].set_linewidth(True)
            plt.gca().spines['right'].set_linewidth(False)
            plt.axis([0, 1.1, 0, 1.1])
            plt.axhline(y=0)
            plt.axvline(x=0)
            plt.scatter(md, nmd, color=color, marker='.')

            if other is not None:
                assert other.qrung == q, 'ERROR: The qrungs are not equal'
                plt.scatter(other.md, other.nmd, color=color, marker='*')

            y = (1 - x ** q) ** (1 / q)

            n = (nmd ** q / (1 - md ** q) * (1 - x ** q)) ** (1 / q)
            m = (md ** q / (1 - nmd ** q) * (1 - x ** q)) ** (1 / q)

            if area[0]:
                # Q-ROFN f addition region
                plt.fill_between(x, n, color=color_area[0], alpha=alpha, where=x > md)
            if area[1]:
                # Q-ROFN f subtraction region
                plt.fill_between(x, n, y, color=color_area[1], alpha=alpha, where=x < md)
            if area[2]:
                # Q-ROFN f multiplication region
                plt.fill_betweenx(x, m, color=color_area[2], alpha=alpha, where=x > nmd)
            if area[3]:
                # Q-ROFN f division region
                plt.fill_betweenx(x, m, y, color=color_area[3], alpha=alpha, where=x < nmd)

            plt.plot(x, y)
            plt.show()
        if self.__mtype == 'ivfn':
            md = self.__md
            nmd = self.__nmd
            q = self.__qrung

            x = np.linspace(0, 1, 1000)

            plt.gca().spines['top'].set_linewidth(False)
            plt.gca().spines['bottom'].set_linewidth(True)
            plt.gca().spines['left'].set_linewidth(True)
            plt.gca().spines['right'].set_linewidth(False)
            plt.axis([0, 1.1, 0, 1.1])
            plt.axhline(y=0)
            plt.axvline(x=0)

            plt.fill([md[0], md[1], md[1], md[0]],
                     [nmd[1], nmd[1], nmd[0], nmd[0]],
                     color=color, alpha=alpha)

            if other is not None:
                assert isinstance(other, mohunum), \
                    'ERROR: other must be a mohunum object.'
                assert other.qrung == q, \
                    'ERROR: The qrungs are not equal'
                assert self.__mtype == other.mtype, \
                    'ERROR: The type of two fuzzy numbers must be same.'
                plt.fill([other.md[0], other.md[1], other.md[1], other.md[0]],
                         [other.nmd[1], other.nmd[1], other.nmd[0], other.nmd[0]],
                         color=color, alpha=alpha)

            y = (1 - x ** q) ** (1 / q)
            plt.plot(x, y)
            plt.show()
