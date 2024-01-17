#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/11/27 下午12:59
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

"""
    Method file
    which implements basic fuzzy number and fuzzy set operations. Most of the methods
    can be run directly through the constructed set or number instance suffix, or with
    mp.xxx (x), similar to np.xxx (x). All methods inherit from the method base class
    Function, and need to specifically implement the abstract method of the base class,
    which is the concrete implementation of each class or method. Each method is a class,
    and then the function interface is used to implement the external call to that method.
"""

import copy
import numpy as np

from ..constant import Approx


class Function:
    """
        The method base class consists of a call function and an abstract function.
        Among them, function is the concrete implementation of its subclass method.
    """

    def __call__(self, *x):
        return self.function(*x)

    def function(self, *x):
        raise NotImplementedError()


class InitializeNum(Function):
    """
        Initialization Method Class of Fuzzy Numbers(Fuzznum)
    """

    def function(self, qrung, md, nmd):
        if isinstance(md, (float, int, np.int_, np.float_)) and \
                isinstance(nmd, (float, int, np.int_, np.float_)):
            assert 0. <= md <= 1. and 0. <= nmd <= 1., \
                'ERROR: md and nmd must be betweenZERO and ONE'
            assert 0. <= md ** qrung + nmd ** qrung <= 1., \
                'ERROR: md ** qrung + nmd ** qrung must be between ZERO and ONE.'

            mtype = 'qrofn'
            memDegree = np.round(md, Approx.round)
            nonMemDegree = np.round(nmd, Approx.round)

            return mtype, memDegree, nonMemDegree

        if isinstance(md, tuple) and isinstance(nmd, tuple):
            assert len(md) == 2 and len(nmd) == 2, \
                'ERROR: The data format contains at least upper and lower bounds.'
            assert md[0] <= md[1] and nmd[0] <= nmd[1], \
                'ERROR: The upper of membership and non-membership must be greater than the lower.'
            assert 0. <= md[0] <= 1. and 0. <= md[1] <= 1., \
                'ERROR: The upper and lower of membership degree must be between 0 and 1.'
            assert 0. <= nmd[0] <= 1. and 0. <= nmd[1] <= 1., \
                'ERROR: The upper and lower of non-membership degree must be between 0 and 1.'
            assert 0. <= md[0] ** qrung + nmd[0] ** qrung <= 1. and 0. <= md[1] ** qrung + nmd[1] ** qrung <= 1., \
                'ERROR: The q powers sum of membership degree and non-membership degree must be between 0 and 1.'

            mtype = 'ivfn'
            memDegree = np.round(md, Approx.round)
            nonMemDegree = np.round(nmd, Approx.round)

            return mtype, memDegree, nonMemDegree

        if isinstance(md, (list, np.ndarray)) and isinstance(nmd, (list, np.ndarray)):
            mds = np.asarray(md)
            nmds = np.asarray(nmd)
            if mds.size == 0 and nmds.size == 0:
                pass
            if mds.size == 0 and nmds.size != 0:
                assert np.max(nmds) <= 1 and np.min(nmds) >= 0, \
                    'non-membership degrees must be in the interval [0,1].'
            if mds.size != 0 and nmds.size == 0:
                assert np.max(mds) <= 1 and np.min(mds) >= 0, \
                    'membership degrees must be in the interval [0,1].'
            if mds.size > 0 and nmds.size > 0:
                assert np.max(mds) <= 1 and np.max(nmds) <= 1 and \
                       np.min(mds) >= 0 and np.min(nmds) >= 0, 'ERROR: must be in [0,1].'
                assert 0 <= np.max(mds) ** qrung + np.max(nmds) ** qrung <= 1, 'ERROR'

            mtype = 'qrohfn'
            memDegree = np.round(md, Approx.round)
            nonMemDegree = np.round(nmd, Approx.round)

            return mtype, memDegree, nonMemDegree

        raise TypeError(f'Unsupported data type or type error, md:{type(md)} and nmd:{type(nmd)}.')


def initializeNum(qrung, md, nmd):
    return InitializeNum()(qrung, md, nmd)


class InitializeSet(Function):
    def function(self, qrung, mtype):
        if qrung is not None or mtype is not None:
            from .base import FuzzType
            assert mtype in FuzzType, f'Unsupported fuzzy types, mtype:{mtype}.'
            assert qrung > 0, f'Qrung must be greater than 0, qrung:{qrung}.'

            qrung = qrung
            mtype = mtype
        else:
            qrung = None
            mtype = None
        return qrung, mtype


