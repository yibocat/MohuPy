#  Copyright (c) yibocat 2025 All Rights Reserved
#  Python: 3.10.9
#  Date: 2025/7/26 15:06
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import collections
import weakref
from abc import ABC, abstractmethod
from typing import Set, Dict, Any, Callable, Optional, Union

from mohupy_.config import get_config
from mohupy_.core.triangular import OperationTNorm


class FuzznumStrategy(ABC):
    # 基础属性定义
    # 在模糊数各种类型里，任何模糊数都有一个 mtype 类型定义。而对于q，一般非q阶的直接设置为1 即可。
    # mtype 被设置为全局配置器的默认值
    q: int = 10
    mtype: str = get_config().DEFAULT_MTYPE

    # 私有属性管理
    _declared_attributes: Set[str] = set()

    # 属性验证器和回调函数
    _attribute_validators: Dict[str, Callable[[Any], bool]] = {}
    _change_callbacks: Dict[str, Callable[[str, Any, Any], None]] = {}

    # 注意：_attribute_validators 和 _change_callbacks 如果希望每个子类实例有自己独立的注册，
    # 应该在 __init__ 中初始化为实例属性。但如果它们是类级别的，表示所有实例共享同一套验证器/回调。
    # 鉴于 add_attribute_validator 和 add_change_callback 是实例方法，且修改的是 self._attribute_validators，
    # 它们实际上修改的是类属性（如果类属性没有被实例覆盖）。

    def __init__(self):

        # object.__setattr__(self, '_lock', threading.Lock())

        # 为 'q' 属性添加一个验证器。
        self.add_attribute_validator('q', lambda x: isinstance(x, int) and 1 <= x <= 100)
        # 'q' 是 FuzznumStrategy 的核心属性，它必须是大于等于1的正整数。
        # 将验证器添加到 _attribute_validators 字典中，确保每次通过 __setattr__ 设置 'q' 时都会进行验证。
        # 这比在 _validate() 中进行事后验证更及时、更有效。
        # 代码逻辑：调用 add_attribute_validator 方法，传入属性名 'q' 和一个 lambda 表达式作为验证函数。
        # 验证函数检查值是否为整数且大于等于 1。

    def __init_subclass__(cls, **kwargs):
        """
        子类初始化自动收集声明的属性
        """
        # 调用父类的 __init_subclass__ 方法，确保继承链上的所有基类都能正确初始化。
        super().__init_subclass__(**kwargs)

        # 初始化当前子类的 _declared_attributes 集合。
        # 注意：这里使用的是 `cls`（类本身），而不是 `self`（实例）。
        # 这意味着这个集合是类级别的，所有该子类的实例将共享同一个声明属性列表。
        cls._declared_attributes = set()

        for attr_name in dir(cls):

            if (not attr_name.startswith('_') and
                    hasattr(cls, attr_name) and
                    not callable(getattr(cls, attr_name))):
                # 排除以单下划线开头的私有属性（Python 约定），因为它们通常是内部实现细节，不应被外部直接访问或修改
                # 确保这个属性名确实存在于类中，以防 dir() 返回一些特殊名称。
                # 排除所有可调用的对象（即方法），因为我们只关心数据属性。

                # 将符合条件的属性名添加到 _declared_attributes 集合中。
                cls._declared_attributes.add(attr_name)
                # 这个集合将用于后续的严格模式检查（__setattr__）和属性序列化（to_dict/from_dict）。

    def __setattr__(self, name: str, value: Any) -> None:
        """属性设置方法"""

        # 内部属性和特殊属性的快速路径
        if name.startswith('_') or name == 'mtype':
            # 如果符合条件，直接调用父类 (object) 的 __setattr__ 方法来设置属性。
            super().__setattr__(name, value)
            # 这是一种“原始”的属性设置方式，不带任何自定义逻辑。
            # 代码逻辑：调用 FuzznumStrategy 的直接父类 (通常是 object 或 ABC) 的 __setattr__。

            return

        # 严格属性模式检查
        config = get_config()
        if (hasattr(config, 'STRICT_ATTRIBUTE_MODE') and
                config.STRICT_ATTRIBUTE_MODE and
                name not in self._declared_attributes):
            # 如果全局配置中存在 'STRICT_ATTRIBUTE_MODE' 且其值为 True (表示启用严格模式)，
            # 并且当前尝试设置的属性名 'name' 不在 `_declared_attributes` 集合中（这个集合
            # 是在 `__init_subclass__` 中自动收集的子类声明的属性），
            # 这意味着用户尝试设置一个未在类中明确声明的属性。

            raise AttributeError(
                f"Attribute '{name}' not declared in {self.__class__.__name__}. "
                f"Declared attributes: {sorted(self._declared_attributes)}"
            )
            # 抛出 AttributeError，明确指出哪个属性未声明，并列出所有已声明的属性，
            # 方便开发者调试和理解。

        # 获取旧值 (用于回调函数)
        old_value = getattr(self, name, None)

        # 属性值验证
        if name in self._attribute_validators:
            # 检查当前属性名 'name' 是否在 `_attribute_validators` 字典中注册了验证器。
            # 开发者可以通过 `add_attribute_validator` 方法为特定属性添加自定义的验证逻辑。

            validator = self._attribute_validators[name]
            # 如果存在，获取对应的验证函数。

            if not validator(value):
                # 调用获取到的验证函数，并传入即将设置的 'value'。
                # 如果验证函数返回 False (表示验证失败)，则抛出异常。
                raise ValueError(f"Validation failed for attribute '{name}' with value '{value}'")

        # 实际设置属性值
        super().__setattr__(name, value)
        # 在通过了所有前置检查（严格模式、属性验证）之后，
        # 最终调用父类 (object) 的 __setattr__ 方法来设置属性的实际值。
        # 这是属性设置的核心操作。

        # 执行属性变更回调
        if name in self._change_callbacks:

            # 如果存在，取出对应的回调函数
            callback = self._change_callbacks[name]
            try:
                callback(name, old_value, value)
            except ValueError as e:
                # 如果回调函数抛出 ValueError，表示这是一个明确的验证失败。
                raise ValueError(f"Attribute '{name}' change rejected by callback: {e}") from e

            except Exception as e:
                # 捕获回调函数执行时可能发生的任何异常
                raise RuntimeError(f"Callback for attribute '{name}' failed, "
                                   f"change has been rolled back.") from e

    def add_attribute_validator(self,
                                attr_name: str,
                                validator: Callable[[Any], bool]) -> None:
        """
        添加属性验证器

        实现属性级验证：它的核心意义是为单个属性提供细粒度的、可定制的验证逻辑。
        提高灵活性：允许开发者为不同的属性定义不同的验证规则，并且这些规则可以在运行时动态添加。
        即时反馈：验证在属性被设置时立即进行，如果值不合法，会立即抛出 ValueError，防止无效数据进入对象状态。

        Args:
            attr_name: 属性名
            validator: 验证函数，返回True表示验证通过
        """
        self._attribute_validators[attr_name] = validator

    def add_change_callback(self, attr_name: str, callback: Callable[[str, Any, Any], None]) -> None:
        """
        添加属性变更回调

        Args:
            attr_name: 属性名
            callback: 回调函数，参数为(属性名, 旧值, 新值)

        Returns:
            None

        Notes:
            - 实现属性变更的副作用：它的核心意义是允许在属性值成功改变后触发额外的行为或副作用。
            - 实现响应式编程：当一个属性的值发生变化时，可以自动执行预定义的逻辑，使得对象能够“响应”其内部状态的变化。
            - 提高可扩展性：开发者可以在不修改 FuzznumStrategy 或其子类核心代码的情况下，为任何属性添加新的响应行为。
        """
        self._change_callbacks[attr_name] = callback

    def get_declared_attributes(self) -> Set[str]:
        """
        获取声明的属性列表

        Returns:
            Set[str]: 包含所有声明属性名称的集合副本。

        Notes:
            - 提供内省能力：它的核心意义是允许外部代码查询一个 FuzznumStrategy 实例（或其子类）有哪些被明确声明为数据属性的成员。
        """
        return self._declared_attributes.copy()

    def validate_all_attributes(self) -> Dict[str, Any]:
        """
        验证所有属性值

        提供了一个统一的接口来触发对一个 FuzznumStrategy 实例的全面健康检查。

        Returns:
            Dict[str, Any]: 验证结果字典，包含验证状态和错误信息。
                            {'is_valid': bool, 'errors': List[str], 'warnings': List[str]}
        """
        validation_result = {
            'is_valid': True,
            'errors': [],
        }
        # 初始化一个字典来存储验证的结果。
        # 'is_valid' 标志表示整体验证是否通过，'errors' 列表收集所有错误信息，

        try:
            # 首先，调用 `_validate()` 方法。
            #  `_validate()` 是一个受保护的方法，通常由子类重写，用于执行特定于该策略类型
            #  的核心或复杂验证逻辑。例如，检查多个属性之间的关系（如 `md + nmd <= 1`）。
            #  如果 `_validate()` 发现严重问题，它会直接抛出异常（如 `ValueError`），
            #  此时外部的 `try-except` 块会捕获这个异常，并将其记录为错误。
            self._validate()

            # 接着，遍历所有在类中明确声明的属性（这些属性是在 `__init_subclass__` 中
            # 收集并存储在 `_declared_attributes` 集合中的）。
            # 这样做是为了确保我们只验证那些属于该策略模型的数据属性，而不是内部私有属性或方法。
            for attr_name in self._declared_attributes:
                if hasattr(self, attr_name):
                    value = getattr(self, attr_name)

                    # 检查是否有为这个属性注册了特定的验证器。
                    # 这些验证器是通过 `add_attribute_validator()` 方法添加的，
                    # 它们通常用于验证单个属性的合法性（例如，值是否在某个范围内、是否是特定类型）。
                    if attr_name in self._attribute_validators:
                        validator = self._attribute_validators[attr_name]

                        # 调用验证函数，并传入属性值。
                        # 如果验证函数返回 `False`，表示该属性的值不符合要求。
                        if not validator(value):
                            validation_result['errors'].append(
                                f"Attribute '{attr_name}' validation failed with value '{value}'"
                            )
                            # 标记验证结果
                            validation_result['is_valid'] = False

        # 捕获在 `_validate()` 方法或属性验证过程中可能抛出的任何异常。
        # 这样做是为了确保 `validate_all_attributes` 方法本身不会因为内部验证失败而崩溃，
        # 而是能够优雅地返回错误信息。
        except Exception as e:
            validation_result['errors'].append(f"Validation error: {e}")
            # 将捕获到的异常信息添加到 `errors` 列表中。

            validation_result['is_valid'] = False
            # 将整体验证状态标记为 `False`。

        return validation_result

    def _validate(self) -> None:
        """
        子类 可重写的验证方法

        此方法应包含特定于子类的验证逻辑。默认实现对 `mtype` 进行基本验证。

        Returns:
            None

        Notes:
            - 定制化：它允许每个具体的 FuzznumStrategy 子类定义其独特的、复杂的验证规则。这是实现策略模式中“不同策略有不同行为”的重要体现。
            - 核心约束：它通常用于检查那些构成模糊数定义的核心数学或逻辑约束，这些约束可能涉及多个属性的联合判断。
            - 快速失败：如果发现严重违反核心约束的情况，它会立即抛出异常，而不是仅仅收集错误信息。这表明对象当前的状态是不可接受的。
            - 继承链：子类在重写此方法时，通常会先调用 super()._validate() 来确保父类的基本验证也得到执行，体现了继承的层次性。

        Raises:
            ValueError: 如果 `mtype` 不符合预期。
        """
        # 这是一个受保护的方法（以下划线开头），意味着它主要供类内部使用或由子类重写。
        # 它的核心目的是提供一个“钩子”（hook），让具体的策略子类能够在此处实现
        # 它们特有的、通常是多属性关联的、或涉及复杂计算的、或在设置时无法立即判断的验证逻辑。
        # 例如，检查模糊数成员度和非成员度之和的约束。

        # 在 `ExampleStrategy` 等子类中，这个方法会被重写，
        # 并且通常会先调用 `super()._validate()` 来执行父类的默认验证，
        # 然后再添加子类特有的验证逻辑。
        if hasattr(self, 'mtype') and (not isinstance(self.mtype, str) or not self.mtype.strip()):
            raise ValueError(f"mtype must be a non-empty string, got '{self.mtype}'")

    def to_dict(self) -> Dict[str, Any]:
        """
        将策略实例转换为字典

        此方法将所有声明的属性及其当前值转换为一个字典。

        Returns:
            Dict[str, Any]: 包含所有声明属性的字典。
        """
        result = {}
        for attr_name in self._declared_attributes:
            if hasattr(self, attr_name):
                result[attr_name] = getattr(self, attr_name)

        return result

    def from_dict(self, data: Dict[str, Any]) -> None:
        """
        从字典设置属性值

        此方法根据传入的字典设置策略实例的属性。
        只会设置那些在 `_declared_attributes` 中存在的属性。

        Args:
            data: 属性字典
        """
        for attr_name, value in data.items():
            if attr_name in self._declared_attributes:
                setattr(self, attr_name, value)

    def add(self, other_strategy: 'FuzznumStrategy', tnorm: OperationTNorm) -> Dict[str, Any]:
        raise NotImplementedError(f"The operation of fuzzy numbers with '{self.mtype}' under the "
                                  f"t-norm '{tnorm.norm_type}' is not yet implemented.")

    def sub(self, other_strategy: 'FuzznumStrategy', tnorm: OperationTNorm) -> Dict[str, Any]:
        raise NotImplementedError(f"The operation of fuzzy numbers with '{self.mtype}' under the "
                                  f"t-norm '{tnorm.norm_type}' is not yet implemented.")

    def mul(self, other_strategy: 'FuzznumStrategy', tnorm: OperationTNorm) -> Dict[str, Any]:
        raise NotImplementedError(f"The operation of fuzzy numbers with '{self.mtype}' under the "
                                  f"t-norm '{tnorm.norm_type}' is not yet implemented.")

    def div(self, other_strategy: 'FuzznumStrategy', tnorm: OperationTNorm) -> Dict[str, Any]:
        raise NotImplementedError(f"The operation of fuzzy numbers with '{self.mtype}' under the "
                                  f"t-norm '{tnorm.norm_type}' is not yet implemented.")

    def pow(self, other_operand: Union[int, float], tnorm: OperationTNorm) -> Dict[str, Any]:
        raise NotImplementedError(f"The operation of fuzzy numbers with '{self.mtype}' under the "
                                  f"t-norm '{tnorm.norm_type}' is not yet implemented.")

    def tim(self, other_operand: Union[int, float], tnorm: OperationTNorm) -> Dict[str, Any]:
        raise NotImplementedError(f"The operation of fuzzy numbers with '{self.mtype}' under the "
                                  f"t-norm '{tnorm.norm_type}' is not yet implemented.")

    def exp(self, other_operand: Union[int, float], tnorm: OperationTNorm) -> Dict[str, Any]:
        raise NotImplementedError(f"The operation of fuzzy numbers with '{self.mtype}' under the "
                                  f"t-norm '{tnorm.norm_type}' is not yet implemented.")

    def log(self, other_operand: Union[int, float], tnorm: OperationTNorm) -> Dict[str, Any]:
        raise NotImplementedError(f"The operation of fuzzy numbers with '{self.mtype}' under the "
                                  f"t-norm '{tnorm.norm_type}' is not yet implemented.")

    def gt(self, other_strategy: 'FuzznumStrategy', tnorm: OperationTNorm) -> Dict[str, Any]:
        raise NotImplementedError(f"The operation of fuzzy numbers with '{self.mtype}' under the "
                                  f"t-norm '{tnorm.norm_type}' is not yet implemented.")

    def lt(self, other_strategy: 'FuzznumStrategy', tnorm: OperationTNorm) -> Dict[str, Any]:
        raise NotImplementedError(f"The operation of fuzzy numbers with '{self.mtype}' under the "
                                  f"t-norm '{tnorm.norm_type}' is not yet implemented.")

    def ge(self, other_strategy: 'FuzznumStrategy', tnorm: OperationTNorm) -> Dict[str, Any]:
        raise NotImplementedError(f"The operation of fuzzy numbers with '{self.mtype}' under the "
                                  f"t-norm '{tnorm.norm_type}' is not yet implemented.")

    def le(self, other_strategy: 'FuzznumStrategy', tnorm: OperationTNorm) -> Dict[str, Any]:
        raise NotImplementedError(f"The operation of fuzzy numbers with '{self.mtype}' under the "
                                  f"t-norm '{tnorm.norm_type}' is not yet implemented.")

    def eq(self, other_strategy: 'FuzznumStrategy', tnorm: OperationTNorm) -> Dict[str, Any]:
        raise NotImplementedError(f"The operation of fuzzy numbers with '{self.mtype}' under the "
                                  f"t-norm '{tnorm.norm_type}' is not yet implemented.")

    def ne(self, other_strategy: 'FuzznumStrategy', tnorm: OperationTNorm) -> Dict[str, Any]:
        raise NotImplementedError(f"The operation of fuzzy numbers with '{self.mtype}' under the "
                                  f"t-norm '{tnorm.norm_type}' is not yet implemented.")

    def intersection(self, other_strategy: 'FuzznumStrategy', tnorm: OperationTNorm) -> Dict[str, Any]:
        raise NotImplementedError(f"The operation of fuzzy numbers with '{self.mtype}' under the "
                                  f"t-norm '{tnorm.norm_type}' is not yet implemented.")

    def union(self, other_strategy: 'FuzznumStrategy', tnorm: OperationTNorm) -> Dict[str, Any]:
        raise NotImplementedError(f"The operation of fuzzy numbers with '{self.mtype}' under the "
                                  f"t-norm '{tnorm.norm_type}' is not yet implemented.")

    def complement(self, other_strategy: 'FuzznumStrategy', tnorm: OperationTNorm) -> Dict[str, Any]:
        raise NotImplementedError(f"The operation of fuzzy numbers with '{self.mtype}' under the "
                                  f"t-norm '{tnorm.norm_type}' is not yet implemented.")

    def implication(self, other_strategy: 'FuzznumStrategy', tnorm: OperationTNorm) -> Dict[str, Any]:
        raise NotImplementedError(f"The operation of fuzzy numbers with '{self.mtype}' under the "
                                  f"t-norm '{tnorm.norm_type}' is not yet implemented.")

    def equivalence(self, other_strategy: 'FuzznumStrategy', tnorm: OperationTNorm) -> Dict[str, Any]:
        raise NotImplementedError(f"The operation of fuzzy numbers with '{self.mtype}' under the "
                                  f"t-norm '{tnorm.norm_type}' is not yet implemented.")

    def difference(self, other_strategy: 'FuzznumStrategy', tnorm: OperationTNorm) -> Dict[str, Any]:
        raise NotImplementedError(f"The operation of fuzzy numbers with '{self.mtype}' under the "
                                  f"t-norm '{tnorm.norm_type}' is not yet implemented.")

    def symdiff(self, other_strategy: 'FuzznumStrategy', tnorm: OperationTNorm) -> Dict[str, Any]:
        raise NotImplementedError(f"The operation of fuzzy numbers with '{self.mtype}' under the "
                                  f"t-norm '{tnorm.norm_type}' is not yet implemented.")


