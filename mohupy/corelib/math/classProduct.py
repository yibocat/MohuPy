#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/7 下午2:17
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import numpy as np

from .base import Mathematics
from ...core import Fuzznum, Fuzzarray


class Dot(Mathematics):
    def function(self, x, y):
        """
            Returns the dot product of two Fuzzarray.

            Parameters
            ----------
            x : Fuzzarray or Fuzznum
                The first Fuzzarray or Fuzznum.
            y : Fuzzarray or Fuzznum
                The second Fuzzarray or Fuzznum.

            Returns
            -------
            Fuzzarray or np.float_
                The dot product of x and y.
        """
        if isinstance(x, Fuzznum) and isinstance(y, Fuzznum):
            return x * y

        if isinstance(x, Fuzznum) and isinstance(y, Fuzzarray):
            if y.ndim == 0:
                return np.dot(x, y.array)
            else:
                newset = Fuzzarray(x.qrung)
                result = np.dot(x, y.array)
                newset.array = result
                return newset

        if isinstance(x, Fuzzarray) and isinstance(y, Fuzznum):
            if x.ndim == 0:
                return np.dot(x.array, y)
            else:
                newset = Fuzzarray(x.qrung)
                result = np.dot(x.array, y)
                newset.array = result
                return newset
        if isinstance(x, Fuzzarray) and isinstance(y, Fuzzarray):
            if x.ndim == 0 and y.ndim == 0:
                return np.dot(x.array, y.array)
            else:
                newset = Fuzzarray(x.qrung)
                result = np.dot(x.array, y.array)
                newset.array = result
                return newset
        raise ValueError(f'Invalid input type {type(x)} and {type(y)}')


class Inner(Mathematics):
    def function(self, x, y):
        """
            Returns the inner product of two Fuzzarray.

            Parameters
            ----------
            x : Fuzzarray or Fuzznum
                The first Fuzzarray or Fuzznum.
            y : Fuzzarray or Fuzznum
                The second Fuzzarray or Fuzznum.

            Returns
            -------
            Fuzzarray or np.float_
                The inner product of x and y.
        """
        if isinstance(x, Fuzznum) and isinstance(y, Fuzznum):
            return x * y

        if isinstance(x, Fuzznum) and isinstance(y, Fuzzarray):
            if y.ndim == 0:
                return np.inner(x, y.array)
            else:
                newset = Fuzzarray(x.qrung)
                result = np.inner(x, y.array)
                newset.array = result
                return newset

        if isinstance(x, Fuzzarray) and isinstance(y, Fuzznum):
            if x.ndim == 0:
                return np.inner(x.array, y)
            else:
                newset = Fuzzarray(x.qrung)
                result = np.inner(x.array, y)
                newset.array = result
                return newset
        if isinstance(x, Fuzzarray) and isinstance(y, Fuzzarray):
            if x.ndim == 0 and y.ndim == 0:
                return np.inner(x.array, y.array)
            else:
                newset = Fuzzarray(x.qrung)
                result = np.inner(x.array, y.array)
                newset.array = result
                return newset
        raise ValueError(f'Invalid input type {type(x)} and {type(y)}')


class Outer(Mathematics):
    def function(self, x, y):
        """
            Returns the outer product of two Fuzzarray.

            Parameters
            ----------
            x : Fuzzarray or Fuzznum
                The first Fuzzarray or Fuzznum.
            y : Fuzzarray or Fuzznum
                The second Fuzzarray or Fuzznum.

            Returns
            -------
            Fuzzarray or np.float_
                The outer product of x and y.
        """
        if isinstance(x, Fuzznum) and isinstance(y, Fuzznum):
            result = np.outer(x, y)
            newset = Fuzzarray(x.qrung)
            newset.array = result
            return newset

        if isinstance(x, Fuzznum) and isinstance(y, Fuzzarray):
            newset = Fuzzarray(x.qrung)
            result = np.outer(x, y.array)
            newset.array = result
            return newset

        if isinstance(x, Fuzzarray) and isinstance(y, Fuzznum):
            newset = Fuzzarray(x.qrung)
            result = np.outer(x.array, y)
            newset.array = result
            return newset
        if isinstance(x, Fuzzarray) and isinstance(y, Fuzzarray):
            newset = Fuzzarray(x.qrung)
            result = np.outer(x.array, y.array)
            newset.array = result
            return newset
        raise ValueError(f'Invalid input type {type(x)} and {type(y)}')


class Cartadd(Mathematics):
    def function(self, x, y):
        """
            Returns the cartesian sum of two Fuzzarray.

            Parameters
            ----------
            x : Fuzzarray or Fuzznum
                The first Fuzzarray or Fuzznum.
            y : Fuzzarray or Fuzznum
                The second Fuzzarray or Fuzznum.

            Returns
            -------
            Fuzzarray or np.float_
                The cartesian sum of x and y.
        """
        """
            1. 模糊数 + 模糊数
            2. 模糊数 + 0 维度模糊集
            3. 模糊数 + 模糊集
            
            4. 0 维度模糊集 + 模糊数
            5. 0 维度模糊集 + 0 维度模糊集
            6. 0 维度模糊集 + 模糊集
            
            7. 模糊集 + 模糊数
            8. 模糊集 + 0 维度模糊集
            9. 模糊集 + 模糊集 
        """
        if isinstance(x, Fuzznum) and isinstance(y, Fuzznum):
            return np.add.outer(x, y)
        if isinstance(x, Fuzznum) and isinstance(y, Fuzzarray):
            if y.ndim == 0:
                return np.add.outer(x, y.array)
            else:
                newset = Fuzzarray(x.qrung)
                newset.array = np.add.outer(x, y.array)
                return newset
        if isinstance(x, Fuzzarray) and isinstance(y, Fuzznum):
            if x.ndim == 0:
                return np.add.outer(x.array, y)
            else:
                newset = Fuzzarray(x.qrung)
                newset.array = np.add.outer(x.array, y)
                return newset
        if isinstance(x, Fuzzarray) and isinstance(y, Fuzzarray):
            if x.ndim == 0 and y.ndim == 0:
                return np.add.outer(x.array, y.array)
            else:
                newset = Fuzzarray(x.qrung)
                newset.array = np.add.outer(x.array, y.array)
                return newset


class Cartprod(Mathematics):
    def function(self, x, y):
        """
            Returns the cartesian product of two Fuzzarray.

            Parameters
            ----------
            x : Fuzzarray or Fuzznum
                The first Fuzzarray or Fuzznum.
            y : Fuzzarray or Fuzznum
                The second Fuzzarray or Fuzznum.

            Returns
            -------
            Fuzzarray or np.float_
                The cartesian product of x and y.
        """
        if isinstance(x, Fuzznum) and isinstance(y, Fuzznum):
            newset = Fuzzarray(x.qrung)
            newset.array = np.asarray(np.meshgrid(x, y))
            return newset
        if isinstance(x, Fuzznum) and isinstance(y, Fuzzarray):
            newset = Fuzzarray(x.qrung)
            newset.array = np.asarray(np.meshgrid(x, y.array))
            return newset
        if isinstance(x, Fuzzarray) and isinstance(y, Fuzznum):
            newset = Fuzzarray(x.qrung)
            newset.array = np.asarray(np.meshgrid(x.array, y))
            return newset
        if isinstance(x, Fuzzarray) and isinstance(y, Fuzzarray):
            newset = Fuzzarray(x.qrung)
            newset.array = np.asarray(np.meshgrid(x.array, y.array))
            return newset
