#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/11/26 下午4:10
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import copy

import numpy as np

from ..constant import Approx


class Attribute:
    def __call__(self, x):
        return self.function(x)

    def function(self, x):
        raise NotImplementedError()


class Report(Attribute):
    """
        Report printout
    """

    def function(self, x):
        from .nums import Fuzznum
        if isinstance(x, Fuzznum):
            if x.mtype == 'qrofn':
                return f'<{np.round(x.md, 4)},{np.round(x.nmd, 4)}>'
            if x.mtype == 'ivfn':
                return f'<{np.round(x.md, 4)},{np.round(x.nmd, 4)}>'
            if x.mtype == 'qrohfn':
                if len(x.md) > 8 >= len(x.nmd):
                    return f'<{np.round(x.md[:8], 4)}..., {np.round(x.nmd, 4)}>'
                if len(x.nmd) > 8 >= len(x.md):
                    return f'<{np.round(x.md, 4)}, {np.round(x.nmd[:8], 4)}...>'
                if len(x.md) > 8 and len(x.nmd) > 8:
                    return f'<{np.round(x.md[:8], 4)}..., {np.round(x.nmd[:8], 4)}...>'
                else:
                    return f'<{np.round(x.md, 4)}, {np.round(x.nmd, 4)}>'
            if x.md is None and x.nmd is None:
                return f'<>'
        from .array import Fuzzarray
        if isinstance(x, Fuzzarray):
            p = str(x.array).replace('\n', '\n' + ' ' * 10)
            return f'Fuzzarray({p}, qrung={x.qrung}, mtype={x.mtype})'
        raise TypeError(f'Unsupported data types:{type(x)}.')


def report(x):
    return Report()(x)


class Str(Attribute):
    def function(self, x):
        from .nums import Fuzznum
        if isinstance(x, Fuzznum):
            if x.mtype == 'qrofn':
                return f'<{np.round(x.md, 4)},{np.round(x.nmd, 4)}>'
            if x.mtype == 'ivfn':
                return f'<{np.round(x.md, 4)},{np.round(x.nmd, 4)}>'
            if x.mtype == 'qrohfn':
                if len(x.md) > 8 >= len(x.nmd):
                    return f'<{np.round(x.md[:8], 4)}..., {np.round(x.nmd, 4)}>'
                if len(x.nmd) > 8 >= len(x.md):
                    return f'<{np.round(x.md, 4)}, {np.round(x.nmd[:8], 4)}...>'
                if len(x.md) > 8 and len(x.nmd) > 8:
                    return f'<{np.round(x.md[:8], 4)}..., {np.round(x.nmd[:8], 4)}...>'
                else:
                    return f'<{np.round(x.md, 4)}, {np.round(x.nmd, 4)}>'
            if x.md is None and x.nmd is None:
                return f'<>'
        from .array import Fuzzarray
        if isinstance(x, Fuzzarray):
            return str(x.array)
        raise TypeError(f'Unsupported data types:{type(x)}.')


def string(x):
    return Str()(x)


class Score(Attribute):
    def function(self, x):
        from .nums import Fuzznum
        if isinstance(x, Fuzznum):
            if x.mtype == 'qrofn':
                return x.md ** x.qrung - x.nmd ** x.qrung
            if x.mtype == 'ivfn':
                m = x.md[0] ** x.qrung + x.md[1] ** x.qrung
                n = x.nmd[0] ** x.qrung + x.nmd[1] ** x.qrung
                return (m - n) / 2
            if x.mtype == 'qrohfn':
                if len(x.md) == 0 or len(x.nmd) == 0:
                    return None
                else:
                    mm = ((x.md ** x.qrung).sum()) / len(x.md)
                    nn = ((x.nmd ** x.qrung).sum()) / len(x.nmd)
                    return mm - nn
        from .array import Fuzzarray
        if isinstance(x, Fuzzarray):
            # TODO: 模糊集
            pass


def score(x):
    return Score()(x)


