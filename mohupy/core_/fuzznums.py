#  Copyright (c) yibocat 2025 All Rights Reserved
#  Python: 3.10.9
#  Date: 2025/7/8 23:34
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
from typing import Dict, Any

from .qrofn import qROFNNumber, qROFNStrategy
from .strategy import ConfigStrategy


# class Fuzznum:
#     TEMPLATE_MAP = {
#         'qrofn': qROFNNumber,  # 使用方案1或方案2的实现
#     }
#
#     def __init__(self, mtype: str):
#         self.mtype = mtype
#         self._strategy = self._get_strategy(mtype)
#         self._configure()
#         self._business_logic = self._create_business_logic()
#
#     def _configure(self):
#         """配置属性"""
#         self._strategy.configure(self)
#
#     def _create_business_logic(self):
#         """创建业务逻辑处理器"""
#         template_class = self.TEMPLATE_MAP[self.mtype]
#         return template_class(self)
#
#     # ============= 智能方法代理 =============
#     def __getattr__(self, name):
#         """智能代理到业务逻辑，如果不支持则提供友好提示"""
#         if hasattr(self._business_logic, name):
#             method = getattr(self._business_logic, name)
#             if callable(method):
#                 return method
#             return method
#         else:
#             # 检查是否是已知的业务方法
#             known_methods = ['report', 'score', 'accuracy', 'complement', 'convert',
#                            'qsort', 'unique', 'normalize', 'validity', 'empty', 'initialize']
#             if name in known_methods:
#                 raise AttributeError(f"'{self.mtype}' 模式不支持 '{name}' 操作")
#             else:
#                 raise AttributeError(f"'{self.__class__.__name__}' 没有属性 '{name}'")
#
#     def get_supported_operations(self):
#         """获取当前模式支持的操作"""
#         if hasattr(self._business_logic, 'get_supported_operations'):
#             return self._business_logic.get_supported_operations()
#
#         # fallback: 检查哪些方法存在且可调用
#         operations = []
#         for method_name in ['report', 'score', 'accuracy', 'complement', 'convert',
#                            'qsort', 'unique', 'normalize', 'validity', 'empty', 'initialize']:
#             if hasattr(self._business_logic, method_name):
#                 operations.append(method_name)
#         return operations


class Fuzznum:
    """修复递归问题的A类"""

    # 策略映射
    _strategies = {
        'qrofn': qROFNStrategy
    }

    # 模板映射
    TEMPLATE_MAP = {
        'qrofn': qROFNNumber,
    }

    def __init__(self, mtype: str):
        """
        初始化A类实例

        Args:
            mtype (str): 模式类型
        """
        # 使用 object.__setattr__ 避免触发 __getattr__
        object.__setattr__(self, 'mtype', mtype)
        object.__setattr__(self, '_initialized', False)

        # 执行初始化
        self._initialize()

        # 标记初始化完成
        object.__setattr__(self, '_initialized', True)

    def _initialize(self):
        """内部初始化方法"""
        # 获取并应用配置策略
        if self.mtype not in self._strategies:
            raise ValueError(f"不支持的模式类型: {self.mtype}")

        strategy = self._strategies[self.mtype]
        strategy.configure(self)

        # 创建业务逻辑处理器
        if self.mtype not in self.TEMPLATE_MAP:
            raise ValueError(f"不支持的业务逻辑模板: {self.mtype}")

        template_class = self.TEMPLATE_MAP[self.mtype]
        object.__setattr__(self, '_business_logic', template_class(self))

    def __getattr__(self, name):
        """
        安全的属性访问代理

        注意：只有在正常属性查找失败时才会调用此方法
        """
        # 防止在初始化过程中的递归调用
        if not getattr(self, '_initialized', False):
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

        # 使用 object.__getattribute__ 安全地获取 _business_logic
        try:
            business_logic = object.__getattribute__(self, '_business_logic')
        except AttributeError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

        # 检查业务逻辑对象是否有该属性
        if hasattr(business_logic, name):
            attr = getattr(business_logic, name)
            if callable(attr):
                return attr
            return attr

        # 如果是已知的业务方法但不支持，给出友好提示
        known_methods = ['report', 'score', 'accuracy', 'complement', 'convert',
                        'qsort', 'unique', 'normalize', 'validity', 'empty', 'initialize']
        if name in known_methods:
            raise AttributeError(f"'{self.mtype}' 模式不支持 '{name}' 操作")

        # 未知属性
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def get_supported_operations(self):
        """获取当前模式支持的操作"""
        if not getattr(self, '_initialized', False):
            return []

        operations = []
        business_logic = object.__getattribute__(self, '_business_logic')

        for method_name in ['report', 'score', 'accuracy', 'complement', 'convert',
                           'qsort', 'unique', 'normalize', 'validity', 'empty', 'initialize']:
            if hasattr(business_logic, method_name):
                # 检查方法是否返回有意义的结果（非None）
                try:
                    if method_name in ['qsort', 'normalize']:  # 需要参数的方法
                        operations.append(method_name)
                    else:
                        result = getattr(business_logic, method_name)()
                        if result is not None:
                            operations.append(method_name)
                except Exception:
                    # 如果调用出错，仍然认为该方法存在
                    operations.append(method_name)

        return operations

    def get_configuration_info(self) -> Dict[str, Any]:
        """获取当前配置信息"""
        if not getattr(self, '_initialized', False):
            return {'status': 'not_initialized'}

        config_attrs = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_') and key != 'mtype':
                config_attrs[key] = value

        return {
            'mtype': self.mtype,
            'attributes': config_attrs,
            'supported_operations': self.get_supported_operations()
        }

    @classmethod
    def register_strategy(cls, strategy: ConfigStrategy):
        """注册新的配置策略"""
        cls._strategies[strategy.type_name] = strategy

    @classmethod
    def register_template(cls, mtype: str, template_class):
        """注册新的业务逻辑模板"""
        cls.TEMPLATE_MAP[mtype] = template_class