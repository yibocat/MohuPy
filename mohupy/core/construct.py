#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/6 下午3:07
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from typing import Union

import numpy as np

from .fuzznums import Fuzznum
from .fuzzarray import Fuzzarray

from .base import Construct


class FuzzNum(Construct):
    """
        The method of generating fuzzy numbers is encapsulated in a fuzzy number
        class, which only generates fuzzy numbers and does not undertake other
        functions.
        'function' returns a fuzzy number of type Fuzznum
    """

    def function(self, qrung, md, nmd):
        return Fuzznum(qrung, md, nmd)


class FuzzSet(Construct):
    """
        This class is just a class for generating a fuzzy array,
            specifically implemented with function. Similar to the numpy.array method.
    """

    def function(self, x):
        if x is None:
            return Fuzzarray()
        if isinstance(x, Fuzznum):
            newset = Fuzzarray(x.qrung)
            newset.array = x
            return newset
        if isinstance(x, Fuzzarray):
            return x
        if isinstance(x, Union[list, tuple, np.ndarray]):
            y = np.asarray(x, dtype=object)

            t = np.random.choice(y)
            qrung = t.qrung

            def checkdata(data: Fuzznum):
                from ..config import Config
                if data.mtype != Config.mtype:
                    raise TypeError(f'Fuzzy type {data.mtype} and {Config.mtype} do not match.')
                if data.qrung != qrung:
                    raise TypeError(f'Fuzzy qrung {data.qrung} and {qrung} do not match.')
                return True

            vec_checkdata = np.vectorize(checkdata)
            if np.all(vec_checkdata(y)):
                newset = Fuzzarray(qrung)
                newset.array = y
                return newset
        raise TypeError(f'Unsupported type: {type(x)}.')


        # if isinstance(x, Fuzznum):
        #     fl = np.asarray(y, dtype=object)
        #     flat = fl.flatten()
        #     r = np.random.choice(flat)
        #     newset = Fuzzarray(r.qrung, r.mtype)
        #     newset.array = fl
        #     return newset
        # if isinstance(x, (list, tuple, np.ndarray)):
        #     y = np.asarray(x, dtype=object)
        #     y = y.flatten()
        #     mt = y[0].mtype
        #     for i in y:
        #         if i.mtype != mt:
        #             raise TypeError(f'Unsupported mtype: {i.mtype}.')
        #         mt = i.mtype
        #
        #     t = np.random.choice(y)
        #     qrung = t.qrung
        #     mtype = t.mtype
        #
        #     newset = Fuzzarray(qrung, mtype)
        #     newset.array = np.array(x, dtype=object)
        #     return newset
        #
        # raise TypeError(f'Unsupported type: {type(x)}.')


def fuzznum(qrung=None, md=None, nmd=None) -> Fuzznum:
    return FuzzNum()(qrung, md, nmd)


def fuzzset(x=None) -> Fuzzarray:
    return FuzzSet()(x)
