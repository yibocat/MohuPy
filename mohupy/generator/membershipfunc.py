#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/12 下午1:49
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import numpy as np

from matplotlib import pyplot as plt


class MembershipFunc(object):
    """
        Membership function class. This class organizes 8 commonly used
        membership functions together. In addition, custom membership
        functions can be set.

        The format of the custom membership function is as follows.
        This is just an example, because the function's range is not in
        the 0-1 interval, so the function is not perfect.

        Attributes
        ----------
            __VARI_START:   float or np.float_ or int or np.int_
                Starting value of independent variable range
            __VARI_END:     float or np.float_ or int or np.int_
                Ending value of independent variable range
            __LINSPACE:     int or np.int_
                Accuracy within the range of the independent variable

            __func:         function
                The function of membership degrees. It can be the 8 defined
                functions or a custom function.
            __parameters:   list or tuple
                The parameters of membership function

            domain:        list or tuple
                range of arguments
            linspace:       int or np.int_
                Accuracy within the range of the independent variable


        Methods
        -------
            max():      The maximum value of the function within the
                            range of the independent variable
            min():      The minimum value of the function within the
                            range of the independent variable
            plot():     Plot the graph within the range of the independent
                            variable.

        Notes
        -----
            This class is a class that sets membership functions, and the
                instances created by this class are callable.
    """
    __VARI_START = 0.
    __VARI_END = 1.
    __LINSPACE = 100

    __func = None
    __parameters = None

    def __init__(self, func=None, *args):
        from ..function import (sigmf, trimf, zmf,
                               trapmf, smf, gaussmf,
                               gauss2mf, gbellmf)

        func_list = [sigmf, trimf, zmf, trapmf, smf, gaussmf, gauss2mf, gbellmf]
        if func is None:
            pass
        elif func in func_list:
            self.__func = func
            self.__parameters = args
        else:
            assert hasattr(func, '__call__'), \
                'ERROR: func must be callable or None.'
            self.__func = func
            self.__parameters = args

    def __repr__(self):
        return 'Function: %s , parameters: %s, domain: (%.f, %.f)' \
            % (str(self.__func), str(self.__parameters), self.__VARI_START, self.__VARI_END)

    def __str__(self):
        return 'Function: %s, parameters: %s' % (self.__func.__name__, str(self.__parameters))

    def __call__(self, x):
        return self.__func(x, *self.__parameters)

    @property
    def func(self):
        return self.__func

    @func.setter
    def func(self, func):
        self.__func = func

    @property
    def parameter(self):
        return self.__parameters

    @parameter.setter
    def parameter(self, parameters):
        self.__parameters = parameters

    @property
    def domain(self):
        return self.__VARI_START, self.__VARI_END

    @domain.setter
    def domain(self, domain):
        self.__VARI_START, self.__VARI_END = domain

    @property
    def linspace(self):
        return self.__LINSPACE

    @linspace.setter
    def linspace(self, linspace):
        self.__LINSPACE = linspace

    def max(self):
        x = np.linspace(self.__VARI_START, self.__VARI_END, self.__LINSPACE)
        return np.max(self.__func(x, *self.__parameters))

    def min(self):
        x = np.linspace(self.__VARI_START, self.__VARI_END, self.__LINSPACE)
        return np.min(self.__func(x, *self.__parameters))

    def plot(self, st='Func', figsize=(5, 3)):
        x = np.linspace(self.__VARI_START, self.__VARI_END, self.__LINSPACE)
        y = self.__func(x, *self.__parameters)
        plt.figure(figsize=figsize)
        plt.plot(x, y,
                 label=st + ': %s, parameters: %s' % (self.__func.__name__, self.__parameters))
        plt.grid(linestyle='-.')
        plt.legend()
        plt.show()