def initializeSet(qrung, mtype):
    return InitializeSet()(qrung, mtype)


class Validity(Function):
    def function(self, x):
        from .nums import Fuzznum
        from .array import Fuzzarray
        if isinstance(x, Fuzznum):
            if x.mtype == 'qrofn':
                if 0. <= x.md <= 1. and 0. <= x.nmd <= 1. \
                        and 0. <= x.md ** x.qrung + x.nmd ** x.qrung <= 1.:
                    return True
                else:
                    return False
            if x.mtype == 'ivfn':
                if not len(x.md) == 2 and len(x.nmd) == 2:
                    return False
                elif not 0. <= np.all(x.md) <= 1. and 0. <= np.all(x.md) <= 1.:
                    return False
                elif not (x.md[0] <= x.md[1] and x.nmd[0] <= x.nmd[1]):
                    return False
                elif not 0. <= x.md[1] ** x.qrung + x.nmd[1] ** x.qrung <= 1.:
                    return False
                else:
                    return True
            if x.mtype == 'qrohfn':
                a1 = x.md.size == 0 and x.nmd.size == 0
                a2 = x.md.size == 0 and 0. <= x.nmd.all() <= 1.
                a3 = x.nmd.size == 0 and 0. <= x.md.all() <= 1.
                a4 = min(x.md) >= 0. and min(x.nmd) >= 0. and max(x.md) ** x.qrung + max(
                    x.nmd) ** x.qrung <= 1.
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
            raise TypeError(f'Unsupported mtype(type:{x.mtype}).')
        if isinstance(x, Fuzzarray):
            vec_func = np.vectorize(lambda u: isValid(u))
            return vec_func(x.array)


def isValid(x):
    return Validity()(x)


class Empty(Function):
    def function(self, x, onlyfn):
        from .nums import Fuzznum
        from .array import Fuzzarray
        if isinstance(x, Fuzznum):
            if x.mtype == 'qrofn':
                if x.md is None and x.nmd is None:
                    return True
                else:
                    return False
            if x.mtype == 'ivfn':
                if x.md is None and x.nmd is None:
                    return True
                else:
                    return False
            if x.mtype == 'qrohfn':
                if x.md.size == 0 and x.nmd.size == 0:
                    return True
                else:
                    return False
            raise TypeError(f'Unsupported mtype, ,type:{x.mtype}.')
        if isinstance(x, Fuzzarray):
            if onlyfn:
                vec_func = np.vectorize(lambda u: isEmpty(u, onlyfn))
                return vec_func(x.array)
            else:
                return True if x.size == 0 else False


def isEmpty(x, onlyfn=False):
    return Empty()(x, onlyfn)


class Initial(Function):
    """
        Determine whether the fuzzy set or fuzzy number is the initialized
        fuzzy set or fuzzy number
    """

    def function(self, x):
        from .nums import Fuzznum
        from .array import Fuzzarray
        if isinstance(x, Fuzznum):
            if x.qrung is not None:
                return False
            if x.mtype is not None:
                return False
            if x.md is not None:
                return False
            if x.nmd is not None:
                return False
            return True
        if isinstance(x, Fuzzarray):
            if x.qrung is not None:
                return False
            if x.mtype is not None:
                return False
            if x.array.size != 0:
                return False
            return True


def isInitial(x):
    return Initial()(x)


class Convert(Function):
    def function(self, x):
        from .nums import Fuzznum
        if isinstance(x, Fuzznum):
            if x.mtype == 'qrofn':
                return x.md, x.nmd
            if x.mtype == 'ivfn':
                return x.md.tolist(), x.nmd.tolist()
            if x.mtype == 'qrohfn':
                return x.md.tolist(), x.nmd.tolist()
        raise TypeError(f'Unsupported type: {type(x)}.')


def convert(x):
    return Convert()(x)


class Qsort(Function):
    def function(self, x, reverse=True):
        from .nums import Fuzznum
        from .array import Fuzzarray
        if isinstance(x, Fuzznum):
            if x.mtype == 'qrohfn':
                newfn = copy.deepcopy(x)
                if reverse:
                    newfn.md = np.sort(x.md)
                    newfn.nmd = np.sort(x.nmd)
                else:
                    newfn.md = np.abs(np.sort(-x.md))
                    newfn.nmd = np.abs(np.sort(-x.nmd))
                return newfn
            else:
                return x
        if isinstance(x, Fuzzarray):
            vec_func = np.vectorize(lambda u: qsort(u, reverse=reverse))
            newset = Fuzzarray(x.qrung, x.mtype)
            newset.array = vec_func(x.array)
            return newset


