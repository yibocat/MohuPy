#  Copyright (c) yibocat 2025 All Rights Reserved
#  Python: 3.10.9
#  Date: 2025/7/27 00:41
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import collections
import logging
import threading
import time
from contextlib import contextmanager

from typing import Optional, Dict, Tuple, Any, Union, Callable, List

from mohupy_.config import get_config
from mohupy_.core.fuzznums import Fuzznum
from mohupy_.core.triangular import OperationTNorm

logger = logging.getLogger(__name__)


class Executor:

    def __init__(self, t_norm_type: Optional[str] = None):
        """
        初始化运算器
        """
        # --- 基础配置 ---
        # 从全局配置中获取配置对象
        self._config = get_config()
        # 初始化一个可重入锁（RLock）
        self._lock = threading.RLock()
        # 初始化t-范数类型
        self._t_norm_type = t_norm_type or self._config.DEFAULT_T_NORM

        # --- 日志和调试 ---
        # 检查配置中是否启用了调试模式。
        self._debug_mode = getattr(self._config, 'DEBUG_MODE', False)
        # 检查配置中是否启用了性能监控。
        self._performance_enabled = getattr(self._config, 'ENABLE_PERFORMANCE_MONITORING', False)

        # --- 缓存机制 ---
        # 检查配置中是否启用了缓存。
        self._cache_enabled = getattr(self._config, 'ENABLE_EXECUTOR_CACHE', True)

        # 初始化用于存储运算结果的缓存字典。
        # 键是根据运算类型和输入 Fuzznum 生成的，值是运算结果。
        self._result_cache: collections.OrderedDict = collections.OrderedDict()

        # 初始化用于存储 Fuzznum 实例的缓存字典。
        # 键是 Fuzznum 的某种标识，值是 Fuzznum 实例。
        # 这可以避免为相同结果重复创建 Fuzznum 对象。
        self._fuzznum_cache: Dict[str, Fuzznum] = {}

        # 初始化缓存统计数据，用于监控缓存效率。
        self._cache_stats = {
            'hits': 0,  # 缓存命中次数
            'misses': 0,  # 缓存未命中次数
            'total_requests': 0,  # 缓存总请求数
            'hit_ratio': 0.0  # 缓存命中率
        }

        # --- 性能监控 ---
        # 初始化执行统计字典，用于记录执行器层面的操作性能。
        self._execution_stats = {
            'total_operations': 0,  # 总操作次数
            'successful_operations': 0,  # 成功操作次数
            'failed_operations': 0,  # 失败操作次数
            'total_execution_time': 0.0,  # 总执行时间
            'avg_execution_time': 0.0,  # 平均执行时间
            'operation_counts': {}  # 各种运算类型的操作次数统计
        }

        # --- 验证统计 ---
        # 初始化 Fuzznum 验证统计字典。
        self._validation_stats = {
            'total_validations': 0,  # 总验证次数
            'failed_validations': 0,  # 失败验证次数
            'validation_errors': []  # 存储验证错误的详细信息
        }

        # 记录执行器实例的创建时间戳。
        self._creation_time = time.perf_counter()

        # 如果处于调试模式，则输出一条执行器初始化成功的调试日志。
        if self._debug_mode:
            logger.debug(f"Executor initialized with t-norm: '{self._t_norm_type}'")

    # ============================== 运算执行（内部方法） ===============================

    def _validate_fuzznum(self, fuzz_obj: Fuzznum) -> None:
        """
        验证模糊数对象

        用于验证输入的 Fuzznum 对象是否有效。在执行任何运算之前，
        确保输入的 Fuzznum 对象符合当前执行器的要求，
        包括类型兼容性、策略属性有效性以及对象自身的状态完整性。验证失败会抛出异常并记录错误信息。

        Args:
            fuzz_obj: 要验证的 Fuzznum 实例。

        Raises:
            ValueError: 如果 Fuzznum 对象验证失败。
        """
        # 记录验证开始时间，用于性能统计。
        start_time = time.perf_counter()

        try:
            # 获取实例锁。
            # 这是为了确保在多线程环境下，对 _validation_stats 字典的修改是线程安全的。
            with self._lock:
                # 增加总验证次数。
                self._validation_stats['total_validations'] += 1

            # --- 验证策略属性 ---
            # 获取 Fuzznum 对象的策略属性字典。
            attr_dict = fuzz_obj.get_strategy_attributes_dict()
            # 遍历策略属性字典中的每一个键值对。
            for key, value in attr_dict.items():
                # 检查属性值是否为 None。
                if value is None:
                    # 如果有属性值为 None，则抛出 ValueError，说明策略属性无效。
                    raise ValueError(f"Fuzzy number must have valid strategy attributes: "
                                     f"'{key}' has invalid value '{value}'.")

            # --- 验证对象状态 ---
            # 调用 Fuzznum 对象自身的 validate_state 方法，进行更深层次的验证。
            validation_result = fuzz_obj.validate_state()
            # 检查验证结果中的 'is_valid' 标志。
            if not validation_result.get('is_valid', True):
                # 如果对象状态无效，则获取验证问题列表。
                issues = validation_result.get('issues', [])
                # 抛出 ValueError，列出所有验证失败的问题。
                raise ValueError(f"Fuzzy number validation failed: {'; '.join(issues)}")

            # 如果所有验证都通过，并且处于调试模式，则输出一条验证通过的调试日志。
            if self._debug_mode:
                logger.debug(f"Fuzznum validation passed for {fuzz_obj.mtype}")

        except Exception as e:
            # 如果在 try 块中发生任何异常（验证失败）。
            # 获取实例锁。
            with self._lock:
                self._validation_stats['failed_validations'] += 1
                self._validation_stats['validation_errors'].append({
                    'error': str(e),  # 错误信息字符串
                    'timestamp': time.perf_counter(),  # 错误发生的时间戳
                    'fuzznum_id': id(fuzz_obj)  # 出错的 Fuzznum 对象的内存ID
                })

            # 如果处于调试模式，则输出一条验证失败的错误日志。
            if self._debug_mode:
                logger.error(f"Fuzznum validation failed: {e}")
            # 重新抛出捕获到的异常，以便调用者能够处理。
            raise

        # finally:
        #     # 无论 try 块是正常完成还是发生异常，finally 块都会执行。
        #     # 计算验证耗时。
        #     execution_time = time.perf_counter() - start_time
        #     # 如果性能监控启用，则更新性能统计。
        #     if self._performance_enabled:
        #         # 调用 _update_performance_stats 方法，传入 'validation' 作为操作类型，
        #         # 验证耗时，以及验证是否成功（由 _validation_stats['failed_validations'] 是否增加判断）。
        #         self._update_performance_stats('validation',
        #                                        execution_time,
        #                                        self._validation_stats['failed_validations'] == 0)

    def _create_result_fuzznum(self,
                               operation_type: str,
                               result: Dict[str, Any]) -> Union[Fuzznum, bool, Dict]:
        """
        创建结果模糊数对象

        用于将底层运算返回的字典结果转换为 Fuzznum 对象或布尔值（针对比较运算）。
        其逻辑思路是：标准化运算的输出，使其对用户来说是易于理解和使用的。
        它还支持对 Fuzznum 实例进行缓存，避免为相同结果重复创建对象。

        Args:
            operation_type: 运算类型字符串（如 'add', 'gt'）。
            result: 由底层运算（通过 factory.execute）返回的结果字典。

        Returns:
            Union[Fuzznum, bool, Dict]: 转换后的结果。
                - 对于比较运算，返回布尔值。
                - 对于其他运算，返回 Fuzznum 实例或原始字典（如果创建失败）。
        """
        config = get_config()

        # --- 处理比较运算结果 ---
        # 定义一个包含所有比较运算类型的集合。
        # 特别注意，在比较运算中返回的结果也必须是字典，且字典的键为 'value'，值为 bool
        comparison_ops = {'gt', 'lt', 'eq', 'ge', 'le', 'ne'}
        if operation_type in comparison_ops:
            if 'value' in result and isinstance(result['value'], bool):
                return result['value']
            # 如果结果格式不符合预期，则抛出 ValueError。
            raise ValueError(f"Comparison operation '{operation_type}' "
                             f"returned an unexpected result format: {result}. "
                             f"Expected a boolean value under 'value' key.")

        # --- 处理其他运算结果 ---
        # 为 Fuzznum 实例生成一个缓存键。
        cache_key = f"fuzznum_{result}_{id(result)}"

        try:
            # --- 检查 Fuzznum 缓存 ---
            # 检查 cache_key 是否存在于 _fuzznum_cache 字典中。

            if cache_key in self._fuzznum_cache:
                # 如果命中缓存，并且处于调试模式，则输出一条复用缓存 Fuzznum 的调试日志。
                if self._debug_mode:
                    logger.debug(f"Reusing cached Fuzznum for {operation_type}")
                    # 直接返回缓存中的 Fuzznum 实例。
                return self._fuzznum_cache[cache_key]

            # --- 创建新的 Fuzznum 实例 ---
            fuzznum = Fuzznum(result['mtype'])
            fuzznum.from_dict(result)

            # --- 缓存 Fuzznum 实例 ---
            if self._cache_enabled:
                self._fuzznum_cache[cache_key] = fuzznum

            # 如果处于调试模式，则输出一条创建新 Fuzznum 的调试日志。
            if self._debug_mode:
                logger.debug(f"Created new Fuzznum for {operation_type}")

            return fuzznum

        except (ValueError, AttributeError, RuntimeError) as e:
            # 如果在尝试创建 Fuzznum 对象时发生已知的异常（如数据格式错误、属性不存在、运行时错误）。
            # 检查配置中的调试模式。
            if config.DEBUG_MODE:
                # 如果处于调试模式，则输出一条警告日志，说明创建 Fuzznum 失败，并返回原始字典。
                logger.warning(f"Failed to create Fuzznum object from result for operation '{operation_type}' "
                               f"with mtype '{result['mtype']}': {e}. Returning raw dictionary: {result}")
            # 返回原始的结果字典。
            return result
        except Exception as e:
            # 如果在尝试创建 Fuzznum 对象时发生任何其他未知的异常。
            # 检查配置中的调试模式。
            if config.DEBUG_MODE:
                # 如果处于调试模式，则输出一条警告日志，说明发生意外错误，并返回原始字典。
                logger.warning(f"An unexpected error occurred during Fuzznum creation for operation '{operation_type}' "
                               f"with mtype '{result['mtype']}': {e}. Returning raw dictionary: {result}")
            # 返回原始的结果字典。
            return result

    def _execute_binary_op(self,
                           operation_type: str,
                           fuzznum_1: Fuzznum,
                           fuzznum_2: Fuzznum,
                           **params) -> Union[Fuzznum, bool, Dict[str, Any]]:
        """
        内部方法：执行二元运算。

        此方法封装了所有二元运算（如加、减、乘、除、比较、逻辑交并等）的执行流程。
        包括：
        1. 缓存检查：避免重复计算。
        2. 输入验证：确保 Fuzznum 对象的有效性和类型兼容性。
        3. 操作数准备：从 Fuzznum 实例中提取底层策略属性。
        4. 委托执行：将运算请求转发给 `OperationFactory`。
        5. 结果转换：将工厂返回的原始结果转换为 Fuzznum 对象或布尔值。
        6. 结果缓存：存储运算结果以供后续使用。

        Args:
            operation_type (str): 运算类型字符串（例如 'add', 'gt', 'and'）。
            fuzznum_1 (Fuzznum): 第一个模糊数操作数。
            fuzznum_2 (Fuzznum): 第二个模糊数操作数。
            **params (Any): 额外的参数

        Returns:
            Union[Fuzznum, bool, Dict[str, Any]]: 运算结果。
                - 对于比较运算，返回布尔值。
                - 对于其他运算，返回 Fuzznum 实例或原始字典（如果 Fuzznum 创建失败）。

        Raises:
            ValueError: 如果 Fuzznum 对象无效、mtype 不一致或结果格式不符合预期。
            Exception: 传播 `OperationFactory` 或底层运算中抛出的任何异常。
        """
        # 定义一个内部嵌套函数 `_execute`，它包含了实际的二元运算逻辑。
        # 这个函数将被传递给 `_execute_with_monitoring` 包装器，
        # 从而自动获得性能监控和异常处理的能力。

        def _execute():

            # --- 1. 验证输入 Fuzznum 对象 ---
            # 调用私有方法 `_validate_fuzznum` 对 Fuzznum 对象进行验证。
            # 这会检查 Fuzznum 的 mtype 是否与当前包装器兼容，以及其内部状态是否有效。
            self._validate_fuzznum(fuzznum_1)
            self._validate_fuzznum(fuzznum_2)

            # --- 2. 检查 Fuzznum 类型的兼容性 ---
            # 对于二元运算，两个模糊数必须具有相同的 mtype。
            if fuzznum_1.mtype != fuzznum_2.mtype:
                # 如果 mtype 不一致，则抛出 ValueError，明确指出错误。
                raise ValueError(f"Fuzznums must have the same mtype for binary operations: "
                                 f"'{fuzznum_1.mtype}' and '{fuzznum_2.mtype}' are not the same.")

            # 对于二元运算，两个模糊数必须具有相同的 qrung。
            if fuzznum_1.q != fuzznum_2.q:
                # 如果 qrung 不一致，则抛出 ValueError，明确指出错误。
                raise ValueError(f"Fuzznums must have the same qrung for binary operations: "
                                 f"'{fuzznum_1.q}' and '{fuzznum_2.q}' are not the same.")

            # --- 3. 创建t-范数实例并获取策略实例 ---
            tnorm_instance = OperationTNorm(self._t_norm_type, q=fuzznum_1.q, **params)
            strategy1 = fuzznum_1.get_strategy_instance()      # 第一个运算数
            strategy2 = fuzznum_2.get_strategy_instance()      # 第二个运算数

            # --- 4. 直接在策略上查找并调用运算方法 ---
            operation_method = getattr(strategy1, operation_type, None)
            if not callable(operation_method):
                raise NotImplementedError(f"Operation '{operation_type}' is not implemented in "
                                          f"strategy '{strategy1.__class__.__name__}'.")

            # --- 5. 执行运算 ---
            result_dict = operation_method(strategy2, tnorm_instance)

            # --- 6. 创建结果 ---
            # 这里调用的是 Fuzznum.create 而不是 from_dict, 更加通用
            # 您需要确保 Fuzznum.create 接受字典形式的参数
            return Fuzznum.create(fuzznum_1, **result_dict)

        # --- 6. 缓存检查 ---
        # 生成一个唯一的缓存键，用于标识本次运算请求。
        # 缓存键的生成考虑了运算类型、两个 Fuzznum 实例的身份和内容，以及额外参数。
        cache_key = self._generate_cache_key(operation_type, fuzznum_1, fuzznum_2, *params)
        # 尝试从内部缓存 `_result_cache` 中获取结果。
        # `cache_hit` 为 True 表示命中缓存，`cached_result` 为缓存中的值。
        cache_hit, cached_result = self._get_cached_result(cache_key)

        # 如果命中缓存，则直接返回缓存的结果，避免重复计算。
        if cache_hit:
            return cached_result

        # --- 7. 执行运算并监控 ---
        # 调用 `_execute_with_monitoring` 包装器来执行 `_execute` 内部函数。
        # 这会自动处理性能统计、日志记录和异常捕获。
        result = self._execute_with_monitoring(operation_type, _execute)

        # --- 8. 缓存结果 ---
        # 将本次运算的最终结果存储到内部缓存 `_result_cache` 中，以便下次相同请求可以直接获取。
        self._cache_result(cache_key, result)

        # 返回最终的运算结果。
        return result

    def _execute_unary_op(self,
                          operation_type: str,
                          fuzznum: Fuzznum,
                          operand: Union[float, int],
                          **params: Any) -> Union[Fuzznum, bool, Dict[str, Any]]:
        """
        内部方法：执行一元运算。

        此方法封装了所有一元运算（如幂、倍数、指数、对数、逻辑补等）的执行流程。
        它包括：
            1. 缓存检查：避免重复计算。
            2. 输入验证：确保 Fuzznum 对象的有效性。
            3. 操作数准备：从 Fuzznum 实例中提取底层策略属性。
            4. 委托执行：将运算请求转发给 `OperationFactory`。
            5. 结果转换：将工厂返回的原始结果转换为 Fuzznum 对象或布尔值。
            6. 结果缓存：存储运算结果以供后续使用。

        Args:
            operation_type (str): 运算类型字符串（例如 'pow', 'not', 'exp'）。
            fuzznum (Fuzznum): 模糊数操作数。
            *params (Any): 额外的位置参数，传递给底层运算。

        Returns:
            Union[Fuzznum, bool, Dict[str, Any]]: 运算结果。
                - 对于比较运算，返回布尔值。
                - 对于其他运算，返回 Fuzznum 实例或原始字典（如果 Fuzznum 创建失败）。

        Raises:
            ValueError: 如果 Fuzznum 对象无效或结果格式不符合预期。
            Exception: 传播 `OperationFactory` 或底层运算中抛出的任何异常。
        """
        # 定义一个内部嵌套函数 `_execute`，它包含了实际的一元运算逻辑。
        # 这个函数将被传递给 `_execute_with_monitoring` 包装器，
        # 从而自动获得性能监控和异常处理的能力。
        def _execute():
            # --- 1. 验证输入 Fuzznum 对象 ---
            # 调用私有方法 `_validate_fuzznum` 对传入的 Fuzznum 对象进行验证。
            # 这会检查 Fuzznum 的 mtype 是否与当前包装器兼容，以及其内部状态是否有效。
            self._validate_fuzznum(fuzznum)

            # --- 3. 创建t-范数实例并获取策略实例 ---
            tnorm_instance = OperationTNorm(self._t_norm_type, q=fuzznum.q, **params)
            strategy = fuzznum.get_strategy_instance()

            # --- 4. 直接在策略上查找并调用运算方法 ---
            operation_method = getattr(strategy, operation_type, None)
            if not callable(operation_method):
                raise NotImplementedError(f"Operation '{operation_type}' is not implemented in "
                                          f"strategy '{strategy.__class__.__name__}'.")

            # --- 5. 执行运算 ---
            result_dict = operation_method(operand, tnorm_instance)

            # --- 6. 创建结果 ---
            # 这里调用的是 Fuzznum.create 而不是 from_dict, 更加通用
            # 您需要确保 Fuzznum.create 接受字典形式的参数
            return Fuzznum.create(fuzznum, **result_dict)

        # --- 6. 缓存检查 ---
        # 生成一个唯一的缓存键，用于标识本次运算请求。
        # 缓存键的生成考虑了运算类型、Fuzznum 实例的身份和内容，以及额外参数。
        # 注意：对于一元运算，`operand` 参数为 None。
        cache_key = self._generate_cache_key(operation_type, fuzznum, operand, *params)
        # 尝试从内部缓存 `_result_cache` 中获取结果。
        # `cache_hit` 为 True 表示命中缓存，`cached_result` 为缓存中的值。
        cache_hit, cached_result = self._get_cached_result(cache_key)

        # 如果命中缓存，则直接返回缓存的结果，避免重复计算。
        if cache_hit:
            return cached_result

        # --- 7. 执行运算并监控 ---
        # 调用 `_execute_with_monitoring` 包装器来执行 `_execute` 内部函数。
        # 这会自动处理性能统计、日志记录和异常捕获。
        result = self._execute_with_monitoring(operation_type, _execute)

        # --- 8. 缓存结果 ---
        # 将本次运算的最终结果存储到内部缓存 `_result_cache` 中，以便下次相同请求可以直接获取。
        self._cache_result(cache_key, result)

        # 返回最终的运算结果。
        return result

        # ============================= 性能监控（执行器层面） ================================

    def _update_performance_stats(self,
                                  operation_type: str,
                                  execution_time: float,
                                  success: bool):
        """
        更新内部性能统计数据。

        此方法用于记录执行器层面各项操作的性能指标，包括总操作次数、成功/失败次数、
        总执行时间以及平均执行时间。它确保统计数据在多线程环境下是线程安全的。

        Args:
            operation_type (str): 执行的操作类型标识符（例如 'add', 'subtract'）。
            execution_time (float): 本次操作的执行耗时（秒）。
            success (bool): 指示本次操作是否成功完成。
        """
        # 检查性能监控是否已启用。
        # 如果 self._performance_enabled 为 False，则直接返回，不执行任何统计更新操作。
        # 这是一个性能优化点，避免在不需要监控时进行不必要的计算。
        if not self._performance_enabled:
            return

        # 使用实例锁 self._lock 保护对共享统计数据 self._execution_stats 的访问。
        # 确保在多线程环境下，对字典的修改是原子性的，防止竞态条件和数据不一致。
        with self._lock:
            # 增加总操作次数。
            self._execution_stats['total_operations'] += 1
            # 根据 'success' 参数的值，增加成功操作次数或失败操作次数。
            if success:
                self._execution_stats['successful_operations'] += 1
            else:
                self._execution_stats['failed_operations'] += 1

            # 累加本次操作的执行时间到总执行时间中。
            self._execution_stats['total_execution_time'] += execution_time
            # 重新计算平均执行时间。
            # 这里通过除以 'total_operations' 来得到平均值。
            # 由于 'total_operations' 至少为 1，所以不会发生除以零的错误。
            self._execution_stats['avg_execution_time'] = (
                    self._execution_stats['total_execution_time'] /
                    self._execution_stats['total_operations']
            )

            # 更新特定运算类型的操作计数。
            # 如果该 operation_type 尚未在 'operation_counts' 中，则初始化为 0。
            if operation_type not in self._execution_stats['operation_counts']:
                self._execution_stats['operation_counts'][operation_type] = 0
            # 增加该 operation_type 的计数。
            self._execution_stats['operation_counts'][operation_type] += 1

    def _execute_with_monitoring(self,
                                 operation_type: str,
                                 operation_func: Callable,
                                 *args, **kwargs) -> Any:
        """
        带性能监控和日志记录的运算执行包装器。

        此方法封装了实际的运算逻辑，并在其执行前后进行计时、成功/失败状态跟踪，
        以及根据调试模式输出日志。它会自动更新执行器的性能统计数据。

        Args:
            operation_type (str): 执行的操作类型标识符。
            operation_func (callable): 实际执行运算逻辑的可调用对象（函数或方法）。
            *args: 传递给 `operation_func` 的位置参数。
            **kwargs: 传递给 `operation_func` 的关键字参数。

        Returns:
            Any: `operation_func` 执行后返回的结果。

        Raises:
            Exception: 传播 `operation_func` 执行过程中抛出的任何异常。
        """
        # 记录运算开始的时间戳。
        # 用于后续计算操作的总执行耗时。
        start_time = time.perf_counter()
        # 初始化 'success' 标志为 True。
        # 假设操作会成功完成，如果发生异常则在 except 块中将其设置为 False。
        success = True

        try:
            # 检查是否启用了调试模式。
            # 如果 self._debug_mode 为 True，则输出一条调试日志，表明当前正在执行的运算类型。
            if self._debug_mode:
                logger.debug(f"Executing {operation_type} operation")

            # 调用传入的实际运算函数 operation_func。
            # 这是执行具体运算逻辑的核心步骤，将所有位置参数和关键字参数传递给它。
            result = operation_func(*args, **kwargs)

            # 再次检查是否启用了调试模式。
            # 如果 self._debug_mode 为 True，则输出一条调试日志，表明运算已成功完成。
            if self._debug_mode:
                logger.debug(f"Successfully completed {operation_type} operation")

            # 返回运算结果。
            return result

        # 捕获在 try 块中可能发生的任何异常。
        except Exception as e:
            # 如果发生异常，将 'success' 标志设置为 False。
            success = False
            # 检查是否启用了调试模式。
            # 如果 self._debug_mode 为 True，则输出一条错误日志，表明运算失败及其原因。
            if self._debug_mode:
                logger.error(f"Failed to execute {operation_type} operation: {e}")
            # 重新抛出捕获到的异常。
            # 这是为了确保调用方能够感知到运算的失败，并进行相应的错误处理。
            raise
        # finally 块无论 try 块是否发生异常，都会被执行。
        finally:
            # 计算操作的实际执行时间。
            execution_time = time.perf_counter() - start_time
            # 调用私有辅助方法 _update_performance_stats 来更新性能统计数据。
            # 传入运算类型、执行时间以及操作是否成功。
            self._update_performance_stats(operation_type, execution_time, success)

    # ============================ 缓存管理（内部结果缓存） ===============================

    @staticmethod
    def _generate_cache_key(operation_type: str,
                            fuzznum_1: Fuzznum,
                            operand: Optional[Union[Fuzznum, float, int]] = None,
                            *params) -> str:
        """
        生成缓存键

        为 Executor 的 _result_cache 生成一个唯一的字符串键。其逻辑思路是：
        将运算类型、输入的 Fuzznum 对象的标识（类型、内存ID、策略属性）以及额外参数组合成一个字符串，
        然后计算其 MD5 哈希值作为缓存键。这确保了对于相同的运算请求和输入，能够生成一致的缓存键。

        Args:
            operation_type: 运算类型字符串（如 'add', 'gt'）。
            fuzznum_1: 第一个 Fuzznum 操作数。
            operand: 可选，第二个 Fuzznum 操作数（用于二元运算），操作数（一元运算的系数）。
            *params: 额外的运算参数。

        Returns:
            str: 用于缓存的唯一键（MD5哈希字符串）。
        """
        # 导入 hashlib 模块，用于计算哈希值。
        import hashlib

        # 将 Fuzznum 的属性字典转换为一个排序后的，可复现的字符串
        def get_stable_dict_str(fuzznum_obj: Fuzznum) -> str:
            attrs = fuzznum_obj.get_strategy_attributes_dict()
            return str(sorted(attrs.items()))

        key_parts = [
            str(sorted(operation_type)),
            str(fuzznum_1.mtype),
            get_stable_dict_str(fuzznum_1)
        ]

        # 如果存在第二个 Fuzznum 操作数（二元运算）
        if operand and isinstance(operand, Fuzznum):
            key_parts.append(get_stable_dict_str(operand))

        if operand and isinstance(operand, float):
            key_parts.append(str(operand))

        # 如果有额外参数
        if params:
            # 添加额外参数的字符串表示到键组成部分列表。
            key_parts.append(str(params))

        # 将所有键组成部分用下划线连接成一个字符串。
        key_str = '_'.join(key_parts)

        # 使用 MD5 算法计算 key_str 的哈希值，并返回十六进制字符串形式。
        return hashlib.md5(key_str.encode()).hexdigest()

    def _get_cached_result(self, cache_key: str) -> Tuple[bool, Any]:
        """
        获取缓存结果

        从 Executor 的 _result_cache 中检索指定运算请求的缓存结果。
        其逻辑思路是：如果缓存启用且缓存中存在对应键的结果，则直接返回缓存结果，避免重复计算，
        从而提高性能。同时，它会更新内部的缓存统计信息。

        Args:
            cache_key: 通过 _generate_cache_key 生成的缓存键。

        Returns:
            tuple[bool, Any]: 一个元组。
                第一个元素是布尔值，表示是否命中缓存 (True 为命中)。
                第二个元素是缓存的值 (如果命中) 或 None (如果未命中)。
        """
        # 检查当前执行器实例的缓存机制是否被禁用。
        # 如果缓存被禁用，则直接返回 False（未命中缓存）和 None。
        if not self._cache_enabled:
            return False, None

        # 获取实例锁。
        # 这是为了确保在多线程环境下，对 _result_cache 字典和 _cache_stats 字典的读取是线程安全的。
        with self._lock:
            # 增加缓存总请求数。
            self._cache_stats['total_requests'] += 1

            if cache_key in self._result_cache:
                # 如果命中缓存，增加缓存命中次数。
                # 并重新计算缓存命中率
                self._cache_stats['hits'] += 1
                self._cache_stats['hit_ratio'] = self._cache_stats['hits'] / self._cache_stats['total_requests']

                # 将被访问的条目移到末尾，标记为最近使用
                self._result_cache.move_to_end(cache_key)

                if self._debug_mode:
                    logger.debug(f"Cache hit for key: {cache_key[:16]}...")

                return True, self._result_cache[cache_key]

            # 如果未命中缓存，增加缓存未命中次数
            # 并重新计算缓存命中率
            self._cache_stats['misses'] += 1
            self._cache_stats['hit_ratio'] = self._cache_stats['hits'] / self._cache_stats['total_requests']

            return False, None

    def _cache_result(self, cache_key: str, result: Any):
        """
        缓存结果

        将运算结果存储到 OperationExecutor 的 _result_cache 中。其逻辑思路是：
        如果缓存启用，则将运算结果与对应的缓存键关联起来并存入字典，以便后续相同运算可以直接从缓存中获取。
        它还包含一个简单的缓存大小控制机制。

        Args:
            cache_key: 通过 _generate_cache_key 生成的缓存键。
            result: 要缓存的运算结果。
        """
        # 检查当前执行器实例的缓存机制是否被禁用。
        # 如果缓存被禁用，则直接返回，不执行任何缓存操作。
        if not self._cache_enabled:
            return

        # 获取实例锁。
        # 这是为了确保在多线程环境下，对 _result_cache 字典的写入是线程安全的。
        with self._lock:
            # 将运算结果存储到 _result_cache 字典中，以 cache_key 为键。
            self._result_cache[cache_key] = result

            # --- 缓存大小控制 ---
            # 从配置中获取最大缓存大小限制（默认为256）。
            max_cache_size = getattr(self._config, 'EXECUTOR_CACHE_SIZE', 256)
            # 检查当前缓存大小是否超过了最大限制。
            if len(self._result_cache) > max_cache_size:

                oldest_key, _ = self._result_cache.popitem(last=False)
                # 如果处于调试模式，则输出一条缓存大小限制已达到并移除旧项的调试日志。
                if self._debug_mode:
                    logger.debug(f"Cache size limit reached, removed LRU item with key: {oldest_key[:16]}...")

    # ========================== 缓存管理（外部接口） ============================

    def enable_cache(self) -> None:
        """启用属性访问缓存。

        此方法激活 `OperationExecutor` 实例内部的运算结果缓存和 Fuzznum 实例缓存机制。
        当缓存启用时，对相同运算请求的后续访问将首先尝试从缓存中获取结果，从而提高性能。

        Args:
            None.

        Returns:
            None.
        """
        # 使用实例锁 self._lock 保护对 _cache_enabled 标志的修改。
        # 确保在多线程环境下，修改缓存启用状态的操作是线程安全的。
        with self._lock:
            # 将 _cache_enabled 标志设置为 True，表示缓存已启用。
            self._cache_enabled = True
            # 检查是否启用了调试模式。
            # 如果 self._debug_mode 为 True，则输出一条调试日志，表明缓存已启用。
            if self._debug_mode:
                logger.debug("Cache enabled")

    def disable_cache(self) -> None:
        """禁用属性访问缓存并清空现有缓存。

        此方法停用 `OperationExecutor` 实例内部的运算结果缓存和 Fuzznum 实例缓存机制。
        同时，为了避免使用过时的缓存数据，它会立即清空所有已缓存的属性值。
        禁用缓存会强制后续所有属性访问都进行委托查找，可能会增加性能开销，
        但它保证了总是获取到属性的最新状态。

        Args:
            None.

        Returns:
            None.
        """
        # 使用实例锁 self._lock 保护对 _cache_enabled 标志和缓存清空操作的修改。
        # 确保在多线程环境下，修改缓存启用状态和清空缓存的操作是线程安全的。
        with self._lock:
            # 将 _cache_enabled 标志设置为 False，表示缓存已禁用。
            self._cache_enabled = False
            # 调用 clear_cache() 方法，清空所有已缓存的运算结果和 Fuzznum 实例。
            # 这样做是为了确保在禁用缓存后，不会有任何过时的数据留在内存中，并且后续访问会强制刷新。
            self._result_cache.clear()
            self._fuzznum_cache.clear()
            # 检查是否启用了调试模式。
            # 如果 self._debug_mode 为 True，则输出一条调试日志，表明缓存已禁用并清空。
            if self._debug_mode:
                logger.debug("Cache disabled and cleared")

    def clear_cache(self) -> None:
        """手动清空所有内部缓存和缓存统计数据。

        此方法用于强制清空 `OperationExecutor` 实例内部的所有已缓存运算结果、
        Fuzznum 实例以及重置缓存命中率等统计数据。无论缓存当前是启用还是禁用状态，
        调用此方法都会移除所有缓存条目。

        清空缓存后，后续对属性的首次访问将再次触发委托查找和可能的重新计算。

        Args:
            None.

        Returns:
            None.
        """
        # 使用实例锁 self._lock 保护对缓存和统计数据清空操作的修改。
        # 确保在多线程环境下，清空操作是线程安全的。
        with self._lock:
            # 清空 _result_cache 字典，移除所有缓存的运算结果。
            self._result_cache.clear()
            # 清空 _fuzznum_cache 字典，移除所有缓存的 Fuzznum 实例。
            self._fuzznum_cache.clear()
            # 重置缓存统计数据，包括命中次数、未命中次数、总请求数和命中率。
            self._cache_stats = {
                'hits': 0,
                'misses': 0,
                'total_requests': 0,
                'hit_ratio': 0.0
            }
            # 检查是否启用了调试模式。
            # 如果 self._debug_mode 为 True，则输出一条调试日志，表明缓存已清空。
            if self._debug_mode:
                logger.debug("Cache cleared")

    @contextmanager
    def cache_disabled(self):
        """临时禁用缓存的上下文管理器。

        此上下文管理器允许用户在特定的代码块中临时禁用 `OperationExecutor`
        实例的属性访问缓存。在进入 `with` 语句块时，缓存会被禁用并清空；
        在退出 `with` 语句块时（无论正常退出还是发生异常），缓存会被恢复
        到进入之前的状态。

        这对于执行一次性操作，需要保证获取最新数据，但又不想永久改变缓存状态
        的场景非常有用。

        Yields:
            None: 上下文管理器在 `with` 语句块中不产生任何值。

        Examples:
            >>> # 假设创建了两个模糊数 fuzznum_a, fuzznum_b
            >>> fuzznum_a, fuzznum_b = Fuzznum(), Fuzznum()
            >>> executor = Executor()
            >>> executor.enable_cache()
            >>> # 第一次运算会缓存结果
            >>> result1 = executor.addition(fuzznum_a, fuzznum_b)
            >>> # 模拟底层数据变化，但缓存未更新
            >>> # fuzznum_a.md = 0.9 # (假设 Fuzznum 允许直接修改)
            >>>
            >>> # 在此块内，缓存被禁用，会强制重新计算最新结果
            >>> with executor.cache_disabled():
            ...     result_latest = executor.addition(fuzznum_a, fuzznum_b)
            ...     print(f"Latest result (cache disabled): {result_latest}")
            >>>
            >>> # 退出块后，缓存恢复到原始状态（启用），再次访问可能会得到旧的缓存值
            >>> result_cached = executor.addition(fuzznum_a, fuzznum_b)
            >>> print(f"Result after cache restored: {result_cached}")
        """
        try:
            # 尝试安全地获取当前缓存的启用状态。
            # 使用 `object.__getattribute__` 是为了避免在初始化阶段 _cache_enabled 属性
            # 可能尚未完全设置时，触发 AttributeError。
            original_state = object.__getattribute__(self, '_cache_enabled')
        except AttributeError:
            # 如果 `_cache_enabled` 属性不存在（例如，在非常早期的初始化阶段），
            # 则默认其为 True（即缓存是启用的），这样在恢复时也能有一个合理的状态。
            original_state = True

        try:
            # 进入 `with` 语句块时，调用 `disable_cache()` 方法禁用并清空缓存。
            # 这使得在 `with` 语句块内部的所有运算都不会使用缓存，从而强制重新计算。
            self.disable_cache()
            # `yield` 关键字将控制权交给 `with` 语句块内部的代码。
            # 当 `with` 块执行完毕后，控制权会回到 `finally` 块。
            yield
        finally:
            # `finally` 块无论 `with` 语句块是正常完成还是因为异常退出，都会执行。
            # 在这里，将 `_cache_enabled` 属性恢复到进入上下文管理器之前的原始状态。
            # 同样使用 `object.__setattr__` 确保安全设置，避免触发自定义的 `__setattr__` 逻辑。
            object.__setattr__(self, '_cache_enabled', original_state)

    # ========================== 性能统计（外部接口） ============================

    def get_performance_stats(self) -> Dict[str, Any]:
        """
        获取性能统计信息。

        Notes:
            此方法返回 `Executor` 实例的综合性能统计数据，包括：
                - 运算执行统计（总操作数、成功/失败数、平均时间等）。
                - 缓存使用统计（命中/未命中次数、命中率）。
                - Fuzznum 验证统计（总验证数、失败数、错误详情）。
                - 当前活跃封装器及其关联策略和模板的统计信息。

        Returns:
            Dict[str, Any]: 包含详细性能统计信息的字典。
        """
        # 使用实例锁 self._lock 保护对所有内部统计数据字典的访问。
        # 确保在多线程环境下，读取这些数据是线程安全的，防止在读取过程中数据被其他线程修改导致不一致。
        with self._lock:
            # 返回一个字典，其中包含了从各个内部统计字典复制过来的数据。
            # 使用 `.copy()` 是为了返回这些字典的副本，防止外部代码直接修改内部状态。
            return {
                't_norm_type': self._t_norm_type,  # 当前运算器的t-范数名称。
                'creation_time': self._creation_time,  # 执行器实例的创建时间戳。
                'age_seconds': time.perf_counter() - self._creation_time,  # 执行器实例自创建以来的存活时间（秒）。
                'execution_stats': self._execution_stats.copy(),  # 运算执行的统计数据。
                'cache_stats': self._cache_stats.copy(),  # 缓存使用情况的统计数据。
                'validation_stats': self._validation_stats.copy(),  # Fuzznum 验证的统计数据。
            }

    def reset_performance_stats(self) -> None:
        """
        重置所有性能统计和缓存统计数据。

        此方法将 `OperationExecutor` 实例内部的所有运算执行统计、
        缓存统计和 Fuzznum 验证统计重置为它们的初始状态（例如，计数器归零，
        列表清空）。这对于开始新的性能测量周期或清理历史数据非常有用。

        Args:
            None.

        Returns:
            None.
        """
        # 使用实例锁 self._lock 保护对所有内部统计数据字典的修改。
        # 确保在多线程环境下，重置操作是线程安全的。
        with self._lock:
            # 重置运算执行统计字典。
            self._execution_stats = {
                'total_operations': 0,
                'successful_operations': 0,
                'failed_operations': 0,
                'total_execution_time': 0.0,
                'avg_execution_time': 0.0,
                'operation_counts': {}  # 清空特定运算类型的计数。
            }
            # 重置缓存统计字典。
            self._cache_stats = {
                'hits': 0,
                'misses': 0,
                'total_requests': 0,
                'hit_ratio': 0.0
            }
            # 重置 Fuzznum 验证统计字典。
            self._validation_stats = {
                'total_validations': 0,
                'failed_validations': 0,
                'validation_errors': []  # 清空所有验证错误记录。
            }
            # 检查是否启用了调试模式。
            # 如果 self._debug_mode 为 True，则输出一条调试日志，表明性能统计已重置。
            if self._debug_mode:
                logger.debug("Performance statistics reset")

    # ======================== 运算执行（公共接口）=========================
    # ----------------------------- 二元运算接口 -----------------------------
    def addition(self, fuzznum_1: Fuzznum, fuzznum_2: Fuzznum, **params: Any) -> Union[Fuzznum, Dict[str, Any]]:
        """执行两个模糊数的加法运算。

        此方法将 `fuzznum_1` 和 `fuzznum_2` 进行加法运算。

        Args:
            fuzznum_1 (Fuzznum): 第一个模糊数操作数。
            fuzznum_2 (Fuzznum): 第二个模糊数操作数。
            **params (Any): 额外的位置参数，传递给底层加法运算。

        Returns:
            Union[Fuzznum, Dict[str, Any]]: 加法运算的结果。
                通常返回一个新的 `Fuzznum` 实例；如果 Fuzznum 创建失败，则返回原始字典。

        Raises:
            ValueError: 如果输入模糊数无效或类型不兼容。
            Exception: 传播底层运算中可能抛出的任何异常。
        """
        # 委托给内部的 _execute_binary_op 方法，指定运算类型为 'add'。
        return self._execute_binary_op('add', fuzznum_1, fuzznum_2, **params)

    def subtract(self, fuzznum_1: Fuzznum, fuzznum_2: Fuzznum, **params: Any) -> Union[Fuzznum, Dict[str, Any]]:
        """执行两个模糊数的减法运算。

        此方法将 `fuzznum_1` 减去 `fuzznum_2`。

        Args:
            fuzznum_1 (Fuzznum): 第一个模糊数操作数（被减数）。
            fuzznum_2 (Fuzznum): 第二个模糊数操作数（减数）。
            **params (Any): 额外的位置参数，传递给底层减法运算。

        Returns:
            Union[Fuzznum, Dict[str, Any]]: 减法运算的结果。
                通常返回一个新的 `Fuzznum` 实例；如果 Fuzznum 创建失败，则返回原始字典。

        Raises:
            ValueError: 如果输入模糊数无效或类型不兼容。
            Exception: 传播底层运算中可能抛出的任何异常。
        """
        # 委托给内部的 _execute_binary_op 方法，指定运算类型为 'sub'。
        return self._execute_binary_op('sub', fuzznum_1, fuzznum_2, **params)

    def multiply(self, fuzznum_1: Fuzznum, fuzznum_2: Fuzznum, **params: Any) -> Union[Fuzznum, Dict[str, Any]]:
        """执行两个模糊数的乘法运算。

        此方法将 `fuzznum_1` 和 `fuzznum_2` 进行乘法运算。

        Args:
            fuzznum_1 (Fuzznum): 第一个模糊数操作数。
            fuzznum_2 (Fuzznum): 第二个模糊数操作数。
            *params (Any): 额外的位置参数，传递给底层乘法运算。

        Returns:
            Union[Fuzznum, Dict[str, Any]]: 乘法运算的结果。
                通常返回一个新的 `Fuzznum` 实例；如果 Fuzznum 创建失败，则返回原始字典。

        Raises:
            ValueError: 如果输入模糊数无效或类型不兼容。
            Exception: 传播底层运算中可能抛出的任何异常。
        """
        # 委托给内部的 _execute_binary_op 方法，指定运算类型为 'mul'。
        return self._execute_binary_op('mul', fuzznum_1, fuzznum_2, **params)

    def divide(self, fuzznum_1: Fuzznum, fuzznum_2: Fuzznum, **params: Any) -> Union[Fuzznum, Dict[str, Any]]:
        """执行两个模糊数的除法运算。

        此方法将 `fuzznum_1` 除以 `fuzznum_2`。

        Args:
            fuzznum_1 (Fuzznum): 第一个模糊数操作数（被除数）。
            fuzznum_2 (Fuzznum): 第二个模糊数操作数（除数）。
            *params (Any): 额外的位置参数，传递给底层除法运算。

        Returns:
            Union[Fuzznum, Dict[str, Any]]: 除法运算的结果。
                通常返回一个新的 `Fuzznum` 实例；如果 Fuzznum 创建失败，则返回原始字典。

        Raises:
            ValueError: 如果输入模糊数无效、类型不兼容或除数为零。
            Exception: 传播底层运算中可能抛出的任何异常。
        """
        # 委托给内部的 _execute_binary_op 方法，指定运算类型为 'div'。
        return self._execute_binary_op('div', fuzznum_1, fuzznum_2, **params)

    # ----------------------------- 一元运算接口 -----------------------------

    def power(self, fuzznum: Fuzznum, operand: Union[int, float], **params: Any) -> Union[Fuzznum, Dict[str, Any]]:
        """执行模糊数的幂运算。

        此方法将 `fuzznum` 进行幂运算（例如，`fuzznum` 的 `p` 次幂）。

        Args:
            fuzznum (Fuzznum): 模糊数操作数。
            operand: 一元运算操作数
            **params (Any): 额外的位置参数，通常包含幂次。

        Returns:
            Union[Fuzznum, Dict[str, Any]]: 幂运算的结果。
                通常返回一个新的 `Fuzznum` 实例；如果 Fuzznum 创建失败，则返回原始字典。

        Raises:
            ValueError: 如果输入模糊数无效。
            Exception: 传播底层运算中可能抛出的任何异常。
        """
        # 委托给内部的 _execute_unary_op 方法，指定运算类型为 'pow'。
        return self._execute_unary_op('pow', fuzznum, operand, **params)

    def times(self, fuzznum: Fuzznum, operand: Union[int, float], **params: Any) -> Union[Fuzznum, Dict[str, Any]]:
        """执行模糊数的倍数运算。

        此方法将 `fuzznum` 乘以一个倍数（例如，`p` 乘以 `fuzznum`）。

        Args:
            fuzznum (Fuzznum): 模糊数操作数。
            operand: 一元运算操作数
            **params (Any): 额外的位置参数，通常包含倍数。

        Returns:
            Union[Fuzznum, Dict[str, Any]]: 倍数运算的结果。
                通常返回一个新的 `Fuzznum` 实例；如果 Fuzznum 创建失败，则返回原始字典。

        Raises:
            ValueError: 如果输入模糊数无效。
            Exception: 传播底层运算中可能抛出的任何异常。
        """
        # 委托给内部的 _execute_unary_op 方法，指定运算类型为 'tim'。
        return self._execute_unary_op('tim', fuzznum, operand, **params)

    def exponential(self, fuzznum: Fuzznum, operand: Union[int, float], **params: Any) -> Union[Fuzznum, Dict[str, Any]]:
        """执行模糊数的指数运算。

        此方法将 `e`（自然对数的底数）或指定底数提升到 `fuzznum` 的幂。

        Args:
            fuzznum (Fuzznum): 模糊数操作数（指数）。
            operand: 一元运算操作数
            *params (Any): 额外的位置参数，可选地包含指数运算的底数。

        Returns:
            Union[Fuzznum, Dict[str, Any]]: 指数运算的结果。
                通常返回一个新的 `Fuzznum` 实例；如果 Fuzznum 创建失败，则返回原始字典。

        Raises:
            ValueError: 如果输入模糊数无效。
            Exception: 传播底层运算中可能抛出的任何异常。
        """
        # 委托给内部的 _execute_unary_op 方法，指定运算类型为 'exp'。
        return self._execute_unary_op('exp', fuzznum, operand, **params)

    def logarithmic(self, fuzznum: Fuzznum, operand: Union[int, float], **params: Any) -> Union[Fuzznum, Dict[str, Any]]:
        """执行模糊数的对数运算。

        此方法计算 `fuzznum` 的对数。

        Args:
            fuzznum (Fuzznum): 模糊数操作数。
            operand: 一元运算操作数
            **params (Any): 额外的位置参数，可选地包含对数运算的底数。

        Returns:
            Union[Fuzznum, Dict[str, Any]]: 对数运算的结果。
                通常返回一个新的 `Fuzznum` 实例；如果 Fuzznum 创建失败，则返回原始字典。

        Raises:
            ValueError: 如果输入模糊数无效或底数不合法。
            Exception: 传播底层运算中可能抛出的任何异常。
        """
        # 委托给内部的 _execute_unary_op 方法，指定运算类型为 'log'。
        return self._execute_unary_op('log', fuzznum, operand, **params)

    # ----------------------------- 比较运算接口 -----------------------------

    def greater_than(self, fuzznum_1: Fuzznum, fuzznum_2: Fuzznum, **params: Any) -> bool:
        """判断第一个模糊数是否严格大于第二个模糊数。

        Args:
            fuzznum_1 (Fuzznum): 第一个模糊数操作数。
            fuzznum_2 (Fuzznum): 第二个模糊数操作数。
            *params (Any): 额外的位置参数，传递给底层比较运算。

        Returns:
            bool: 如果 `fuzznum_1` 大于 `fuzznum_2` 则返回 True，否则返回 False。

        Raises:
            ValueError: 如果输入模糊数无效或类型不兼容。
            Exception: 传播底层运算中可能抛出的任何异常。
        """
        # 委托给内部的 _execute_binary_op 方法，指定运算类型为 'gt'。
        return self._execute_binary_op('gt', fuzznum_1, fuzznum_2, **params)

    def less_than(self, fuzznum_1: Fuzznum, fuzznum_2: Fuzznum, **params: Any) -> bool:
        """判断第一个模糊数是否严格小于第二个模糊数。

        Args:
            fuzznum_1 (Fuzznum): 第一个模糊数操作数。
            fuzznum_2 (Fuzznum): 第二个模糊数操作数。
            **params (Any): 额外的位置参数，传递给底层比较运算。

        Returns:
            bool: 如果 `fuzznum_1` 小于 `fuzznum_2` 则返回 True，否则返回 False。

        Raises:
            ValueError: 如果输入模糊数无效或类型不兼容。
            Exception: 传播底层运算中可能抛出的任何异常。
        """
        # 委托给内部的 _execute_binary_op 方法，指定运算类型为 'lt'。
        return self._execute_binary_op('lt', fuzznum_1, fuzznum_2, **params)

    def equal(self, fuzznum_1: Fuzznum, fuzznum_2: Fuzznum, **params: Any) -> bool:
        """判断两个模糊数是否相等。

        Args:
            fuzznum_1 (Fuzznum): 第一个模糊数操作数。
            fuzznum_2 (Fuzznum): 第二个模糊数操作数。
            **params (Any): 额外的位置参数，传递给底层比较运算。

        Returns:
            bool: 如果 `fuzznum_1` 等于 `fuzznum_2` 则返回 True，否则返回 False。

        Raises:
            ValueError: 如果输入模糊数无效或类型不兼容。
            Exception: 传播底层运算中可能抛出的任何异常。
        """
        # 委托给内部的 _execute_binary_op 方法，指定运算类型为 'eq'。
        return self._execute_binary_op('eq', fuzznum_1, fuzznum_2, **params)

    def greater_equal(self, fuzznum_1: Fuzznum, fuzznum_2: Fuzznum, **params: Any) -> bool:
        """判断第一个模糊数是否大于或等于第二个模糊数。

        Args:
            fuzznum_1 (Fuzznum): 第一个模糊数操作数。
            fuzznum_2 (Fuzznum): 第二个模糊数操作数。
            *params (Any): 额外的位置参数，传递给底层比较运算。

        Returns:
            bool: 如果 `fuzznum_1` 大于或等于 `fuzznum_2` 则返回 True，否则返回 False。

        Raises:
            ValueError: 如果输入模糊数无效或类型不兼容。
            Exception: 传播底层运算中可能抛出的任何异常。
        """
        # 委托给内部的 _execute_binary_op 方法，指定运算类型为 'ge'。
        return self._execute_binary_op('ge', fuzznum_1, fuzznum_2, **params)

    def less_equal(self, fuzznum_1: Fuzznum, fuzznum_2: Fuzznum, **params: Any) -> bool:
        """判断第一个模糊数是否小于或等于第二个模糊数。

        Args:
            fuzznum_1 (Fuzznum): 第一个模糊数操作数。
            fuzznum_2 (Fuzznum): 第二个模糊数操作数。
            **params (Any): 额外的位置参数，传递给底层比较运算。

        Returns:
            bool: 如果 `fuzznum_1` 小于或等于 `fuzznum_2` 则返回 True，否则返回 False。

        Raises:
            ValueError: 如果输入模糊数无效或类型不兼容。
            Exception: 传播底层运算中可能抛出的任何异常。
        """
        # 委托给内部的 _execute_binary_op 方法，指定运算类型为 'le'。
        return self._execute_binary_op('le', fuzznum_1, fuzznum_2, **params)

    def not_equal(self, fuzznum_1: Fuzznum, fuzznum_2: Fuzznum, **params: Any) -> bool:
        """判断两个模糊数是否不相等。

        Args:
            fuzznum_1 (Fuzznum): 第一个模糊数操作数。
            fuzznum_2 (Fuzznum): 第二个模糊数操作数。
            **params (Any): 额外的位置参数，传递给底层比较运算。

        Returns:
            bool: 如果 `fuzznum_1` 不等于 `fuzznum_2` 则返回 True，否则返回 False。

        Raises:
            ValueError: 如果输入模糊数无效或类型不兼容。
            Exception: 传播底层运算中可能抛出的任何异常。
        """
        # 委托给内部的 _execute_binary_op 方法，指定运算类型为 'ne'。
        return self._execute_binary_op('ne', fuzznum_1, fuzznum_2, **params)

    # ----------------------------- 逻辑运算接口 -----------------------------

    def intersection(self, fuzznum_1: Fuzznum, fuzznum_2: Fuzznum, **params: Any) -> Union[Fuzznum, Dict[str, Any]]:
        """执行两个模糊数的逻辑交（AND）运算。

        Args:
            fuzznum_1 (Fuzznum): 第一个模糊数操作数。
            fuzznum_2 (Fuzznum): 第二个模糊数操作数。
            **params (Any): 额外的位置参数，传递给底层逻辑交运算。

        Returns:
            Union[Fuzznum, Dict[str, Any]]: 逻辑交运算的结果。
                通常返回一个新的 `Fuzznum` 实例；如果 Fuzznum 创建失败，则返回原始字典。

        Raises:
            ValueError: 如果输入模糊数无效或类型不兼容。
            Exception: 传播底层运算中可能抛出的任何异常。
        """
        # 委托给内部的 _execute_binary_op 方法，指定运算类型为 'and'。
        return self._execute_binary_op('and', fuzznum_1, fuzznum_2, **params)

    def union(self, fuzznum_1: Fuzznum, fuzznum_2: Fuzznum, **params: Any) -> Union[Fuzznum, Dict[str, Any]]:
        """执行两个模糊数的逻辑并（OR）运算。

        Args:
            fuzznum_1 (Fuzznum): 第一个模糊数操作数。
            fuzznum_2 (Fuzznum): 第二个模糊数操作数。
            **params (Any): 额外的位置参数，传递给底层逻辑并运算。

        Returns:
            Union[Fuzznum, Dict[str, Any]]: 逻辑并运算的结果。
                通常返回一个新的 `Fuzznum` 实例；如果 Fuzznum 创建失败，则返回原始字典。

        Raises:
            ValueError: 如果输入模糊数无效或类型不兼容。
            Exception: 传播底层运算中可能抛出的任何异常。
        """
        # 委托给内部的 _execute_binary_op 方法，指定运算类型为 'or'。
        return self._execute_binary_op('or', fuzznum_1, fuzznum_2, **params)

    def complement(self, fuzznum: Fuzznum, **params: Any) -> Union[Fuzznum, Dict[str, Any]]:
        """执行模糊数的逻辑补（NOT）运算。

        Args:
            fuzznum (Fuzznum): 模糊数操作数。
            **params (Any): 额外的位置参数，传递给底层逻辑补运算。

        Returns:
            Union[Fuzznum, Dict[str, Any]]: 逻辑补运算的结果。
                通常返回一个新的 `Fuzznum` 实例；如果 Fuzznum 创建失败，则返回原始字典。

        Raises:
            ValueError: 如果输入模糊数无效。
            Exception: 传播底层运算中可能抛出的任何异常。
        """
        # 委托给内部的 _execute_binary_op 方法，指定运算类型为 'not'。
        return self._execute_binary_op('not', fuzznum, **params)

    def implication(self, fuzznum_1: Fuzznum, fuzznum_2: Fuzznum, **params: Any) -> Union[Fuzznum, Dict[str, Any]]:
        """执行两个模糊数的逻辑蕴含（IMPLIES）运算。

        Args:
            fuzznum_1 (Fuzznum): 第一个模糊数操作数（前提）。
            fuzznum_2 (Fuzznum): 第二个模糊数操作数（结论）。
            **params (Any): 额外的位置参数，传递给底层逻辑蕴含运算。

        Returns:
            Union[Fuzznum, Dict[str, Any]]: 逻辑蕴含运算的结果。
                通常返回一个新的 `Fuzznum` 实例；如果 Fuzznum 创建失败，则返回原始字典。

        Raises:
            ValueError: 如果输入模糊数无效或类型不兼容。
            Exception: 传播底层运算中可能抛出的任何异常。
        """
        # 委托给内部的 _execute_binary_op 方法，指定运算类型为 'impl'。
        return self._execute_binary_op('impl', fuzznum_1, fuzznum_2, **params)

    def equivalence(self, fuzznum_1: Fuzznum, fuzznum_2: Fuzznum, **params: Any) -> Union[Fuzznum, Dict[str, Any]]:
        """执行两个模糊数的逻辑等价（EQUIVALENCE）运算。

        Args:
            fuzznum_1 (Fuzznum): 第一个模糊数操作数。
            fuzznum_2 (Fuzznum): 第二个模糊数操作数。
            **params (Any): 额外的位置参数，传递给底层逻辑等价运算。

        Returns:
            Union[Fuzznum, Dict[str, Any]]: 逻辑等价运算的结果。
                通常返回一个新的 `Fuzznum` 实例；如果 Fuzznum 创建失败，则返回原始字典。

        Raises:
            ValueError: 如果输入模糊数无效或类型不兼容。
            Exception: 传播底层运算中可能抛出的任何异常。
        """
        # 委托给内部的 _execute_binary_op 方法，指定运算类型为 'equiv'。
        return self._execute_binary_op('equiv', fuzznum_1, fuzznum_2, **params)

    def difference(self, fuzznum_1: Fuzznum, fuzznum_2: Fuzznum, **params: Any) -> Union[Fuzznum, Dict[str, Any]]:
        """执行两个模糊数的逻辑差（DIFFERENCE）运算。

        Args:
            fuzznum_1 (Fuzznum): 第一个模糊数操作数。
            fuzznum_2 (Fuzznum): 第二个模糊数操作数。
            **params (Any): 额外的位置参数，传递给底层逻辑差运算。

        Returns:
            Union[Fuzznum, Dict[str, Any]]: 逻辑差运算的结果。
                通常返回一个新的 `Fuzznum` 实例；如果 Fuzznum 创建失败，则返回原始字典。

        Raises:
            ValueError: 如果输入模糊数无效或类型不兼容。
            Exception: 传播底层运算中可能抛出的任何异常。
        """
        # 委托给内部的 _execute_binary_op 方法，指定运算类型为 'diff'。
        return self._execute_binary_op('diff', fuzznum_1, fuzznum_2, **params)

    def symmetric_difference(self,
                             fuzznum_1: Fuzznum,
                             fuzznum_2: Fuzznum,
                             **params: Any) -> Union[Fuzznum, Dict[str, Any]]:
        """执行两个模糊数的逻辑对称差（SYMMETRIC DIFFERENCE）运算。

        Args:
            fuzznum_1 (Fuzznum): 第一个模糊数操作数。
            fuzznum_2 (Fuzznum): 第二个模糊数操作数。
            **params (Any): 额外的位置参数，传递给底层逻辑对称差运算。

        Returns:
            Union[Fuzznum, Dict[str, Any]]: 逻辑对称差运算的结果。
                通常返回一个新的 `Fuzznum` 实例；如果 Fuzznum 创建失败，则返回原始字典。

        Raises:
            ValueError: 如果输入模糊数无效或类型不兼容。
            Exception: 传播底层运算中可能抛出的任何异常。
        """
        # 委托给内部的 _execute_binary_op 方法，指定运算类型为 'symdiff'。
        return self._execute_binary_op('symdiff', fuzznum_1, fuzznum_2, **params)

    # ======================== 批量运算接口 ============================

    def batch_operation(self,
                        operation_type: str,
                        fuzznums: List[Fuzznum],
                        **params: Any) -> List[Union[Fuzznum, bool, Dict[str, Any]]]:
        """批量执行运算。

        此方法对一个 `Fuzznum` 对象列表执行指定类型的批量运算。
        它支持一元运算（对列表中的每个 `Fuzznum` 独立执行）和
        二元运算（对列表中相邻的 `Fuzznum` 对执行）。
        它的逻辑思路是：根据传入的 operation_type 判断是执行一元运算还是二元运算。
        对于一元运算，它会独立地作用于列表中的每个 Fuzznum；对于二元运算，它通常会作用于列表
        中相邻的 Fuzznum 对。整个过程会收集每个运算的结果，并能捕获单个运算的错误，使得批量操作更加健壮。

        Args:
            operation_type (str): 要执行的运算类型字符串（例如 'add', 'pow', 'not'）。
            fuzznums (List[Fuzznum]): 参与运算的 `Fuzznum` 对象列表。
            **params (Any): 额外的位置参数，传递给底层运算。

        Returns:
            List[Union[Fuzznum, bool, Dict[str, Any]]]: 运算结果列表。
                列表中每个元素是对应运算的结果，可以是 `Fuzznum` 实例、布尔值（比较运算）
                或包含错误信息的字典（如果某个运算失败）。

        Raises:
            ValueError: 如果 `fuzznums` 列表为空。
            Exception: 传播底层运算中可能抛出的任何异常。
        """
        # 如果输入的 `fuzznums` 列表为空，则直接返回一个空列表。
        # 避免后续处理空列表的逻辑。
        if not fuzznums:
            return []

        # 初始化一个空列表，用于存储所有运算的结果。
        results = []

        # 遍历 `fuzznums` 列表，使用 `enumerate` 同时获取索引 `i` 和 `fuzznum` 对象。
        for i, fuzznum in enumerate(fuzznums):
            try:
                # 判断当前操作是属于一元运算还是二元运算。
                # 'pow', 'tim', 'exp', 'log', 'not' 是预定义的一元运算类型。
                if operation_type in ['pow', 'tim', 'exp', 'log', 'not']:
                    # 如果是已知的一元运算类型，则调用私有方法 `_execute_unary_operation` 执行运算。
                    # `fuzznum` 是当前操作数，`*params` 是额外参数。
                    result = self._execute_unary_op(operation_type, fuzznum, **params)
                # 如果不是一元运算，则尝试作为二元运算处理。
                # 二元运算需要两个操作数，通常是当前 `fuzznum` 和列表中的下一个 `fuzznum`。
                elif i + 1 < len(fuzznums):
                    # 确保列表中还有下一个元素可用于二元运算。
                    # 调用私有方法 `_execute_binary_operation` 执行运算。
                    # `fuzznum` 是第一个操作数，`fuzznums[i + 1]` 是第二个操作数。
                    result = self._execute_binary_op(operation_type, fuzznum, fuzznums[i + 1], **params)
                else:
                    # 如果是列表中的最后一个元素，且当前操作是二元运算，
                    # 则无法找到第二个操作数，跳出循环。
                    break

                # 将当前运算的结果添加到 `results` 列表中。
                results.append(result)

            # 捕获在单个运算过程中可能发生的任何异常。
            except Exception as e:
                # 检查是否启用了调试模式。
                # 如果 self._debug_mode 为 True，则输出一条错误日志，表明哪个模糊数操作失败。
                if self._debug_mode:
                    logger.error(f"Batch operation failed for fuzznum {i}: {e}")
                # 将包含错误信息和索引的字典添加到 `results` 列表中。
                # 这样即使某个运算失败，整个批量操作也能继续，并且结果中会包含失败的记录。
                results.append({'error': str(e), 'index': i})

        # 返回所有运算结果的列表。
        return results

    # ============================= 链式运算接口 ================================

    def chain_operation(self,
                        operation_types: List[str],
                        fuzznums: List[Fuzznum],
                        params_list: Optional[List[Dict[str, Any]]] = None,
                        ) -> Union[Fuzznum, bool, Dict[str, Any]]:
        """执行链式运算。

        此方法按顺序执行一系列运算。前一个运算的结果将作为后一个运算的输入。
        支持一元和二元运算的混合链式调用。它的逻辑思路是：通过一个内部函数 _execute_chain 迭代地执行每个操作，
        并根据操作类型（一元或二元）从 fuzznums 列表中获取相应的操作数。整个链式执行过程被
        _execute_with_monitoring 包装，以实现性能跟踪和统一的错误处理。

        Args:
            operation_types (List[str]): 运算类型字符串列表，定义链中每个步骤的运算。
            fuzznums (List[Fuzznum]): 参与运算的 `Fuzznum` 对象列表。
                                      第一个 `Fuzznum` 是链的起始输入；
                                      后续的 `Fuzznum` 用于二元运算的第二个操作数。
            params_list (Optional[List[List[Any]]]): 可选的参数列表，
                                                      其中每个子列表对应 `operation_types` 中
                                                      一个运算的额外参数。如果为 None，则默认为空列表。

        Returns:
            Union[Fuzznum, bool, Dict[str, Any]]: 链式运算的最终结果。
                可以是 `Fuzznum` 实例、布尔值（如果链的最后一个操作是比较运算）
                或包含错误信息的字典（如果 Fuzznum 创建失败）。

        Raises:
            ValueError: 如果输入列表为空、长度不匹配或链式运算中间结果类型不兼容。
            Exception: 传播底层运算中可能抛出的任何异常。
        """
        # --- 输入参数校验 ---
        # 检查 `fuzznums` 列表是否为空。
        if not fuzznums:
            raise ValueError("Fuzznums list cannot be empty for chain operation.")
        # 检查 `operation_types` 列表是否为空。
        if not operation_types:
            raise ValueError("Operation types list cannot be empty for chain operation.")

        # 如果 `params_list` 为 None，则将其初始化为一个与 `operation_types` 长度相同的空列表的列表。
        if params_list is None:
            params_list = [[] for _ in operation_types]
        # 检查 `operation_types` 和 `params_list` 的长度是否匹配。
        # 确保每个操作都有对应的参数列表。
        if len(operation_types) != len(params_list):
            raise ValueError("Length of 'operation_types' must match length of 'params_list'.")

        # 定义一个内部嵌套函数 `_execute_chain`，它包含了链式运算的实际逻辑。
        # 这个函数将被传递给 `_execute_with_monitoring` 包装器，
        # 从而自动获得性能监控和异常处理的能力。
        def _execute_chain():
            # 初始化 `current_result` 为链式运算的第一个输入 `Fuzznum`。
            current_result = fuzznums[0]
            # 初始化 `fuzznum_idx` 为 0，用于跟踪 `fuzznums` 列表中当前使用的索引。
            fuzznum_idx = 0

            # 定义二元运算类型集合，用于判断操作是二元还是其他。
            binary_ops = {'add', 'sub', 'mul', 'div', 'and', 'or', 'impl', 'equiv', 'diff', 'symdiff',
                          'gt', 'lt', 'eq', 'ge', 'le', 'ne'}
            # 定义一元运算类型集合。
            unary_ops = {'pow', 'tim', 'exp', 'log', 'not'}

            # 遍历 `operation_types` 列表，执行链中的每一个操作。
            for i, op_type in enumerate(operation_types):
                # 获取当前操作对应的额外参数列表。
                op_params = params_list[i]

                # 关键检查：确保 `current_result` 在进行下一个操作之前仍然是一个 `Fuzznum` 对象。
                # 如果前一个操作是比较运算（返回布尔值），那么 `current_result` 将不再是 `Fuzznum`，
                # 此时链式运算无法继续，需要抛出错误。
                if not isinstance(current_result, Fuzznum):
                    raise ValueError(f"Chain operation requires intermediate result to be a Fuzznum object, "
                                     f"but got type '{type(current_result)}' at step {i} for operation '{op_type}'.")

                # 判断当前操作类型。
                if op_type in binary_ops:
                    # 如果是二元运算，需要从 `fuzznums` 列表中获取第二个操作数。
                    fuzznum_idx += 1  # 移动到下一个 `fuzznum`。
                    # 检查 `fuzznums` 列表是否还有足够的元素来提供第二个操作数。
                    if fuzznum_idx >= len(fuzznums):
                        raise ValueError(f"Binary operation '{op_type}' at step {i} requires a second fuzznum, "
                                         f"but 'fuzznums' list is exhausted.")

                    # 调用私有方法 `_execute_binary_operation` 执行二元运算。
                    # `current_result` 是第一个操作数，`fuzznums[fuzznum_idx]` 是第二个操作数。
                    current_result = self._execute_binary_op(op_type,
                                                             current_result,
                                                             fuzznums[fuzznum_idx],
                                                             **op_params)

                elif op_type in unary_ops:
                    # 如果是一元运算，直接对 `current_result` 执行运算。
                    current_result = self._execute_unary_op(op_type,
                                                            current_result,
                                                            **op_params)

                else:
                    # 如果遇到不支持的运算类型，则抛出错误。
                    raise ValueError(f"Unsupported chain operation type: '{op_type}'.")

            # 返回链式运算的最终结果。
            return current_result

        # 调用 `_execute_with_monitoring` 包装器来执行 `_execute_chain` 内部函数。
        # 这会自动处理性能统计、日志记录和异常捕获，确保整个链式运算的健壮性。
        return self._execute_with_monitoring('chain_operation', _execute_chain)