class Accuracy(Attribute):
    def function(self, x):
        from .nums import Fuzznum
        from .array import Fuzzarray
        if isinstance(x, Fuzznum):
            if x.mtype == 'qrofn':
                return x.md ** x.qrung + x.nmd ** x.qrung
            if x.mtype == 'ivfn':
                m = x.md[0] ** x.qrung + x.md[1] ** x.qrung
                n = x.nmd[0] ** x.qrung + x.nmd[1] ** x.qrung
                return (m + n) / 2
            if x.mtype == 'qrohfn':
                if len(x.md) == 0 or len(x.nmd) == 0:
                    return None
                else:
                    mm = ((x.md ** x.qrung).sum()) / len(x.md)
                    nn = ((x.nmd ** x.qrung).sum()) / len(x.nmd)
                    return mm + nn
        if isinstance(x, Fuzzarray):
            # TODO: 模糊集
            pass


def acc(x):
    return Accuracy()(x)


class Indeterminacy(Attribute):
    def function(self, x):
        from .nums import Fuzznum
        from .array import Fuzzarray
        if isinstance(x, Fuzznum):
            if x.mtype == 'qrofn':
                acc = x.md ** x.qrung + x.nmd ** x.qrung
                if acc == np.round(1., Approx.round):
                    return np.round(0., Approx.round)
                else:
                    return (1. - acc) ** (1. / x.qrung)
            if x.mtype == 'ivfn':
                m = x.md[0] ** x.qrung + x.md[1] ** x.qrung
                n = x.nmd[0] ** x.qrung + x.nmd[1] ** x.qrung
                if m + n:
                    return np.round(0., Approx.round)
                else:
                    return (1. - (m + n) / 2) ** (1. / x.qrung)
            if x.mtype == 'qrohfn':
                if len(x.md) == 0 or len(x.nmd) == 0:
                    return None
                else:
                    mm = ((x.md ** x.qrung).sum()) / len(x.md)
                    nn = ((x.nmd ** x.qrung).sum()) / len(x.nmd)
                    if mm + nn == 1.:
                        return np.round(0., Approx.round)
                    else:
                        return (1. - mm - nn) ** (1. / x.qrung)
        if isinstance(x, Fuzzarray):
            # TODO: 模糊集
            pass


def ind(x):
    return Indeterminacy()(x)


class Complement(Attribute):
    def function(self, x):
        from .nums import Fuzznum
        from .array import Fuzzarray
        if isinstance(x, Fuzznum):
            if x.mtype == 'qrofn':
                newf = copy.deepcopy(x)
                newf.md = x.nmd
                newf.nmd = x.md
                return newf
            if x.mtype == 'ivfn':
                newf = copy.deepcopy(x)
                newf.md = x.nmd
                newf.nmd = x.md
                return newf
            if x.mtype == 'qrohfn':
                newfn = copy.deepcopy(x)
                if len(x.md) == 0 and len(x.nmd) != 0:
                    newfn.md = np.array([])
                    newfn.nmd = 1. - np.array(x.nmd)
                elif len(x.md) != 0 and len(x.nmd) == 0:
                    newfn.md = 1. - np.array(x.md)
                    newfn.nmd = np.array([])
                else:
                    newfn.md = x.nmd
                    newfn.nmd = x.md
                return newfn
        if isinstance(x, Fuzzarray):
            # TODO: 模糊集
            pass


def comp(x):
    return Complement()(x)


# class MemDegrees(Attribute):
#     def function(self, x):
#         from .nums import Fuzznum
#         from .array import Fuzzarray
#
#         def membership(t):
#             if isinstance(t.md, (int, float, np.float_, np.int_)):
#                 return np.float_(t.md)
#             if isinstance(t.md, (np.ndarray, list)):
#                 return np.array(t.md, dtype=object)
#         if isinstance(x, Fuzznum):
#             return membership(x)
#         if isinstance(x, Fuzzarray):
#             vec_func = np.vectorize(membership)
#             return vec_func(x.array)
#
#
# def memDegrees(x):
#     return MemDegrees()(x)
#
#
# class NonMemDegrees(Attribute):
#     def function(self, x):
#         from .nums import Fuzznum
#         from .array import Fuzzarray
#
#         def nonmembership(t):
#             if isinstance(t.nmd, (int, float, np.float_, np.int_)):
#                 return np.float_(t.nmd)
#             if isinstance(t.nmd, (np.ndarray, list)):
#                 return np.array(t.nmd, dtype=object)
#         if isinstance(x, Fuzznum):
#             return nonmembership(x)
#         if isinstance(x, Fuzzarray):
#             vec_func = np.vectorize(nonmembership)
#             return vec_func(x.array)
#
#
# def nonMemDegrees(x):
#     return NonMemDegrees()(x)



