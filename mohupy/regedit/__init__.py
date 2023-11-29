#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/11/28 下午3:10
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
__all__ = []

from .construct import fuzzZeros, fuzzPoss, fuzzNegs, fuzzZero, fuzzPos, fuzzNeg

from .distance import fuzzDis
from .str2num import fuzzString
from .random import fuzzRandom
from .plotlib import fuzzPlot

__all__ += [
    'fuzzZeros',
    'fuzzPoss',
    'fuzzNegs',
    'fuzzZero',
    'fuzzPos',
    'fuzzNeg',
    'fuzzDis',
    'fuzzString',
    'fuzzRandom',
    'fuzzPlot',
]

### Archimedean Norms Dictionary(AND)
archimedeanDict = dict()
__all__ += ['archimedeanDict']


### Add algebraic norms to AND
from .algebraic_operation import algebAdd, algebSub, algebMul, algebDiv, algebPow, algebTim
archimedeanDict['algebraic'] = {'add': algebAdd,
                                'sub': algebSub,
                                'mul': algebMul,
                                'div': algebDiv,
                                'pow': algebPow,
                                'tim': algebTim}


