#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/9/30 下午5:49
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from .core.interface import mohuParent

# Initialize fuzzy parent class, also indicates the currently used fuzzy number type
# It is worth noting: fuzzyParent is a dictionary whose keys represent parent classes
# and values represent subclasses.
fuzzParent = mohuParent.memo

from .core.mohu import fuzzType
from .registry.distance import fuzzDis
from .registry.image import fuzzPlot
from .registry.string2num import fuzzString
from .registry.random import fuzzRandom
from .registry.construct import fuzzZeros, fuzzPoss, fuzzNegs


class info:
    type = fuzzType
    distance = fuzzDis
    plot = fuzzPlot
    string = fuzzString
    random = fuzzRandom
    zeros = fuzzZeros
    poss = fuzzPoss
    negs = fuzzNegs


class runtime:
    ...
