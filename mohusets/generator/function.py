#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/21 上午4:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets

import numpy as np


def sigmf(x, bc):
    """
        The basic sigmoid function, 'bc' is a list containing two parameters,
        representing the sigmoid function parameters. where the first value
        represents the left-right deviation or deviation. The second value
        represents the active area, and the larger it is, the flatter it is.

        parameters:
        ----------
            x:  float or np.ndarray
                the independent variable
            bc:  list
                a list containing two parameters, representing the sigmoid
                function parameters.
        returns:
        -------
            y:  np.float or np.ndarray
                the sigmoid function value

    """
    assert len(bc) == 2, 'parameter list length must be 2.'
    b, c = np.r_[bc]
    return 1. / (1. + np.exp(- b * (x - c)))


def trimf(x, abc):
    """
        Triangular function, 'x' represents the independent variable, 'abc'
        is a 3-valued array that satisfies a<=b<=c, that is, the three angles
        when the independent variable takes three values.

        parameters:
        ----------
            x:  float or np.ndarray
                the independent variable
            abc:  list
                3-valued array that satisfies a<=b<=c, that is, the three angles
        returns:
        -------
            y:  np.float np.ndarray
                the triangular function value
    """
    assert len(abc) == 3, 'parameter must have exactly three elements.'
    a, b, c = np.r_[abc]  # Zero-indexing in Python
    assert a <= b <= c, 'abc requires the three elements a <= b <= c.'

    if type(x) != np.ndarray:
        x = np.array([x])
    y = np.zeros(len(x))

    # Left side
    if a != b:
        idx = np.nonzero(np.logical_and(a < x, x < b))[0]
        y[idx] = (x[idx] - a) / float(b - a)

    # Right side
    if b != c:
        idx = np.nonzero(np.logical_and(b < x, x < c))[0]
        y[idx] = (c - x[idx]) / float(c - b)

    idx = np.nonzero(x == b)
    y[idx] = 1
    if len(y) == 1:
        return y[0]
    return y


def zmf(x, ab):
    """
        Z-shape function, 'x' is the argument and 'ab' is a list of two values
        representing the function parameters. The first value is do change,
        the second value is right change. The zigzag function is shaped like a
        capital letter Z.

        parameters:
        ----------
            x:  float or np.ndarray
                the independent variable
            ab:  list
                2-valued array that satisfies a<=b
        returns:
        -------
            y:  float or np.ndarray
                the z-shape function value
    """
    assert len(ab) == 2, 'parameter list length must be 2.'
    a, b = np.r_[ab]
    assert a <= b, 'a <= b is required.'

    if type(x) != np.ndarray:
        x = np.array([x])
    y = np.ones(len(x))

    idx = np.logical_and(a <= x, x < (a + b) / 2.)
    y[idx] = 1 - 2. * ((x[idx] - a) / (b - a)) ** 2.

    idx = np.logical_and((a + b) / 2. <= x, x <= b)
    y[idx] = 2. * ((x[idx] - b) / (b - a)) ** 2.

    idx = x >= b
    y[idx] = 0
    if len(y) == 1:
        return y[0]
    return y


def trapmf(x, abcd):
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
    assert len(abcd) == 4, 'abcd parameter must have exactly four elements.'
    a, b, c, d = np.r_[abcd]
    assert a <= b <= c <= d, 'abcd requires the four elements \
                                          a <= b <= c <= d.'
    if type(x) != np.ndarray:
        x = np.array([x])
    y = np.ones(len(x))

    idx = np.nonzero(x <= b)[0]
    y[idx] = trimf(x[idx], np.r_[a, b, b])

    idx = np.nonzero(x >= c)[0]
    y[idx] = trimf(x[idx], np.r_[c, c, d])

    idx = np.nonzero(x < a)[0]
    y[idx] = np.zeros(len(idx))

    idx = np.nonzero(x > d)[0]
    y[idx] = np.zeros(len(idx))
    if len(y) == 1:
        return y[0]
    return y


def smf(x, ab):
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
            ab:  list
                2-valued array that satisfies a<=b
        returns:
        -------
            y:  float or np.ndarray
                the S-shape function value
    """
    assert len(ab) == 2, 'parameter list length must be 2.'
    a, b = np.r_[ab]
    assert a <= b, 'a <= b is required.'
    if type(x) != np.ndarray:
        x = np.array([x])
    y = np.ones(len(x))
    idx = x <= a
    y[idx] = 0

    idx = np.logical_and(a <= x, x <= (a + b) / 2.)
    y[idx] = 2. * ((x[idx] - a) / (b - a)) ** 2.

    idx = np.logical_and((a + b) / 2. <= x, x <= b)
    y[idx] = 1 - 2. * ((x[idx] - b) / (b - a)) ** 2.
    if len(y) == 1:
        return y[0]
    return y


def gaussmf(x, ms):
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
            ms:  list
                2-valued array of Gaussian function parameters
        returns:
        -------
            y:  float or np.ndarray
                the Gaussian function value
    """
    assert len(ms) == 2, 'parameter list length must be 2.'
    mean, sigma = np.r_[ms]
    return np.exp(-((x - mean) ** 2.) / (2 * sigma ** 2.))


def gauss2mf(x, ms):
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
            ms:  list
                4-valued array of Bi-Gaussian function parameters
        returns:
        -------
            y:  float or np.ndarray
                the Bi-Gaussian function value
    """
    assert len(ms) == 4, 'parameter list length must be 4.'
    mean1, sigma1, mean2, sigma2 = np.r_[ms]
    assert mean1 <= mean2, 'mean1 <= mean2 is required.  See docstring.'
    if type(x) != np.ndarray:
        x = np.asarray([x])
    y = np.ones(len(x))
    idx1 = x <= mean1
    idx2 = x > mean2
    y[idx1] = gaussmf(x[idx1], [mean1, sigma1])
    y[idx2] = gaussmf(x[idx2], [mean2, sigma2])
    if len(y) == 1:
        return y[0]
    return y


def gbellmf(x, abc):
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
            abc:  list
                3-valued array of the generalized Bell function parameters
        returns:
        -------
            y:  float or np.ndarray
                the generalized Bell function value
    """
    assert len(abc) == 3, 'parameter list length must be 3.'
    a, b, c = np.r_[abc]
    return 1. / (1. + np.abs((x - c) / a) ** (2 * b))