class FuzznumTemplate(ABC):
    """
    模糊数模板抽象基类，定义了模糊数的表示方式和相关辅助功能
    """

    mtype: str = get_config().DEFAULT_MTYPE

    def __init__(self, instance: Any):
        if instance is None:
            raise ValueError("Template instance cannot be None.")

        # 创建对传入 `instance`（通常是 Fuzznum 实例）的弱引用。
        self._instance_ref = weakref.ref(instance, self._on_instance_cleanup)

        self._instance_id = id(instance)
        # 存储关联实例的唯一标识符（内存地址）。

        # 初始化一个布尔标志，表示当前模板实例是否仍然有效
        # 如果关联的 Fuzznum 实例被垃圾回收，此标志将变为 False。
        self._is_valid = True

        config = get_config()
        self._max_cache_size = getattr(config, 'TEMPLATE_CACHE_SIZE', 256)
        self._template_cache: collections.OrderedDict = collections.OrderedDict()
        # 初始化一个空字典，作为模板计算结果的缓存。
        # 模板通常会生成报告字符串、简洁字符串表示或计算得分等，这些结果可以被缓存起来，

        # 缓存开启默认为 True，表示缓存是启用的。
        self._cache_enabled = config.ENABLE_CACHE

    def _on_instance_cleanup(self, ref: weakref.ref) -> None:
        """实例被垃圾回收时的清理回调"""
        self._is_valid = False
        self._template_cache.clear()

    @property
    def instance(self) -> Any:
        if not self._is_valid:
            # 首先检查 `_is_valid` 标志。如果它已经是 False，说明关联实例已经被回收，
            raise RuntimeError(
                f"Template for mtype '{self.mtype}' is no longer valid. "
                f"Associated Fuzznum instance (id: {self._instance_id}) has been garbage collected."
            )

        instance = self._instance_ref()

        if instance is None:
            # 如果弱引用返回 None，说明 Fuzznum 实例在上次检查后已被回收。

            self._is_valid = False

            raise RuntimeError(
                f"Template for mtype '{self.mtype}' has lost its Fuzznum instance "
                f"(id: {self._instance_id}). Instance has been garbage collected."
            )

        return instance

    def is_template_valid(self) -> bool:
        """检查模板是否仍然有效"""

        if not self._is_valid:
            return False

        instance = self._instance_ref()

        if instance is None:
            self._is_valid = False
            return False

        return True

    def get_cached_value(self, key: str, compute_func: Optional[Callable[[], Any]] = None) -> Any:
        """
        获取缓存值，如果不存在则计算并缓存

        一般就是模糊数中的一些特殊属性值，比如得分函数，准确函数等等
        对于一些复杂的得分函数，没必要一直重新算。

        Args:
            key: 缓存键
            compute_func: 计算函数，当缓存不存在时调用

        Returns:
            缓存的值或计算的新值
        """
        # 如果缓存机制被禁用，则直接执行计算函数（如果提供），不进行缓存操作。
        if not self._cache_enabled:
            return compute_func() if compute_func else None

        # 检查缓存中是否已经存在指定 `key` 的值。
        # 命中缓存，将其移到末尾表示最近使用
        if key in self._template_cache:
            self._template_cache.move_to_end(key)
            return self._template_cache[key]

        # 如果缓存中没有，并且提供了 `compute_func`（计算函数）。
        # 调用 `compute_func` 来计算值。`compute_func` 应该是一个无参数的函数。
        # 将计算得到的值存储到缓存中，以便下次访问时可以直接获取。
        # 检查缓存是否超过大小限制，如果是，则移除最旧的条目
        if compute_func:
            value = compute_func()
            self._template_cache[key] = value
            if len(self._template_cache) > self._max_cache_size:
                self._template_cache.popitem(last=False)
            return value

        return None

    def clear_cache(self) -> None:
        """清空模板缓存"""
        self._template_cache.clear()

    def enable_cache(self) -> None:
        """启用缓存"""
        self._cache_enabled = True

    def disable_cache(self) -> None:
        """禁用缓存并清空现有缓存"""
        self._cache_enabled = False
        self.clear_cache()

    def report(self) -> str:
        """生成模糊数报告"""
        raise NotImplementedError("report method must be implemented by subclasses")

    def str(self) -> str:
        """生成模糊数字符串表示"""
        raise NotImplementedError("str method must be implemented by subclasses")

    def get_template_info(self) -> Dict[str, Any]:
        """
        获取模板信息

        Returns:
            包含模板状态和缓存信息的字典
        """
        return {
            'mtype': self.mtype,  # 模板关联的模糊数类型。
            'is_valid': self._is_valid,  # 模板是否仍然有效（关联实例是否还存在）。
            'instance_id': self._instance_id,  # 关联 Fuzznum 实例的唯一 ID。
            'cache_enabled': self._cache_enabled,  # 缓存是否启用。
            'cache_size': len(self._template_cache),  # 缓存中存储的条目数量。
            'cache_keys': list(self._template_cache.keys())
            # 缓存中的所有键列表。如果键的数量超过 10 个，则只显示数量，以避免输出过长。
            if len(self._template_cache) < 10 else f"{len(self._template_cache)} items"
        }


