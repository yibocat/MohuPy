#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/9/29 上午10:37
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

# from .mohu import MohuQROFN, MohuQROIVFN
# from sympy import symbols, Symbol
#
#
# class MohuQROFNSym(MohuQROFN):
#     def __init__(self, md: str = None, nmd: str = None):
#         super(MohuQROFNSym, self).__init__(md=md, nmd=nmd)
#         self.qrung = Symbol('q')
#         self.md = Symbol(md)
#         self.nmd = Symbol(nmd)
#
#     def __repr__(self):
#         return f'<{self.md},{self.nmd}>'
#
#     def __str__(self):
#         return f'<{self.md},{self.nmd}>'
#
#     def __add__(self, other):
#         q = self.qrung
#         newfn = MohuQROFNSym(md='mu', nmd='nu')
#         newfn.md = (self.md ** q + other.md ** q
#                     - self.md ** q * other.md ** q) ** (1 / q)
#         newfn.nmd = self.nmd * other.nmd
#         return newfn