def qsort(x, reverse=True):
    return Qsort()(x, reverse)


class Unique(Function):
    """
        Simplify the membership and non-membership degrees with Approx.round precision
    """

    def function(self, x, onlyfn=False):
        from .nums import Fuzznum
        from .array import Fuzzarray
        if isinstance(x, Fuzznum):
            if x.mtype == 'qrohfn':
                t = copy.deepcopy(x)
                t.md = np.unique(x.md)
                t.nmd = np.unique(x.nmd)
                return t
            else:
                return x
        if isinstance(x, Fuzzarray):
            if onlyfn:
                vec_func = np.vectorize(lambda u: unique(u, onlyfn))
                newset = Fuzzarray(x.qrung, x.mtype)
                newset.array = vec_func(x.array)
                return newset
            else:
                uni = np.unique(x.array)
                newset = Fuzzarray(x.qrung, x.mtype)
                newset.array = uni
                return newset


def unique(x, onlyfn=False):
    return Unique()(x, onlyfn)


class Transpose(Function):
    def function(self, x):
        from .nums import Fuzznum
        from .array import Fuzzarray
        if isinstance(x, Fuzznum):
            return copy.copy(x)
        if isinstance(x, Fuzzarray):
            st = x.array
            s = st.T

            newset = Fuzzarray(x.qrung, x.mtype)
            newset.array = s
            del st, s
            return newset


def transpose(x):
    return Transpose()(x)


class Append(Function):
    """
        1. 模糊数 + 模糊数
        2. 模糊数 + 模糊集
        3. 模糊集 + 模糊数
        4. 模糊集 + 模糊集
    """

    def function(self, x, e):
        from .nums import Fuzznum
        from .array import Fuzzarray
        if isinstance(x, Fuzznum) and isinstance(e, Fuzznum):
            assert x.qrung == e.qrung, f'qrung mismatch(x.qrung:{x.qrung} and e.qrung:{e.qrung}).'
            assert x.mtype == e.mtype, f'mtype mismatch(x.mtype:{x.mtype} and e.mtype:{e.mtype}).'
            newset = Fuzzarray(x.qrung, x.mtype)
            newset.array = np.append(newset.array, [x, e])
            return newset
        if isinstance(x, Fuzznum) and isinstance(e, Fuzzarray):
            if e.mtype is not None and e.qrung is not None:
                assert x.qrung == e.qrung, f'qrung mismatch(x.qrung:{x.qrung} and e.qrung:{e.qrung}).'
                assert x.mtype == e.mtype, f'mtype mismatch(x.mtype:{x.mtype} and e.mtype:{e.mtype}).'
                e.array = np.insert(e.array, 0, x)
                return e
            else:
                e.qrung = x.qrung
                e.mtype = x.mtype
                e.array = np.append(e.array, x)
                return e
        if isinstance(x, Fuzzarray) and isinstance(e, Fuzznum):
            if x.mtype is not None and x.qrung is not None:
                assert x.qrung == e.qrung, f'qrung mismatch(x.qrung:{x.qrung} and e.qrung:{e.qrung}).'
                assert x.mtype == e.mtype, f'mtype mismatch(x.mtype:{x.mtype} and e.mtype:{e.mtype}).'
                x.array = np.append(x.array, e)
                return x
            else:
                x.qrung = e.qrung
                x.mtype = e.mtype
                x.array = np.append(x.array, e)
                return x
        if isinstance(x, Fuzzarray) and isinstance(e, Fuzzarray):
            if x.mtype is not None and x.qrung is not None and e.mtype is not None and e.qrung is not None:
                assert x.qrung == e.qrung, f'qrung mismatch(x.qrung:{x.qrung} and e.qrung:{e.qrung}).'
                assert x.mtype == e.mtype, f'mtype mismatch(x.mtype:{x.mtype} and e.mtype:{e.mtype}).'
                x.array = np.append(x.array, e.array)
                return x
            elif x.mtype is not None and x.qrung is not None and e.mtype is None and e.qrung is None:
                x.array = np.append(x.array, e.array)
                return x
            elif x.mtype is None and x.qrung is None and e.mtype is not None and e.qrung is not None:
                e.array = np.append(e.array, x.array)
                return e
            else:
                return x
        raise TypeError(f'Unsupported type({type(x)} and {type(e)}).')


