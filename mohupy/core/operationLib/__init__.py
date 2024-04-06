#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/6 下午2:42
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

archimedeanDict = dict()
__all__ = []

from .algebraicoperation import algebAdd, algebSub, algebMul, algebDiv, algebPow, algebTim
archimedeanDict['algebraic'] = {'add': algebAdd,
                                'sub': algebSub,
                                'mul': algebMul,
                                'div': algebDiv,
                                'pow': algebPow,
                                'tim': algebTim}

__all__ += ['archimedeanDict']