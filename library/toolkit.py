#  Copyright (c) yibocat 2023 All Rights Reserved
#  Date: 2023/1/29 下午9:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzyKit


import re

from scipy import stats

import fuzzyelement.DHFElements as dh
import fuzzyelement.FNumbers as fn
import fuzzyelement.IVFNumbers as ifn

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def plot_stats(data):
    """
        Draw a graph to show the shape of the data set
        to determine whether it is a normal distribution.
        Parameters
        ----------
            data : pandas.DataFrame
                Input data.

        Returns
        -------
    """
    s = pd.DataFrame(data, columns=['value'])
    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(2, 1, 1)  # 创建子图1
    ax1.scatter(s.index, s.values)
    plt.grid()

    ax2 = fig.add_subplot(2, 1, 2)  # 创建子图2
    s.hist(bins=30, alpha=0.5, ax=ax2)
    s.plot(kind='kde', secondary_y=True, ax=ax2)
    plt.grid()


def ks_test_norm(data):
    """
        Kolmogorov-Smirnov test for normal distribution.
        Parameters
        ----------
            data : pandas.DataFrame
                Input data.

        Returns
        -------
            statistic : float
                Kolmogorov-Smirnov statistic.
            p_value : float
                P-value.
    """
    s = pd.DataFrame(data, columns=['value'])
    u = s['value'].mean()  # 计算均值
    std = s['value'].std()  # 计算标准差
    return stats.kstest(s['value'], 'norm', (u, std))


def random_split(data, l):
    """
        Randomly split a dataset into two datasets proportionally.
        Parameters
        ----------
            data : pandas.DataFrame
                Input data.
            l : float
                Proportion of data.

        Returns
        -------
            data_1 : pandas.DataFrame
                First dataset.
            data_2 : pandas.DataFrame
                Second dataset.
    """
    n = len(data)
    lam = int(np.round(n * l, 0))  # 获取按照拆分比例的数据个数
    # print(lam,type(lam))

    index_1 = np.random.choice(data.shape[0], lam, False)  # 随机选择一半数据，获取该数据的索引
    index_2 = np.delete(np.arange(data.shape[0]), index_1)  # 获取另一半数据的索引

    data_1 = data[index_1]
    data_2 = data[index_2]

    return data_1, data_2


def qrunghfe_convert(s, q: float):
    """
        Convert input data to Q-rung hesitant fuzzy element.
        Note: When the input data is '0', it should be set to '0.'.

        Q-rung Hesitant Fuzzy convert function accepts three forms
        of input data:
        {{x,x,x,x},{x,x,x,x}};
        {[x,x,x,x],[x,x,x,x]};
        [[x,x,x,x],[x,x,x,x]].

        Parameters
        ----------
            s : str
                Input data.
            q : str
                Fuzzy element.
        Returns
        -------
            dhf : DHFElements
    """
    dhf = dh.qrunghfe(q, [], [])
    c = 0
    x = re.findall(r'\d.?\d*|},\{|],\[', s)
    for i in range(len(x)):
        if x[i] == '],[' or x[i] == '},{':
            c = i
    for y in range(len(x)):
        if y < c:
            dhf.md = np.append(dhf.md, float(x[y]))
        elif y > c:
            dhf.nmd = np.append(dhf.nmd, float(x[y]))
        else:
            continue
    assert dhf.isLegal(), 'Invalid data!'
    return dhf


def qrungfn_convert(s, q):
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
    fnf = fn.qrungfn(q, 0., 0.)
    x = re.findall(r'\d.?\d*|},\{|],\[', s)
    assert len(x) == 2, 'Invalid data'
    fnf.md = np.asarray(float(x[0]))
    fnf.nmd = np.asarray(float(x[1]))
    assert fnf.isLegal(), 'Invalid data!'
    return fnf


def qrungivfn_convert(s, q):
    """
        Convert input data to interval-valued fuzzy number.
        Note: When the input data is 0, it should be set to 0.

        Q-rung Interval-valued fuzzy convert function accepts the form:
        [[x,x],[x,x]]

        Parameters
        ----------
        s : str
            Input data.
        q : int
            Q-rung

        Returns
        -------
        ivf : IVFNumbers
    """
    ivf = ifn.qrungivfn(q, [0., 0.], [0., 0.])
    x = re.findall(r'\d.?\d*|],\[', s)  # 正则表达式判断所有的数字和 '],[' 字符串，列表形式
    assert '],[' in x and x[2] == '],[', \
        'Invalid data! Format error, possibly missing \'],[\' ' + \
        'or wrong interval-valued.'  # 断言是否存在 '],[' 字符串且 '],[' 位置是否为 2
    x.remove('],[')  # 删除字符列表中的 '],[' 字符串
    assert len(x) == 4, 'Invalid data! Data format mismatch.'  # 断言字符列表中的数字是否为 4 个
    ivf.md[0] = np.asarray(float(x[0]))
    ivf.md[1] = np.asarray(float(x[1]))
    ivf.nmd[0] = np.asarray(float(x[2]))
    ivf.nmd[1] = np.asarray(float(x[3]))
    assert ivf.isLegal(), 'Invalid data! Illegal Q-rung interval-valued fuzzy number.'
    return ivf
