#  Copyright (c) wangyibo 2025 All Rights Reserved
#  Python: 3.10.9
#  Date: 2025/7/15 15:21
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
from dataclasses import dataclass, field


@dataclass
class Config:

    """
    模糊计算统一配置类。

    该类定义了 MohuPy 框架中所有可配置的参数及其默认值。
    每个字段都包含 `metadata`，用于指定其所属的类别和验证规则。

    Attributes:
        DEFAULT_WRAPPER (str): 默认模糊计算包装器。
            影响执行器和计算工厂类的默认选择。
        DEFAULT_MTYPE (str): 默认模糊数类型。
            影响 Fuzznum 无参构造时的类型选择。
        DEFAULT_PRECISION (int): 默认计算精度（小数位数）。
            影响所有数值计算和显示。
        DEFAULT_EPSILON (float): 默认数值容差。
            用于浮点数比较和零值判断。
        ENABLE_CACHE (bool): 是否启用运算缓存。
            影响工厂类和执行器等计算和创建实例的缓存行为。
        ENABLE_CACHE_FUZZNUM: 是否启用 Fuzznum 缓存
            是否启用 Fuzznum 计算缓存，主要影响 Fuzznum 中属性和方法的缓存行为
        CACHE_SIZE: 缓存大小
            运算缓存的最大条目数，控制内存使用
        DEBUG_MODE (bool): 调试模式开关。
            启用详细的调试信息。
        STRICT_TYPE_CHECKING (bool): 严格类型检查开关。
            启用严格的数据类型检查。
    """

    # ================== 基础配置 ===================
    DEFAULT_MTYPE: str = field(
        default='qrofn',
        metadata={
            'category': 'basic',
            'description': '默认模糊数类型，影响 Fuzznum 无参构造时的类型选择',
            'validator': lambda x: isinstance(x, str) and len(x) > 0,
            'error_msg': "必须是非空字符串。"
        }
    )

    DEFAULT_T_NORM: str = field(
        default='algebraic',
        metadata={
            'category': 'basic',
            'description': '默认t-范数类型，影响 Fuzznum 的运算规则',
            'validator': lambda x: isinstance(x, str) and len(x) > 0,
            'error_msg': "必须是非空字符串。"
        }
    )

    STRICT_ATTRIBUTE_MODE: bool = field(
        default=True,
        metadata={
            'category': 'basic',
            'description': '严格属性检查，主要用于 FuzznumStrategy 中 __setattr__ 方法的属性检查',
            'validator': lambda x: isinstance(x, bool),
            'error_msg': "必须是布尔值 (True/False)。"
        }
    )

    ENABLE_CACHE: bool = field(
        default=True,
        metadata={
            'category': 'performance',
            'description': '是否启用运算缓存，影响工厂类和执行器等计算和创建实例的缓存行为',
            'validator': lambda x: isinstance(x, bool),
            'error_msg': "必须是布尔值 (True/False)。"
        }
    )

    TEMPLATE_CACHE_SIZE: int = field(
        default=256,
        metadata={
            'category': 'performance',
            'description': 'Fuzznum Template 运算缓存的最大条目数，控制内存使用',
            'validator': lambda x: isinstance(x, int) and x >= 0,
            'error_msg': "必须是非负整数。。"
        }
    )

    EXECUTOR_CACHE_SIZE: int = field(
        default=256,
        metadata={
            'category': 'performance',
            'description': '运算缓存的最大条目数，控制内存使用',
            'validator': lambda x: isinstance(x, int) and x >= 0,
            'error_msg': "必须是非负整数。。"
        }
    )

    ENABLE_EXECUTOR_CACHE: bool = field(
        default=True,
        metadata={
            'category': 'performance',
            'description': '是否启用执行器缓存，影响执行器计算和创建实例的缓存行为',
            'validator': lambda x: isinstance(x, bool),
            'error_msg': "必须是布尔值 (True/False)。"
        }
    )

    ENABLE_FUZZNUM_CACHE: bool = field(
        default=True,
        metadata={
            'category': 'performance',
            'description': '是否启用模糊数缓存，影响模糊数实例的缓存行为',
            'validator': lambda x: isinstance(x, bool),
            'error_msg': "必须是布尔值 (True/False)。"
        }
    )

    ENABLE_PERFORMANCE_MONITORING: bool = field(
        default=True,
        metadata={
            'category': 'debug',
            'description': '启动性能监控，用于调制监控一些计算的性能信息',
            'validator': lambda x: isinstance(x, bool),
            'error_msg': "必须是布尔值 (True/False)。"
        }
    )

    ENABLE_LOGGING: bool = field(
        default=True,
        metadata={
            'category': 'debug',
            'description': '启动日志记录',
            'validator': lambda x: isinstance(x, bool),
            'error_msg': "必须是布尔值 (True/False)。"
        }
    )

    DEBUG_MODE: bool = field(
        default=True,
        metadata={
            'category': 'debug',
            'description': '调试模式开关，启用详细的调试信息',
            'validator': lambda x: isinstance(x, bool),
            'error_msg': "必须是布尔值 (True/False)。"
        }
    )






    # # ================== 基础配置 ===================
    # # 系统核心参数，影响整个框架的基本行为
    #
    # DEFAULT_MTYPE: str = field(
    #     default='qrofn',
    #     metadata={
    #         'category': 'basic',
    #         'description': '默认模糊数类型，影响 Fuzznum 无参构造时的类型选择',
    #         'validator': lambda x: isinstance(x, str) and len(x) > 0,
    #         'error_msg': "必须是非空字符串。"
    #     }
    # )
    #
    # DEFAULT_PRECISION: int = field(
    #     default=6,
    #     metadata={
    #         'category': 'basic',
    #         'description': '默认计算精度（小数位数），影响所有数值计算和显示',
    #         'validator': lambda x: isinstance(x, int) and x >= 0,
    #         'error_msg': "必须是非负整数。"
    #     }
    # )
    #
    # DEFAULT_EPSILON: float = field(
    #     default=1e-12,
    #     metadata={
    #         'category': 'basic',
    #         'description': '默认数值容差，用于浮点数比较和零值判断',
    #         'validator': lambda x: isinstance(x, (int, float)) and x > 0,
    #         'error_msg': "必须是正数。"
    #     }
    # )
    #
    # # ==================== 性能配置 ====================
    # # 缓存和性能优化相关参数
    #
    # ENABLE_CACHE: bool = field(
    #     default=True,
    #     metadata={
    #         'category': 'performance',
    #         'description': '是否启用运算缓存，影响工厂类和执行器等计算和创建实例的缓存行为',
    #         'validator': lambda x: isinstance(x, bool),
    #         'error_msg': "必须是布尔值 (True/False)。"
    #     }
    # )
    #
    # ENABLE_CACHE_FUZZNUM: bool = field(
    #     default=True,
    #     metadata={
    #         'category': 'performance',
    #         'description': '是否启用 Fuzznum 计算缓存，主要影响 Fuzznum 中属性和方法的缓存行为',
    #         'validator': lambda x: isinstance(x, bool),
    #         'error_msg': "必须是布尔值 (True/False)。"
    #     }
    # )
    # TEMPLATE_CACHE_SIZE: int = field(
    #     default=256,
    #     metadata={
    #         'category': 'performance',
    #         'description': 'Fuzznum Template 运算缓存的最大条目数，控制内存使用',
    #         'validator': lambda x: isinstance(x, int) and x >= 0,
    #         'error_msg': "必须是非负整数。。"
    #     }
    # )
    #
    # EXECUTOR_CACHE_SIZE: int = field(
    #     default=256,
    #     metadata={
    #         'category': 'performance',
    #         'description': '运算缓存的最大条目数，控制内存使用',
    #         'validator': lambda x: isinstance(x, int) and x >= 0,
    #         'error_msg': "必须是非负整数。。"
    #     }
    # )
    #
    # # ==================== 调试配置 ====================
    #
    #
    # ENABLE_PERFORMANCE_MONITORING: bool = field(
    #     default=True,
    #     metadata={
    #         'category': 'debug',
    #         'description': '启动性能监控，用于调制监控一些计算的性能信息',
    #         'validator': lambda x: isinstance(x, bool),
    #         'error_msg': "必须是布尔值 (True/False)。"
    #     }
    # )
    #
    # # ==================== 安全配置 ====================
    #
    # STRICT_TYPE_CHECKING: bool = field(
    #     default=False,
    #     metadata={
    #         'category': 'security',
    #         'description': '严格类型检查开关，启用严格的数据类型检查',
    #         'validator': lambda x: isinstance(x, bool),
    #         'error_msg': "必须是布尔值 (True/False)。"
    #     }
    # )
    #
    # STRICT_CALLBACK_HANDLING: bool = field(
    #     default=True,
    #     metadata={
    #         'category': 'security',
    #         'description': '回调函数严格检查开关，启用严格的属性回滚机制',
    #         'validator': lambda x: isinstance(x, bool),
    #         'error_msg': "必须是布尔值 (True/False)。"
    #     }
    # )
    #















