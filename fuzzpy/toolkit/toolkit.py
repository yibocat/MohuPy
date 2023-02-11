#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/1 下午5:37
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzPy


# import re

from scipy import stats

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
