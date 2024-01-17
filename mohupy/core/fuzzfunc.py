#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/12/23 下午2:59
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import numpy as np
from .nums import Fuzznum
from .array import Fuzzarray


class FuzzFunc:
    """
        The method base class consists of a call function and an abstract function.
        Among them, function is the concrete implementation of its subclass method.
    """

    def __call__(self, *x):
        return self.function(*x)

    def function(self, *x):
        raise NotImplementedError()


class FuzzNum(FuzzFunc):
    """
        The method of generating fuzzy numbers is encapsulated in a fuzzy number
        class, which only generates fuzzy numbers and does not undertake other
        functions.
        'function' returns a fuzzy number of type Fuzznum
    """

    def function(self, qrung, md, nmd):
        return Fuzznum(qrung, md, nmd)


def fuzznum(qrung=None, md=None, nmd=None) -> Fuzznum:
    return FuzzNum()(qrung, md, nmd)


class FuzzSet(FuzzFunc):
    """
        This class is just a class for generating a fuzzy array,
            specifically implemented with function. Similar to the numpy.array method.
    """

    def function(self, x):
        if x is None:
            return Fuzzarray()
        y = x
        if isinstance(x, Fuzznum):
            fl = np.asarray(y, dtype=object)
            flat = fl.flatten()
            r = np.random.choice(flat)
            newset = Fuzzarray(r.qrung, r.mtype)
            newset.array = fl
            return newset
        if isinstance(x, (list, tuple, np.ndarray)):
            y = np.asarray(x, dtype=object)
            y = y.flatten()
            mt = y[0].mtype
            for i in y:
                if i.mtype != mt:
                    raise TypeError(f'Unsupported mtype: {i.mtype}.')
                mt = i.mtype

            t = np.random.choice(y)
            qrung = t.qrung
            mtype = t.mtype

            newset = Fuzzarray(qrung, mtype)
            newset.array = np.array(x, dtype=object)
            return newset

        raise TypeError(f'Unsupported type: {type(x)}.')


def fuzzset(x=None) -> Fuzzarray:
    return FuzzSet()(x)
