#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/21 上午4:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets

import numpy as np
from matplotlib import pyplot as plt

from .function import (sigmf, trimf, zmf,
                       trapmf, smf, gaussmf,
                       gauss2mf, gbellmf)

fdict = {'sigmf': sigmf,
         'trimf': trimf,
         'zmf': zmf,
         'trapmf': trapmf,
         'smf': smf,
         'gaussmf': gaussmf,
         'gauss2mf': gauss2mf,
         'gbellmf': gbellmf}


class memfunc(object):
    """
        Membership function class. This class organizes 8 commonly used
        membership functions together. In addition, custom membership
        functions can be set.
        Custom membership functions are adjusted according to the 'custom'
        attribute. When custom=True, 'func' is a custom membership function.
        The format of the custom membership function is as follows.
        This is just an example, because the function's range is not in
        the 0-1 interval, so the function is not perfect.
        ---------------------------------
        |   def func_test(x,*p):        |
        |       return p[0]*x + p[1]    |
        ---------------------------------
        Note that when 'custom==True', the attribute 'func' becomes a
        function. When 'custom==False', the attribute 'func' is the function
        name of a common membership function.

        Attributes
        ----------
            __func: str
                the name of the membership function
                (e.g. 'gaussmf')
            __parameter: list
                the parameter of the membership function
                (e.g. [0.1, 0.2, 0.3])
            __variable_start: float
                the start of the independent variable
                (e.g. 0.)
            __variable_end: float
                the end of the independent variable
                (e.g. 1.)
            __linspace: int
                the number of points of the independent variable
                (e.g. 100)
            __custom: bool
                if the membership function is a custom function
                (e.g. True)

            func: function
                the membership function
            parameter:
                the parameter of the membership function
            custom:
                if the membership function is a custom function
            intervalinfo:
                the interval information of the membership function
        Methods
        -------
            __call__(x):
                direct calculation of the membership function
                (e.g. memfunc(0.5))
            __str__(self):
                string representation of the membership function
            __repr__(self):
                string representation of the membership function
                (e.g. 'Function: gaussmf, parameter: [0.1, 0.3]')

            setvariable:
                set the start and end of the independent variable
                (e.g. memfunc.setvariable(0.1, 0.3, 100))
            setfunc:
                set the membership function
                (e.g. memfunc.setfunc('gaussmf', [0.4,0.5]))
            setparameter:
                set the parameter of the membership function
                (e.g. memfunc.setparameter([0.1, 0.2, 0.3]))
            getfunc:
                get the membership function
                (e.g. memfunc.getfunc())
                note: this function returns the function object
            minmd_in_interval:
                get the minimum membership degree in the interval
                (e.g. memfunc.minmd_in_interval())
            maxmd_in_interval:
                get the maximum membership degree in the interval
                (e.g. memfunc.maxmd_in_interval())
            plot:
                plot the membership function
                (e.g. memfunc.plot())
    """

    __func = None
    __parameter = []
    __variable_start = 0.
    __variable_end = 1.
    __linspace = 100
    __custom = False
    __funcnum = 1

    def __init__(self, func, parameter, custom=False):
        self.__funcnum = len(parameter)
        if custom:
            assert hasattr(func, '__call__'), 'custom membership function is not a function class'
            self.__func = func
            self.__parameter = parameter
            self.__custom = True
        else:
            assert func in fdict, 'membership function does not exist.'
            self.__func = func
            self.__parameter = parameter

    def __repr__(self):
        s = ''
        for i in range(self.__funcnum):
            if self.__custom:
                s += 'Function %d: %s, parameter: %s \n' % (i + 1, self.__func.__name__, self.__parameter[i])
            else:
                s += 'Function %d: %s, parameter: %s \n' % (i + 1, self.__func, self.__parameter[i])
        return s

    def __call__(self, x):
        """
        Direct calculation of degree of membership
        Args:
            x:  float or np.ndarray

        Returns:
            float or np.ndarray
            the membership degree of the membership function
        """
        y = []
        for i in range(self.__funcnum):
            if self.__custom:
                y.append(self.__func(x, *self.__parameter[i]))
            else:
                y.append(fdict[self.__func](x, self.__parameter[i]))
        return np.array(y)

    def __str__(self):
        s = ''
        for i in range(self.__funcnum):
            if self.__custom:
                s += 'Function %d: %s, parameter: %s \n' % (i + 1, self.__func.__name__, self.__parameter[i])
            else:
                s += 'Function %d: %s, parameter: %s \n' % (i + 1, self.__func, self.__parameter[i])
        return s

    @property
    def func(self):
        if self.__custom:
            return self.__func.__name__
        else:
            return self.__func

    @property
    def parameter(self):
        return self.__parameter

    @property
    def custom(self):
        return self.__custom

    @property
    def intervalinfo(self):
        """
            Get the interval information of the independent variable.

            Returns:
                tuple: (start, end, linspace)
        """
        return self.__variable_start, self.__variable_end, self.__linspace

    def setvariable(self, start, end, linspace):
        """
            Set the variable range of the independent variable. This
            function is used to generate the spatial extent of
            membership function instances.

            Args:
                start:  float
                    start of the variable range
                end:  float
                    end of the variable range
                linspace:  int
                    number of points in the variable range
        """
        self.__variable_start = start
        self.__variable_end = end
        self.__linspace = linspace

    def setfunc(self, func, parameter, info=False):
        """
            Set the membership function and parameter.

            Args:
                func:  str
                    name of the membership function
                parameter:  list or np.ndarray
                    parameter of the membership function
                info:  bool
                    whether to print the information of the function
        """
        self.__func = func
        self.__parameter = parameter
        if info:
            print(self.__str__())

    def setparameter(self, parameter):
        """
            Set the parameter of the membership function.

            Args:
                parameter:  list or np.ndarray
                    parameter of the membership function
        """
        self.__parameter = parameter

    def getfunc(self):
        """
            Get the membership function.

            Returns: function
                the membership function
        """
        if self.__custom:
            return self.__func
        else:
            return fdict[self.__func]

    def minmd_in_interval(self):
        """
            Get the minimum value in the current setting interval

        Returns: np.float64
            the minimum value in the current setting interval
        """
        x = np.linspace(self.__variable_start, self.__variable_end, self.__linspace)
        return np.min(self(x),axis=1)

    def maxmd_in_interval(self):
        """
            Get the maximum value in the current setting interval

        Returns: np.float64
            the maximum value in the current setting interval
        """
        x = np.linspace(self.__variable_start, self.__variable_end, self.__linspace)
        return np.max(self(x),axis=1)

    def plot(self, st='Func', figsize=(5, 3)):
        """
            Plot the membership function.

            Args:
                st:  str
                    the string of the title of the plot. Default is 'Func:'
                figsize:  tuple
                    the size of the figure. Default is (5, 3)
        """
        if self.__custom:
            name = self.__func.__name__
        else:
            name = self.__func

        x = np.linspace(self.__variable_start, self.__variable_end, self.__linspace)
        y = self(x)
        plt.figure(figsize=figsize)
        for j in range(self.__funcnum):
            plt.plot(x, y[j], label=st + ': ' + name + '_%d' % (j + 1) + str(self.__parameter[j]))
        plt.grid(linestyle='-.')
        plt.legend()
        plt.show()
