#  Copyright (c) wangyibo 2025 All Rights Reserved
#  Python: 3.10.9
#  Date: 2025/7/15 15:24
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
from pathlib import Path
from typing import Union, Any, Optional

from .conf import Config
from .manager import ConfigManager

# 创建全局唯一的配置管理器实例

_config_manager = ConfigManager()


def get_config() -> Config:
    """
    获取当前配置的便捷函数。

    Returns:
        Config: 当前配置实例。
    """
    return _config_manager.get_config()


def set_config(**kwargs: Any):
    """
    设置配置参数的便捷函数。

    Args:
        **kwargs: 键值对形式的配置参数，键为配置项名称，值为要设置的新值。
                  例如：`set_config(DEFAULT_PRECISION=8, ENABLE_CACHE=False)`。
    """
    _config_manager.set_config(**kwargs)


def load_config_file(file_path: Union[str, Path]):
    """
    加载配置文件的便捷函数。

    Args:
        file_path (Union[str, Path]): 配置文件路径，可以是字符串或 Path 对象。
    """
    _config_manager.load_config_file(file_path)


def save_config_file(file_path: Union[str, Path]):
    """
    保存当前配置到指定文件的便捷函数。

    Args:
        file_path (Union[str, Path]): 保存配置文件的路径，可以是字符串或 Path 对象。
    """
    _config_manager.save_config_file(file_path)


def reset_config():
    """
    重置当前配置为默认值的便捷函数。
    """
    _config_manager.reset_config()
