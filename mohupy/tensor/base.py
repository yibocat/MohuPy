#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/7 下午3:04
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import abc


class FuzzTensorBase(abc.ABC):
    """
        FuzzTensorBase is a tensor base based on Fuzzarray
    """


class Function:
    """
        The method base class consists of a call function and
        an abstract function. Among them, function is the concrete
        implementation of its subclass method.
    """

    def __call__(self, *x):
        return self.function(*x)

    def function(self, *x):
        raise NotImplementedError()
