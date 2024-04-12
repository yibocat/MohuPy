#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/9/30 下午5:49
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

# from .core.interface import mohuParent

# Initialize fuzzy parent class, also indicates the currently used fuzzy number type
# It is worth noting: fuzzyParent is a dictionary whose keys represent parent classes
# and values represent subclasses.
# fuzzParent = mohuParent.memo

from .corelib.regedit import *
from .core import FuzzType, archimedeanDict
from .corelib.regedit import (fuzzZeros, fuzzPoss, fuzzNegs,
                              fuzzDis, fuzzString, fuzzRandom, fuzzPlot)


class info:
    type = FuzzType
    archDict = archimedeanDict

    zeros = fuzzZeros
    poss = fuzzPoss
    negs = fuzzNegs
    distance = fuzzDis
    string = fuzzString
    random = fuzzRandom
    plotlib = fuzzPlot


class runtime:
    ...
