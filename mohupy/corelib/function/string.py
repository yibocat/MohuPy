#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/12 下午2:36
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from ...core import Fuzznum


def fuzz_str2fuzz(s: str, qrung: int) -> Fuzznum:
    """
    将字符串转换为模糊数
    需要注意的是，字符串形式最好是 '<[xxx],[xxx]>','<xxx,xxx>' 类型

    :param s:       待转换的字符串
    :param qrung:   待转换的模糊数的q阶序对
    :return:        模糊数
    """
    from ..lib import StrToFuzz
    return StrToFuzz(qrung)(s)
