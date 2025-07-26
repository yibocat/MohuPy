#  Copyright (c) yibocat 2025 All Rights Reserved
#  Python: 3.10.9
#  Date: 2025/7/8 22:01
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from abc import ABC, abstractmethod


# ====================== Configuration Layer =======================
class ConfigStrategy(ABC):
    """
        配置策略抽象基类 - 专注于属性配置
    """

    @abstractmethod
    def configure(self, instance) -> None:
        """
            配置实例的属性
        """
        pass

    @property
    @abstractmethod
    def type_name(self) -> str:
        """
            返回配置策略的类型名称
            其实就是模糊集的类型，比如内置的 ‘qrofn’,'qivfn','qrohfn' 等
        """
        pass

