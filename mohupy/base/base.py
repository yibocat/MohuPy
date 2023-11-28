#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/11/26 下午2:48
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy


import abc


class MohuBase(abc.ABC):
    """
        Fuzzy base class is an abstract class, which is the base class of
        fuzzy numbers and fuzzy sets.
    """


class mohunum(MohuBase):
    ...


class mohuset(MohuBase):
    ...


FuzzType = {'qrofn', 'ivfn', 'qrohfn'}