# ======================== 改进的示例实现 ========================
# 并不参与到初始化和任何运算过程，仅仅用来展示一个示例

class ExampleStrategy(FuzznumStrategy):
    """一个示例模糊数策略类，演示了如何定义隶属度和非隶属度属性，并为其添加验证和回调。

    此类继承自 `FuzznumStrategy`，具体实现了模糊数的核心属性 `md`（隶属度）和 `nmd`（非隶属度）。
    它展示了如何利用基类提供的机制来：
        - 为 `md` 和 `nmd` 设置值范围验证器。
        - 在 `md` 或 `nmd` 改变时触发回调，检查模糊数的基本约束（`md + nmd <= 1`）。
        - 扩展基础的验证逻辑，在 `_validate` 方法中强制检查 `md + nmd` 的和。

    Attributes:
        mtype (str): 该策略对应的模糊数类型标识符，固定为 "example_fuzznum"。
        md (Optional[float]): 隶属度，一个可选的浮点数，表示元素属于模糊集的程度。
            其值应在 [0, 1] 范围内。
        nmd (Optional[float]): 非隶属度，一个可选的浮点数，表示元素不属于模糊集的程度。
            其值应在 [0, 1] 范围内。
    """
    mtype = "example_fuzznum"
    md: Optional[float] = None
    nmd: Optional[float] = None

    def __init__(self):
        """初始化 ExampleStrategy 实例。

        在此构造函数中，会调用父类的初始化方法，并为 `md` 和 `nmd` 属性注册验证器和变更回调。
        """
        super().__init__()
        # 调用父类 FuzznumStrategy 的初始化方法，这将初始化实例锁并为 'q' 属性添加验证器。

        # 添加属性验证器
        self.add_attribute_validator('md', lambda x: x is None or (isinstance(x, (int, float)) and 0 <= x <= 1))
        self.add_attribute_validator('nmd', lambda x: x is None or (isinstance(x, (int, float)) and 0 <= x <= 1))
        # 为 'md' 属性添加一个验证器。该验证器确保 'md' 的值要么是 None，要么是一个在 [0, 1] 范围内的整数或浮点数。
        # 为 'nmd' 属性添加一个验证器。该验证器确保 'nmd' 的值要么是 None，要么是一个在 [0, 1] 范围内的整数或浮点数。

        # 添加变更回调
        self.add_change_callback('md', self._on_membership_change)
        self.add_change_callback('nmd', self._on_membership_change)
        # 当 'md' 属性的值发生变化时，注册 `_on_membership_change` 方法作为回调函数。
        # 当 'nmd' 属性的值发生变化时，注册 `_on_membership_change` 方法作为回调函数。

    def _on_membership_change(self, attr_name: str, old_value: Any, new_value: Any) -> None:
        """隶属度或非隶属度变更时的回调函数。

        此回调函数在 `md` 或 `nmd` 属性被设置时触发。它会检查模糊数约束条件
        `md + nmd <= 1`，如果违反则发出警告。

        Args:
            attr_name (str): 发生变化的属性名（'md' 或 'nmd'）。
            old_value (Any): 属性的旧值。
            new_value (Any): 属性的新值。
        """
        if new_value is not None and hasattr(self, 'md') and hasattr(self, 'nmd'):
            # 只有当新值不为 None，并且实例上同时存在 'md' 和 'nmd' 属性时才执行后续检查。
            # 这确保了在对象初始化过程中，当属性可能尚未完全设置时，不会触发不完整的检查。

            if self.md is not None and self.nmd is not None:
                # 只有当 'md' 和 'nmd' 都已被赋值（非 None）时，才执行模糊数约束检查。
                # 检查模糊数约束条件：通常，隶属度 (md) 和非隶属度 (nmd) 之和不应大于 1。
                if self.md + self.nmd > 1:
                    # **关键修改：从 warnings.warn 改为 raise ValueError。**
                    # **这会触发 FuzznumStrategy.__setattr__ 中的回滚逻辑。**
                    raise ValueError(f"md + nmd = {self.md + self.nmd} > 1, violates fuzzy number constraints")

    def _validate(self) -> None:
        """
        扩展策略的验证方法，添加对隶属度和非隶属度之和的检查。

        此方法在父类 `_validate` 的基础上，进一步检查 `md` 和 `nmd` 属性的组合约束。
        如果 `md + nmd` 的和大于 1，则抛出 `ValueError`。
        """
        super()._validate()
        # 调用父类 FuzznumStrategy 的 _validate 方法，执行其默认的验证逻辑（例如对 mtype 的检查）。

        # 检查隶属度和非隶属度的约束：md + nmd 必须不大于 1。
        # 只有当 'md' 和 'nmd' 都已被赋值（非 None）时，才执行此组合约束检查。
        if (self.md is not None and self.nmd is not None and
                self.md + self.nmd > 1):
            raise ValueError(f"md + nmd = {self.md + self.nmd} must not exceed 1")
            # 如果 md 和 nmd 的和大于 1，则抛出 ValueError，指示模糊数的状态无效。


