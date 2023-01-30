import numpy as np


def sigmf(x, b, c):
    """
        基本激活函数，x 表示一个自变量，b 表示左右偏差或偏离，c 表示激活区域，c 越大越平坦
        ======================================================================
        输入：
            x: np.array数据类型，也可以是一个值，表示自变量
    """
    return 1. / (1. + np.exp(- c * (x - b)))


def trimf(x, abc):
    """
        三角函数，x 表示自变量，abc 为一个 3 值数组，满足 a<=b<=c，也就是自变量取三个值时的三个角
    """
    assert len(abc) == 3, 'abc parameter must have exactly three elements.'
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


def zmf(x, a, b):
    """
        Z 函数，x 表示自变量，a 表示 z 函数左变化，b 表示函数右变化，
        Z 函数形状如同一个大写字母 Z
    """
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
        梯形函数，x 表示自变量，abcd 表示四值数组，f分别表示四个转折点，满足 a<=b<=c<=d
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


def smf(x, a, b):
    """
        S 函数，形状如 S 一样，与激活函数类似，a 表示从 0 开始爬升的点，b 表示趋于 1 的平稳的点
    """
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


def gaussmf(x, mean, sigma):
    """
        高斯函数，或者称作正态分布函数，mean 表示均值或中心值，sigma 表示标准差的高斯参数
    """
    return np.exp(-((x - mean) ** 2.) / (2 * sigma ** 2.))


def gauss2mf(x, mean1, sigma1, mean2, sigma2):
    """
        两个高斯函数结合的高斯函数，mean1 和 sigma1 表示一个高斯函数的参数，mean2 和 sigma2
        为另一个高斯函数的参数，满足 mean1<=mean2
        当 mean1<=x<=mean2 时，函数值为 1
    """
    assert mean1 <= mean2, 'mean1 <= mean2 is required.  See docstring.'
    if type(x) != np.ndarray:
        x = np.array([x])
    y = np.ones(len(x))
    idx1 = x <= mean1
    idx2 = x > mean2
    y[idx1] = gaussmf(x[idx1], mean1, sigma1)
    y[idx2] = gaussmf(x[idx2], mean2, sigma2)
    if len(y) == 1:
        return y[0]
    return y


def gbellmf(x, a, b, c):
    """
        广义贝尔函数，x 表示自变量，a 表示宽度，b 表示斜率，c 表示偏差或中心点
        Definition of Generalized Bell function is:
        y(x) = 1 / (1 + abs([x - c] / a) ** [2 * b])
    """
    return 1. / (1. + np.abs((x - c) / a) ** (2 * b))
