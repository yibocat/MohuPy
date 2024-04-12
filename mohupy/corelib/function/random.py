#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/12 下午3:09
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from ...core import Fuzznum, Fuzzarray


def rand_fuzz(*n, qrung=1, minnum=1, maxnum=5) -> Fuzznum | Fuzzarray:
    """
    随机化一个任意模糊数或任意形状的模糊数向量
    :param n:       模糊集合（向量）形状
    :param qrung:   q阶序对
    :param minnum:  q阶序对犹豫模糊数隶属度集合和非隶属度集合的最小个数，非q阶序对犹豫模糊数该参数可无视
    :param maxnum:  q阶序对犹豫模糊数隶属度集合和非隶属度集合的最大个数，非q阶序对犹豫模糊数该参数可无视
    :return:
    """
    from ..random import Rand
    return Rand(qrung, minnum, maxnum)(*n)


def random_choice_fuzz(fuzz: Fuzznum | Fuzzarray,
                       size: int | tuple[int] | list[int] = None, replace=False) -> Fuzznum | Fuzzarray:
    """
    从一个模糊数或任意模糊高维数组中按照 size 随意抽取模糊数
    :param fuzz:        指定待抽取的模糊数或模糊数组
    :param size:        抽取形状
    :param replace:     是否可替换
    :return:            Fuzznum | Fuzzarray
    """
    from ..random import Choice
    return Choice()(fuzz, size, replace)
