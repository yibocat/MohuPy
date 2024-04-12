#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/12 下午1:48
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import numpy as np


def sigmf(x, *args):
    """
        The basic sigmoid function, 'bc' is a list containing two parameters,
        representing the sigmoid function parameters. where the first value
        represents the left-right deviation or deviation. The second value
        represents the active area, and the larger it is, the flatter it is.

        parameters:
        ----------
            x:  float or np.ndarray
                the independent variable
            *args:
                two parameters, representing the sigmoid
                function parameters.
        returns:
        -------
            y:  np.float_ or np.ndarray
                the sigmoid function value

    """
    assert len(args) == 2, 'parameter list length must be 2.'
    return 1. / (1. + np.exp(- args[0] * (x - args[1])))


def trimf(x, *args):
    """
        Triangular function, 'x' represents the independent variable, 'abc'
        is a 3-valued array that satisfies a<=b<=c, that is, the three angles
        when the independent variable takes three values.

        parameters:
        ----------
            x:  float or np.ndarray
                the independent variable
            *args:
                3-valued array that satisfies a<=b<=c, that is, the three angles
        returns:
        -------
            y:  np.float np.ndarray
                the triangular function value
    """
    assert len(args) == 3, 'parameter must have exactly three elements.'
    assert args[0] <= args[1] <= args[2], 'parameters requires the three elements a <= b <= c.'

    if isinstance(x, np.ndarray):
        x = np.array([x])
    y = np.zeros(len(x))

    # Left side
    if args[0] != args[1]:
        idx = np.nonzero(np.logical_and(args[0] < x, x < args[1]))[0]
        y[idx] = (x[idx] - args[0]) / float(args[1] - args[0])

    # Right side
    if args[1] != args[2]:
        idx = np.nonzero(np.logical_and(args[1] < x, x < args[2]))[0]
        y[idx] = (args[2] - x[idx]) / float(args[2] - args[1])

    idx = np.nonzero(x == args[1])
    y[idx] = 1
    if len(y) == 1:
        return y[0]
    return y


def zmf(x, *args):
    """
        Z-shape function, 'x' is the argument and 'ab' is a list of two values
        representing the function parameters. The first value is do change,
        the second value is right change. The zigzag function is shaped like a
        capital letter Z.

        parameters:
        ----------
            x:  float or np.ndarray
                the independent variable
            *args:
                2-valued array that satisfies a<=b
        returns:
        -------
            y:  float or np.ndarray
                the z-shape function value
    """
    assert len(args) == 2, 'parameter list length must be 2.'
    assert args[0] <= args[1], 'a <= b is required.'

    if isinstance(x, np.ndarray):
        x = np.array([x])
    y = np.ones(len(x))

    idx = np.logical_and(args[0] <= x, x < (args[0] + args[1]) / 2.)
    y[idx] = 1 - 2. * ((x[idx] - args[0]) / (args[1] - args[0])) ** 2.

    idx = np.logical_and((args[0] + args[1]) / 2. <= x, x <= args[1])
    y[idx] = 2. * ((x[idx] - args[1]) / (args[1] - args[0])) ** 2.

    idx = x >= args[1]
    y[idx] = 0
    if len(y) == 1:
        return y[0]
    return y


def trapmf(x, *args):
    """
        Trapezoidal function, 'x' represents the independent variable, 'abcd'
        is a four-value array, representing four turning points respectively,
        satisfying a<=b<=c<=d.

        parameters:
        ----------
            x:  float or np.ndarray
                the independent variable
            abcd:  list
                4-valued array that satisfies a<=b<=c<=d
        returns:
            y:  float or np.ndarray
                the trapezoidal function value
    """
    assert len(args) == 4, 'abcd parameter must have exactly four elements.'
    assert args[0] <= args[1] <= args[2] <= args[3], 'abcd requires the four elements \
                                          a <= b <= c <= d.'
    if isinstance(x, np.ndarray):
        x = np.array([x])
    y = np.ones(len(x))

    idx = np.nonzero(x <= args[1])[0]
    y[idx] = trimf(x[idx], np.r_[args[0], args[1], args[1]])

    idx = np.nonzero(x >= args[2])[0]
    y[idx] = trimf(x[idx], np.r_[args[2], args[2], args[3]])

    idx = np.nonzero(x < args[0])[0]
    y[idx] = np.zeros(len(idx))

    idx = np.nonzero(x > args[3])[0]
    y[idx] = np.zeros(len(idx))
    if len(y) == 1:
        return y[0]
    return y


