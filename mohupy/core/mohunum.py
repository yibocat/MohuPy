#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/9/29 上午10:38
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

# import numpy as np
# from typing import Union
#
# from .mohu import MohuQROFN, MohuQROIVFN
#
#
# class mohunum(MohuQROFN, MohuQROIVFN):
#
#     def __init__(self, qrung, md, nmd):
#         """
#         Parameters
#         ----------
#             qrung: int, np.int_
#                 The qrung number.
#             md: float, int, np.int_, np.float_, list, tuple, np.ndarray
#                 The membership degree
#             nmd: float, int, np.int_, np.float_, list, tuple, np.ndarray
#                 The non-membership degree
#         """
#         if isinstance(md, Union[float, int, np.int_, np.float_]) and \
#                 isinstance(nmd, Union[float, int, np.int_, np.float_]):
#             MohuQROFN.__init__(self, qrung, md, nmd)
#         elif isinstance(md, Union[list, tuple, np.ndarray]) and \
#                 isinstance(nmd, Union[list, tuple, np.ndarray]):
#             MohuQROIVFN.__init__(self, qrung, md, nmd)
#
#     def __repr__(self):
#         if self.mtype == 'qrofn':
#             return MohuQROFN.__repr__(self)
#         if self.mtype == 'ivfn':
#             return MohuQROIVFN.__repr__(self)
#
#     def __str__(self):
#         if self.mtype == 'qrofn':
#             return MohuQROFN.__str__(self)
#         if self.mtype == 'ivfn':
#             return MohuQROIVFN.__str__(self)
#
#     @property
#     def score(self):
#         if self.mtype == 'qrofn':
#             return MohuQROFN.score(self)
#         if self.mtype == 'ivfn':
#             return MohuQROIVFN.score(self)
#
#     @property
#     def acc(self):
#         if self.mtype == 'qrofn':
#             return MohuQROFN.acc(self)
#         if self.mtype == 'ivfn':
#             return MohuQROIVFN.acc(self)
#
#     @property
#     def ind(self):
#         if self.mtype == 'qrofn':
#             return MohuQROFN.ind(self)
#         if self.mtype == 'ivfn':
#             return MohuQROIVFN.ind(self)
#
#     @property
#     def comp(self):
#         if self.mtype == 'qrofn':
#             return MohuQROFN.comp(self)
#         if self.mtype == 'ivfn':
#             return MohuQROIVFN.comp(self)
#
#     @property
#     def T(self):
#         newfn = mohunum(self.qrung, self.md, self.nmd)
#         return newfn
#
#     def is_valid(self):
#         if self.mtype == 'qrofn':
#             return MohuQROFN.is_valid(self)
#         if self.mtype == 'ivfn':
#             return MohuQROIVFN.is_valid(self)
#
#     def isEmpty(self):
#         if self.mtype == 'qrofn':
#             return MohuQROFN.isEmpty(self)
#         if self.mtype == 'ivfn':
#             return MohuQROIVFN.isEmpty(self)
#
#     def convert(self):
#         if self.mtype == 'qrofn':
#             return MohuQROFN.convert(self)
#         if self.mtype == 'ivfn':
#             return MohuQROIVFN.convert(self)
#
#     def reshape(self, *n):
#         from ..utils import asfuzzset
#         if n == (1,):
#             return asfuzzset([self])
#         raise ValueError(f'cannot reshape mohunum of size {self.size} to {n}')
#
#     def plot(self,
#              other=None,
#              area=None,
#              color='red',
#              color_area=None,
#              alpha=0.3):
#         if self.mtype == 'qrofn':
#             return MohuQROFN.plot(self, other, area, color, color_area, alpha)
#         if self.mtype == 'ivfn':
#             return MohuQROIVFN.plot(self, other, color, alpha)


from typing import Union
from .interface import mohuParent

import numpy as np


def mohunum(qrung, md, nmd):
    """
        Dynamically inherit factory function to determine which type of fuzzy
        number is inherited based on the input. Note that mohuParent is a dynamically
        inherited parent class function. The parent class can be Q-rung orthopair
        fuzzy number or interval-valued q-rung orthopair fuzzy. number, or even a
        custom fuzzy number type.

        fuzzyType represents the currently registered fuzzy type, and mohuParent
        represents the currently inherited fuzzy type.
    """
    mohuType = None

    if isinstance(md, Union[int, float, np.int_, np.float_]) and \
            isinstance(nmd, Union[int, float, np.int_, np.float_]):
        mohuType = 'qrofn'

    if isinstance(md, tuple) and isinstance(nmd, tuple):
        mohuType = 'ivfn'

    if isinstance(md, Union[list, np.ndarray]) and isinstance(nmd, Union[list, np.ndarray]):
        mohuType = 'qrohfn'

    from .mohu import fuzzType
    return mohuParent(fuzzType.get(mohuType))(qrung, md, nmd)
