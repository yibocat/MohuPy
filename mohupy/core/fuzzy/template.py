#  Copyright (c) yibocat 2025 All Rights Reserved
#  Python: 3.10.9
#  Date: 2025/7/8 14:36
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from abc import ABC, abstractmethod


class ConfigStrategy(ABC):
    """
        配置策略抽象基类
    """

    @abstractmethod
    def config(self, instance) -> None:
        """配置实例的属性"""
        pass

    @property
    @abstractmethod
    def type_name(self) -> str:
        """
            返回配置策略的类型名称
            其实就是模糊集的类型，比如内置的 ‘qrofn’,'qivfn','qrohfn' 等
        """
        pass


class Template:

    """
        模糊集合的模板类。
        所有的模糊集合类都应该继承这个类。
        这个类定义了所有模糊集合的基本属性和方法。
        所有的模糊集合类都应该实现这个类的所有方法。
    """

    def __init__(self, *fuzz_param):
        self.fuzz_param = fuzz_param

    # 模糊属性库
    def report(self): raise NotImplementedError()
    def str(self): raise NotImplementedError()
    def score(self): raise NotImplementedError()
    def accuracy(self): raise NotImplementedError()
    def indeterminacy(self): raise NotImplementedError()
    def complement(self): raise NotImplementedError()

    # 模糊方法函数库
    def initialize(self): raise NotImplementedError()
    def validity(self): raise NotImplementedError()
    def empty(self): raise NotImplementedError()
    def convert(self): raise NotImplementedError()
    def qsort(self, *sort_param): raise NotImplementedError()
    def unique(self): raise NotImplementedError()
    def normalize(self, *norm_param): raise NotImplementedError()
