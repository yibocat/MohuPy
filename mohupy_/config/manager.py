#  Copyright (c) wangyibo 2025 All Rights Reserved
#  Python: 3.10.9
#  Date: 2025/7/15 15:23
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import json
import threading

from dataclasses import asdict, fields
from pathlib import Path
from typing import Any, Union, Optional, Dict, List

from .conf import Config


class ConfigManager:
    """
    全局配置管理器。

    该类实现了单例模式，确保在整个应用程序中只有一个配置实例。
    负责配置的加载、保存、设置、获取以及验证。
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """
        实现单例模式，确保 ConfigManager 只有一个实例。

        Returns:
            ConfigManager: ConfigManager 的唯一实例。
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        初始化 ConfigManager 实例。

        如果实例已经初始化过，则跳过重复初始化。
        """
        if hasattr(self, '_initialized'):
            return

        self._config = Config()
        self._config_source = None       # 配置来源跟踪
        self._is_modified = False        # 修改状态跟踪

        # TODO: 为未来扩展预留
        self._observers = []             # 观察者列表(暂未使用)
        self._config_history = []        # 配置历史记录(暂未使用)
        self._validation_rules = {}      # 验证规则(暂未使用)

        self._initialized = True

    def get_config(self) -> Config:
        """
        获取当前配置实例。

        Returns:
            Config: 当前配置实例。
        """
        return self._config

    def set_config(self, **kwargs):
        """
        设置一个或多个配置参数的值。

        Args:
            **kwargs: 键值对形式的配置参数，键为配置项名称，值为要设置的新值。

        Raises:
            ValueError: 如果传入了未知参数或参数值不符合验证规则。
        """
        for key, value in kwargs.items():
            # 查找 Config dataclass 中是否存在该参数
            config_field = None
            for f in fields(self._config):
                if f.name == key:
                    config_field = f
                    break

            if config_field is None:
                available_params = [
                    field.name
                    for field in fields(self._config)]
                raise ValueError(
                    f"未知配置参数: '{key}'。 "
                    f"可用参数: {', '.join(available_params)}"
                )

            # 参数验证
            self._validate_parameter(key, value)

            # 设置参数
            setattr(self._config, key, value)
            self._is_modified = True

    # ==================== 配置文件操作 ====================

    def load_config_file(self, file_path: Union[str, Path]):
        """
        从指定路径加载配置文件并更新当前配置。

        Args:
            file_path (Union[str, Path]): 配置文件的路径。

        Raises:
            FileNotFoundError: 如果指定路径的文件不存在。
            ValueError: 如果文件内容不是有效的 JSON 格式，或 JSON 结构不正确，
                        或文件中包含的配置值不符合验证规则。
            RuntimeError: 如果加载过程中发生其他不可预期的错误。
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"配置文件未找到: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)

            if not isinstance(config_data, dict):
                raise ValueError("配置文件内容必须是一个 JSON 对象 (字典)。")

            # 批量设置配置，这将触发每个参数的验证
            self.set_config(**config_data)
            self._config_source = str(file_path)

        except json.JSONDecodeError as e:
            raise ValueError(f"配置文件 '{file_path}' 的 JSON 格式无效: {e}")
        except ValueError as e:  # 捕获来自 set_config 的验证错误
            raise ValueError(f"从文件 '{file_path}' 加载的配置数据验证失败: {e}")
        except Exception as e:
            raise RuntimeError(f"加载配置文件 '{file_path}' 时发生错误: {e}")

    def save_config_file(self, file_path: Union[str, Path]):
        """
        将当前配置保存到指定路径的 JSON 文件。

        Args:
            file_path (Union[str, Path]): 保存配置文件的路径。如果父目录不存在，将自动创建。

        Raises:
            RuntimeError: 如果保存过程中发生错误。
        """
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            # 将 Config dataclass 实例转换为字典
            config_data = asdict(self._config)
            with open(file_path, 'w', encoding='utf-8') as f:
                # 使用 indent 进行美化打印，ensure_ascii=False 以支持中文
                json.dump(config_data, f, indent=2, ensure_ascii=False)

            self._is_modified = False  # 保存后重置修改状态

        except Exception as e:
            raise RuntimeError(f"保存配置文件 '{file_path}' 失败: {e}")

    # ==================== 配置管理 ====================

    def reset_config(self):
        """
        将当前配置重置为默认值。
        """
        self._config = Config()
        self._config_source = None
        self._is_modified = False

    def is_modified(self) -> bool:
        """
        检查当前配置自上次加载或保存以来是否被修改过。

        Returns:
            bool: 如果配置被修改过则返回 True，否则返回 False。
        """
        return self._is_modified

    def get_config_source(self) -> Optional[str]:
        """
        获取当前配置的来源文件路径。

        Returns:
            Optional[str]: 配置来源文件的路径字符串，如果配置不是从文件加载的则为 None。
        """
        return self._config_source

    # ==================== 配置验证 ====================

    def _validate_parameter(self, param_name: str, value: Any):
        """
        验证单个配置参数的值。

        Args:
            param_name (str): 配置参数的名称。
            value (Any): 要验证的参数值。

        Raises:
            ValueError: 如果参数值不符合预设的验证规则。
        """
        config_field = None
        for f in fields(self._config):
            if f.name == param_name:
                config_field = f
                break

        # 理论上，这个检查应在调用 _validate_parameter 之前完成，但作为安全措施仍保留。
        if config_field is None:
            raise ValueError(f"内部错误: 尝试验证未知参数 '{param_name}'。")

        if 'validator' in config_field.metadata:
            validator = config_field.metadata['validator']
            error_msg = config_field.metadata.get('error_msg', "值无效。")
            if not validator(value):
                raise ValueError(f"参数 '{param_name}' 验证失败: {error_msg} 给定值: {value}")
        # 如果 metadata 中没有定义 validator，则默认参数是有效的。

    # ==================== 诊断和工具方法 ====================

    def get_config_summary(self) -> Dict[str, Any]:
        """
        获取当前配置的摘要信息，按类别分组。

        Returns:
            Dict[str, Any]: 包含配置项及其当前值的字典，按 'category' 元数据分组，
                            并包含 'meta' 信息（如配置来源和修改状态）。
        """
        summary = {}
        config = self._config

        # 遍历 Config 类的所有字段
        for f in fields(config):
            category = f.metadata.get('category', 'uncategorized')  # 获取类别，默认为 'uncategorized'

            # 如果该类别在 summary 中不存在，则创建
            if category not in summary:
                summary[category] = {}

            # 将配置项及其当前值添加到对应的类别中
            summary[category][f.name] = getattr(config, f.name)

        # 添加元信息
        summary['meta'] = {
            'config_source': self._config_source,
            'is_modified': self._is_modified,
        }

        return summary

    def validate_all_config(self) -> List[str]:
        """
        验证当前所有配置项的值是否符合其定义规则。

        Returns:
            List[str]: 包含所有验证失败的错误消息列表。如果列表为空，表示所有配置项都有效。
        """
        errors = []
        # 遍历 Config dataclass 的所有字段
        for f in fields(self._config):
            param_name = f.name
            value = getattr(self._config, param_name)
            try:
                self._validate_parameter(param_name, value)
            except ValueError as e:
                errors.append(str(e))  # 附加错误消息

        return errors

    @staticmethod
    def create_config_template(file_path: Union[str, Path]):
        """
        创建一个包含所有默认配置项的 JSON 格式配置文件模板。

        Args:
            file_path (Union[str, Path]): 模板文件的保存路径。如果父目录不存在，将自动创建。
        """
        template = {
            "_comment":
                "MohuPy Configuration File Template",
            "_description":
                "Please modify the following configuration parameters as needed:",
            "_version": "1.0",

            # 实际配置参数
            **asdict(Config())
        }

        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2, ensure_ascii=False)

    # ==================== 未来扩展预留接口 ====================

    # TODO: 观察者模式和配置历史记录（预留接口）
    def add_config_observer(self, observer: Any):
        """
        添加一个配置变更观察者。

        Args:
            observer (Any): 实现了配置变更通知接口的观察者对象。
        """
        # 暂未实现，为未来扩展预留
        self._observers.append(observer)

    def remove_observer(self, observer: Any):
        """
        移除一个配置变更观察者。

        Args:
            observer (Any): 要移除的观察者对象。
        """
        # 暂未实现，为未来扩展预留
        if observer in self._observers:
            self._observers.remove(observer)

    def get_config_history(self) -> List[Any]:
        """
        获取配置变更历史记录。

        Returns:
            List[Any]: 配置变更历史记录的副本。
        """
        # 暂未实现，为未来扩展预留
        return self._config_history.copy()