def append(x, e):
    return Append()(x, e)


class Remove(Function):
    def function(self, x, e):
        from .nums import Fuzznum
        from .array import Fuzzarray
        if isinstance(x, Fuzznum):
            raise ValueError(f'Deletion is not supported for {str(x)}')
        if isinstance(x, Fuzzarray):
            assert x.size > 0, 'The set is empty, can not be removed.'
            assert e in x.array, f'{x} is not in the set.'
            x.array = np.delete(x.array, np.where(x.array == e))
            return x


def remove(x, e):
    return Remove()(x, e)


class Pop(Function):
    def function(self, x, i):
        from .nums import Fuzznum
        from .array import Fuzzarray
        if isinstance(x, Fuzznum):
            raise ValueError(f'Deletion is not supported for {str(x)}')
        if isinstance(x, Fuzzarray):
            x.array = np.delete(x.array, i)
            return x


def pop(x, e):
    return Pop()(x, e)


class Reshape(Function):
    def function(self, x, *shape):
        from .nums import Fuzznum
        from .array import Fuzzarray
        if isinstance(x, Fuzznum):
            newset = Fuzzarray(x.qrung, x.mtype)
            newset.array = np.reshape(x, *shape)
            return newset
        if isinstance(x, Fuzzarray):
            newset = Fuzzarray(x.qrung, x.mtype)
            newset.array = x.array.reshape(*shape)
            return newset


def reshape(x, *shape):
    return Reshape()(x, *shape)


class Squeeze(Function):
    def function(self, x, axis):
        from .nums import Fuzznum
        from .array import Fuzzarray
        if isinstance(x, Fuzznum):
            return x
        if isinstance(x, Fuzzarray):
            newset = Fuzzarray(x.qrung, x.mtype)
            newset.array = np.squeeze(x.array, axis)
            return newset


def squeeze(x, axis=None):
    return Squeeze()(x, axis)


class Broadcast(Function):
    def function(self, x, shape):
        from .nums import Fuzznum
        from .array import Fuzzarray
        if isinstance(x, Fuzznum):
            newset = Fuzzarray(x.qrung, x.mtype)
            newset.array = np.broadcast_to(x, shape)
            return newset
        if isinstance(x, Fuzzarray):
            newset = Fuzzarray(x.qrung, x.mtype)
            newset.array = np.broadcast_to(x.array, shape)
            return newset


def broadcast_to(x, shape):
    return Broadcast()(x, shape)


class Clear(Function):
    def function(self, x):
        from .nums import Fuzznum
        from .array import Fuzzarray
        if isinstance(x, Fuzznum):
            x.qrung = None
            x.mtype = None
            x.md = None
            x.nmd = None
            return x
        if isinstance(x, Fuzzarray):
            x.array = np.array([], dtype=object)
            x.qrung = None
            x.mtype = None
            return x


def clear(x):
    return Clear()(x)


class Ravel(Function):
    def function(self, x):
        from .nums import Fuzznum
        from .array import Fuzzarray
        if isinstance(x, Fuzznum):
            newset = Fuzzarray(x.qrung, x.mtype)
            newset.array = np.ravel(x)
            return newset
        if isinstance(x, Fuzzarray):
            newset = Fuzzarray(x.qrung, x.mtype)
            newset.array = np.ravel(x.array)
            return newset


def ravel(x):
    return Ravel()(x)


class Flatten(Function):
    def function(self, x):
        from .nums import Fuzznum
        from .array import Fuzzarray
        if isinstance(x, Fuzznum):
            newset = Fuzzarray(x.qrung, x.mtype)
            newset.array = np.array([x])
            return newset
        if isinstance(x, Fuzzarray):
            newset = Fuzzarray(x.qrung, x.mtype)
            newset.array = x.array.flatten()
            return newset


def flatten(x):
    return Flatten()(x)


class GetMax(Function):
    def function(self, x, show, axis):
        from .nums import Fuzznum
        from .array import Fuzzarray
        if isinstance(x, Fuzznum):
            return x
        if isinstance(x, Fuzzarray):
            if axis is None:
                index = np.unravel_index(np.argmax(x.array), x.shape)
                if show:
                    print(index)
                return x.array[index]
            else:
                m = np.max(x.array, axis=axis)
                if isinstance(m, Fuzznum):
                    return m
                if isinstance(m, np.ndarray):
                    newset = Fuzzarray(x.qrung, x.mtype)
                    newset.array = m
                    return newset


