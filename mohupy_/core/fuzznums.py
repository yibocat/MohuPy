#  Copyright (c) yibocat 2025 All Rights Reserved
#  Python: 3.10.9
#  Date: 2025/7/26 18:20
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import difflib
import threading
import datetime
import warnings
from contextlib import contextmanager
from typing import Optional, Any, Dict, Callable, Set, List

from mohupy_.config import get_config
from mohupy_.core.base import FuzznumStrategy, FuzznumTemplate
from mohupy_.core.registry import get_registry


class Fuzznum:

    # 这是一个类级别的集合，用于存储 Fuzznum 实例在初始化过程中或其生命周期内，
    # 需要通过 Python 内置的 `object.__setattr__` 和 `object.__getattribute__`
    # 直接访问和设置的内部属性名称。
    _INTERNAL_ATTRS = {
        'mtype',  # 模糊数类型标识符，核心且不可变。
        # 'q',
        '_initialized',  # 实例初始化状态标志，防止在初始化完成前进行不安全操作。
        '_lock',  # 实例级别的可重入锁，用于保护并发访问和修改。
        '_creation_time',  # 实例创建时的时间戳，用于计算对象存活时间。
        '_attr_cache',  # 内部属性缓存字典，存储委托属性的最新值。
        '_cache_enabled',  # 控制属性缓存是否启用的布尔标志。
        '_access_stats',  # 属性访问统计字典，记录各属性访问次数。
        '_monitor_enabled',  # 控制性能监控是否启用的布尔标志。
        '_access_times',  # 属性最近访问时间字典，记录各属性的最新访问时间戳。
        '_strategy_instance',  # 关联的 FuzznumStrategy 实例。
        '_template_instance',  # 关联的 FuzznumTemplate 实例。
        '_bound_strategy_methods',  # 从策略实例动态绑定到 Fuzznum 实例的方法字典。
        '_bound_strategy_attributes',  # 从策略实例动态绑定到 Fuzznum 实例的属性名称集合。
        '_bound_template_methods',  # 从模板实例动态绑定到 Fuzznum 实例的方法字典。
        '_bound_template_attributes',  # 从模板实例动态绑定到 Fuzznum 实例的属性名称集合。
        '_validation_cache',  # 内部验证缓存，用于存储验证结果，避免重复验证。
    }

    def __init__(self, mtype: Optional[str] = None, qrung: Optional[int] = None):
        object.__setattr__(self, '_creation_time',
                           float(datetime.datetime.now().strftime("%Y%m%d%H%M%S.%f")))
        object.__setattr__(self, '_initialized', False)
        object.__setattr__(self, '_lock', threading.RLock())
        object.__setattr__(self, '_attr_cache', {})
        object.__setattr__(self, '_cache_enabled', get_config().ENABLE_FUZZNUM_CACHE)
        object.__setattr__(self, '_access_stats', {})
        object.__setattr__(self, '_validation_cache', {})
        object.__setattr__(self, '_monitor_enabled',
                           get_config().ENABLE_PERFORMANCE_MONITORING)
        object.__setattr__(self, '_access_times', {})

        config = get_config()
        if mtype is None:
            mtype = config.DEFAULT_MTYPE
            warnings.warn(f"Fuzzy number type not specified, using default type: '{mtype}'")

        if qrung is None:
            qrung = 1

        if not isinstance(mtype, str):
            raise TypeError(f"mtype must be a string type, got '{type(mtype).__name__}'")

        if not isinstance(qrung, int):
            raise TypeError(f"qrung must be an integer, got '{type(qrung).__name__}'")

        object.__setattr__(self, 'mtype', mtype)
        object.__setattr__(self, 'q', qrung)

        # 执行具体的初始化流程，并处理可能的异常
        # 尝试调用 `_initialize` 方法来完成 Fuzznum 实例的复杂初始化逻辑，
        # 包括配置策略、模板和性能监控。
        try:
            self._initialize()
            # 在 `_initialize` 成功完成后，将 `_initialized` 标志设置为 True。
            # 这个标志对于 `__getattr__` 和 `__setattr__` 方法至关重要，
            # 它们会根据这个标志来判断实例是否已完成初始化，从而避免在不完整状态下进行属性访问和设置。

            object.__setattr__(self, '_initialized', True)

        except Exception:
            self._cleanup_partial_initialization()
            raise

    def _initialize(self) -> None:
        """执行具体的初始化流程"""

        self._configure_strategy()
        self._configure_template()

        # 设置性能监控机制
        self._setup_performance_monitoring()

    def _configure_strategy(self) -> None:

        # 获取全局注册表实例，用于查找和管理模糊数策略和模板
        registry = get_registry()

        # 检查当前 mtype 是否在注册表中存在对应的策略。
        # 如果不存在，表示该模糊数类型不被支持，抛出 ValueError。
        # 这确保了只有已注册的、有效的模糊数类型才能被实例化。
        if self.mtype not in registry.strategies:
            available_mtypes = ', '.join(registry.strategies.keys())
            raise ValueError(
                f"Unsupported strategy mtype: '{self.mtype}'."
                f"Available mtypes: {available_mtypes}"
            )

        # 从注册表中获取并实例化与当前 mtype 对应的 FuzznumStrategy 类。
        # 例如，如果 mtype 是 'qrofn'，这里会创建 QROFNStrategy 的一个实例。
        strategy_instance = registry.strategies[self.mtype](self.q)
        # 调用 `_bind_instance_members` 辅助方法，将策略实例的公共方法和属性绑定到当前的 Fuzznum 实例上。
        # 这样，用户就可以直接通过 Fuzznum 实例访问策略的方法和属性（例如 `fuzznum_instance.md` 或 `fuzznum_instance.calculate_value()`)，
        # 而无需先获取策略实例，实现了透明的属性委托。
        bound_methods, bound_attributes = self._bind_instance_members(
            strategy_instance, 'strategy'
        )

        # 使用 `object.__setattr__` 安全地存储策略实例和绑定成员的信息。
        # 这些属性属于内部管理，同样需要避免触发自定义的 `__setattr__`。
        object.__setattr__(self, '_strategy_instance', strategy_instance)
        object.__setattr__(self, '_bound_strategy_methods', bound_methods)
        object.__setattr__(self, '_bound_strategy_attributes', bound_attributes)

    def _configure_template(self) -> None:
        """配置模板实例并绑定其方法和属性"""
        # 获取全局注册表实例。
        registry = get_registry()

        # 检查当前 mtype 是否在注册表中存在对应的模板。
        # 类似的，如果不存在，抛出 ValueError。
        if self.mtype not in registry.templates:
            available_templates = ', '.join(registry.templates.keys())
            raise ValueError(
                f"Unsupported template mtype: '{self.mtype}'."
                f"Available templates: {available_templates}"
            )

        # 从注册表中获取并实例化与当前 mtype 对应的 FuzznumTemplate 类。
        # 关键点：在实例化模板时，将当前的 `Fuzznum` 实例 `self` 作为参数传递给模板的构造函数。
        # 这使得模板实例能够持有对其关联的 Fuzznum 实例的引用（通常是弱引用），
        # 从而在模板内部访问 Fuzznum 实例的属性和方法（例如 `self.instance.md`）。
        template_instance = registry.templates[self.mtype](self)
        # 调用 `_bind_instance_members` 辅助方法，将模板实例的公共方法和属性绑定到当前的 Fuzznum 实例上。
        # 这样，用户就可以直接通过 Fuzznum 实例访问模板的方法和属性（例如 `fuzznum_instance.report()` 或 `fuzznum_instance.str()`）。
        bound_methods, bound_attributes = self._bind_instance_members(
            template_instance, 'template'
        )

        # 使用 `object.__setattr__` 安全地存储模板实例和绑定成员的信息。
        object.__setattr__(self, '_template_instance', template_instance)
        object.__setattr__(self, '_bound_template_methods', bound_methods)
        object.__setattr__(self, '_bound_template_attributes', bound_attributes)

    def _bind_instance_members(self,
                               instance: Any,
                               instance_type: str) -> tuple[Dict[str, Callable[..., Any]], Set[str]]:
        """
        绑定实例的方法和属性到当前对象

        这个方法是 Fuzznum 类实现“门面模式”（Facade Pattern）的关键。
        它负责将底层 `FuzznumStrategy` 或 `FuzznumTemplate` 实例的公共方法和属性，
        动态地“复制”或“绑定”到 Fuzznum 实例自身上。
        这样，外部用户可以直接通过 Fuzznum 对象访问这些方法和属性，
        而无需直接与策略或模板实例交互，从而简化了 API 和提高了抽象层次。

        Args:
            instance: 要绑定其成员的策略或模板实例。
            instance_type: 实例的类型，用于区分处理（例如 'strategy' 或 'template'）。

        Returns:
            tuple[Dict[str, Callable[..., Any]], Set[str]]:
                一个元组，包含两个元素：

                    1. bound_methods (Dict[str, Callable[..., Any]]): 绑定到 Fuzznum 实例上的方法字典，
                       键为方法名，值为方法本身。
                    2. bound_attributes (Set[str]): 绑定到 Fuzznum 实例上的属性名集合。

        Raises:
            RuntimeError: 如果在绑定过程中发生任何异常。
        """
        bound_methods: Dict[str, Callable[..., Any]] = {}
        bound_attributes: Set[str] = set()
        # 定义需要排除的属性名称。
        # 对于模板实例，'mtype' 和 'instance'（指向 Fuzznum 自身的引用）通常不应该被直接绑定，
        # 因为它们是模板内部管理或与 Fuzznum 关联的特殊属性。
        # 对于策略实例，只排除 'mtype'。
        exclude_attrs = {'mtype', 'instance'} if instance_type == 'template' else {'mtype'}

        try:
            # 遍历传入实例的所有成员名称。
            # `dir(instance)` 会返回实例的所有属性和方法名称，包括继承来的。
            for attr_name in dir(instance):
                # 过滤掉私有属性（以单下划线开头的）和预定义的排除属性。
                # 私有属性通常是内部实现细节，不应暴露给 Fuzznum 实例的外部接口。
                if attr_name.startswith('_') or attr_name in exclude_attrs:
                    continue

                # 获取属性描述符，用于判断是否是 property。
                # `getattr(instance.__class__, attr_name, None)` 尝试从类的角度获取属性，
                # 这对于识别 `property` 很有用，因为 `property` 是类级别的描述符。
                attr_descriptor = getattr(instance.__class__, attr_name, None)

                # 判断成员类型并进行绑定。
                # 如果是 property，则将其名称添加到 `bound_attributes` 集合中。
                # `property` 属性的值通常通过 `__getattr__` 动态获取，而不是直接绑定。
                if isinstance(attr_descriptor, property):
                    bound_attributes.add(attr_name)
                else:
                    # 如果不是 property，则获取其实际值。
                    attr_value = getattr(instance, attr_name)
                    # 如果是可调用对象（即方法），则直接绑定到 Fuzznum 实例上。
                    # 使用 `object.__setattr__` 是为了避免触发 Fuzznum 自身重写的 `__setattr__`，
                    # 从而防止在绑定过程中可能出现的递归问题。
                    if callable(attr_value):
                        object.__setattr__(self, attr_name, attr_value)
                        bound_methods[attr_name] = attr_value
                    else:
                        # 如果是普通数据属性（非 property 且不可调用），则将其名称添加到 `bound_attributes` 集合。
                        # 这些属性的值也将通过 `__getattr__` 动态获取。
                        bound_attributes.add(attr_name)

            # 返回绑定方法和属性的字典/集合。
            return bound_methods, bound_attributes

        except Exception as e:
            # 捕获绑定过程中可能发生的任何异常，并重新抛出为 RuntimeError，
            # 提供了更清晰的错误信息，指明是哪个实例类型的绑定失败。
            raise RuntimeError(f"{instance_type} '{self.mtype}' 的动态绑定失败: {e}")

    def _setup_performance_monitoring(self) -> None:
        """
        设置性能监控

        根据全局配置决定是否启用对 Fuzznum 实例属性访问的性能监控。
        如果启用，系统将记录哪些属性被访问了多少次，以及最近的访问时间。
        这对于调试、性能分析和优化非常有用。
        """
        config = get_config()
        # 检查配置对象中是否存在 `ENABLE_PERFORMANCE_MONITORING` 属性，
        # 并且该属性的值是否为 True。
        # `hasattr` 用于安全地检查属性是否存在，避免因配置中缺少该属性而引发 AttributeError。

        if hasattr(config, 'ENABLE_PERFORMANCE_MONITORING') and config.ENABLE_PERFORMANCE_MONITORING:
            # 如果配置启用了性能监控，则将实例的 `_monitor_enabled` 内部属性设置为 True。
            # 同样使用 `object.__setattr__` 确保在初始化阶段安全设置。
            object.__setattr__(self, '_monitor_enabled', True)

    def _cleanup_partial_initialization(self) -> None:
        """
        清理部分初始化的状态

        当 Fuzznum 实例的构造函数 `__init__` 在执行过程中遇到异常时，
        此方法会被调用。它的目的是清理或重置那些可能已经部分初始化但尚未完全配置的内部属性，
        以防止实例处于不一致或损坏的状态。这有助于在初始化失败后，
        避免资源泄露或后续操作中出现意外行为。
        """
        # 定义一个列表，包含所有需要清理的内部属性名称。
        # 这些属性通常在 `_initialize` 方法中被设置。
        cleanup_attrs = [
            '_strategy_instance',
            '_template_instance',
            '_bound_strategy_methods',
            '_bound_strategy_attributes',
            '_bound_template_methods',
            '_bound_template_attributes',
            '_attr_cache',
            '_access_stats',
            '_validation_cache'
        ]

        # 遍历需要清理的属性列表。
        for attr in cleanup_attrs:
            try:
                # 尝试删除实例的属性。
                # `object.__delattr__` 用于直接删除属性，绕过自定义的 `__delattr__`（如果有）。
                object.__delattr__(self, attr)
            except AttributeError:
                # 如果属性不存在，则捕获 AttributeError 并静默忽略。
                # 这意味着即使某个属性在异常发生前没有被设置，清理过程也不会中断。
                pass

    def _is_initialized(self) -> bool:
        """
        安全地检查初始化状态，避免递归调用

        此方法提供了一种安全、无副作用的方式来查询 Fuzznum 实例的初始化状态。
        它被 `__getattr__` 和 `__setattr__` 等方法调用，
        以判断实例是否已经完成了所有的初始化步骤。
        这对于防止在对象尚未完全准备好时进行属性访问或修改而导致的递归或错误至关重要。

        Returns:
            bool: 如果实例已完全初始化则返回 True，否则返回 False。
        """
        try:
            # 直接使用 `object.__getattribute__` 来获取 `_initialized` 属性的值。
            # 这是为了确保在检查初始化状态时，不会触发 Fuzznum 自身重写的 `__getattr__`，
            # 从而避免无限递归。
            return object.__getattribute__(self, '_initialized')
        except AttributeError:
            # 如果 `_initialized` 属性尚未存在（例如，在 `__init__` 的非常早期阶段），
            # 则捕获 AttributeError 并返回 False。
            # 这表示对象尚未初始化到可以安全查询 `_initialized` 属性的程度。
            return False

    def get_template_instance(self) -> FuzznumTemplate:
        """
        获取模板实例

        此方法提供了一个受保护的接口，用于安全地获取 Fuzznum 实例内部关联的
        `FuzznumTemplate` 实例。它在需要访问模板特定功能（如 `report()` 或 `str()`）时被调用。
        通过集中管理访问，可以确保在实例不存在或初始化不完整时提供明确的错误信息。

        Returns:
            FuzznumTemplate: 关联的模板实例。

        Raises:
            RuntimeError: 如果模板实例未找到或尚未完全初始化。
        """
        try:
            # 直接使用 `object.__getattribute__` 来获取 `_template_instance` 属性的值。
            # 同样是为了避免递归调用。
            template_instance = object.__getattribute__(self, '_template_instance')
            # 额外的检查：确保获取到的实例不是 None。
            # 尽管在正常初始化流程中不应为 None，但这是一个防御性检查。
            if template_instance is None:
                raise RuntimeError("Template instance not found.")
            return template_instance
        except AttributeError:
            # 如果 `_template_instance` 属性不存在，则抛出 RuntimeError。
            # 这通常意味着对象尚未完全初始化，或者初始化过程中出现了问题。
            raise RuntimeError("Template instance not found.")

    def get_strategy_instance(self) -> FuzznumStrategy:
        """
        获取策略实例

        此方法提供了一个受保护的接口，用于安全地获取 Fuzznum 实例内部关联的
        `FuzznumStrategy` 实例。它在需要访问策略特定功能（如属性值或核心算法）时被调用。
        与 `get_template_instance` 类似，它确保在实例不存在或初始化不完整时提供明确的错误信息。

        Returns:
            FuzznumStrategy: 关联的策略实例。

        Raises:
            RuntimeError: 如果策略实例未找到或尚未完全初始化。
        """
        try:
            # 直接使用 `object.__getattribute__` 来获取 `_strategy_instance` 属性的值。
            strategy_instance = object.__getattribute__(self, '_strategy_instance')
            # 额外的检查：确保获取到的实例不是 None。
            if strategy_instance is None:
                raise RuntimeError("Strategy instance not found.")
            return strategy_instance
        except AttributeError:
            # 如果 `_strategy_instance` 属性不存在，则抛出 RuntimeError。
            raise RuntimeError("Strategy instance not found.")

    def _record_access(self, name: str) -> None:
        """
        记录属性访问统计

        此方法用于在性能监控启用时，记录 Fuzznum 实例上特定属性的访问情况。
        它会更新属性的访问计数，并记录最近一次访问的时间戳。
        这对于分析属性的使用频率和模式非常有用。

        Args:
            name: 被访问属性的名称。
        """

        try:
            # 首先安全地检查性能监控是否已启用。
            if object.__getattribute__(self, '_monitor_enabled'):
                # 获取实例锁，确保在更新统计数据时是线程安全的。
                # 多个线程可能同时访问属性，需要防止竞态条件。
                with object.__getattribute__(self, '_lock'):
                    # 获取访问统计字典，并更新指定属性的访问计数。
                    stats = object.__getattribute__(self, '_access_stats')
                    stats[name] = stats.get(name, 0) + 1

                    # 获取访问时间字典，并记录指定属性的最新访问时间。
                    access_times = object.__getattribute__(self, '_access_times')
                    access_times[name] = float(datetime.datetime.now().strftime("%Y%m%d%H%M%S.%f"))
        except AttributeError:
            # 如果在获取 `_monitor_enabled` 或其他监控相关属性时发生 AttributeError，
            # 这通常意味着监控系统尚未完全初始化。在这种情况下，静默忽略此记录操作。
            pass

    def _get_cached_attribute(self, name: str) -> Any:
        """
        获取缓存的属性值

        此方法用于尝试从内部属性缓存 `_attr_cache` 中检索指定名称的属性值。
        它在属性访问路径中扮演着重要的角色，通过返回缓存值来避免重复计算或昂贵的查找操作，
        从而提高性能。同时，它也会在命中缓存时记录属性访问统计。

        Args:
            name: 要获取的属性名称。

        Returns:
            tuple[bool, Any]: 一个元组，第一个元素是一个布尔值，表示是否命中缓存 (True 为命中，False 为未命中)；
                              第二个元素是缓存的值 (如果命中)，否则为 None。
        """
        try:
            # 检查缓存是否被禁用。
            # 如果 `_cache_enabled` 为 False，则直接返回未命中缓存，不进行任何缓存查找。
            if not object.__getattribute__(self, '_cache_enabled'):
                return False, None

            # 获取实例锁，确保对 `_attr_cache` 的访问是线程安全的。
            # 多个线程可能同时尝试获取或修改缓存，需要防止竞态条件。
            with object.__getattribute__(self, '_lock'):
                # 获取属性缓存字典。
                cache = object.__getattribute__(self, '_attr_cache')

                if name in cache:
                    # 如果命中缓存，记录属性访问统计。
                    self._record_access(name)
                    # 返回命中状态和缓存的值。
                    return True, cache[name]
                # 如果未命中缓存，返回未命中状态和 None。
                return False, None

        except AttributeError:
            # 如果在获取 `_cache_enabled` 或 `_attr_cache` 时发生 AttributeError，
            # 这通常意味着缓存系统尚未完全初始化。在这种情况下，静默忽略并返回未命中。
            return False, None

    def _cache_attribute(self, name: str, value: Any) -> None:
        """
        缓存属性值

        此方法用于将计算或获取到的属性值存储到内部属性缓存 `_attr_cache` 中。
        它确保了后续对相同属性的访问可以直接从缓存中获取，从而提高效率。
        只有当缓存机制启用时，才会执行实际的缓存操作。

        Args:
            name: 要缓存的属性名称。
            value: 要缓存的属性值。
        """
        try:
            # 检查缓存是否启用。
            # 如果 `_cache_enabled` 为 False，则不进行缓存操作。
            if object.__getattribute__(self, '_cache_enabled'):
                # 获取实例锁，确保对 `_attr_cache` 的修改是线程安全的。
                with object.__getattribute__(self, '_lock'):
                    # 获取属性缓存字典。
                    cache = object.__getattribute__(self, '_attr_cache')
                    # 将属性值存储到缓存中，键为属性名，值为属性值。
                    cache[name] = value
        except AttributeError:
            # 如果在获取 `_cache_enabled` 或 `_attr_cache` 时发生 AttributeError，
            # 这通常意味着缓存系统未初始化。在这种情况下，静默忽略此缓存操作。
            pass

    def _invalidate_cache_for_attribute(self, name: str) -> None:
        """
        使特定属性的缓存失效

        当 Fuzznum 实例的某个属性被修改时，其在缓存中的旧值可能会变得无效。
        此方法用于从缓存中删除指定属性的条目，确保下次访问该属性时，
        会重新计算或从源头获取最新值，而不是使用过时的缓存数据。

        Args:
            name: 要使其缓存失效的属性名称。
        """
        try:
            # 获取实例锁，确保对 `_attr_cache` 的修改是线程安全的。
            with object.__getattribute__(self, '_lock'):
                # 获取属性缓存字典。
                cache = object.__getattribute__(self, '_attr_cache')
                # 从缓存中移除指定名称的属性。
                # `pop(name, None)` 方法在键不存在时不会引发 KeyError，而是返回 None，
                # 确保操作的健壮性。
                cache.pop(name, None)
        except AttributeError:
            # 如果在获取 `_attr_cache` 时发生 AttributeError，
            # 这通常意味着缓存系统未初始化。在这种情况下，静默忽略此操作。
            pass

    def _clear_cache(self) -> None:
        """
        清除属性缓存

        此方法用于清空内部属性缓存 `_attr_cache` 中的所有条目。
        这在需要强制刷新所有属性值，或者在禁用缓存时清理内存时非常有用。

        Notes:
            此操作会移除所有缓存的属性值，后续对这些属性的访问将触发重新计算或从源头获取。
        """
        try:
            # 获取实例锁，确保清空缓存操作的线程安全。
            with object.__getattribute__(self, '_lock'):
                # 获取属性缓存字典。
                cache = object.__getattribute__(self, '_attr_cache')
                # 清空缓存字典中的所有条目。
                cache.clear()
        except AttributeError:
            # 如果在获取 `_attr_cache` 时发生 AttributeError，
            # 这通常意味着缓存系统未初始化。在这种情况下，静默忽略此操作。
            pass

    def _delegate_attribute_access(self, name: str) -> Any:
        """
        委托属性访问的具体实现

        此方法是 Fuzznum 类实现其核心“属性委托”机制的关键。
        当 `__getattribute__` 无法直接在 Fuzznum 实例上找到属性时，
        它将调用此方法来尝试从关联的策略实例 (`_strategy_instance`) 或
        模板实例 (`_template_instance`) 中获取属性值。
        它还集成了缓存查找和性能监控。

        Args:
            name: 要访问的属性名称。

        Returns:
            Any: 找到的属性值。

        Raises:
            AttributeError: 如果属性在 Fuzznum 实例、策略实例和模板实例中都未找到。
            RuntimeError: 如果策略或模板实例未正确初始化。
        """
        # 检查缓存
        # 尝试从缓存中获取属性值。如果命中缓存，则直接返回缓存值，避免后续的查找。
        cache_hit, cached_value = self._get_cached_attribute(name)
        if cache_hit:
            return cached_value

        try:
            # 策略属性优先
            # 策略属性优先
            # 获取绑定到 Fuzznum 实例上的策略属性名称集合。
            # 使用 `object.__getattribute__` 避免递归。
            bound_strategy_attrs = object.__getattribute__(self, '_bound_strategy_attributes')
            # 如果要访问的属性名在策略属性集合中。
            if name in bound_strategy_attrs:
                # 从策略实例中获取属性值。
                # 调用 `get_strategy_instance()` 确保获取到有效的策略实例。
                value = getattr(self.get_strategy_instance(), name)
                # 将获取到的值缓存起来，以便后续访问。
                self._cache_attribute(name, value)
                # 记录属性访问统计。
                self._record_access(name)
                return value

            # 模板属性
            # 获取绑定到 Fuzznum 实例上的模板属性名称集合。
            bound_template_attrs = object.__getattribute__(self, '_bound_template_attributes')
            # 如果要访问的属性名在模板属性集合中。
            if name in bound_template_attrs:
                # 从模板实例中获取属性值。
                # 调用 `get_template_instance()` 确保获取到有效的模板实例。
                value = getattr(self.get_template_instance(), name)
                # 将获取到的值缓存起来。
                self._cache_attribute(name, value)
                # 记录属性访问统计。
                self._record_access(name)
                return value

        except (AttributeError, RuntimeError):
            # 捕获在尝试获取策略/模板实例或其属性时可能发生的 `AttributeError` 或 `RuntimeError`。
            # 这通常意味着实例未初始化或属性不存在于策略/模板中。
            # 在这里静默忽略，以便将控制权传递给 `__getattr__` 进行最终处理。
            pass

        # 委托给 __getattr__ 进行最终处理
        # 如果在缓存、策略或模板中都未找到属性，则将控制权转交给 `__getattr__`。
        # `__getattr__` 是 Python 的一个特殊方法，它在属性查找失败时被调用，
        # 通常用于处理动态属性或抛出最终的 `AttributeError`。
        return self.__getattr__(name)

    def __getattribute__(self, name: str) -> Any:
        """
        优化的属性访问方法 - 修复递归错误版本

        `__getattribute__` 是 Python 中属性查找的第一个入口点。
        无论属性是否存在，每次访问实例的属性时，都会首先调用这个方法。
        它负责拦截所有属性访问，并根据属性的类型（内部属性、特殊方法、自身属性、委托属性）
        进行不同的处理，以实现复杂的属性委托和避免递归。

        Args:
            name: 要访问的属性名称（字符串）。

        Returns:
            Any: 访问到的属性值。

        Raises:
            AttributeError: 如果属性最终未找到。
            RuntimeError: 如果对象在初始化过程中尝试访问未就绪的属性。
        """
        # 内部属性直接获取，避免递归
        # 对于在 `_INTERNAL_ATTRS` 中定义的内部属性，它们在 `__init__` 阶段就通过
        # `object.__setattr__` 直接设置。为了防止在 `__getattribute__` 内部
        # 访问这些属性时再次触发 `__getattribute__` 导致无限递归，
        # 这里直接使用 `object.__getattribute__(self, name)` 来获取它们。
        if name in Fuzznum._INTERNAL_ATTRS:
            return object.__getattribute__(self, name)

        # 特殊方法和私有属性直接获取
        # 对于 Python 的特殊方法（如 `__str__`, `__repr__` 等）和以单下划线开头的私有属性，
        # 它们通常不参与 Fuzznum 的属性委托逻辑。直接使用 `object.__getattribute__` 获取，
        # 可以提高效率并避免不必要的复杂处理。
        if name.startswith('_') or name in ('__dict__', '__class__'):
            return object.__getattribute__(self, name)

        # 尝试从自身获取
        # 首先尝试从 Fuzznum 实例自身（即 `self.__dict__`）中查找属性。
        # 如果属性直接存在于 Fuzznum 实例上，则直接返回其值。
        # 这种方式优先处理 Fuzznum 自身的属性，避免了委托的开销。
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            # 如果在 Fuzznum 实例自身中没有找到属性，则捕获 `AttributeError`，
            # 并继续执行后续的委托逻辑。
            pass

        # 初始化检查 - 使用安全方法
        # 在尝试进行属性委托之前，检查 Fuzznum 实例是否已经完成了初始化。
        # `_is_initialized()` 方法是安全的，不会导致递归。
        # 如果对象尚未完全初始化，则抛出 `AttributeError`，防止在不完整状态下进行属性访问。
        if not self._is_initialized():
            raise AttributeError(
                f"'{self.__class__.__name__}' 对象没有属性 '{name}'。"
                f"The Fuzznum is still initializing or the property does not exist."
            )

        # 委托属性访问
        # 如果属性不在 Fuzznum 自身，且对象已初始化，则将属性访问委托给 `_delegate_attribute_access` 方法。
        # 这个方法会尝试从缓存、策略实例或模板实例中查找属性。
        return self._delegate_attribute_access(name)

    def __getattr__(self, name: str) -> Any:
        """
        属性访问的最终处理方法 - 修复递归错误版本

        `__getattr__` 是 Python 属性查找机制中的“最后一道防线”。
        当 `__getattribute__`（以及它内部调用的 `_delegate_attribute_access`）
        无法找到请求的属性时，`__getattr__` 就会被调用。
        它的主要职责是处理那些动态生成的属性，或者在属性确实不存在时，
        提供一个详细且有用的 `AttributeError` 错误信息。

        Args:
            name: 尝试访问但未找到的属性名称。

        Returns:
            Any: (理论上，如果找到动态属性) 找到的属性值。

        Raises:
            AttributeError: 属性在所有可能的查找路径中都未找到。
        """
        # 避免在初始化期间的递归调用
        # 再次检查初始化状态，以防在 `__getattribute__` 内部的某种异常路径下，
        # `__getattr__` 在对象尚未完全初始化时被调用。
        if not self._is_initialized():
            raise AttributeError(
                f"'{self.__class__.__name__}' 对象没有属性 '{name}'。"
                f"The Fuzznum is still initializing."
            )

        # 收集可用属性信息
        # 调用 `_get_available_members_info` 方法，获取当前 Fuzznum 实例
        # （通过其关联的策略和模板）所有可用的方法和属性列表。
        # 这对于生成有用的错误信息至关重要。
        available_info = self._get_available_members_info()

        # 构建详细的错误信息
        error_msg = f"'{self.__class__.__name__}' object has no attribute '{name}'."
        # 查找可能的匹配项
        all_members = available_info['attributes'] + available_info['methods']
        suggestions = difflib.get_close_matches(name, all_members, n=3, cutoff=0.6)
        if suggestions:
            error_msg += f" Did you mean: {', '.join(suggestions)}?"

        # 仅在调试模式下显示所有可用成员，避免信息过载
        config = get_config()
        if getattr(config, 'DEBUG_MODE', False):
            if available_info['attributes']:
                error_msg += f"\nAvailable attributes: {', '.join(sorted(available_info['attributes']))}."

            if available_info['methods']:
                error_msg += f"\nAvailable methods: {', '.join(sorted(available_info['methods']))}."

        # 最终抛出 `AttributeError`，并附带详细的错误信息。
        raise AttributeError(error_msg)

    def __setattr__(self, name: str, value: Any) -> None:
        """
        属性设置方法 - 修复递归错误版本

        `__setattr__` 是 Python 中属性赋值的拦截点。
        每次尝试设置实例的属性（例如 `obj.attr = value`）时，都会调用这个方法。
        它负责根据属性的特性（内部属性、不可变属性、委托属性）进行不同的处理，
        实现属性的校验、委托和缓存失效。

        Args:
            name: 要设置的属性名称。
            value: 要赋给属性的值。

        Raises:
            AttributeError: 如果尝试修改不可变属性，或者属性是只读的。
            RuntimeError: 在委托设置过程中发生意外错误。
        """
        # 初始化期间或内部属性直接设置
        # 类似于 `__getattribute__`，对于在 `_INTERNAL_ATTRS` 中定义的内部属性，
        # 或者在对象尚未完全初始化时，直接使用 `object.__setattr__` 进行设置。
        # 这确保了这些核心属性能够被可靠地设置，而不会触发自定义逻辑或导致递归。
        if (name in Fuzznum._INTERNAL_ATTRS or
                name.startswith('_') or not self._is_initialized()):
            object.__setattr__(self, name, value)
            return

        # `mtype` 属性是 Fuzznum 实例的核心标识符，一旦创建就不应更改。
        # 强制将其设为不可变属性，尝试修改时抛出 `AttributeError`。
        if name == 'mtype':
            raise AttributeError(f"Cannot modify immutable attribute '{name}' of Fuzznum instance.")

        # 清除相关缓存
        # 在属性值被修改之前，使该属性在缓存中的旧值失效。
        # 这样可以确保下次访问该属性时，会从策略或模板实例中获取最新值，而不是使用过时的缓存。
        self._invalidate_cache_for_attribute(name)

        try:
            # 尝试委托给策略实例设置属性
            # 获取绑定到 Fuzznum 实例上的策略属性名称集合。
            strategy_attributes = object.__getattribute__(self, '_bound_strategy_attributes')
            # 如果要设置的属性名在策略属性集合中。
            if name in strategy_attributes:
                try:
                    # 获取策略实例。
                    strategy_instance = self.get_strategy_instance()
                    # 尝试从策略类的角度获取属性描述符，以判断是否为 `property`。
                    strategy_class = strategy_instance.__class__
                    attr_descriptor = getattr(strategy_class, name, None)

                    # 如果是 `property` 且定义了 `fset` (setter 方法)，则通过 `setattr` 调用其 setter。
                    if isinstance(attr_descriptor, property):
                        if attr_descriptor.fset:
                            setattr(strategy_instance, name, value)
                            return
                        else:
                            # 如果是 `property` 但没有定义 `fset`，则表示该属性是只读的。
                            raise AttributeError(f"The attribute '{name}' is read-only "
                                                 f"for the fuzzy number mtype '{self.mtype}'.")
                    else:
                        # 如果不是 `property`，则直接通过 `setattr` 设置策略实例的属性。
                        setattr(strategy_instance, name, value)
                        object.__setattr__(self, name, value)
                        return

                except AttributeError as e:
                    raise AttributeError(f"Cannot set property '{name}' on the policy instance "
                                         f"(fuzzy number mtype '{self.mtype}'): {e}")
                except Exception as e:
                    raise RuntimeError(f"An unexpected error occurred while setting the property '{name}' "
                                       f"on the strategy instance (fuzzy number type '{self.mtype}'): {e}")

            # 尝试委托给模板实例设置属性
            # 逻辑与策略属性设置类似，但通常模板属性不常被外部直接设置。
            template_attributes = object.__getattribute__(self, '_bound_template_attributes')
            if name in template_attributes:
                try:
                    template_instance = self.get_template_instance()
                    template_class = template_instance.__class__
                    attr_descriptor = getattr(template_class, name, None)

                    if isinstance(attr_descriptor, property):
                        if attr_descriptor.fset:
                            setattr(template_instance, name, value)
                            return
                        else:
                            raise AttributeError(f"属性 '{name}' 对于模糊数类型 '{self.mtype}' 是只读的。")
                    else:
                        setattr(template_instance, name, value)
                        return
                except AttributeError as e:
                    raise AttributeError(f"Cannot set attribute '{name}' on template instance "
                                         f"(fuzzy number type '{self.mtype}'): {e}")
                except Exception as e:
                    raise RuntimeError(f"An unexpected error occurred while setting the property '{name}' "
                                       f"on the template instance (fuzzy number type '{self.mtype}'): {e}")

        except AttributeError:
            # 绑定信息不存在，直接设置到对象上
            pass

        # 最终设置到 Fuzznum 实例自身
        # 如果属性不属于内部属性，不是 `mtype`，且无法委托给策略或模板实例设置，
        # 那么就将其作为 Fuzznum 实例自身的普通属性进行设置。
        object.__setattr__(self, name, value)

    def __del__(self) -> None:
        """
        析构函数，清理资源

        `__del__` 方法在对象即将被垃圾回收时调用。
        它提供了一个机会来执行必要的清理工作，例如释放资源、关闭文件句柄、
        或者在此处清空内部容器，以确保没有循环引用导致内存泄漏（尽管 Python 的垃圾回收器
        通常能处理循环引用，但显式清理有助于及时释放内存并避免潜在问题）。

        Notes:
            - `__del__` 的调用时机不确定，不应依赖它来执行关键的资源释放。
              更好的做法是使用上下文管理器 (`with` 语句) 或显式 `close()` 方法。
            - 这里的清理主要是为了确保内部字典和集合被清空，释放它们持有的引用。
        """
        try:
            # 获取实例锁，确保在清理过程中对共享资源的访问是线程安全的。
            # 这是防御性编程，以防在多线程环境中对象被并发销毁。
            lock = object.__getattribute__(self, '_lock')
            with lock:
                # 定义需要清理的内部容器属性列表。
                cleanup_attrs = ['_bound_strategy_methods',
                                 '_bound_template_methods',
                                 '_attr_cache',
                                 '_access_stats',
                                 '_validation_cache']

                # 遍历这些属性。
                for attr in cleanup_attrs:
                    try:
                        # 尝试获取属性值。
                        container = object.__getattribute__(self, attr)
                        # 如果属性是一个容器（如字典或集合），且有 `clear()` 方法，则调用它清空容器。
                        # 这会解除容器中所有元素的引用，有助于垃圾回收。
                        if hasattr(container, 'clear'):
                            container.clear()
                    except AttributeError:
                        # 如果在清理过程中某个属性不存在，静默忽略。
                        pass
        except AttributeError:
            # 如果在获取 `_lock` 时发生 `AttributeError`，
            # 这可能意味着对象在非常早期的阶段就失败了，或者已经处于不完整状态。
            # 静默忽略，因为此时可能没有太多可清理的资源。
            pass

    def _get_available_members_info(self) -> Dict[str, List[str]]:
        """
        获取所有可用成员信息

        此方法旨在收集当前 `Fuzznum` 实例通过其关联的 `FuzznumStrategy` 和
        `FuzznumTemplate` 实例所暴露的所有公共方法和属性的名称。
        它的主要用途是在 `__getattr__` 方法中，当用户尝试访问一个不存在的属性时，
        提供一个详细的、用户友好的错误消息，列出所有可用的属性和方法，
        从而帮助用户快速定位问题或了解对象的可用接口。

        Returns:
            Dict[str, List[str]]: 一个字典，包含两个键：
                 - 'attributes': 一个列表，存储所有可用的属性名称。
                 - 'methods': 一个列表，存储所有可用的方法名称。
                 如果由于初始化问题无法获取信息，则返回空列表。
        """
        try:
            # 安全地获取绑定到 Fuzznum 实例上的策略方法、策略属性、模板方法和模板属性的集合/字典。
            # 使用 `object.__getattribute__` 是为了避免在获取这些内部状态时触发递归。
            strategy_methods = object.__getattribute__(self, '_bound_strategy_methods')
            strategy_attrs = object.__getattribute__(self, '_bound_strategy_attributes')
            template_methods = object.__getattribute__(self, '_bound_template_methods')
            template_attrs = object.__getattribute__(self, '_bound_template_attributes')

            # 将策略和模板的所有属性名称合并到一个列表中。
            # 将策略和模板的所有方法名称（字典的键）合并到一个列表中。
            # 返回一个包含这些合并后列表的字典。
            return {
                'attributes': list(strategy_attrs) + list(template_attrs),
                'methods': list(strategy_methods.keys()) + list(template_methods.keys())
            }
        except AttributeError:
            # 如果在尝试获取任何内部绑定信息时发生 `AttributeError`，
            # 这通常意味着对象尚未完全初始化，或者初始化过程中出现了问题，
            # 导致这些内部属性不存在。在这种情况下，返回空的属性和方法列表，
            # 以避免在生成错误信息时引发新的异常。
            return {'attributes': [], 'methods': []}

    # ======================== 生命周期管理 ========================
    # Fuzznum 类的生命周期管理模块旨在提供便捷、安全且符合预期的对象创建、
    #   复制和销毁机制。在面向对象编程中，对象的生命周期管理是确保资源有效利用、
    #   避免内存泄漏和维护数据一致性的关键。
    # 对于 Fuzznum 这样的复杂对象，其内部依赖于 FuzznumStrategy 和
    #   FuzznumTemplate 实例，并且具有内部状态（如缓存、性能统计）。因此，
    #   提供明确的创建和复制方法，而不是仅仅依赖于默认的构造函数和浅拷贝，
    #   对于维护对象的完整性和易用性至关重要。
    # 核心目标有三个：
    # 1. 便捷创建 (create): 提供一个更高级别的工厂方法，简化 Fuzznum 实例的创建过程，
    #    并允许在创建时批量设置属性。
    # 2. 安全复制 (copy): 确保在复制 Fuzznum 实例时，不仅复制其基本类型，
    #    还能正确地复制其内部状态（特别是策略实例的属性），从而得到一个独立且功能完整的副本。
    # 3. 资源清理 (__del__): 虽然 __del__ 方法已在前面讲解过，但它也是生命周期管理的一部分，
    #    负责在对象销毁前进行必要的清理。

    # TODO: create 这个方法还存在缺陷，设置q为默认值1，但是每次先验证 md 和 nmd，可能会导致约束条件验证失败。
    #  应该先设置q值
    def create(self, **kwargs) -> 'Fuzznum':
        """
        便捷的创建方法

        `create` 方法是一个类方法（`@classmethod`），它充当 `Fuzznum` 实例的工厂函数。
        它简化了 `Fuzznum` 对象的创建过程，允许用户在实例化时直接指定模糊数类型 (`mtype`)，
        并可选地通过关键字参数 (`**kwargs`) 批量设置其关联策略实例的属性。
        这种方法提高了代码的可读性和便利性，隐藏了底层复杂的初始化细节。

        Args:
            **kwargs: 可选的关键字参数，用于在实例创建后批量设置其属性。
                      这些属性通常是底层策略实例的属性（如 `md`, `nmd`, `q` 等）。

        Returns:
            Fuzznum: 一个新创建并已初始化的 Fuzznum 实例。

        Examples:
            >>> # 假设 'example_fuzznum' 已注册，且其策略有 'md' 和 'nmd' 属性
            >>> fuzz = Fuzznum.create(md=0.7, nmd=0.2, q=2)
            >>> print(fuzz.mtype)
            example_fuzznum
            >>> print(fuzz.md)
            0.7
            >>> print(fuzz.nmd)
            0.2
        """
        # 调用类的构造函数 `__init__` 来创建 Fuzznum 实例。
        # 这会触发 Fuzznum 内部的初始化流程，包括配置策略和模板。
        instance = Fuzznum(self.mtype, self.q)

        # 批量设置属性
        # 如果 `kwargs` 不为空，则遍历其中的每个键值对，并尝试将其设置到新创建的实例上。
        # 这利用了 Fuzznum 的 `__setattr__` 机制，该机制会负责将属性委托给底层的策略实例。
        if kwargs:
            for key, value in kwargs.items():
                try:
                    # 尝试设置属性。
                    # 如果属性不存在或不可设置（例如，因为严格属性模式），`__setattr__` 可能会抛出 AttributeError。
                    setattr(instance, key, value)
                except AttributeError:
                    raise f"The parameter '{key}' is invalid for the fuzzy number mtype '{self.mtype}'"

        return instance

    def copy(self) -> 'Fuzznum':
        """
        创建当前实例的副本

        `copy` 方法用于创建一个当前 `Fuzznum` 实例的独立副本。
        它执行的是一种“深拷贝”的逻辑，确保新创建的副本拥有与原实例相同的所有属性值，
        并且这些属性值是独立的，修改副本不会影响到原实例。
        这对于需要基于现有模糊数创建新变体，或者在不修改原始对象的情况下进行操作的场景非常有用。

        Returns:
            Fuzznum: 当前实例的一个独立副本。

        Raises:
            RuntimeError: 如果尝试复制一个尚未完全初始化的对象。

        Examples:
            >>> fuzz1 = Fuzznum.create(md=0.7, nmd=0.2)
            >>> fuzz2 = fuzz1.copy()
            >>> fuzz2.md = 0.5 # 修改副本不会影响原实例
            >>> print(fuzz1.md)
            0.7
            >>> print(fuzz2.md)
            0.5
        """
        # 复制操作的前提是对象必须已经完全初始化。
        # 如果对象尚未初始化完成，则抛出 `RuntimeError`，因为此时复制可能会得到不完整或不一致的状态。
        if not self._is_initialized():
            raise RuntimeError("Cannot copy uninitialized object")

        # 获取当前所有属性值
        current_params = {}
        try:
            # 安全地获取绑定到 Fuzznum 实例上的策略属性名称集合。
            # 只有策略属性才需要被复制，因为它们代表了模糊数的核心数据。
            # 模板属性通常是计算结果或表示层面的，不需要直接复制其值。
            strategy_attrs = object.__getattribute__(self, '_bound_strategy_attributes')

            for attr_name in strategy_attrs:
                # 遍历所有策略属性名称。
                try:
                    # 尝试获取每个策略属性的当前值。
                    # 使用 `getattr(self, attr_name)` 会触发 `__getattribute__` 和 `_delegate_attribute_access`，
                    # 确保获取到的是实际的属性值（可能来自缓存或策略实例）。
                    current_params[attr_name] = getattr(self, attr_name)

                except AttributeError:
                    # 如果某个策略属性在此时无法获取（例如，因为它是只写的 property），则静默忽略。
                    pass
        except AttributeError:
            # 如果在获取 `_bound_strategy_attributes` 时发生 `AttributeError`，
            # 这可能意味着内部状态不一致，静默忽略并继续，但复制可能不完整。
            pass

        # 使用 `create` 类方法来创建一个新的 Fuzznum 实例。
        # 将原实例的 `mtype` 传递给 `create` 方法，以确保新副本是相同类型的模糊数。
        # 将收集到的 `current_params` 作为关键字参数传递，以便在创建时设置新副本的属性。
        # 这种方式确保了新副本的初始化过程与普通创建过程一致，并且属性值被正确地复制。
        return self.create(**current_params)

    # ======================== 缓存管理 ========================

    def enable_cache(self) -> None:
        """
        启用属性访问缓存

        此方法用于激活 `Fuzznum` 实例的内部属性缓存机制。
        当缓存启用时，对属性的后续访问会首先尝试从缓存中获取值。
        如果缓存命中，则直接返回缓存值，避免了对底层策略或模板实例的委托查找，
        从而提高属性访问的效率。

        Notes:
            此操作只会启用缓存，不会清空现有缓存。如果需要清空缓存，请调用 `clear_cache()`。
        """
        # 直接使用 `object.__setattr__` 来设置 `_cache_enabled` 内部属性为 True。
        # 这是为了确保在任何时候都能安全地修改这个内部标志，而不会触发自定义的 `__setattr__` 逻辑。
        object.__setattr__(self, '_cache_enabled', True)

    def disable_cache(self) -> None:
        """
        禁用属性访问缓存并清空现有缓存

        此方法用于停用 `Fuzznum` 实例的内部属性缓存机制。
        当缓存禁用时，所有属性访问都将直接委托给底层策略或模板实例，
        不再尝试从缓存中获取值。
        同时，为了避免使用过时的缓存数据，它会立即清空所有已缓存的属性值。

        Notes:
            禁用缓存会强制后续所有属性访问都进行委托查找，可能会增加性能开销。
            但它保证了总是获取到属性的最新状态。
        """
        # 直接使用 `object.__setattr__` 来设置 `_cache_enabled` 内部属性为 False。
        object.__setattr__(self, '_cache_enabled', False)
        # 调用 `_clear_cache()` 方法，清空所有已缓存的属性值。
        # 这样做是为了确保在禁用缓存后，不会有任何过时的数据留在内存中，并且后续访问会强制刷新。
        self._clear_cache()

    def clear_cache(self) -> None:
        """
        手动清空属性缓存

        此方法用于强制清空 `Fuzznum` 实例内部的所有已缓存属性值。
        无论缓存当前是启用还是禁用状态，调用此方法都会移除 `_attr_cache` 中的所有条目。
        这在底层数据发生变化，需要确保下次访问属性时获取最新值，或者需要释放缓存占用的内存时非常有用。

        Notes:
            清空缓存后，后续对属性的首次访问将再次触发委托查找和可能的重新计算。
        """
        # 调用内部的 `_clear_cache()` 方法来执行实际的清空操作。
        # 这个内部方法已经包含了线程安全锁，确保操作的原子性。
        self._clear_cache()

    @contextmanager
    def cache_disabled(self):
        """
        临时禁用缓存的上下文管理器

        此方法提供了一个便捷的上下文管理器（使用 `@contextmanager` 装饰器），
        允许用户在特定的代码块中临时禁用 `Fuzznum` 实例的属性缓存。
        在进入 `with` 语句块时，缓存会被禁用并清空；在退出 `with` 语句块时（无论正常退出还是发生异常），
        缓存会被恢复到进入之前的状态。
        这对于执行一次性操作，需要保证获取最新数据，但又不想永久改变缓存状态的场景非常有用。

        Yields:
            None: 上下文管理器在 `with` 语句块中不产生任何值。

        Examples:
            >>> fuzz = Fuzznum.create(md=0.5)
            >>> fuzz.enable_cache()
            >>> _ = fuzz.md # 第一次访问，会缓存
            >>> # 模拟外部修改了底层策略的 md 属性，但 Fuzznum 实例的缓存未更新
            >>> fuzz._strategy_instance.md = 0.8
            >>> print(fuzz.md) # 此时可能仍然是 0.5 (缓存值)
            0.5
            >>> with fuzz.cache_disabled():
            ...     print(fuzz.md) # 在此块内，缓存被禁用，会获取到 0.8 (最新值)
            0.8
            >>> print(fuzz.md) # 退出块后，缓存恢复，再次获取到 0.5 (旧缓存值)
            0.5
        """
        try:
            # 安全地获取当前缓存的启用状态。
            # 使用 `object.__getattribute__` 避免递归，并处理 `_cache_enabled` 可能尚未存在的情况。
            original_state = object.__getattribute__(self, '_cache_enabled')
        except AttributeError:
            # 如果 `_cache_enabled` 属性不存在，则默认其为 True（即缓存是启用的），
            # 这样在恢复时也能有一个合理的状态。
            original_state = True

        try:
            # 进入 `with` 语句块时，调用 `disable_cache()` 禁用并清空缓存。
            self.disable_cache()
            # `yield` 将控制权交给 `with` 语句块内部的代码。
            yield
        finally:
            # 无论 `with` 语句块是正常完成还是因为异常退出，`finally` 块都会执行。
            # 在这里，将 `_cache_enabled` 属性恢复到进入上下文管理器之前的原始状态。
            # 同样使用 `object.__setattr__` 确保安全设置。
            object.__setattr__(self, '_cache_enabled', original_state)

    # ======================== 信息和调试 ========================
    # Fuzznum 类的信息和调试模块提供了一系列方法，用于在运行时获取实例的内部状态、
    # 性能指标和健康状况。这些功能对于开发者理解对象的行为、诊断问题、
    # 监控性能以及确保数据一致性至关重要。
    # 核心目标：
    # 1. 状态内省: 提供获取对象基本信息和配置的接口。
    # 2. 性能监控: 暴露属性访问的统计数据，帮助识别性能瓶颈。
    # 3. 健康检查: 验证对象内部状态的完整性和一致性，及时发现潜在问题。
    # 4. 调试辅助: 为开发者提供有用的诊断信息，简化问题排查过程。

    def get_strategy_attributes_dict(self) -> Dict[str, Any]:
        """
        获取当前 Fuzznum 实例关联的策略实例的所有公共属性及其值。

        此方法通过访问内部的策略实例 (`_strategy_instance`)，收集其所有
        在 `_declared_attributes` 中声明的公共属性，并返回一个包含
        这些属性名及其当前值的字典。这对于序列化、缓存键生成以及需要
        完整策略状态的运算执行器 (`OperationExecutor`) 至关重要。

        Returns:
            Dict[str, Any]: 一个字典，键是策略属性的名称（字符串），
                            值是该属性的当前值。

        Raises:
            RuntimeError: 如果策略实例尚未初始化或无法访问。
            AttributeError: 如果在获取某个声明的属性时发生错误。

        Examples:
            >>> # 假设 fuzznum 是一个已初始化的 Fuzznum 实例
            >>> # 其策略包含 'md', 'nmd', 'q' 等属性
            >>> fuzznum = Fuzznum.create(md=0.8, nmd=0.5, q=3)
            >>> attrs_dict = fuzznum.get_strategy_attributes_dict()
            >>> print(attrs_dict)
            {'q': 3, 'md': 0.8, 'nmd': 0.5} # 注意：字典键的顺序可能不同
        """
        # 检查对象是否已完全初始化，确保 _strategy_instance 可用。
        if not self._is_initialized():
            raise RuntimeError("Cannot get strategy attributes from an uninitialized Fuzznum object.")

        # 安全地获取策略实例。
        strategy_instance = self.get_strategy_instance()

        # 获取策略实例中所有已声明的属性名称集合。
        # _bound_strategy_attributes 是在 Fuzznum 初始化时从策略实例中收集的。
        try:
            declared_attrs = object.__getattribute__(self, '_bound_strategy_attributes')
        except AttributeError:
            # 如果 _bound_strategy_attributes 不存在，说明初始化不完整。
            raise RuntimeError("Fuzznum's internal strategy attribute bindings are not properly initialized.")

        # 构建并返回包含所有声明属性及其当前值的字典。
        # 使用字典推导式高效地完成此操作。
        # getattr(strategy_instance, attr) 会获取策略实例上该属性的最新值。
        return {
            attr: getattr(strategy_instance, attr)
            for attr in declared_attrs
            if hasattr(strategy_instance, attr)  # 确保属性确实存在于实例上
        }

    def get_info(self) -> Dict[str, Any]:
        """
        获取对象基本信息

        此方法提供了一个概览，返回当前 `Fuzznum` 实例的基本状态和配置信息。
        它能够帮助开发者快速了解实例的类型、生命周期、绑定情况以及缓存状态。

        Returns:
            Dict[str, Any]: 包含对象基本信息的字典。
                            如果对象尚未完全初始化，则返回简化的信息。
        """
        # 检查对象是否已完全初始化。
        # 如果尚未初始化，则返回一个简化的信息字典，避免访问未就绪的属性。
        if not self._is_initialized():
            return {
                'mtype': getattr(self, 'mtype', 'unknown'),
                'status': 'not_initialized',
                'creation_time': getattr(self, '_creation_time', None)
            }

        try:
            # 安全地获取各种内部属性，这些属性包含了对象的核心信息。
            # 使用 `object.__getattribute__` 确保在获取这些内部属性时不会触发递归。
            strategy_methods = object.__getattribute__(self, '_bound_strategy_methods')
            strategy_attributes = object.__getattribute__(self, '_bound_strategy_attributes')
            template_attributes = object.__getattribute__(self, '_bound_template_attributes')
            template_methods = object.__getattribute__(self, '_bound_template_methods')
            creation_time = object.__getattribute__(self, '_creation_time')
            attr_cache = object.__getattribute__(self, '_attr_cache')
            cache_enabled = object.__getattribute__(self, '_cache_enabled')

            # 构造并返回包含详细信息的字典。
            return {
                'mtype': self.mtype,  # 模糊数类型
                'status': 'initialized',  # 对象状态
                'creation_time': float(creation_time),  # 创建时间戳
                'binding_info': {
                    # 绑定到 Fuzznum 实例上的所有方法名称（来自策略和模板）
                    'bound_methods': sorted(list(strategy_methods.keys()) + list(template_methods.keys())),
                    # 绑定到 Fuzznum 实例上的所有属性名称（来自策略和模板）
                    'bound_attributes': sorted(list(strategy_attributes) + list(template_attributes)),
                    'cache_size': len(attr_cache),  # 缓存中条目数量
                    'cache_enabled': cache_enabled  # 缓存是否启用
                }
            }
        except AttributeError as e:
            # 如果在获取信息过程中发生 `AttributeError`，
            # 这可能意味着对象处于部分初始化状态，无法提供完整信息。
            # 返回一个包含错误信息的字典，指示部分初始化状态。
            return {
                'mtype': getattr(self, 'mtype', 'unknown'),
                'status': 'partially_initialized',
                'error': str(e)
            }

    def get_performance_stats(self) -> Dict[str, Any]:
        """
        获取性能统计信息

        此方法返回与 `Fuzznum` 实例属性访问相关的性能统计数据。
        它依赖于内部的性能监控机制（如果启用），提供属性访问次数、最近访问时间等信息，
        以及缓存命中率，帮助识别热点属性和评估缓存效果。

        Returns:
            Dict[str, Any]: 包含性能统计信息的字典。
                            如果性能监控未启用或未初始化，则返回相应的状态。
        """
        try:
            # 安全地检查性能监控是否启用。
            monitor_enabled = object.__getattribute__(self, '_monitor_enabled')
            if not monitor_enabled:
                # 如果监控未启用，直接返回相应的状态。
                return {'monitoring_enabled': False}

            # 获取属性访问统计和访问时间记录。
            access_stats = object.__getattribute__(self, '_access_stats')
            access_times = object.__getattribute__(self, '_access_times')

            # 构造并返回包含详细性能统计的字典。
            return {
                'monitoring_enabled': True,  # 监控是否启用
                'total_accesses': sum(access_stats.values()),  # 总访问次数
                'unique_attributes_accessed': len(access_stats),  # 访问过的唯一属性数量
                # 访问次数最多的属性及其计数，如果 `access_stats` 为空则为 None。
                'most_accessed': max(access_stats.items(), key=lambda x: x[1]) if access_stats else None,
                # 最近 60 秒内被访问过的属性及其最新访问时间。
                'recent_accesses': {k: v for k, v in access_times.items() if
                                    float(datetime.datetime.now().strftime("%Y%m%d%H%M%S.%f")) - v < 60},
                'cache_hit_ratio': self._calculate_cache_hit_ratio()  # 缓存命中率
            }
        except AttributeError:
            # 如果在获取监控相关属性时发生 `AttributeError`，
            # 说明性能监控系统可能未初始化。
            return {'monitoring_enabled': False, 'error': 'Performance monitoring not initialized'}

    def set_performance_monitoring(self, enable: bool) -> None:
        """
        安全设置性能监控

        此方法允许在运行时动态启用或禁用 `Fuzznum` 实例的属性访问性能监控。
        当禁用监控时，相关的统计数据（访问计数和时间）也会被清空。

        Args:
            enable: 布尔值，True 表示启用监控，False 表示禁用监控。
        """
        try:
            # 获取实例锁，确保在修改监控状态和统计数据时是线程安全的。
            # 使用 `object.__getattribute__` 来安全地获取锁本身。
            lock = object.__getattribute__(self, '_lock')
            with lock:
                # 使用 `object.__setattr__` 安全地设置 `_monitor_enabled` 标志，
                # 避免触发自定义的 `__setattr__`，这对于修改内部状态至关重要。
                object.__setattr__(self, '_monitor_enabled', enable)

                if not enable:
                    # 如果监控被禁用，清空累积的统计数据。
                    # 这确保了当监控重新启用时，它将从最新的数据开始。
                    # 安全地获取 `_access_stats` 和 `_access_times` 字典。
                    access_stats = object.__getattribute__(self, '_access_stats')
                    access_times = object.__getattribute__(self, '_access_times')
                    access_stats.clear()
                    access_times.clear()
        except AttributeError:
            # 如果在获取锁或其他内部属性时发生 `AttributeError`，
            # 这可能意味着对象尚未完全初始化，此时无法设置监控。
            raise

    def _calculate_cache_hit_ratio(self) -> float:
        """
        计算缓存命中率

        此辅助方法计算属性缓存的命中率。
        它通过比较当前缓存中存储的属性数量与理论上所有可缓存属性的总数来估算。
        这个指标可以帮助评估缓存的效率和覆盖范围。

        Returns:
            float: 缓存命中率，范围在 0.0 到 1.0 之间。
                   如果无法计算（例如，属性信息未初始化），则返回 0.0。
        """
        try:
            # 获取当前缓存中条目的数量。
            cache_size = len(object.__getattribute__(self, '_attr_cache'))
            # 获取策略和模板实例中所有可缓存属性的总数。
            strategy_attrs = object.__getattribute__(self, '_bound_strategy_attributes')
            template_attrs = object.__getattribute__(self, '_bound_template_attributes')
            total_attributes = len(strategy_attrs) + len(template_attrs)

            # 计算命中率。为了避免除以零错误，如果 `total_attributes` 为 0，则使用 1。
            return cache_size / max(1, total_attributes)

        except AttributeError:
            # 如果在获取缓存或绑定属性信息时发生 `AttributeError`，
            # 说明相关数据未初始化，此时无法计算命中率，返回 0.0。
            return 0.0

    def validate_state(self) -> Dict[str, Any]:
        """
        验证对象状态的一致性

        此方法对 `Fuzznum` 实例的内部状态进行全面的健康检查。
        它验证关键属性是否存在、初始化状态是否一致，并尝试调用底层策略和模板的验证方法。
        这对于确保对象处于有效且可操作的状态，以及在调试复杂问题时提供诊断信息非常有用。

        Returns:
            Dict[str, Any]: 验证结果字典，包含 `is_valid`（布尔值）、`issues`（问题列表）、
                            `warnings`（警告列表）和 `timestamp`。
        """
        validation_result = {
            'is_valid': True,
            'issues': [],
            'warnings': [],
            'timestamp': float(datetime.datetime.now().strftime("%Y%m%d%H%M%S.%f"))
        }

        try:
            # 检查基本状态：确保 `mtype` 属性存在。
            if not hasattr(self, 'mtype'):
                validation_result['issues'].append("Missing mtype attribute")
                validation_result['is_valid'] = False

            # 检查对象是否已完全初始化。
            # 如果未初始化，则记录问题并返回，因为后续的检查依赖于完整的初始化。
            if not self._is_initialized():
                validation_result['issues'].append("Object not fully initialized")
                validation_result['is_valid'] = False
                return validation_result

            # 检查初始化状态一致性：确保所有必需的内部属性都已存在。
            # 这些属性是在 `_initialize` 过程中设置的。
            required_attrs = [
                '_strategy_instance', '_template_instance',
                '_bound_strategy_methods', '_bound_strategy_attributes',
                '_bound_template_methods', '_bound_template_attributes'
            ]

            for attr in required_attrs:
                # 使用 `hasattr` 安全检查属性是否存在。
                if not hasattr(self, attr):
                    validation_result['issues'].append(f"The initialized object is missing required attributes.: {attr}")
                    validation_result['is_valid'] = False

            # 验证策略和模板状态
            try:
                # 获取策略实例，并尝试调用其 `validate_all_attributes` 方法（如果存在）。
                # `FuzznumStrategy` 的子类可以实现这个方法来进行更深层次的自身验证。
                strategy_instance = self.get_strategy_instance()
                if hasattr(strategy_instance, 'validate_all_attributes'):
                    strategy_validation = strategy_instance.validate_all_attributes()
                    if not strategy_validation['is_valid']:
                        # 将策略验证中发现的错误添加到 Fuzznum 的问题列表中。
                        validation_result['issues'].extend([f"Strategy Validation: "
                                                            f"{err}" for err in strategy_validation['errors']])
                        validation_result['is_valid'] = False
            except RuntimeError as e:
                # 如果获取策略实例失败，或策略验证本身抛出异常。
                validation_result['issues'].append(f"Strategy instance validation failed: {e}")
                validation_result['is_valid'] = False

            try:
                # 获取模板实例，并尝试调用其 `is_valid` 方法（如果存在）。
                # `FuzznumTemplate` 实例具有 `is_valid()` 方法来检查其关联的 Fuzznum 实例是否仍然存在。
                template_instance = self.get_template_instance()
                if hasattr(template_instance, 'is_valid') and not template_instance.is_valid():
                    validation_result['issues'].append("The template instance has expired.")
                    validation_result['is_valid'] = False
            except RuntimeError as e:
                # 如果获取模板实例失败，或模板 `is_valid` 检查抛出异常。
                validation_result['issues'].append(f"Template instance validation failed: {e}")
                validation_result['is_valid'] = False

        except Exception as e:
            # 捕获在验证过程中可能发生的任何其他意外异常，并将其记录为问题。
            validation_result['issues'].append(f"An exception occurred during the verification process.: {e}")
            validation_result['is_valid'] = False

        return validation_result

    # ======================== 序列化支持 ========================
    # 序列化是将对象的状态转换为可以存储或传输的格式（例如字节流、字符串、JSON、字典等）的过程，
    # 而反序列化则是将这种格式恢复为原始对象的过程。对于 Fuzznum 这样的复杂对象，
    # 序列化支持具有以下重要意义：
    # 1. 持久化 (Persistence): 允许将 Fuzznum 实例的状态保存到文件或数据库中，
    #   以便在程序关闭后重新加载，实现数据的持久存储。
    # 2. 数据交换 (Data Transfer): 使得 Fuzznum 实例可以在不同的进程、
    #   机器或系统之间进行传输和共享。例如，通过网络发送一个模糊数对象的状态。
    # 3. 调试与日志 (Debugging & Logging): 将对象状态转换为可读格式，
    #   有助于在调试时检查对象内容，或在日志中记录关键对象状态。
    # 4. 配置与初始化 (Configuration & Initialization): 可以通过外部配置
    #   文件（如 JSON）来定义模糊数的初始状态，然后反序列化为 Fuzznum 实例。
    # 5. 克隆与复制 (Cloning & Copying): 尽管 copy() 方法提供了对象复制，
    #   但序列化/反序列化也是实现深度复制的一种通用机制，尤其是在对象结构复杂时。

    def to_dict(self, include_cache: bool = False) -> Dict[str, Any]:
        """
        将模糊数实例序列化为字典

        此方法将 `Fuzznum` 实例的核心状态转换为一个 Python 字典。
        这个字典包含了模糊数的类型 (`mtype`)、创建时间以及其底层策略实例的所有属性值。
        可选地，还可以包含内部的属性缓存。这使得 `Fuzznum` 实例能够被方便地存储、传输或检查。

        Args:
            include_cache: 布尔值，如果为 True，则在序列化结果中包含内部的属性缓存 (`_attr_cache`)。
                           通常情况下不需要包含缓存，因为缓存是瞬态的优化数据，而不是对象的核心状态。

        Returns:
            Dict[str, Any]: 包含实例状态的字典。

        Raises:
            RuntimeError: 如果尝试序列化一个尚未完全初始化的对象。
        """
        # 序列化操作的前提是对象必须已经完全初始化。
        # 如果对象尚未初始化完成，则抛出 `RuntimeError`，因为此时获取其状态可能会导致不一致。
        if not self._is_initialized():
            raise RuntimeError("Unable to serialize uninitialized object")

        try:
            # 初始化结果字典，包含 mtype 和创建时间。
            # `mtype` 是重建对象所必需的，`creation_time` 提供额外信息。
            result = {
                'mtype': self.mtype,
                'attributes': {},       # 用于存储策略属性的字典
                'creation_time': object.__getattribute__(self, '_creation_time')
            }

            # 收集策略属性
            # 获取绑定到 Fuzznum 实例上的策略属性名称集合。
            # 只有策略属性才代表了模糊数的核心数据，需要被序列化。
            # 模板属性通常是计算结果或表示层面的，不需要直接序列化。
            strategy_attrs = object.__getattribute__(self, '_bound_strategy_attributes')
            # 遍历所有策略属性名称。
            for attr_name in strategy_attrs:
                try:
                    # 尝试获取每个策略属性的当前值，并将其添加到 `attributes` 字典中。
                    # 使用 `getattr(self, attr_name)` 会触发 `__getattribute__` 和 `_delegate_attribute_access`，
                    # 确保获取到的是实际的属性值（可能来自缓存或策略实例）。
                    result['attributes'][attr_name] = getattr(self, attr_name)
                except AttributeError:
                    # 如果某个策略属性在此时无法获取（例如，它是只写的 property），则静默忽略。
                    pass

            # 如果 `include_cache` 为 True，则将内部属性缓存的副本添加到结果字典中。
            # 使用 `.copy()` 是为了避免直接暴露内部缓存，防止外部修改。
            if include_cache:
                result['cache'] = object.__getattribute__(self, '_attr_cache').copy()

            return result
        except AttributeError as e:
            # 如果在获取内部属性时发生 `AttributeError`，
            # 说明对象可能处于不一致状态，无法完成序列化。
            raise RuntimeError(f"Failed to serialize: {e}")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Fuzznum':
        """
        从字典反序列化模糊数实例

        此方法是一个类方法（`@classmethod`），用于从一个字典重建 `Fuzznum` 实例。
        它是 `to_dict()` 方法的逆操作，允许从序列化的数据中恢复对象状态。

        Args:
            cls: 类本身 (Fuzznum)。
            data: 包含模糊数实例状态的字典，通常由 `to_dict()` 方法生成。
                  必须包含 'mtype' 键。

        Returns:
            Fuzznum: 从字典数据重建的新 `Fuzznum` 实例。

        Raises:
            ValueError: 如果输入字典缺少 'mtype' 键。
        """
        # 检查输入字典是否包含 'mtype' 键，这是重建对象所必需的。
        if 'mtype' not in data:
            raise ValueError("字典必须包含 'mtype' 键")

        # 使用 `mtype` 调用 Fuzznum 的构造函数来创建基础实例。
        # 这会触发正常的初始化流程，包括策略和模板的配置。
        instance = cls(data['mtype'])

        # 设置属性
        # 如果字典中包含 'attributes' 键（存储了策略属性），则遍历并设置这些属性。
        # 使用 `setattr(instance, attr_name, value)` 会触发 `Fuzznum` 实例的 `__setattr__` 方法，
        # 从而确保属性值被正确地委托给底层的策略实例，并触发任何相关的验证和回调。
        if 'attributes' in data:
            for attr_name, value in data['attributes'].items():
                try:
                    setattr(instance, attr_name, value)
                except AttributeError:
                    # 如果某个属性无法设置（例如，只读属性或未声明的属性），则静默忽略。
                    pass

        # 恢复缓存（如果存在）
        # 如果字典中包含 'cache' 键，则尝试将缓存数据恢复到新实例的内部缓存中。
        # 这通常用于调试或特定场景，一般不建议在生产环境中恢复缓存，因为缓存是瞬态的。
        if 'cache' in data:
            try:
                # 安全地获取新实例的内部缓存字典。
                cache = object.__getattribute__(instance, '_attr_cache')
                # 使用 `update()` 方法将恢复的缓存数据合并到新实例的缓存中。
                cache.update(data['cache'])
            except AttributeError:
                # 如果新实例的缓存系统未初始化，静默忽略。
                pass

        return instance

    def __repr__(self) -> str:
        """
        对象的字符串表示

        作用：
            `__repr__` 方法提供了一个“官方”的、无歧义的字符串表示，主要用于开发者和调试。
            其目标是生成一个字符串，如果将其作为有效的 Python 表达式输入，
            可以（在理想情况下）重新创建具有相同值的对象。
            对于 `Fuzznum` 实例，它显示了实例的类型、初始化状态、存活时间、
            以及其关联的策略和模板的具体类名，并尝试包含一些关键属性的值。

        Returns:
            str: 对象的正式字符串表示。
        """
        # 如果对象尚未完全初始化，则返回一个简化的表示，指示其未初始化状态。
        if not self._is_initialized():
            return f"Fuzznum(mtype='{getattr(self, 'mtype', 'unknown')}', status='not_initialized')"

        try:
            # 获取核心信息
            mtype = self.mtype
            obj_id = id(self)   # 获取对象内存地址作为ID

            # 获取策略和模板类名
            strategy_cls_name = "N/A"
            template_cls_name = "N/A"
            try:
                # 尝试获取策略实例并获取其类名
                strategy_instance = self.get_strategy_instance()
                strategy_cls_name = strategy_instance.__class__.__name__
            except RuntimeError:
                # 如果策略实例未完全就绪或未找到，则保持为 N/A
                pass

            try:
                # 尝试获取模板实例并获取其类名
                template_instance = self.get_template_instance()
                template_cls_name = template_instance.__class__.__name__
            except RuntimeError:
                # 如果模板实例未完全就绪或未找到，则保持为 N/A
                pass

            # 收集关键属性
            # 尝试获取策略实例的关键属性值，例如 q, md, nmd。
            # 遍历 _bound_strategy_attributes 集合，获取其值。
            # 限制显示的属性数量，避免 repr 过长。
            key_attrs = []
            # 安全地获取绑定策略属性的名称集合
            bound_strategy_attrs = object.__getattribute__(self, '_bound_strategy_attributes')

            # 优先显示一些常见的模糊数属性，例如 q, md, nmd
            attrs_to_prioritize = ['q', 'md', 'nmd']

            # 首先添加优先属性
            for attr_name in attrs_to_prioritize:
                if attr_name in bound_strategy_attrs:
                    try:
                        # 使用 getattr(self, attr_name) 来利用 Fuzznum 自身的 __getattribute__ 机制，
                        # 这样可以处理属性委托和缓存。
                        attr_value = getattr(self, attr_name)
                        # 使用 !r 格式化，确保值的表示是可重构的（例如字符串会带引号）
                        key_attrs.append(f"{attr_name}={attr_value!r}")
                    except AttributeError:
                        # 属性可能不可读或此时不可访问，跳过
                        pass

            # 如果还有其他绑定属性未被优先显示，再添加少量
            other_attrs_count = 0
            # 对所有绑定属性进行排序，以确保输出顺序一致
            for attr_name in sorted(bound_strategy_attrs):
                if attr_name not in attrs_to_prioritize:
                    try:
                        attr_value = getattr(self, attr_name)
                        key_attrs.append(f"{attr_name}={attr_value!r}")
                        other_attrs_count += 1
                        if other_attrs_count >= 2:  # 限制额外属性的数量，避免过于冗长
                            break
                    except AttributeError:
                        # 属性可能不可读或此时不可访问，跳过
                        pass

            # 将收集到的属性字符串用逗号连接起来
            attrs_str = ", ".join(key_attrs)

            # 构造最终的 repr 字符串
            return (
                f"Fuzznum({attrs_str}"
                f"\n mtype='{mtype}'"
                f"\n id={obj_id}"
                f"\n is_valid={self.validate_state()['is_valid']}"
                f"\n status=initialized"
                f"\n creation_time={self._creation_time}"
                f"\n strategy={strategy_cls_name}"
                f"\n template={template_cls_name})"
            )
        except Exception as e:
            # 如果在获取详细信息过程中发生任何错误，回退到基本表示
            # 并且在基本表示中包含错误信息，这对于调试非常有用。
            return f"Fuzznum(mtype='{self.mtype}', status='initialized', error='Failed to generate detailed repr: {e}')"

    def __str__(self) -> str:
        """
        用户友好的字符串表示

        `__str__` 方法提供了一个“非正式”的、用户友好的字符串表示，主要用于最终用户。
        它旨在生成一个简洁、易读的字符串，通常用于 `print()` 函数或 `str()` 类型转换。
        对于 `Fuzznum` 实例，它优先尝试调用其关联模板实例的 `str()` 方法，
        因为模板负责定义模糊数的外部表示。如果模板不可用或其 `str()` 方法失败，
        则回退到一个默认的表示。

        Returns:
            str: 对象的简洁、用户友好的字符串表示。
        """
        # 检查 Fuzznum 实例是否拥有一个名为 'str' 的属性，并且该属性是可调用的（即一个方法）。
        # 这通常意味着它已经通过 `_bind_instance_members` 绑定了其模板实例的 `str()` 方法。
        if hasattr(self, 'str') and callable(self.str):
            try:
                # 尝试调用绑定到 Fuzznum 实例上的 `str()` 方法（来自模板）。
                # 这是首选的方式，因为模板定义了模糊数的特定表示。
                return self.get_template_instance().str()
            except Exception:
                # 如果模板的 `str()` 方法在执行过程中抛出任何异常，
                # 则静默捕获异常，并回退到默认的字符串表示，以避免程序崩溃。
                pass

        # 如果没有绑定模板的 `str()` 方法，或者模板的 `str()` 方法执行失败，
        # 则返回一个默认的、包含 `mtype` 的简单字符串表示。
        return f"Fuzznum[{getattr(self, 'mtype', 'unknown')}]"
