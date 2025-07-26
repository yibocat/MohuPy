#  Copyright (c) yibocat 2025 All Rights Reserved
#  Python: 3.10.9
#  Date: 2025/7/8 22:03
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import logging

from abc import ABC, abstractmethod


class Template(ABC):
    """
        逻辑层模板类 - 定义通用方法接口
        实际上就是模糊集合的模板类，之后可以通过模板类直接创建用户自定义的模糊集合
    """

    def __init__(self, instance):
        """
        Args:
            instance: 配置好的模糊实例
        """

        self.instance = instance

    # 抽象核心属性类方法（必须实现）
    @abstractmethod
    def report(self): raise NotImplementedError("打印模糊数，必须在子类实现")

    @abstractmethod
    def str(self): raise NotImplementedError("模糊数字符形式，必须在子类实现")

    @abstractmethod
    def initialize(self): raise NotImplementedError("初始化模糊数，必须在子类实现")

    # 可选实现属性
    def score(self): pass
    def accuracy(self): pass
    def indeterminacy(self): pass
    def complement(self): pass

    # 可选实现方法
    def validity(self): pass
    def empty(self): pass
    def convert(self): pass
    def qsort(self, *sort_param): pass
    def unique(self): pass
    def normalize(self, *norm_param): pass

    # 辅助方法
    def get_supported_operations(self):
        """
            获取支持的操作列表
        """
        supported = []
        for method_name in  ['score','accuracy','indeterminacy',
                             'complement','validity','empty','convert',
                             'qsort','unique','normalize']:
            try:
                result = getattr(self, method_name)()
                if result is not None:
                    supported.append(method_name)
            except NotImplementedError:
                pass
        return supported
























