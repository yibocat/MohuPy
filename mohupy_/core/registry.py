#  Copyright (c) yibocat 2025 All Rights Reserved
#  Python: 3.10.9
#  Date: 2025/7/26 19:44
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import logging
import threading
from contextlib import contextmanager
from typing import Optional, Dict, Type, List, Any, Callable, Tuple

from mohupy_.config import get_config
from mohupy_.core.base import FuzznumStrategy, FuzznumTemplate

logger = logging.getLogger(__name__)


class FuzznumRegistry:
    # 作用：这是一个类级别的私有变量，用于存储 FuzznumRegistry 类的唯一单例实例。
    # 初始值为 None，表示在类加载时还没有创建任何实例。
    _instance: Optional['FuzznumRegistry'] = None

    # 作用：这是一个类级别的私有可重入锁（Reentrant Lock）。
    # 1. 在单例模式的实现（__new__ 方法）中，它用于保护 _instance 的创建过程，确保在多线程环境下，
    #    FuzznumRegistry 的实例只被创建一次，避免竞态条件。
    # 2. 在 FuzznumRegistry 实例内部，它也用于保护对注册表的核心数据结构（如 strategies, templates）
    #    以及统计信息（_registration_stats）的并发访问和修改，确保注册、注销等操作的线程安全。
    _lock: threading.RLock = threading.RLock()

    _initialized: bool = False

    def __new__(cls, *args, **kwargs) -> 'FuzznumRegistry':
        # 这是“双重检查锁定”模式的第一层检查。
        # 如果 _instance 已经存在，说明实例已经被创建，直接跳过锁的获取和后续的创建逻辑，
        # 从而提高性能，避免不必要的同步开销。
        # 如果 _instance 为 None，则可能需要创建实例，进入同步块。

        if cls._instance is None:
            # 获取类级别的锁。
            # 确保在多线程环境下，同一时刻只有一个线程能够进入这个代码块来创建实例。
            # 避免多个线程同时判断 _instance 为 None，然后都尝试创建实例，导致创建出多个实例。
            with cls._lock:
                if cls._instance is None:
                    # 这是“双重检查锁定”模式的第二层检查。
                    # 在获取锁之后再次检查 _instance。这是至关重要的，因为在第一个线程
                    # 进入锁之前，可能有另一个线程已经完成了实例的创建并释放了锁。
                    # 如果没有这个二次检查，第二个线程会再次创建实例，破坏单例模式。
                    cls._instance = super().__new__(cls)
                    # 调用父类（object）的 __new__ 方法来实际创建一个新的 FuzznumRegistry 实例。
                    # 这个新创建的实例被赋值给类级别的 _instance 变量，确保它是唯一的。
        return cls._instance

    def __init__(self):
        # 事务实例属性，用于标记当前 FuzznumRegistry 是否出在事务中
        self._in_transaction = None

        if not FuzznumRegistry._initialized:
            # 说明注册表已经被完全初始化过，直接跳过后续的初始化逻辑。

            with FuzznumRegistry._lock:
                if not FuzznumRegistry._initialized:
                    # 这是双重检查锁定的第二部分，防止在并发情况下，多个线程都尝试初始化。
                    # 通过三重锁机制，对注册表进行初始化
                    # 所有的实例属性和默认设置都在 _init_registry 中完成。
                    self._init_registry()
                    FuzznumRegistry._initialized = True

    def _init_registry(self) -> None:
        """实际的初始化逻辑"""
        # 该方法只在 FuzznumRegistry 实例的生命周期中被调用一次。
        # 注册表存储：
        self.strategies: Dict[str, Type[FuzznumStrategy]] = {}
        self.templates: Dict[str, Type[FuzznumTemplate]] = {}

        # 注册历史统计
        self._registration_history: List[Dict[str, Any]] = []

        # 存储注册操作的统计数据
        # - 'total_registrations'：成功调用 register 方法的总次数。
        # - 'failed_registrations'：调用 register 方法失败的总次数。
        # - 'overwrites'：注册时覆盖了现有策略或模板的次数。
        self._registration_stats = {
            'total_registrations': 0,
            'failed_registrations': 0,
            'overwrites': 0
        }

        # 事务支持：
        self._transaction_stack: List[Dict[str, Any]] = []
        # 作用：一个列表，用于在事务开始时存储注册表状态的快照。

        # 用于防止事务的重复开启或处理嵌套事务。
        self._in_transaction = False

        # 观察者模式支持：
        self._observers: List[Callable[[str, Dict[str, Any]], None]] = []

        config = get_config()

        if config.DEBUG_MODE:
            logger.debug(f"FuzznumRegistry initialized. ID: {id(self)}")

        # 调用私有方法来加载预定义的默认模糊数类型。
        self._load_default_fuzznum_types()

    def _load_default_fuzznum_types(self) -> None:
        """加载默认的模糊数策略和模板类"""
        config = get_config()
        if config.DEBUG_MODE:
            logger.info("Loading default fuzzy number types...")

        # 调用 _get_default_types 方法，获取一个包含所有默认模糊数策略和模板类元组的列表。
        default_types = self._get_default_types()

        with self.transaction():
            # 作用：使用注册表提供的事务上下文管理器。
            # 这确保了所有默认类型的注册操作是一个原子性的批处理。
            # 如果在注册任何一个默认类型时发生错误，整个批处理操作都会被回滚，
            # 从而保证注册表在加载默认类型后仍处于一致的状态。

            for strategy_cls, template_cls in default_types:
                try:
                    # 调用 register 方法，将策略和模板类注册到注册表中。
                    self.register(strategy=strategy_cls, template=template_cls)

                    if config.DEBUG_MODE:
                        logger.debug(f"Loaded default type: {strategy_cls.mtype}")
                except Exception as e:
                    # 如果注册某个默认类型失败（例如，mtype 定义有误），
                    # 记录一条警告信息，但不会阻止其他默认类型的加载（因为在事务中，
                    # 最终会根据事务结果决定是否回滚）。
                    logger.warning(f"Failed to load default type {strategy_cls.mtype}: {e}")

    def _get_default_types(self) -> List[Tuple[Type[FuzznumStrategy], Type[FuzznumTemplate]]]:
        """获取默认模糊数类型定义"""

        # 作用：这个方法定义了框架内置的、作为默认加载的模糊数策略和模板类。
        # 它返回一个列表，其中每个元素都是一个 (策略类, 模板类) 的元组。
        # 这些类通常是作为嵌套类（内部类）定义的，以保持封装性，并且它们直接继承自 FuzznumStrategy 和 FuzznumTemplate。
        # TODO: 后续会用专门写好的模糊数类型来改进

        class QROFNStrategy(FuzznumStrategy):
            mtype = 'qrofn'
            md: Optional[float] = None
            nmd: Optional[float] = None

            def _validate(self) -> None:
                # 模糊数的约束条件
                # 一些模糊数规则

                super()._validate()
                if (self.md is not None and self.nmd is not None and
                        pow(self.md, self.q) + pow(self.nmd, self.q) > 1):
                    # QROFN（Q-rung Orthopair Fuzzy Number）的核心约束是：
                    # 隶属度 (md) 的 q 次幂加上非隶属度 (nmd) 的 q 次幂必须小于等于 1。
                    # 这里检查是否违反了这个约束。
                    raise ValueError(f"md^q + nmd^q = {pow(self.md, self.q) + pow(self.nmd, self.q)} must not exceed 1")

        class QROFNTemplate(FuzznumTemplate):
            """Q阶序对模糊数模板"""

            mtype = 'qrofn'

            def report(self) -> str:
                # 实现 FuzznumTemplate 的抽象方法 report。
                # 这里简单地返回 str() 的结果，可以根据需要扩展为更详细的报告。
                return self.str()

            def str(self) -> str:
                # 实现 FuzznumTemplate 的抽象方法 str。
                # 返回 QROFN 的简洁字符串表示形式，包含 md, nmd 和 q。
                # 通过 self.instance 访问关联的 Fuzznum 实例的属性。

                if self.instance.md and self.instance.nmd:
                    return f"<{self.instance.md},{self.instance.nmd}>_q={self.instance.q}"
                return f"<>"

        class IVQFNStrategy(FuzznumStrategy):
            """区间值Q序对模糊数策略"""
            mtype = 'ivqfn'
            md: Optional[Tuple[float, float]] = None  # 隶属度现在是一个区间
            nmd: Optional[Tuple[float, float]] = None  # 非隶属度现在是一个区间
            # 注意：此处未实现 _validate 方法，如果需要，应添加对区间值约束的验证。

        class IVQFNTemplate(FuzznumTemplate):
            """区间值Q序对模糊数模板"""
            mtype = 'ivqfn'

            def report(self) -> str:
                # 实现 FuzznumTemplate 的抽象方法 report。
                # 这里简单地返回 str() 的结果，可以根据需要扩展为更详细的报告。
                return self.str()

            def str(self) -> str:
                # 实现 FuzznumTemplate 的抽象方法 str。
                # 返回 IVQFN 的简洁字符串表示形式，包含 md 区间, nmd 区间 和 q。
                # 通过 self.instance 访问关联的 Fuzznum 实例的属性。
                return f"<{self.instance.md},{self.instance.nmd}>_q={self.instance.q}"

        return [
            (QROFNStrategy, QROFNTemplate),
            (IVQFNStrategy, IVQFNTemplate)
        ]

    # ======================== 事务支持 ========================
    # 事务支持在 FuzznumRegistry 中至关重要，它确保了对注册表状态进行批量修改时的原子性。
    #   这意味着一系列操作要么全部成功并持久化，要么全部失败并回滚到操作之前的状态，从而维护了注册表的数据一致性。
    # 这个模块主要由一个上下文管理器 transaction 和两个辅助方法
    #   _create_snapshot、_restore_snapshot 构成。

    @contextmanager
    def transaction(self):
        """
        注册事务上下文管理器

        Usage:
            with registry.transaction():
                registry.register(strategy1, template1)
                registry.register(strategy2, template2)
                # 如果发生异常，所有注册都会回滚
        """

        if self._in_transaction:
            # 检查当前注册表实例是否已经处于一个事务中。
            # 这处理了“嵌套事务”的情况。如果已经在一个事务中，则不创建新的快照，
            # 而是直接将控制权交给内部的 with 块，内部操作将作为外部事务的一部分。
            # 这意味着只有最外层的事务会负责快照创建和最终的回滚/提交。
            yield
            # 将控制权交给 with 语句块内部的代码。
            return

        # 开始事务
        self._in_transaction = True

        # 在事务开始之前创建快照
        snapshot = self._create_snapshot()

        try:
            yield
            # 将控制权交给 with 语句块内部的代码。
            # 所有的注册、注销等操作都在这里执行。

            # 事物成功，清理快照
            self._transaction_stack.clear()

        except Exception as e:
            # 如果 with 语句块内部发生任何异常，说明事务失败。
            logger.warning(f"Transaction failed, rolling back: {e}")
            # 调用 _restore_snapshot 方法，将注册表的状态恢复到事务开始前创建的快照。
            self._restore_snapshot(snapshot)
            # 重新抛出捕获到的异常。
            # 这是非常重要的，它使得外部调用者能够感知到事务的失败，并进行相应的错误处理。
            # 如果不重新抛出异常就会被这个上下文管理器“吞掉”。
            raise

        finally:
            self._in_transaction = False
            # 无论事务是成功提交还是失败回滚，最终都会执行到这里。
            # 将 _in_transaction 标志重置为 False，表示事务结束，允许新的事务开始。

    def _create_snapshot(self) -> Dict[str, Any]:
        """创建注册表快照"""
        # 这个方法负责在事务开始时，捕获 FuzznumRegistry 的当前状态。
        # 捕获的状态包括：已注册的策略、已注册的模板以及当前的统计数据。

        return {
            'strategies': self.strategies.copy(),
            # 复制当前的 strategies 字典。
            # 使用 .copy() 是关键，它创建了一个字典的浅拷贝，确保快照是独立的，
            # 事务内部对 self.strategies 的修改不会影响到快照中的数据。

            'templates': self.templates.copy(),
            # 复制当前的 templates 字典。
            # 同样使用 .copy() 来保证独立性。

            'stats': self._registration_stats.copy()
            # 复制当前的 _registration_stats 字典。
            # 确保统计数据在快照中也是独立的。
        }

    def _restore_snapshot(self, snapshot: Dict[str, Any]) -> None:
        """恢复注册表快照"""

        # 清空当前注册表中的所有策略。
        # 清空当前注册表中的所有模板。
        self.strategies.clear()
        self.templates.clear()

        # 使用快照中保存的 strategies 字典来更新当前的 strategies 字典。
        # 这将注册表中的策略恢复到事务开始时的状态。
        # 这将注册表中的模板恢复到事务开始时的状态。
        # 确保统计数据也回滚到事务开始时的状态，保持一致性。
        self.strategies.update(snapshot['strategies'])
        self.templates.update(snapshot['templates'])
        self._registration_stats.update(snapshot['stats'])

    # ======================== 观察者模式 ========================
    # 观察者模式（Observer Pattern）是一种行为设计模式，它定义了对象之间一对多的依赖关系，
    # 当一个对象的状态发生改变时，所有依赖于它的对象都会得到通知并自动更新。
    # 在 FuzznumRegistry 中，它使得外部组件可以“监听”注册表的状态变化
    # （例如，有新的模糊数类型被注册或注销），而无需与注册表紧密耦合。
    # 观察者模式的意义：
    # 解耦：注册表不再需要知道谁关心它的状态变化，它只需要在状态改变时调用 _notify_observers。
    #   关心这些变化的组件（观察者）则独立地注册自己。这种松散耦合使得系统更易于维护和扩展。
    # 事件驱动：它将注册表的操作转换为事件，允许其他模块以事件驱动的方式响应这些变化。
    #   例如，一个日志模块可以注册为观察者来记录所有注册/注销事件，一个缓存管理模块可以在类型注销时清除相关缓存。
    # 可扩展性：添加新的响应逻辑非常容易，只需编写一个新的观察者函数并注册即可，
    #   无需修改 FuzznumRegistry 的核心代码。
    # 可测试性：由于逻辑是解耦的，观察者和注册表可以独立进行单元测试。

    def add_observer(self, observer: Callable[[str, Dict[str, Any]], None]) -> None:
        """
        添加注册观察者

        Args:
            observer: 观察者函数，参数为(事件类型, 事件数据)
        """
        if observer not in self._observers:
            # 核心逻辑：这个方法允许外部代码将一个可调用对象（通常是一个函数或方法）注册为观察者。
            # 它首先检查传入的 `observer` 是否已经存在于内部的 `_observers` 列表中。
            # 如果不存在，就将其添加到列表中。
            # 这个检查是为了避免同一个观察者被重复注册多次，从而导致重复通知。
            self._observers.append(observer)

    def remove_observer(self, observer: Callable[[str, Dict[str, Any]], None]) -> None:
        """移除注册观察者"""
        if observer in self._observers:
            # 核心逻辑：这个方法允许外部代码从观察者列表中移除一个已注册的可调用对象。
            # 它首先检查传入的 `observer` 是否存在于 `_observers` 列表中。
            # 如果存在，就将其从列表中移除。
            # 这使得观察者可以在不再需要接收通知时“取消订阅”，避免不必要的资源消耗或错误行为。
            self._observers.remove(observer)

    def _notify_observers(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """通知所有观察者"""
        for observer in self._observers:
            # 核心逻辑：这个方法是观察者模式的“通知”部分，它遍历所有当前已注册的观察者。
            # 对于列表中的每一个 `observer`，它都会尝试调用该观察者。

            try:
                observer(event_type, event_data)
                # 核心逻辑：调用观察者函数，并传递两个参数：
                # 1. `event_type` (字符串)：表示发生的事件类型，例如 'register' 或 'unregister'。
                # 2. `event_data` (字典)：包含事件的详细信息，例如注册的 `mtype`、注册结果等。
                # 这样，每个观察者都可以根据事件类型和数据来执行其特定的响应逻辑。

            except Exception as e:
                # 核心逻辑：这里有一个关键的 `try-except` 块。
                # 它捕获在调用单个观察者函数时可能发生的任何异常。
                # 这是一个非常重要的设计决策：如果一个观察者函数在执行过程中出现错误，
                # 这个异常不应该阻止其他观察者接收通知。
                # 如果没有这个 `try-except`，一个有缺陷的观察者可能会导致整个通知过程中断，
                # 使得其他观察者无法收到通知，从而影响系统的稳定性和一致性。
                logger.warning(f"Observer notification failed: {e}")
                # 记录一条警告日志，指示哪个观察者通知失败以及失败的原因，
                # 但允许通知过程继续进行，不影响其他观察者。

    # ======================== 注册管理 ========================

    def register(self,
                 strategy: Optional[Type[FuzznumStrategy]] = None,
                 template: Optional[Type[FuzznumTemplate]] = None) -> Dict[str, Any]:
        """
        注册新的模糊数类型 - 优化版本

        此方法用于向注册表添加新的模糊数策略和/或模板类。
        它执行严格的类型检查、mtype 一致性检查，并支持覆盖现有注册。
        注册操作是线程安全的。

        Args:
            strategy: 可选，要注册的 FuzznumStrategy 子类。
            template: 可选，要注册的 FuzznumTemplate 子类。

        Returns:
            Dict[str, Any]: 包含注册结果的字典，如 mtype、是否注册成功、是否完整等。

        Raises:
            ValueError: 如果缺少策略或模板，或 mtype 不一致。
            TypeError: 如果传入的不是正确的类类型。
        """

        if not strategy and not template:
            raise ValueError("At least one of 'strategy' or 'template' must be provided.")

        # 调用辅助方法对传入的策略和模板类进行预验证，确保它们是合法的 FuzznumStrategy/FuzznumTemplate 子类。
        if strategy is not None:
            self._validate_strategy_class(strategy)
        if template is not None:
            self._validate_template_class(template)

        # 从提供的策略或模板中提取模糊数类型标识符 (mtype)
        # 这是注册的关键，因为 mtype 是注册表中查找和管理这些类的唯一键。
        mtype = self._extract_mtype(strategy, template)

        if strategy is not None and template is not None:
            if strategy.mtype != template.mtype:
                raise ValueError(
                    f"Strategy and template mtype mismatch: "
                    f"strategy='{strategy.mtype}', template='{template.mtype}'"
                )

        with self._lock:
            # 线程安全：获取注册表级别的锁。
            # 这确保了在多线程环境下，对注册表内部数据结构（self.strategies, self.templates）
            # 的修改是原子性的，防止竞态条件和数据损坏。

            # 判断该 mtype 是否已经存在对应的策略或模板，用于后续的覆盖警告和统计。
            existing_strategy = mtype in self.strategies
            existing_template = mtype in self.templates

            # 准备注册结果字典：
            # 初始化一个字典来记录本次注册操作的详细结果，包括 mtype、注册状态、是否覆盖等。
            result = {
                'mtype': mtype,
                'strategy_registered': False,
                'template_registered': False,
                'is_complete': False,
                'overwrote_existing': {
                    'strategy': existing_strategy and strategy is not None,
                    'template': existing_template and template is not None
                },
                'timestamp': self._get_timestamp()
            }

            try:
                # 注册策略和模板：
                # 如果提供了策略类，将其注册到 self.strategies 字典中。
                # 如果提供了模板类，将其注册到 self.templates 字典中。
                # 如果存在同名，会发出警告并覆盖。
                if strategy is not None:
                    if existing_strategy:
                        logger.warning(f"Overwriting existing strategy for mtype '{mtype}'")
                        self._registration_stats['overwrites'] += 1
                    self.strategies[mtype] = strategy
                    result['strategy_registered'] = True
                    logger.debug(f"Registered strategy: {strategy.__name__} for mtype '{mtype}'")

                if template is not None:
                    if existing_template:
                        logger.warning(f"Overwriting existing template for mtype '{mtype}'")
                        self._registration_stats['overwrites'] += 1
                    self.templates[mtype] = template
                    result['template_registered'] = True
                    logger.debug(f"Registered template: {template.__name__} for mtype '{mtype}'")

                # 检查完整性：
                result['is_complete'] = (mtype in self.strategies and mtype in self.templates)

                # 更新统计：
                self._registration_stats['total_registrations'] += 1

                # 通知观察者：
                # 调用 _notify_observers 方法，通知所有已注册的观察者，有新的注册事件发生。
                # 观察者可以根据这个通知执行相应的逻辑（如日志记录、缓存更新等）。
                self._notify_observers('register', result)

                logger.info(f"Successfully registered mtype '{mtype}' (complete: {result['is_complete']})")

                return result

            except Exception as e:
                self._registration_stats['failed_registrations'] += 1
                logger.error(f"Registration failed for mtype '{mtype}': {e}")
                raise

    @staticmethod
    def _validate_strategy_class(strategy: Type[FuzznumStrategy]) -> None:
        """验证策略类"""
        # 检查：传入的 `strategy` 是否是一个类（而不是实例或其他类型）。
        if not isinstance(strategy, type):
            raise TypeError(f"Strategy must be a class, got {type(strategy).__name__}")

        # 检查：传入的 `strategy` 是否是 `FuzznumStrategy` 的子类。
        # 这是确保策略类符合接口定义的关键。
        if not issubclass(strategy, FuzznumStrategy):
            raise TypeError(f"Strategy must be a subclass of FuzznumStrategy, got {strategy.__name__}")

        # 检查：策略类是否定义了 `mtype` 属性。
        # `mtype` 是模糊数类型的唯一标识符，对于注册和查找至关重要。
        if not hasattr(strategy, 'mtype'):
            raise ValueError(f"Strategy class {strategy.__name__} must define 'mtype' attribute")

    @staticmethod
    def _validate_template_class(template: Type[FuzznumTemplate]) -> None:
        """验证模板类"""
        # 检查：传入的 `template` 是否是一个类。
        if not isinstance(template, type):
            raise TypeError(f"Template must be a class, got {type(template).__name__}")

        # 检查：传入的 `template` 是否是 `FuzznumTemplate` 的子类。
        # 这是确保模板类符合接口定义的关键。
        if not issubclass(template, FuzznumTemplate):
            raise TypeError(f"Template must be a subclass of FuzznumTemplate, got {template.__name__}")

        # 检查：模板类是否定义了 `mtype` 属性。
        # `mtype` 是模糊数类型的唯一标识符，对于注册和查找至关重要。
        if not hasattr(template, 'mtype'):
            raise ValueError(f"Template class {template.__name__} must define 'mtype' attribute")

    @staticmethod
    def _extract_mtype(strategy: Optional[Type[FuzznumStrategy]],
                       template: Optional[Type[FuzznumTemplate]]) -> str:
        """提取模糊数类型"""
        # 核心逻辑：这个方法从提供的策略或模板类中提取 `mtype` 字符串。
        # 它优先从 `strategy` 中获取 `mtype`，如果 `strategy` 为 None，则从 `template` 中获取。
        if strategy is not None:
            return str(strategy.mtype)
        elif template is not None:
            return str(template.mtype)
        else:
            # 如果策略和模板都为 None，则无法提取 mtype，抛出错误。
            raise ValueError("Cannot extract mtype: both strategy and template are None")

    @staticmethod
    def _get_timestamp():
        import datetime
        return datetime.datetime.now().strftime("%Y%m%d%H%M%S.%f")

    def batch_register(self, registrations: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        执行多个模糊数类型的批量注册（事务性）。

        此方法允许在一个原子操作中注册多个模糊数策略和/或模板。
        如果批处理中的任何注册失败，则在该批处理操作期间所做的所有更改都将回滚，
        从而确保注册表的一致性。

        Args:
            registrations (List[Dict[str, Any]]): 字典列表，每个字典指定要注册的策略和/或模板。
                每个字典应包含 'strategy' (Type[FuzznumStrategy]) 和/或 'template' (Type[FuzznumTemplate]) 键，
                对应于要注册的类。

        Returns:
            Dict[str, Dict[str, Any]]: 字典，其中键是 `mtype` 字符串，值是每个类型的注册结果。
                如果在批处理中某个特定注册发生错误，即使整个事务已回滚，返回的字典中也可能包含
                一个键为 "error_N"（N 是输入列表中的索引）且值为错误详细信息的条目。

        Raises:
            TypeError: 如果 `registrations` 不是列表，或者列表中任何项不是字典。
            Exception: 如果批处理中的任何单个注册失败，原始异常（例如 `ValueError`、`TypeError`）
                将在事务回滚后重新抛出。这意味着如果 `batch_register` 抛出异常，
                注册表的状态将恢复到调用该方法之前的状态。
        """
        if not isinstance(registrations, list):
            raise TypeError(f"Registrations must be a list, got {type(registrations).__name__}")

        results = {}

        with self.transaction():
            # 核心逻辑：使用 `self.transaction()` 上下文管理器包装整个批量注册过程。
            # 这确保了所有在 `with` 块内部的注册操作都具有原子性：
            # 如果任何一个 `register` 调用失败，整个 `batch_register` 操作都会被回滚，
            # 注册表将恢复到 `batch_register` 调用之前的状态。

            for i, registration in enumerate(registrations):
                # 遍历传入的注册请求列表。
                # 检查：确保列表中的每个元素都是一个字典。
                if not isinstance(registration, dict):
                    raise TypeError(f"Each registration must be a dict, got {type(registration).__name__} at index {i}")

                strategy = registration.get('strategy')
                template = registration.get('template')

                try:
                    result = self.register(strategy=strategy, template=template)
                    # 调用 `register` 方法来处理单个注册请求。
                    results[result['mtype']] = result
                    # 将单个注册的结果存储到 `results` 字典中。

                except Exception as e:
                    # 错误处理：如果单个 `register` 调用失败，捕获异常。
                    # 记录错误信息，并重新抛出异常。
                    # 关键点：重新抛出异常会导致 `self.transaction()` 上下文管理器捕获到异常，
                    # 从而触发整个事务的回滚机制。
                    error_info = {
                        'error': str(e),
                        'index': i,
                        'timestamp': self._get_timestamp()
                    }
                    results[f"error_{i}"] = error_info
                    raise

        return results

    def unregister(self, mtype: str,
                   remove_strategy: bool = True,
                   remove_template: bool = True) -> Dict[str, Any]:

        # 检查：确保传入的 `mtype` 是一个字符串。
        if not isinstance(mtype, str):
            raise TypeError(f"mtype must be a string, got {type(mtype).__name__}")

        with self._lock:
            # 线程安全：获取注册表级别的锁。
            # 这确保了在多线程环境下，对注册表内部数据结构（self.strategies, self.templates）
            # 的修改是原子性的。

            # 准备注销结果字典：
            # 初始化一个字典来记录本次注销操作的详细结果，包括 mtype、移除状态、注销前是否完整等。
            result = {
                'mtype': mtype,
                'strategy_removed': False,
                'template_removed': False,
                'was_complete': (mtype in self.strategies and mtype in self.templates),
                'timestamp': self._get_timestamp()
            }

            # 移除策略：
            # 如果 `remove_strategy` 为 True 且该 `mtype` 存在对应的策略，则将其从 `self.strategies` 中删除。
            if remove_strategy and mtype in self.strategies:
                del self.strategies[mtype]
                result['strategy_removed'] = True
                logger.debug(f"Removed strategy for mtype '{mtype}'")

            # 移除模板：
            # 如果 `remove_template` 为 True 且该 `mtype` 存在对应的模板，则将其从 `self.templates` 中删除。
            if remove_template and mtype in self.templates:
                del self.templates[mtype]
                result['template_removed'] = True
                logger.debug(f"Removed template for mtype '{mtype}'")

            # 记录历史：
            # 将本次注销操作的详细结果（副本）添加到注册历史列表中，用于追踪和审计。
            self._registration_history.append(result.copy())

            # 通知观察者：
            # 调用 _notify_observers 方法，通知所有已注册的观察者，有新的注销事件发生。
            self._notify_observers('unregister', result)

            logger.info(
                f"Unregistered mtype '{mtype}' (strategy: {result['strategy_removed']}, template: {result['template_removed']})")

            return result

    # ======================== 自省方法 ========================

    def get_strategy(self, mtype: str) -> Type[FuzznumStrategy]:
        """
        获取指定 `mtype` 的策略类。

        Args:
            mtype (str): 模糊数类型标识符。

        Returns:
            Type[FuzznumStrategy]: 对应的策略类。

        Raises:
            ValueError: 如果指定 `mtype` 的策略类未在注册表中找到。
        """
        # 这个方法根据模糊数类型标识符 `mtype`，从已注册的策略字典中查找并返回对应的策略类。
        # 它是 Fuzznum 对象在初始化时获取具体策略实现的关键途径。
        strategy_cls = self.strategies.get(mtype)
        if strategy_cls is None:
            raise ValueError(f"Strategy for mtype '{mtype}' not found in registry.")
        return strategy_cls
        # 直接使用字典的 `get()` 方法。如果 `mtype` 存在，则返回对应的策略类；
        # 如果不存在，则返回 `None`，避免抛出 KeyError。

    def get_template(self, mtype: str) -> Type[FuzznumTemplate]:
        """
        获取指定 `mtype` 的模板类。

        Args:
            mtype (str): 模糊数类型标识符。

        Returns:
            Type[FuzznumTemplate]: 对应的模板类。

        Raises:
            ValueError: 如果指定 `mtype` 的模板类未在注册表中找到。
        """
        # 这个方法根据模糊数类型标识符 `mtype`，从已注册的模板字典中查找并返回对应的模板类。
        # 它是 Fuzznum 对象在初始化时获取具体模板实现的关键途径。
        template_cls = self.templates.get(mtype)
        if template_cls is None:
            raise ValueError(f"Template for mtype '{mtype}' not found in registry.")
        return template_cls
        # 同样使用字典的 `get()` 方法。如果 `mtype` 存在，则返回对应的模板类；
        # 如果不存在，则返回 `None`。

    def get_registered_mtypes(self) -> Dict[str, Dict[str, Any]]:
        """获取所有已注册的模糊数类型信息 - 优化版本"""
        # 这个方法提供了一个全面的概览，列出所有在注册表中出现过的模糊数类型，
        # 并指示每种类型是否拥有策略、模板，以及是否是“完整”的（即策略和模板都存在）。

        all_mtypes = set(self.strategies.keys()) | set(self.templates.keys())
        # 核心逻辑：通过对 `strategies` 字典的键集合和 `templates` 字典的键集合执行并集操作，
        # 获取所有在注册表中出现过的唯一 `mtype` 集合。这确保了即使只有策略或只有模板的类型也会被包含。

        result = {}
        # 初始化一个空字典，用于存储最终的类型信息。

        for mtype in all_mtypes:
            has_strategy = mtype in self.strategies
            has_template = mtype in self.templates

            result[mtype] = {
                'has_strategy': has_strategy,
                'has_template': has_template,
                'strategy_class': self.strategies[mtype].__name__ if has_strategy else None,
                # 如果有策略，则记录策略类的名称；否则为 None。
                'template_class': self.templates[mtype].__name__ if has_template else None,
                # 如果有模板，则记录模板类的名称；否则为 None。
                'is_complete': has_strategy and has_template
                # 只有当策略和模板都存在时，才认为该类型是“完整”的。
            }

        return result

    def get_statistics(self) -> Dict[str, Any]:
        """获取注册表统计信息"""
        # 这个方法提供注册表操作的量化统计数据，便于监控和分析注册表的活跃度和状态。
        return {
            'total_strategies': len(self.strategies),
            # 已注册的策略类的总数量。
            'total_templates': len(self.templates),
            # 已注册的模板类的总数量。
            'complete_types': len(set(self.strategies.keys()) & set(self.templates.keys())),
            # 核心逻辑：通过对 `strategies` 键集合和 `templates` 键集合执行交集操作，
            # 得到同时拥有策略和模板的 `mtype` 的数量，即“完整”类型的数量。
            'registration_stats': self._registration_stats.copy(),
            # 返回内部统计字典 `_registration_stats` 的副本，包含注册成功、失败、覆盖等计数。
            # 返回副本是为了防止外部直接修改内部统计数据。
            'observer_count': len(self._observers)
            # 当前注册的观察者数量。
        }

    def get_health_status(self) -> Dict[str, Any]:
        """获取注册表健康状态"""
        # 这个方法评估注册表的“健康”状况，识别潜在的问题，如不完整或缺失的类型定义。

        complete_types = set(self.strategies.keys()) & set(self.templates.keys())
        # 核心逻辑：计算同时拥有策略和模板的 `mtype` 集合。

        incomplete_types = (set(self.strategies.keys()) | set(self.templates.keys())) - complete_types
        # 核心逻辑：计算所有出现过的 `mtype` 集合（并集）减去完整类型集合，
        # 得到那些只有策略或只有模板的“不完整”类型。

        return {
            'is_healthy': len(incomplete_types) == 0,
            # 如果没有不完整的类型，则认为注册表是健康的。
            'total_types': len(self.strategies) + len(self.templates),
            # 策略和模板的总数（可能重复计数）。
            'complete_types': list(complete_types),
            # 完整类型的 `mtype` 列表。
            'incomplete_types': list(incomplete_types),
            # 不完整类型的 `mtype` 列表。
            'missing_strategies': list(set(self.templates.keys()) - set(self.strategies.keys())),
            # 核心逻辑：计算只有模板而没有策略的 `mtype` 列表。
            # 这表示存在模板但其对应的算法实现缺失。
            'missing_templates': list(set(self.strategies.keys()) - set(self.templates.keys())),
            # 核心逻辑：计算只有策略而没有模板的 `mtype` 列表。
            # 这表示存在算法实现但其对应的表示方式缺失。
            'error_rate': (self._registration_stats['failed_registrations'] /
                           max(1, self._registration_stats['total_registrations']))
            # 计算注册失败率。`max(1, ...)` 用于防止 `total_registrations` 为 0 时发生除以零错误。
        }


# ======================== 全局单例和工厂方法 ========================

# 全局注册表实例

_registry_instance: Optional[FuzznumRegistry] = None
_registry_lock = threading.RLock()


def get_registry() -> FuzznumRegistry:
    """
    获取全局模糊数注册表实例。

    这是一个工厂函数，用于获取 `FuzznumRegistry` 的唯一单例实例。
    它确保在整个应用程序中，无论调用多少次，都只会返回同一个注册表实例。

    Returns:
        FuzznumRegistry: 全局唯一的模糊数注册表实例。

    Examples:
        >>> registry_instance = get_registry()
        >>> print(registry_instance) # 打印注册表实例
    """
    global _registry_instance

    if _registry_instance is None:
        with _registry_lock:
            if _registry_instance is None:
                _registry_instance = FuzznumRegistry()

    return _registry_instance


# 便捷的全局函数
def register_fuzznum(strategy: Optional[Type[FuzznumStrategy]] = None,
                     template: Optional[Type[FuzznumTemplate]] = None) -> Dict[str, Any]:
    """
    全局注册函数：注册单个模糊数策略和/或模板。

    此函数是 `get_registry().register()` 的便捷封装。

    Args:
        strategy (Optional[Type[FuzznumStrategy]]): 要注册的模糊数策略类。
        template (Optional[Type[FuzznumTemplate]]): 要注册的模糊数模板类。

    Returns:
        Dict[str, Any]: 包含注册结果的字典。

    Examples:
        # >>> from mohupy.core.base import ExampleStrategy, ExampleTemplate
        >>> # 注册一个新类型
        >>> result = register_fuzznum(strategy=ExampleStrategy, template=ExampleTemplate)
        >>> print(result['mtype'], result['is_complete'])
        my_type True
        >>> # 验证是否已注册
        >>> print(get_registry().get_registered_mtypes().get('my_type', {}).get('is_complete'))
        True
    """
    return get_registry().register(strategy=strategy, template=template)


def batch_register_fuzznums(registrations: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    全局批量注册函数：执行多个模糊数类型的批量注册（事务性）。

    此函数是 `get_registry().batch_register()` 的便捷封装。

    Args:
        registrations (List[Dict[str, Any]]): 字典列表，每个字典指定要注册的策略和/或模板。

    Returns:
        Dict[str, Dict[str, Any]]: 字典，其中键是 `mtype` 字符串，值是每个类型的注册结果。

    Examples:
        >>> # 假设 MyStrategyA, MyTemplateA, MyStrategyB, MyTemplateB 已经定义如下:
        >>> # class MyStrategyA(FuzznumStrategy): mtype = "type_a"; pass
        >>> # class MyTemplateA(FuzznumTemplate): mtype = "type_a"; def report(self): return ""; def str(self): return ""
        >>> # class MyStrategyB(FuzznumStrategy): mtype = "type_b"; pass
        >>> # class MyTemplateB(FuzznumTemplate): mtype = "type_b"; def report(self): return ""; def str(self): return ""
        >>>
        >>> # 构建批量注册请求列表
        >>> registrations_list = [
        ...     {'strategy': MyStrategyA, 'template': MyTemplateA},
        ...     {'strategy': MyStrategyB, 'template': MyTemplateB}
        ... ]
        >>>
        >>> # 执行批量注册
        >>> results = batch_register_fuzznums(registrations_list)
        >>> print(results['type_a']['is_complete'], results['type_b']['is_complete'])
        (True, True)
        >>> # 验证是否成功注册
        >>> print(get_registry().get_registered_mtypes().get('type_a', {}).get('is_complete'))
        True
    """
    return get_registry().batch_register(registrations)


def unregister_fuzznum(mtype: str,
                       remove_strategy: bool = True,
                       remove_template: bool = True) -> Dict[str, Any]:
    """全局注销函数：从注册表注销一个模糊数类型。

    此函数是 `get_registry().unregister()` 的便捷封装。

    Args:
        mtype (str): 要注销的模糊数类型标识符。
        remove_strategy (bool): 是否移除对应的策略类 (默认为 True)。
        remove_template (bool): 是否移除对应的模板类 (默认为 True)。

    Returns:
        Dict[str, Any]: 包含注销结果的字典。

    Examples:
        >>> result = unregister_fuzznum("my_type")
        >>> print(result['mtype'], result['strategy_removed'], result['template_removed'])
        my_type True True
        >>> # 验证是否已注销
        >>> print(get_registry().get_registered_mtypes().get('my_type'))
        None
    """
    return get_registry().unregister(
        mtype=mtype,
        remove_strategy=remove_strategy,
        remove_template=remove_template
    )


def get_strategy(mtype: str) -> Optional[Type[FuzznumStrategy]]:
    """

    此函数是 `get_registry().get_strategy()` 的便捷封装。

    Args:
        mtype (str): 模糊数类型标识符。

    Returns:
        Optional[Type[FuzznumStrategy]]: 对应的策略类，如果不存在则为 `None`。

    Examples:
        >>> strategy_cls = get_strategy("my_type")
        >>> print(strategy_cls.__name__)
        MyStrategy
        >>> # 获取不存在的策略类
        >>> non_existent_strategy = get_strategy("non_existent_type")
        >>> print(non_existent_strategy)
        None
    """
    return get_registry().get_strategy(mtype)


def get_template(mtype: str) -> Optional[Type[FuzznumTemplate]]:
    """
    全局获取模板函数：获取指定 `mtype` 的模板类。

    此函数是 `get_registry().get_template()` 的便捷封装。

    Args:
        mtype (str): 模糊数类型标识符。

    Returns:
        Optional[Type[FuzznumTemplate]]: 对应的模板类，如果不存在则为 `None`。

    Examples:
        >>> # 获取模板类
        >>> template_cls = get_template("my_type")
        >>> print(template_cls.__name__)
        MyTemplate
        >>> # 获取不存在的模板类
        >>> non_existent_template = get_template("non_existent_type")
        >>> print(non_existent_template)
        None
    """
    return get_registry().get_template(mtype)


def get_registered_mtypes() -> Dict[str, Dict[str, Any]]:
    """
    全局获取注册类型函数：获取所有已注册的模糊数类型信息。

    此函数是 `get_registry().get_registered_mtypes()` 的便捷封装。

    Returns:
        Dict[str, Dict[str, Any]]: 包含所有已注册类型信息的字典。

    Examples:
        >>> # 获取所有已注册类型
        >>> all_types = get_registered_mtypes()
        >>> # 打印 'some_type' 的信息 (如果已注册)
        >>> print(all_types.get('some_type', {}).get('is_complete'))
        True
        >>> # 打印所有注册的 mtype 键
        >>> print(sorted(list(all_types.keys())))
        ['ivqfn', 'qrofn', 'some_type'] # 可能会包含默认注册的类型
    """
    return get_registry().get_registered_mtypes()
