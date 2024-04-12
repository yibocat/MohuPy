#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/12 下午2:24
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from ...core import Fuzznum, Fuzzarray


def fuzz_plot(fuzz: Fuzznum | Fuzzarray,
              other: Fuzznum=None,
              add=None,
              sub=None,
              mul=None,
              div=None,
              color='red',
              color_area=None,
              alpha=0.3,
              label='',
              legend=False):
    """
    对模糊数或模糊集合画图。可以通过该方法清楚地查看每个模糊数在其限制区间内的分布。
    通过将 add, sub, mul, div 设置为 True 可以看到每个模糊数的加法区间，减法区间，
    乘法区间和除法区间。color 表示每个点的颜色。color_area 表示是一个四元素的数组，
    从前往后分别表示每个运算区间的颜色。
    值得注意的是，该方法不仅适用于 Fuzznum 类型，还适用于 Fuzzarray 类型。但面对
    大量的模糊数时，该方法性能有限。

    :param fuzz:        进行画图的模糊数或模糊集合
    :param other:       Fuzznum 类型，用来判断该点位于 fuzz 的哪个运算区间内
    :param add:         bool 类型，加法区间
    :param sub:         bool 类型，减法区间
    :param mul:         bool 类型，乘法区间
    :param div:         bool 类型，除法区间
    :param color:       模糊数点的颜色
    :param color_area:  模糊数运算区间的颜色
    :param alpha:       画图的透明度
    :param label:       标签
    :param legend:      bool 类型，是否显示标签 label
    :return:
    """
    from ..lib import Plot
    Plot()(fuzz, other, add, sub, mul, div,
           color, color_area, alpha, label, legend)
