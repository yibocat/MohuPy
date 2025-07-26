#  Copyright (c) yibocat 2025 All Rights Reserved
#  Python: 3.10.9
#  Date: 2025/7/8 20:49
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy


from .base import Function
from .fuzzy import fuzz_directory


class InitializeNum(Function):

    def __init__(self, mtype):
        self.mtype = mtype

    def function(self, qrung, md, nmd):
        return fuzz_directory[self.mtype](qrung, md, nmd)


# class InitializeSet(Function):
#     def function(self, qrung):
#         if qrung is not None:
#             assert qrung > 0, f'Qrung must be greater than 0, qrung:{qrung}.'
#
#             qrung = qrung
#         else:
#             qrung = None
#
#         return qrung, Config.mtype
