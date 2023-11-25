#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/9/21 下午8:25
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import numpy as np


def choquet(e: (list, np.ndarray), func, *args, measurable_func=None, info=False, summation=True):
    """
         Choquet integral based on arbitrary fuzzy measures over a subset of a
            fixed set.

        For the existing set of fuzzy measures and a measurable
            function, if the measurable function is None, then directly calculate
            the Choquet Integral corresponding to each fuzzy measure. Otherwise,
            computes the value corresponding to the measurable function.

        Parameters
        ----------
            e: list, np.ndarray
                The subset of Choquet integrals to be found.
            func: function
                The fuzzy measure function.
                Optional: dirac_meas, add_meas, sym_meas, lambda_meas, zeta_trans
            args : list
                The fixed sets.
            measurable_func: function
                The measurable function.
            info: bool
                Whether to print intermediate information.
            summation:  bool
                summation or not

        Returns
        -------
            np.float_
            The Choquet integral.

        Examples
        --------
        1.  In [1]: from mohupy import measure as mm
            In [2]: mm.choquet([0.4,0.25,0.37,0.2], mm.lambda_meas, [0.4,0.25,0.37,0.2])
            Out[2]: 0.34044280478185107
        2.  In [3]: mm.choquet([0.4,0.37,0.2], mm.lambda_meas, [0.4,0.25,0.37,0.2])
            Out[3]: 0.3072721945914217
    """
    assert isinstance(e, (list, np.ndarray)), \
        'ERROR: The subset must be a list or numpy array.'
    assert func is not None, \
        'ERROR: The function must not be None.'
    RI = (np.asarray(*args)     # When no args are set, use the fuzzy measure e directly.
          if measurable_func is None else measurable_func(*args)) if len(args) > 0 else np.asarray(e)
    index = np.argsort(-RI)  # fuzzy measure subscripts in descending sort
    sub = np.sort(e)[::-1]

    p = []
    for i in range(len(index)):
        p.append(func(sub[:i + 1], sub) - func(sub[:i], sub))
    p = np.asarray(p)

    # Arrange the derivatives of the fuzzy measure set function in descending order
    p = p[::-1]

    fz = np.sort(RI)
    if info:
        print('The fuzzy measure: \n' +
              str(e))
        print('The descending sorting of fuzzy measures: \n  '
              + str(sub))
        print('Index of fuzzy measures in ascending order: \n  '
              + str(index + 1))
        print('Descending Order of Function Derivatives of Fuzzy Measure Set: \n  '
              + str(p))
        print('Measurable functions in ascending order: \n  '
              + str(fz))

    integral = np.array([])
    for i in range(len(index)):
        integral = np.append(integral, fz[i] * p[i])
    return sum(integral) if summation else integral


def sugeno(e: (list, np.ndarray), func, *args, measurable_func=None):
    """
        Sugeno integral based on arbitrary fuzzy measures over a subset of a
            fixed set.

        For the existing set of fuzzy measures and a measurable function,
            if the measurable function is None, then directly calculate the
            Sugeno Integral corresponding to each fuzzy measure. Otherwise,
            computes the value corresponding to the measurable function.

        Parameters
        ----------
            e: list, np.ndarray
                The subset of Choquet integrals to be found.
            func: function
                The fuzzy measure function.
                Optional: dirac_meas, add_meas, sym_meas, lambda_meas, zeta_trans
            args : list
                The fixed sets.
            measurable_func: function
                The measurable function.

        Returns
        -------
            np.float_
            The Sugeno integral.

        Examples
        --------
            In [1]: from mohupy import measure as mm
            In [2]: mm.sugeno([0.4,0.25,0.37,0.2], mm.lambda_meas, [0.4,0.25,0.37,0.2])
            Out[2]: 0.4
    """
    assert isinstance(e, (list, np.ndarray)), \
        'ERROR: The subset must be a list or numpy array.'
    assert func is not None, \
        'ERROR: The function must not be None.'
    RI = (np.asarray(*args)     # When no args are set, use the fuzzy measure e directly.
          if measurable_func is None else measurable_func(*args)) if len(args) > 0 else np.asarray(e)

    sub = np.sort(e)
    res = np.array([])
    for i in range(len(sub)):
        res = np.append(res, min(sub[i], func(sub[i:], sub)))
    return np.max(res)


def shilkret(e: (list or np.ndarray), func, *args, measurable_func=None):
    """
        The Shilkret integral is a continuous piecewise linear idempotent
            aggregation function. The Shilkret integral is homogeneous and the
            values of the fuzzy measure are returned at the vertices of the
            unit cube, regardless of whether μ is maxitive.

        Parameters
        ----------
            e: list, np.ndarray
                The subset of Choquet integrals to be found.
            func: function
                The fuzzy measure function.
                Optional: dirac_meas, add_meas, sym_meas, lambda_meas, zeta_trans
            args : list
                The fixed sets.
            measurable_func: function
                The measurable function.

        Returns
        -------
            np.float_
            The Shilkret integral.

        Examples
        --------
            1.  In [1]: from mohupy import measure as mm
                In [2]: mm.shilkret([0.4,0.25,0.37,0.2], mm.lambda_meas, [0.4,0.25,0.37,0.2])
                Out[2]: 0.2607891583171406
            2.  In [3]: mm.shilkret([0.4,0.25], mm.lambda_meas, [0.4,0.25,0.37,0.2])
                Out[3]: 0.16000000000000003
    """
    assert isinstance(e, (list, np.ndarray)), \
        'ERROR: The subset must be a list or numpy array.'
    assert func is not None, \
        'ERROR: The function must not be None.'
    RI = (np.asarray(*args)     # When no args are set, use the fuzzy measure e directly.
          if measurable_func is None else measurable_func(*args)) if len(args) > 0 else np.asarray(e)

    sub = np.sort(e)
    res = np.array([])
    for i in range(len(sub)):
        res = np.append(res, sub[i] * func(sub[i:], sub))
    return np.max(res)
