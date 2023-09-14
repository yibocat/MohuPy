#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/21 上午4:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets

import re

import numpy as np
from matplotlib import pyplot as plt

from .fuzzy_element import qrungifn


def random(q: int):
    """
        Generate a randomQHF Q-rung fuzzy number.

        Args:
            q (float): the q-rung number.
        Returns:
            FNumbers
    """
    newf = qrungifn(q, 0., 0.)
    newf.set_md(np.random.rand(1))
    newf.set_nmd(np.random.rand(1))
    while not newf.isLegal():
        newf.set_md(np.random.rand(1))
        newf.set_nmd(np.random.rand(1))
    return newf


def str_to_fn(s, q):
    """
        Convert input data to fuzzy number.
        Note: When the input data is 0, it should be set to 0.

        Q-rung fuzzy convert function accepts the form:
        [x,x]

        Parameters
        ----------
            s : str
                Input data.
            q : int
                Q-rung

        Returns
        -------
            fnf : FNumbers
    """
    fnf = qrungifn(q, 0., 0.)
    t = re.findall(r'^\[(\d.*?\d)]$', s)
    assert len(t) == 1, 'ERROR: data format error.'
    x = re.findall(r'\d.?\d*', t[0])
    assert len(x) == 2, 'ERROR: data format error.'
    fnf.set_md(np.asarray(float(x[0])))
    fnf.set_nmd(np.asarray(float(x[1])))
    assert fnf.isLegal(), 'ERROR: The data format is correct, but the data is invalid.'
    return fnf


def pos(q):
    return qrungifn(q, 1., 0.)


def neg(q):
    return qrungifn(q, 0., 1.)


def zero(q):
    return qrungifn(q, 0., 0.)


def plot(x, other=None, add=None, sub=None, mul=None, div=None):
    """
        Plots the fuzzy number distribution for a given fuzzy number.

        Parameters
        ----------
        region : str
            The region of operations.
            optional: 'all','add','sub','mul' or 'div'
        other: fns.qrungifn
            The other fuzzy number to plot. Used to determine whether other is
            within the range of x

        Returns
        -------
    """
    md = x.md
    nmd = x.nmd
    q = x.qrung

    x = np.linspace(0, 1, 1000)

    plt.gca().spines['top'].set_linewidth(False)
    plt.gca().spines['bottom'].set_linewidth(True)
    plt.gca().spines['left'].set_linewidth(True)
    plt.gca().spines['right'].set_linewidth(False)
    plt.axis([0, 1.1, 0, 1.1])
    plt.axhline(y=0)
    plt.axvline(x=0)
    plt.scatter(md, nmd, color='red', marker='o')
    if other is not None:
        assert other.qrung == q, 'ERROR: The qrungs are not equal'
        omd = other.md
        onmd = other.nmd
        plt.scatter(omd, onmd, color='blue', marker='*')

    y = (1 - x ** q) ** (1 / q)

    n = (nmd ** q / (1 - md ** q) * (1 - x ** q)) ** (1 / q)
    m = (md ** q / (1 - nmd ** q) * (1 - x ** q)) ** (1 / q)

    if add:
        # Q-ROFN f addition region
        plt.fill_between(x, n, color='blue', alpha=0.1, where=x > md)
    if sub:
        # Q-ROFN f subtraction region
        plt.fill_between(x, n, y, color='red', alpha=0.1, where=x < md)
    if mul:
        # Q-ROFN f multiplication region
        plt.fill_betweenx(x, m, color='blue', alpha=0.1, where=x > nmd)
    if div:
        # Q-ROFN f division region
        plt.fill_betweenx(x, m, y, color='red', alpha=0.1, where=x < nmd)

    plt.plot(x, y)
    # plt.plot(x,n,linestyle='--')
    # plt.plot(m,x,linestyle='--')
    plt.show()