def smf(x, *args):
    """
        S-shape function. Similar to the sigmoid function, 'ab' is a list
        of two values. The first value represents the point to climb from
        the beginning, and the second value represents the point to a
        plateau of 1. The shape of the S-shape function is like a capital
        letter 'S'.

        parameters:
        ----------
            x:  float or np.ndarray
                the independent variable
            *args:
                2-valued array that satisfies a<=b
        returns:
        -------
            y:  float or np.ndarray
                the S-shape function value
    """
    assert len(args) == 2, 'parameter list length must be 2.'
    assert args[0] <= args[1], 'a <= b is required.'
    if isinstance(x, np.ndarray):
        x = np.array([x])
    y = np.ones(len(x))
    idx = x <= args[0]
    y[idx] = 0

    idx = np.logical_and(args[0] <= x, x <= (args[0] + args[1]) / 2.)
    y[idx] = 2. * ((x[idx] - args[0]) / (args[1] - args[0])) ** 2.

    idx = np.logical_and((args[0] + args[1]) / 2. <= x, x <= args[1])
    y[idx] = 1 - 2. * ((x[idx] - args[1]) / (args[1] - args[0])) ** 2.
    if len(y) == 1:
        return y[0]
    return y


def gaussmf(x, *args):
    """
        The Gaussian function, also known as the normal distribution
        function. 'ms' is a list of two values representing the parameters
        of the Gaussian function. where the first value represents the
        mean or center value. The second value represents the standard
        deviation.

        parameters:
        ----------
            x:  float or np.ndarray
                the independent variable
            *args:
                2-valued of Gaussian function parameters
                args[0] is the mean
                args[1] is the standard deviation
        returns:
        -------
            y:  float or np.ndarray
                the Gaussian function value
    """
    assert len(args) == 2, 'parameter list length must be 2.'
    return np.exp(-((x - args[0]) ** 2.) / (2 * args[1] ** 2.))


def gauss2mf(x, *args):
    """
        Bi-Gaussian associative function. A Gaussian function that combines
        two Gaussian functions. 'ms' is a list of four values. The first
        and second values represent the mean and standard deviation of the
        first Gaussian function, and the third and fourth values represent
        the mean and standard deviation of the second Gaussian function.
        The function needs to satisfy mean1 < = mean2.
        When mean1<=x<=mean2, the function value is 1.

        parameters:
            x:  float or np.ndarray
                the independent variable
            *args:
                4-valued of Bi-Gaussian function parameters
                args[0] is the mean of the first Gaussian function
                args[1] is the standard deviation of the first Gaussian function
                args[2] is the mean of the second Gaussian function
                args[3] is the standard deviation of the second Gaussian function
        returns:
        -------
            y:  float or np.ndarray
                the Bi-Gaussian function value
    """
    assert len(args) == 4, 'parameter list length must be 4.'
    assert args[0] <= args[2], 'args[0] <= args[2] is required.  See docstring.'
    if isinstance(x, np.ndarray):
        x = np.asarray([x])
    y = np.ones(len(x))
    idx1 = x <= args[0]
    idx2 = x > args[2]
    y[idx1] = gaussmf(x[idx1], [args[0], args[1]])
    y[idx2] = gaussmf(x[idx2], [args[2], args[3]])
    if len(y) == 1:
        return y[0]
    return y


def gbellmf(x, *args):
    """
        Generalized Bell functions. abc is an argument list with three
        values. where the first value represents the width, the second
        value represents the slope, and the third value represents the
        deviation or center point.

        Definition of Generalized Bell function is:
        y(x) = 1 / (1 + abs([x - c] / a) ** [2 * b])

        parameters:
        ----------
            x:  float or np.ndarray
                the independent variable
            *args:
                3-valued of the generalized Bell function parameters
        returns:
        -------
            y:  float or np.ndarray
                the generalized Bell function value
    """
    assert len(args) == 3, 'parameter list length must be 3.'
    return 1. / (1. + np.abs((x - args[2]) / args[0]) ** (2 * args[1]))