def getmax(x, show=False, axis=None):
    return GetMax()(x, show, axis)


class GetMin(Function):
    def function(self, x, show, axis):
        from .nums import Fuzznum
        from .array import Fuzzarray
        if isinstance(x, Fuzznum):
            return x
        if isinstance(x, Fuzzarray):
            if axis is None:
                index = np.unravel_index(np.argmin(x.array), x.shape)
                if show:
                    print(index)
                return x.array[index]
            else:
                m = np.min(x.array, axis=axis)
                if isinstance(m, Fuzznum):
                    return m
                if isinstance(m, np.ndarray):
                    newset = Fuzzarray(x.qrung, x.mtype)
                    newset.array = m
                    return newset


def getmin(x, show=False, axis=None):
    return GetMin()(x, show, axis)


class GetFmax(Function):
    def function(self, x, func, *args, show, axis):
        from .nums import Fuzznum
        from .array import Fuzzarray
        if isinstance(x, Fuzznum):
            raise TypeError(f'Unsupported type({type(x)})')
        if isinstance(x, Fuzzarray):
            slist = func(x.array, *args)
            if axis is None:
                index = np.unravel_index(np.argmax(slist), x.shape)
                if show:
                    print(index)
                return x.array[index]
            else:
                m = np.max(slist, axis=axis)
                if isinstance(m, Fuzznum):
                    return m
                if isinstance(slist, np.ndarray):
                    newset = Fuzzarray(x.qrung, x.mtype)
                    newset.array = m
                    return newset


def fmax(x, func, *args, show=False, axis=None):
    return GetMax()(x, func, *args, show, axis)


class GetFmin(Function):
    def function(self, x, func, *args, show, axis):
        from .nums import Fuzznum
        from .array import Fuzzarray
        if isinstance(x, Fuzznum):
            raise TypeError(f'Unsupported type({type(x)})')
        if isinstance(x, Fuzzarray):
            slist = func(x.array, *args)
            if axis is None:
                index = np.unravel_index(np.argmin(slist), x.shape)
                if show:
                    print(index)
                return x.array[index]
            else:
                m = np.min(slist, axis=axis)
                if isinstance(m, Fuzznum):
                    return m
                if isinstance(slist, np.ndarray):
                    newset = Fuzzarray(x.qrung, x.mtype)
                    newset.array = m
                    return newset


def fmin(x, func, *args, show=False, axis=None):
    return GetFmin()(x, func, *args, show, axis)


class GetSum(Function):
    def function(self, x, axis, keepdims):
        from .nums import Fuzznum
        from .array import Fuzzarray
        if isinstance(x, Fuzznum):
            return x
        if isinstance(x, Fuzzarray):
            if axis is None:
                return np.sum(x.array)
            else:
                s = np.sum(x.array, axis=axis, keepdims=keepdims)
                if isinstance(s, Fuzznum):
                    return s
                if isinstance(s, np.ndarray):
                    newset = Fuzzarray(x.qrung, x.mtype)
                    newset.array = s
                    return newset


def getsum(x, axis=None, keepdims=False):
    return GetSum()(x, axis, keepdims)


class GetProd(Function):
    def function(self, x, axis, keepdims):
        from .nums import Fuzznum
        from .array import Fuzzarray
        if isinstance(x, Fuzznum):
            return x
        if isinstance(x, Fuzzarray):
            if axis is None:
                return np.prod(x.array)
            else:
                s = np.prod(x.array, axis=axis, keepdims=keepdims)
                if isinstance(s, Fuzznum):
                    return s
                if isinstance(s, np.ndarray):
                    newset = Fuzzarray(x.qrung, x.mtype)
                    newset.array = s
                    return newset


def getprod(x, axis=None, keepdims=False):
    return GetProd()(x, axis, keepdims)


class Mean(Function):
    def function(self, x, axis):
        from .nums import Fuzznum
        from .array import Fuzzarray
        if isinstance(x, Fuzznum):
            return x
        if isinstance(x, Fuzzarray):
            if axis is None:
                return np.mean(x.array)
            else:
                s = np.mean(x.array, axis=axis)
                if isinstance(s, Fuzznum):
                    return s
                if isinstance(s, np.ndarray):
                    newset = Fuzzarray(x.qrung, x.mtype)
                    newset.array = s
                    return newset


def mean(x, axis=None):
    return Mean()(x, axis)


