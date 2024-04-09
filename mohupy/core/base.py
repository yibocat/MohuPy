#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/6 下午2:04
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import abc


class MohuBase(abc.ABC):
    """
        MohuBase is an abstract class, which is the base class of
        fuzzy numbers and fuzzy sets.
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


class Attribute:
    def __call__(self, x):
        return self.function(x)

    def function(self, x):
        raise NotImplementedError()


class Archimedean:
    """
        The method base class consists of a call function and an abstract function.
        Among them, function is the concrete implementation of its subclass method.
    """

    def __call__(self, *x):
        return self.function(*x)

    def function(self, *x):
        raise NotImplementedError()


class Operation:
    def __call__(self, *args):
        return self.function(*args)

    def function(self, *args):
        raise NotImplementedError()


class Construct:
    """
        The method base class consists of a call function and an abstract function.
        Among them, function is the concrete implementation of its subclass method.
    """

    def __call__(self, *x):
        return self.function(*x)

    def function(self, *x):
        raise NotImplementedError()


FuzzType = {'qrofn', 'ivfn', 'qrohfn'}