class ExampleTemplate(FuzznumTemplate):
    """
    一个改进的示例模糊数模板实现，演示了如何生成模糊数的字符串表示、详细报告，以及添加自定义的计算方法。

    此类继承自 `FuzznumTemplate`，为 "example_fuzznum" 类型的模糊数提供了具体的表示逻辑。
    它展示了如何利用基类的缓存机制来：
        - 生成简洁的字符串表示（`str`）。
        - 生成详细的报告字符串（`report`）。
        - 计算一个自定义的得分函数（`score`）。
    所有这些计算结果都会被缓存，以提高重复访问的性能。

    Attributes:
        mtype (str): 该模板对应的模糊数类型标识符，固定为 "example_fuzznum"。
    """

    mtype = "example_fuzznum"

    def report(self) -> str:
        """生成模糊数的详细报告字符串。

        此方法利用 `FuzznumTemplate` 的缓存机制，生成一个包含模糊数所有关键参数的详细报告。
        报告内容包括隶属度 (`md`)、非隶属度 (`nmd`) 和阶数 (`q`)。

        Returns:
            str: 详细的模糊数报告字符串，例如 "ExampleFuzz(md=0.8, nmd=0.1, q=2)"。
        """
        return self.get_cached_value(
            'report',
            # 缓存键，用于在 _template_cache 中查找或存储报告字符串。
            lambda: f"ExampleFuzz(md={self.instance.md}, nmd={self.instance.nmd}, q={self.instance.q})"
            # 计算报告字符串的函数。
            # 它通过 `self.instance` 安全地访问关联 Fuzznum 实例的属性。
        )

    def str(self) -> str:
        """生成模糊数的简洁字符串表示。

        此方法利用 `FuzznumTemplate` 的缓存机制，生成一个简洁的模糊数字符串表示。
        通常用于 `print()` 或 `str()` 调用。

        Returns:
            str: 简洁的模糊数字符串表示，例如 "<0.8,0.1>_q=2"。
        """
        return self.get_cached_value(
            'str',
            # 缓存键，用于在 _template_cache 中查找或存储简洁字符串表示。
            lambda: f"<{self.instance.md},{self.instance.nmd}>_q={self.instance.q}"
            # 计算简洁字符串表示的函数。
            # 它通过 `self.instance` 安全地访问关联 Fuzznum 实例的属性。
        )

    def score(self) -> float:
        """计算模糊数的得分函数。

        此方法计算模糊数的得分，定义为隶属度与非隶属度之差 (`md - nmd`)。
        它利用 `FuzznumTemplate` 的缓存机制，避免重复计算。
        如果 `md` 或 `nmd` 为 None，则在计算中将其视为 0。

        Returns:
            float: 计算得到的模糊数得分。
        """
        return self.get_cached_value(
            'score',
            # 缓存键，用于在 _template_cache 中查找或存储得分。
            lambda: (self.instance.md or 0) - (self.instance.nmd or 0)
            # 计算得分的函数。
            # `(self.instance.md or 0)` 确保如果 md 为 None，则使用 0 进行计算，避免 TypeError。
        )