class Normalize(Function):
    def function(self, d1, d2, t):
        """
            The normalization function for two q-rung orthopair hesitant fuzzy numbers.
                The parameter 't' is the risk factor of normalization process, which in
                the interval [0, 1]. 't=1' indicates optimistic normalization and
                't=0' indicates pessimistic normalization.

            Parameters
            ----------
                d1 : Fuzznum
                    The first q-rung orthopair hesitant fuzzy number
                d2 : Fuzznum
                    The second q-rung orthopair hesitant fuzzy number
                t : float or np.float_
                    The risk factor of normalization process

            References
            ----------
                A. R. Mishra, S.-M. Chen, and P. Rani, “Multiattribute decision-making
                based on Fermatean hesitant fuzzy sets and modified VIKOR method,”
                Inform Sciences, vol. 607, pp. 1532–1549, 2022, doi: 10.1016/j.ins.2022.06.037.
        """
        if d1.mtype == d2.mtype == 'qrohfn':
            def __adj(d, tm):
                return tm * d.max() + (1. - tm) * d.min()

            d_1 = copy.deepcopy(d1)
            d_2 = copy.deepcopy(d2)

            md_len = len(d_1.md) - len(d_2.md)
            nmd_len = len(d_1.nmd) - len(d_2.nmd)

            if md_len > 0:
                # Explain that the number of membership elements in d1 is greater than d2,
                # and it is necessary to add elements of d2 membership.
                i = 0.
                m = d_2.md
                while i < md_len:
                    d_2.md = np.append(d_2.md, __adj(m, t))
                    i += 1
            else:
                # Explain that the number of membership elements in d1 is less than d2,
                # and it is necessary to increase the elements of d1 membership.
                i = 0.
                m = d_1.md
                while i < (-md_len):
                    d_1.md = np.append(d_1.md, __adj(m, t))
                    i += 1

            if nmd_len > 0:
                # Explain that the number of membership elements in d1 is greater than d2,
                # and it is necessary to add elements of d2 membership.
                i = 0.
                u = d_2.nmd
                while i < nmd_len:
                    d_2.nmd = np.append(d_2.nmd, __adj(u, t))
                    i += 1
            else:
                i = 0.
                u = d_1.nmd
                while i < (-nmd_len):
                    d_1.nmd = np.append(d_1.nmd, __adj(u, t))
                    i += 1
            return d_1.qsort(), d_2.qsort()
        else:
            raise TypeError(f'Unsupported fuzzy type, {d1.mtype} and {d2.mtype}')


def normalize(d1, d2, t=1.):
    return Normalize()(d1, d2, t)


# TODO：待实现
class Absolute(Function):
    def function(self, x, y):
        pass


def absolute(x, y):
    return Absolute()(x, y)


# class FuzzNum(Function):
#     """
#         The method of generating fuzzy numbers is encapsulated in a fuzzy number
#         class, which only generates fuzzy numbers and does not undertake other
#         functions.
#         'function' returns a fuzzy number of type Fuzznum
#     """
#
#     def function(self, qrung, md, nmd):
#         from .nums import Fuzznum
#         return Fuzznum(qrung, md, nmd)
#
#
# def fuzznum(qrung=None, md=None, nmd=None):
#     return FuzzNum()(qrung, md, nmd)
#
#
# class FuzzSet(Function):
#     """
#         This class is just a class for generating a fuzzy array,
#             specifically implemented with function. Similar to the numpy.array method.
#     """
#
#     def function(self, x):
#         from .array import Fuzzarray
#         from .nums import Fuzznum
#         if x is None:
#             return Fuzzarray()
#         y = x
#         if isinstance(x, Fuzznum):
#             fl = np.asarray(y, dtype=object)
#             flat = fl.flatten()
#             r = np.random.choice(flat)
#             newset = Fuzzarray(r.qrung, r.mtype)
#             newset.array = fl
#             return newset
#         if isinstance(x, (list, tuple, np.ndarray)):
#             y = np.asarray(x, dtype=object)
#             y = y.flatten()
#             mt = y[0].mtype
#             for i in y:
#                 if i.mtype != mt:
#                     raise TypeError(f'Unsupported mtype: {i.mtype}.')
#                 mt = i.mtype
#
#             t = np.random.choice(y)
#             qrung = t.qrung
#             mtype = t.mtype
#
#             newset = Fuzzarray(qrung, mtype)
#             newset.array = np.array(x, dtype=object)
#             return newset
#
#         raise TypeError(f'Unsupported type: {type(x)}.')
#
#
# def fuzzset(x=None):
#     return FuzzSet()(x)
