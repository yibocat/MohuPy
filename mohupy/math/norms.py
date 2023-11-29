# #  Copyright (c) yibocat 2023 All Rights Reserved
# #  Python: 3.10.9
# #  Date: 2023/10/1 下午5:03
# #  Author: yibow
# #  Email: yibocat@yeah.net
# #  Software: MohuPy
#
# from ..core.__multi_func import fuzznum
# from .archimedean import *
# from ..core.base import mohunum
#
#
# # TODO: 将爱因斯坦运算注册到范数运算表中，这里暂时写成函数，后期改成爱因斯坦类
#
#
# def ein_plus(f1: mohunum, f2: mohunum) -> mohunum:
#     """
#         The einstein plus of two fuzzy mohunums.
#     """
#     assert f1.qrung == f2.qrung, \
#         'ERROR: The qrung of two fuzzy number must be same.'
#     assert f1.mtype == f2.mtype, \
#         'ERROR: The type of two fuzzy numbers must be same.'
#     q = f1.qrung
#     mtype = f1.mtype
#
#     if mtype == 'qrofn':
#         newfn = fuzznum(q, 0., 0.)
#     elif mtype == 'ivfn':
#         newfn = fuzznum(q, (0., 0.), (0., 0.))
#     else:
#         raise TypeError(f'Invalid mtype {mtype}')
#     newfn.md = einstein_S(f1.md ** q, f2.md ** q) ** (1 / q)
#     newfn.nmd = einstein_T(f1.nmd ** q, f2.nmd ** q) ** (1 / q)
#     return newfn
#
#
# def ein_mul(f1: mohunum, f2: mohunum) -> mohunum:
#     """
#         The einstein multiplication of two fuzzy numbers.
#     """
#     assert f1.qrung == f2.qrung, \
#         'ERROR: The qrung of two fuzzy number must be same.'
#     assert f1.mtype == f2.mtype, \
#         'ERROR: The type of two fuzzy numbers must be same.'
#     q = f1.qrung
#     mtype = f1.mtype
#
#     if mtype == 'qrofn':
#         newfn = fuzznum(q, 0., 0.)
#     elif mtype == 'ivfn':
#         newfn = fuzznum(q, (0., 0.), (0., 0.))
#     else:
#         raise TypeError(f'Invalid mtype {mtype}')
#     newfn.md = einstein_T(f1.md ** q, f2.md ** q) ** (1 / q)
#     newfn.nmd = einstein_S(f1.nmd ** q, f2.nmd ** q) ** (1 / q)
#     return newfn
#
#
# def ein_times(f: mohunum, l) -> mohunum:
#     assert l >= 0, 'The value must be greater than or equal to 0.'
#     q = f.qrung
#     if f.mtype == 'qrofn':
#         newfn = fuzznum(q, 0., 0.)
#     elif f.mtype == 'ivfn':
#         newfn = fuzznum(q, (0., 0.), (0., 0.))
#     else:
#         raise TypeError(f'Invalid mtype {f.mtype}')
#
#     newfn.md = (((1. + f.md ** q) ** l - (1. - f.md ** q) ** l) / (
#             (1. + f.md ** q) ** l + (1. - f.md ** q) ** l)) ** (1. / q)
#     newfn.nmd = ((2. * (f.nmd ** q) ** l) / (
#             (2. - f.nmd ** q) ** l + (f.nmd ** q) ** l)) ** (1. / q)
#     return newfn
#
#
# def ein_power(f: mohunum, l) -> mohunum:
#     assert l >= 0, 'The value must be greater than or equal to 0.'
#     q = f.qrung
#     if f.mtype == 'qrofn':
#         newfn = fuzznum(q, 0., 0.)
#     elif f.mtype == 'ivfn':
#         newfn = fuzznum(q, (0., 0.), (0., 0.))
#     else:
#         raise TypeError(f'Invalid mtype {f.mtype}')
#     newfn.md = ((2. * (f.md ** q) ** l) / (
#             (2. - f.md ** q) ** l + (f.md ** q) ** l)) ** (1. / q)
#     newfn.nmd = (((1. + f.nmd ** q) ** l - (1. - f.nmd ** q) ** l) / (
#             (1. + f.nmd ** q) ** l + (1. - f.nmd ** q) ** l)) ** (1. / q)
#     return newfn
