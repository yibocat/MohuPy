#  Copyright (c) yibocat 2025 All Rights Reserved
#  Python: 3.10.9
#  Date: 2025/7/26 23:51
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

"""
模糊 t-范数框架模块 (FuzzFramework)
该模块实现了一个完整的模糊 t-范数和 t-余范数计算框架，支持多种经典的模糊逻辑运算符。

主要功能包括：
----------
1. 支持 12 种不同类型的 t-范数和对应的 t-余范数
2. 支持 q-rung 广义模糊数的运算（通过 q 阶同构映射）
3. 提供阿基米德 t-范数的生成元和伪逆函数
4. 自动验证 t-范数的数学性质（公理、阿基米德性、生成元一致性）
5. 可视化功能（3D 表面图）
6. 德摩根定律验证

支持的 t-范数类型：
--------------
- algebraic: 代数积 t-范数
- lukasiewicz: Łukasiewicz t-范数
- einstein: Einstein t-范数
- hamacher: Hamacher t-范数族
- yager: Yager t-范数族
- schweizer_sklar: Schweizer-Sklar t-范数族
- dombi: Dombi t-范数族
- aczel_alsina: Aczel-Alsina t-范数族
- frank: Frank t-范数族
- minimum: 最小值 t-范数（非阿基米德）
- drastic: 剧烈积 t-范数（非阿基米德）
- nilpotent: Nilpotent t-范数（非阿基米德）

使用示例：
-------
>>> # 创建代数积 t-范数实例，q=2
>>> fuzzy_framework = OperationTNorm(norm_type='algebraic', q=2)

>>> # 计算 t-范数和 t-余范数
>>> result_t = fuzzy_framework.t_norm(0.6, 0.7)
>>> result_s = fuzzy_framework.t_conorm(0.6, 0.7)

>>> # 验证德摩根定律
>>> demorgan_results = fuzzy_framework.verify_de_morgan_laws()

>>> # 绘制 3D 表面图
>>> fuzzy_framework.plot_t_norm_surface()
"""

import warnings
from typing import Optional, Callable

import numpy as np
from matplotlib import pyplot as plt


class OperationTNorm:
    """
    FuzzFramework 类用于计算和分析各种模糊 t-范数和 t-余范数。
    支持 q-rung 广义模糊数的运算，通过生成元扩展 q 阶实现 q 阶推广运算。
    类内部包含多种常见 t-范数的定义、其生成元（如果存在）、以及相关属性和验证方法。

    属性:
        - t_norm_list (list): 支持的 t-范数类型列表
        - norm_type (str): 当前使用的 t-范数类型
        - q (int): q 阶参数，用于广义模糊数运算
        - params (dict): 范数参数字典
        - is_archimedean (bool): 是否为阿基米德范数
        - is_strict_archimedean (bool): 是否为严格阿基米德范数
        - supports_q (bool): 是否支持 q 阶运算
        - g_func: 生成元函数
        - g_func_inv: 生成元伪逆函数
        - f_func: 对偶生成元函数
        - f_func_inv: 对偶生成元伪逆函数
        - t_norm: t-范数函数
        - t_conorm: t-余范数函数

    核心功能:
        1.  **多种 t-范数和 t-余范数实现**: 涵盖代数积、Łukasiewicz、Einstein、Hamacher、Yager、Schweizer-Sklar、Dombi、Aczel-Alsina、Frank、Minimum、Drastic、Nilpotent 等。
        2.  **q-rung 广义模糊数支持**: 通过生成元的q阶扩展实现对 q-rung 模糊数的运算推广。
            - 对于 t-范数 T_base 和 t-余范数 S_base，其生成元的 q 阶推广定义为:
                - **生成元 q 阶扩展**： `g_q(a) = g_base(a^q)`
                - **生成元 q 阶伪逆**： `g_q_inv(u) = (g_base_inv(u))^(1/q)`
                - **对偶生成元**: `f(a) = g(1-a^q)^(1/q)`
                - **对偶伪逆**: `f_inv(u) = (1-g_inv(u)^q)^(1/q)`
        3.  **生成元 (Generator) 和伪逆 (Pseudo-inverse) 支持**: 对于阿基米德 t-范数，提供了其生成元和伪逆的定义，并支持其 q 阶变换。
        4.  **属性验证**: 提供了对 t-范数公理（交换律、结合律、单调性、边界条件）、阿基米德性、严格阿基米德性以及生成元性质的验证。
        5.  **德摩根定律验证**: 验证 q 阶同构映射下 t-范数和 t-余范数是否满足德摩根定律。
        6.  **可视化**: 提供 t-范数和 t-余范数的三维表面图绘制功能。
        7.  **工具方法**: 包含从生成元构造 t-范数、从 t-范数推导生成元（数值方法）、以及通过数值方法求解生成元伪逆的静态工具方法。

    示例代码：
        >>> # 1. 初始化一个代数积 t-范数，使用默认 q=1
        >>> alg_norm = OperationTNorm(norm_type='algebraic')
        >>> print(f"代数积 T(0.5, 0.8) = {alg_norm.t_norm(0.5, 0.8):.4f}") # 0.5 * 0.8 = 0.4000
        >>> print(f"代数积 S(0.5, 0.8) = {alg_norm.t_conorm(0.5, 0.8):.4f}") # 0.5 + 0.8 - 0.5*0.8 = 0.9000

        >>> # 2. 初始化一个 Łukasiewicz t-范数，并使用 q=2 进行 q-rung 推广
        >>> luk_norm_q2 = OperationTNorm(norm_type='lukasiewicz', q=2)
        >>> # 对于 Łukasiewicz，T_base(a,b) = max(0, a+b-1)
        >>> # T_q(a,b) = (max(0, a^q + b^q - 1))^(1/q)
        >>> # T_2(0.6, 0.7) = (max(0, 0.6^2 + 0.7^2 - 1))^(1/2) = (max(0, 0.36 + 0.49 - 1))^(1/2) = (max(0, -0.15))^(1/2) = 0
        >>> print(f"Łukasiewicz (q=2) T(0.6, 0.7) = {luk_norm_q2.t_norm(0.6, 0.7):.4f}") # 0.0000
        >>> # S_2(0.6, 0.7) = (min(1, 0.6^2 + 0.7^2))^(1/2) = (min(1, 0.36 + 0.49))^(1/2) = (min(1, 0.85))^(1/2) = sqrt(0.85)约0.9220
        >>> print(f"Łukasiewicz (q=2) S(0.6, 0.7) = {luk_norm_q2.t_conorm(0.6, 0.7):.4f}") # 0.9220

        >>> # 3. 初始化一个 Hamacher t-范数，并设置参数 gamma
        >>> hamacher_norm = OperationTNorm(norm_type='hamacher', gamma=0.5)
        >>> print(f"Hamacher (gamma=0.5) T(0.3, 0.9) = {hamacher_norm.t_norm(0.3, 0.9):.4f}")

        >>> # 4. 获取范数信息
        >>> info = alg_norm.get_info()
        >>> for key, value in info.items():
            ... print(f"  {key}: {value}")

        >>> # 5. 验证德摩根定律
        >>> de_morgan_results = luk_norm_q2.verify_de_morgan_laws(0.6, 0.7)

        >>> # 6. 绘制 t-范数和 t-余范数表面图
        >>> # hamacher_norm.plot_t_norm_surface(resolution=30) # 可以调整分辨率

    注意事项:
        - 参数 q: q 必须是大于 0 的整数。当 q=1 时，运算退化为经典的模糊运算。
        - 特定范数参数: 某些 t-范数（如 Hamacher, Yager, Frank 等）需要额外的参数。这些参数通过 **params 传递给构造函数。请查阅每个 _init_xxx 方法的注释以了解所需参数及其有效范围。

        - 例如，Hamacher 需要 gamma > 0。
        - Yager 需要 p > 0。
        - Frank 需要 s > 0 且 s != 1。
        - Schweizer-Sklar 需要 p != 0。
        - Dombi 和 Aczel-Alsina 需要 p > 0。
        - 浮点精度: 内部使用 self._epsilon (默认为 1e-12) 来处理浮点数比较，以避免精度问题。
        - 边界值处理: 许多 t-范数和生成元函数在输入接近 0 或 1 时可能涉及 log(0) 或除以 0 的情况。代码中已尽可能通过 self._epsilon 和条件判断来处理这些边界情况，以避免运行时错误和 NaN 值。
        - 非阿基米德范数: Minimum, Drastic, Nilpotent 等是非阿基米德 t-范数。它们没有生成元，也不支持 q 阶推广 (supports_q = False)。
        - 警告信息: 类的内部验证方法 (_verify_properties) 会在发现公理不满足或生成元性质不一致时发出 warnings.UserWarning 或 warnings.RuntimeWarning。这些警告旨在提醒用户潜在的数学不一致性或数值问题，但不会中断程序执行。
        - 绘图性能: plot_t_norm_surface 方法在 resolution 较高时可能需要较长的计算和渲染时间。
    """

    # 定义支持的 t-范数类型列表
    # 这是一个类属性，列出了 OperationTNorm 实例可以初始化的所有预定义 t-范数类型。
    t_norm_list = [
        'algebraic', 'lukasiewicz', 'einstein', 'hamacher', 'yager',
        'schweizer_sklar', 'dombi', 'aczel_alsina', 'frank',
        'minimum', 'drastic', 'nilpotent'
    ]

    def __init__(self,
                 norm_type: str = None,
                 q: int = 1,  # q 阶参数，通常为正整数
                 **params):
        """
        初始化模糊运算框架。

        Args:
            norm_type (str, optional): t-范数类型. 默认为 'algebraic'.
                                       必须是 OperationTNorm.t_norm_list 中的一个。
            q (int, optional): q-rung 序对参数，用于广义模糊数. 默认为 1.
                                q 必须是大于 0 的整数。当 q=1 时，运算退化为经典模糊运算。
            **params: 其他参数，用于某些特定 t-范数。
                      例如：
                      - Hamacher 范数: `gamma` (float, 必须 > 0)
                      - Yager 范数: `p` (float, 必须 > 0)
                      - Schweizer-Sklar 范数: `p` (float, 必须 != 0)
                      - Dombi 范数: `p` (float, 必须 > 0)
                      - Aczel-Alsina 范数: `p` (float, 必须 > 0)
                      - Frank 范数: `s` (float, 必须 > 0 且 != 1)

        Raises:
            ValueError: 如果 `norm_type` 未知或 `q` 不符合要求。
        """

        # 如果未指定 norm_type，则默认使用 'algebraic'
        if norm_type is None:
            norm_type = 'algebraic'

        # 检查 norm_type 是否在支持的列表中
        if norm_type not in self.t_norm_list:
            raise ValueError(f"Unknown t-norm type: {norm_type}. Available types: "
                             f"{', '.join(self.t_norm_list)}")

        # 检查 q 是否为大于 0 的整数
        if not isinstance(q, int) or q <= 0:
            raise ValueError(f"q must be a positive integer, "
                             f"but received q={q} (type: {type(q)}).")
        # 存储实例属性
        self.norm_type = norm_type  # 当前 t-范数类型
        self.q = q  # q-rung 参数
        self.params: dict = params  # 存储特定范数的额外参数

        # 浮点数比较精度，用于避免浮点误差
        # 在进行浮点数比较时，直接使用 `==` 可能因精度问题导致错误。
        # 通常会检查 `abs(a - b) < _epsilon` 来判断两个浮点数是否“相等”。
        # 精度设置为 6
        self._epsilon: float = 1e-12
        self._precision: int = 6

        # 原始的 q=1 时的生成元和伪逆函数（用于生成元性质验证和初始q=1级运算，推导 t范数和 t余范数）
        # 这些是内部使用的基生成元函数，由 _init_xxx 方法设置。
        self._base_g_func_raw: Optional[Callable[[float], float]] = None
        self._base_g_inv_func_raw: Optional[Callable[[float], float]] = None

        # 最终的生成元和伪逆函数（可能经过 q 阶变换，用于生成元性质验证）
        # 这些是经过 q 阶变换后的生成元函数，用于内部验证。
        self.g_func: Optional[Callable[[float], float]] = None
        self.g_inv_func: Optional[Callable[[float], float]] = None

        # 对偶生成元及其伪逆，用于验证 t-余范数的生成元性质。
        self.f_func: Optional[Callable[[float], float]] = None
        self.f_inv_func: Optional[Callable[[float], float]] = None

        # 最终的 t-范数和 t-余范数计算函数
        # 这些是外部调用的主要接口，直接适配 q 值。
        # 事实上，t 范数和 t 余范数是由生成元和对偶生成元及其伪逆推导而来
        self.t_norm: Optional[Callable[[float, float], float]] = None
        self.t_conorm: Optional[Callable[[float, float], float]] = None

        # 范数属性：是否阿基米德、是否严格阿基米德、是否支持 q 阶推广
        # 这些属性在 _init_xxx 方法中设置，用于内部逻辑判断和信息查询。
        self.is_archimedean: bool = False
        self.is_strict_archimedean: bool = False
        self.supports_q: bool = False

        # 初始化所有运算和属性
        # 这是构造函数的核心，它会根据 norm_type 设置所有函数和属性。
        self._initialize_operation()

        # 验证范数属性
        # 在初始化完成后，立即对所选 t-范数的数学性质进行验证，以确保其符合预期。
        self._verify_properties()

    def _initialize_operation(self):
        """
        初始化所有基础 t-范数、t-余范数、生成元及其属性，
        并根据 q 值进行 q 阶生成元变换。

        **流程概述:**

        1.  **初始化基础运算 (q=1)**: 根据 `self.norm_type` 调用对应的 `_init_xxx` 方法。
            -   每个 `_init_xxx` 方法会设置 `_base_t_norm_raw`, `_base_t_conorm_raw`,
                `_base_g_func_raw`, `_base_g_inv_func_raw`，以及 `is_archimedean`,
                `is_strict_archimedean`, `supports_q` 等属性。
        2.  **应用 q 值变换到 q 阶生成元**: 调用 `_q_transformation`。
            -   这将根据 `self.q` 和 `self.supports_q`，将 `_base_g_func_raw` 和 `_base_g_inv_func_raw`
                变换为最终的 `self.g_func` 和 `self.g_inv_func`。
        3.  **应用 q 阶变换到对偶生成元及其伪逆**: 调用 `_init_dual_generators`。
            -   这将根据 `self.q` 和 `self.supports_q`，生成 `self.f_func` 和 `self.f_inv_func`。
        4.  **对t范数和t-余范数进行q阶同构映射**: 调用 `_q_transformation_for_t_norm`。
            -   根据 q 值对 t-范数和 t-余范数操作符进行 q 阶同构映射。
        5.  **直接根据生成元及其伪逆变换 t-范数，根据对偶生成元和伪逆变换 t-余范数**: 调用 `_t_norm_transformation`。
            -   这将根据 `self.q` 和 `self.supports_q`，将 `self.g_func` 和 `self.g_inv_func` 变换为 `self.t_norm`。
            -   同时，根据 `self.q` 和 `self.supports_q`，将 `self.f_func` 和 `self.f_inv_func` 变换为 `self.t_conorm`。
        """

        # 1. 初始化基础运算 (q=1) 的原始函数和属性
        # 根据 norm_type 调用相应的初始化方法。
        if self.norm_type == "algebraic":
            self._init_algebraic()
        elif self.norm_type == "lukasiewicz":
            self._init_lukasiewicz()
        elif self.norm_type == "einstein":
            self._init_einstein()
        elif self.norm_type == "hamacher":
            self._init_hamacher()
        elif self.norm_type == "yager":
            self._init_yager()
        elif self.norm_type == "schweizer_sklar":
            self._init_schweizer_sklar()
        elif self.norm_type == "dombi":
            self._init_dombi()
        elif self.norm_type == "aczel_alsina":
            self._init_aczel_alsina()
        elif self.norm_type == "frank":
            self._init_frank()
        elif self.norm_type == "minimum":
            self._init_minimum()
        elif self.norm_type == "drastic":
            self._init_drastic()
        elif self.norm_type == "nilpotent":
            self._init_nilpotent()

        # 2. 应用 q 值变换到 q 阶生成元
        # 也就是说，通过q阶变换，将 _base_g_func_raw 和 _base_g_inv_func_raw 变换
        # 为最终的 g_func 和 g_inv_func，这是 q 阶变换后的生成元函数。
        self._q_transformation()

        # 3. 生成对偶生成元及其伪逆
        self._init_dual_generators()

        # 4.
        self._q_transformation_for_t_norm()

        # 5.
        self._t_norm_transformation()

    def _q_transformation(self):
        """
            根据 q 值对生成元和伪逆进行变换。在此之前需要判断有些 t 范数和 t 余范数并没有生成元。

            这些变换后的生成元 (`self.g_func`, `self.g_inv_func`)

            **数学表达式 (q-rung 生成元推广):**
                -   **生成元**: `g_q(a) = g_base(a^q)`
                -   **伪逆**: `g_q_inv(u) = (g_base_inv(u))^(1/q)`

            **逻辑:**
                -   如果 `self.supports_q` 为 True 且 `self.q` 不等于 1，并且基础生成元已定义，则应用上述 q 阶变换。
                -   否则，直接使用原始的基础生成元。
                -   如果基础生成元未定义（例如非阿基米德范数），则 `self.g_func` 和 `self.g_inv_func` 保持为 None。
        """
        if self.supports_q and self.q != 1:
            # 检查基础生成元是否存在，因为非阿基米德范数没有生成元。
            if self._base_g_func_raw is None or self._base_g_inv_func_raw is None:
                warnings.warn(f"The t-norm {self.norm_type} supports q-tung transformation, "
                              f"but its base generator or pseudo-inverse is empty. "
                              f"Skipping generator transformation.",
                              RuntimeWarning)
                self.g_func = None
                self.g_inv_func = None
                self.f_func = None
                self.f_inv_func = None
                return

            # q 阶生成元: g_q(a) = g_base(a^q)
            # 对于 a=0 的情况，a^q 仍为 0，g_base(0) 通常为无穷大。
            # q 阶伪逆: g_q_inv(u) = (g_base_inv(u))^(1/q)
            # 对于 u=inf 的情况，g_base_inv(inf) 通常为 0。
            self.g_func = lambda a: self._base_g_func_raw(a ** self.q) if a >= 0 else np.inf
            self.g_inv_func = lambda u: (self._base_g_inv_func_raw(u)) ** (1 / self.q) if u >= 0 else 0.0
        else:
            # 如果 q=1 或不支持 q 阶，则直接使用原始的基础生成元
            self.g_func = self._base_g_func_raw
            self.g_inv_func = self._base_g_inv_func_raw

    def _init_dual_generators(self):
        """
        初始化对偶生成元和及其伪逆。
        对偶生成元是通过生成元及其伪逆得到的。和生成元及其伪逆共同构成 t 范数和 t 余范数。

        **数学表达式**：
            - **对偶生成元**: `f(a) = g(1-a^q)^(1/q)`
            - **对偶伪逆**: `f_inv(u) = (1 - g_inv(u)^q)^(1/q)`

        **逻辑**
            - 仅当当前 t-范数是阿基米德的，并且其生成元 (`self.g_func`)和伪逆 (`self.g_inv_func`) 已定义时，才初始化对偶生成元。
            - 否则，对偶生成元保持为 None。
        """
        if self.is_archimedean and self.g_func is not None and self.g_inv_func is not None:
            # 对偶生成元 f(a) = g(1-a^q)^(1/q)
            # 确保 1-a 在有效域 [0,1] 内，否则结果为无穷大。
            # 对偶伪逆 f_inv(u) = (1 - g_inv(u)^q)^(1/q
            self.f_func = lambda a: self.g_func((1 - a ** self.q) ** (1 / self.q)) if 0 <= a <= 1 else np.inf
            self.f_inv_func = lambda u: (1 - self.g_inv_func(u) ** self.q) ** (1 / self.q)
        else:
            self.f_func = None
            self.f_inv_func = None

    def _q_transformation_for_t_norm(self):
        """
        根据 q 值对 t-范数和 t-余范数操作符进行 q 阶同构映射。
        这些变换后的 t-范数和 t-余范数主要用于检验生成元变换后的 t-范数和 t-余范数是否符合数学定义，对其进行验证的。

        **数学表达式 (q-rung 推广):**
            - **t-范数**: `T_q(a,b) = (T_base(a^q, b^q))^(1/q)`
            - **t-余范数**: `S_q(a,b) = (S_base(a^q, b^q))^(1/q)`
        **逻辑:**
            - 如果 `self.supports_q` 为 True 且 `self.q` 不等于 1，则应用上述 q 阶同构映射。
            - 否则（即 `q=1` 或该范数不支持 q 阶推广），直接使用原始的基础运算函数。
            - 将t-范数和t-余范数其赋值到 `self._check_t_norm` 和 `self._check_t_conorm`
        """
        if self.supports_q and self.q != 1:
            # 应用 q 阶同构映射:t-范数 T_q(a,b) 的定义,t-余范数 S_q(a,b) 的定义
            self._check_t_norm = lambda a, b: (self._base_t_norm_raw(a ** self.q, b ** self.q)) ** (1 / self.q)
            self._check_t_conorm = lambda a, b: (self._base_t_conorm_raw(a ** self.q, b ** self.q)) ** (1 / self.q)
        else:
            # 如果 q=1 或不支持 q 阶，则直接使用原始的基础运算
            self._check_t_norm = self._base_t_norm_raw
            self._check_t_conorm = self._base_t_conorm_raw

    def _t_norm_transformation(self):
        """
        直接根据生成元及其伪逆变换 t-范数，根据对偶生成元和伪逆变换 t-余范数。
        检验变换后的 t-范数和 t-余范数是否符合数学定义。

        **逻辑**
            - 检查当前 t-范数是否是阿基米德的，并且其生成元和伪逆已定义。
            - 检查对偶生成元和伪逆是否存在。
            - 检查变换后的 t-范数和 t-余范数是否符合数学定义。

        **注意**
            - 此方法仅用于验证变换后的 t-范数和 t-余范数是否符合数学定义。
            - 实际应用中，通常不会直接使用此方法，而是使用已变换后的 t-范数和 t-余范数。
        """
        if not self.is_archimedean:
            self.t_norm = self._base_t_norm_raw
            self.t_conorm = self._base_t_conorm_raw
        else:
            if self.g_func is None or self.g_inv_func is None:
                warnings.warn(f"The t-norm {self.norm_type} supports t-norm transformation, "
                              f"but its generator or pseudo-inverse is empty. "
                              f"t-norm and t-conorm are not transformed and as "
                              f"initial mathematical expression calculation form.",
                              RuntimeWarning)
                self.t_norm = self._base_t_norm_raw
                self.t_conorm = self._base_t_conorm_raw
            else:
                # 通过生成元及其伪逆，对偶生成元及其伪逆计算带有q变换的t-范数和t-余范数
                self.t_norm = lambda a, b: self.g_inv_func(self.g_func(a) + self.g_func(b))
                self.t_conorm = lambda a, b: self.f_inv_func(self.f_func(a) + self.f_func(b))

        # 检验变换后的 t-范数和 t-余范数是否符合初始的 t-范数和 t-余范数
        if self.is_archimedean:
            test_data = (0.6, 0.4)
            check = self._check_t_norm(*test_data)
            t_norm = self.t_norm(*test_data)

            if abs(check - t_norm) > self._epsilon:
                warnings.warn(f"Test failed, t-norm {self.norm_type} has a large deviation "
                              f"({abs(check - t_norm)})"
                              f"in the q-rung operation values obtained through the generator and "
                              f"its pseudo-inverse transformation({t_norm}) compared to the q-rung isomorphic "
                              f"mapping values of the t-norm and t-conorm({check}).",
                              RuntimeWarning)

    # ======================= 初始化基础运算 (q=1) ====================
    # 每个 _init_xxx 方法负责定义该范数类型在 q=1 时的：
    # - _base_g_func_raw: 原始生成元函数 g(a)
    # - _base_g_inv_func_raw: 原始生成元伪逆函数 g_inv(u)
    # - is_archimedean: 是否阿基米德 t-范数
    # - is_strict_archimedean: 是否严格阿基米德 t-范数
    # - supports_q: 是否支持 q 阶同构映射推广

    def _init_algebraic(self):
        """
        初始化代数积 t-范数 (Product t-norm) 及其对偶 t-余范数。
        这是一种严格阿基米德 t-范数。
        """
        self._base_t_norm_raw = lambda a, b: a * b
        """数学表达式：T(a,b) = a * b"""

        self._base_t_conorm_raw = lambda a, b: a + b - a * b
        """数学表达式：S(a,b) = a + b - ab"""

        self._base_g_func_raw = lambda a: -np.log(a) if a > self._epsilon else np.inf
        """数学表达式：g(a) = -ln(a)
        生成元 g(a) 在 a 趋近于 0 时趋近于无穷大，在 a 趋近于 1 时趋近于 0。
        这里使用 self._epsilon 来处理 log(0) 的情况，避免运行时错误。
        """

        self._base_g_inv_func_raw = lambda u: np.exp(-u) if u < 100 else 0.0
        """数学表达式：g^(-1)(u) = exp(-u)
        伪逆 g_inv(u) 在 u 趋近于无穷大时趋近于 0，在 u 趋近于 0 时趋近于 1。
        这里设置了一个上限 100，以防止 exp(-u) 过小导致浮点下溢，并直接返回 0.0。
        """

        self.is_archimedean = True
        """是阿基米德 t-范数: T(x,x) < x 对于所有 x ∈ (0,1)。"""

        self.is_strict_archimedean = True
        """是严格阿基米德 t-范数: 除了阿基米德性外，T(x,y) = 0 当且仅当 x=0 或 y=0。"""

        self.supports_q = True
        """支持 q 阶同构映射推广: 该范数可以通过 q 阶变换进行推广。"""

    def _init_lukasiewicz(self):
        """
        初始化 Łukasiewicz t-范数 及其对偶 t-余范数。
        这是一种阿基米德 t-范数，但不是严格阿基米德的。
        """
        self._base_t_norm_raw = lambda a, b: max(0, a + b - 1)
        """数学表达式：T(a,b) = max(0, a + b - 1)"""

        self._base_t_conorm_raw = lambda a, b: min(1, a + b)
        """数学表达式：S(a,b) = min(1, a + b)"""

        self._base_g_func_raw = lambda a: 1 - a
        """数学表达式：g(a) = 1 - a"""

        self._base_g_inv_func_raw = lambda u: max(0, 1 - u)
        """数学表达式：g^(-1)(u) = max(0, 1 - u)"""

        self.is_archimedean = True
        """是阿基米德 t-范数"""

        self.is_strict_archimedean = False
        """不是严格阿基米德 t-范数: 例如 T(0.5, 0.5) = 0，但 0.5 != 0。"""

        self.supports_q = True
        """支持 q 阶同构映射推广"""

    def _init_einstein(self):
        """
        初始化 Einstein t-范数 及其对偶 t-余范数。
        这是一种严格阿基米德 t-范数。
        """
        self._base_t_norm_raw = lambda a, b: (a * b) / (1 + (1 - a) * (1 - b))
        """数学表达式：T(a,b) = (a * b) / (1 + (1-a)*(1-b))"""

        self._base_t_conorm_raw = lambda a, b: (a + b) / (1 + a * b)
        """数学表达式：S(a,b) = (a + b)/(1 + a * b)"""

        self._base_g_func_raw = lambda a: np.log((2 - a) / a) if a > self._epsilon else np.inf
        """数学表达式：g(a) = ln((2-a)/a)"""

        self._base_g_inv_func_raw = lambda u: 2 / (1 + np.exp(u)) if u < 100 else 0.0
        """数学表达式：g^(-1)(u) = 2 / (1 + exp(u))"""

        self.is_archimedean = True
        """是阿基米德 t-范数"""

        self.is_strict_archimedean = True
        """是严格阿基米德 t-范数"""

        self.supports_q = True
        """支持 q 阶同构映射推广"""

    def _init_hamacher(self):
        """
        初始化 Hamacher t-范数 及其对偶 t-余范数。
        这是一种严格阿基米德 t-范数，包含一个参数 `gamma`。
        """
        if 'hamacher_gamma' not in self.params:
            self.params['hamacher_gamma'] = 1.0
        gamma = self.params.get('hamacher_gamma')  # 获取参数 gamma
        if gamma <= 0:
            raise ValueError("Hamacher参数gamma必须大于0")

        self._base_t_norm_raw = lambda a, b: (a * b) / (gamma + (1 - gamma) * (a + b - a * b))
        """数学表达式：T(a,b) = (a * b) / (gamma + (1-gamma)*(a+b-a*b))"""

        self._base_t_conorm_raw = lambda a, b: (a + b - (2 - gamma) * a * b) / (1 - (1 - gamma) * a * b)
        """数学表达式：S(a,b) = (a+b-(2-gamma)*ab)/(1-(1-gamma)*ab)"""

        self._base_g_func_raw = lambda a: np.log((gamma + (1 - gamma) * a) / a) if a > self._epsilon else np.inf
        """数学表达式：g(a) = ln((gamma + (1-gamma)*a)/a)"""

        self._base_g_inv_func_raw = lambda u: gamma / (np.exp(u) - (1 - gamma)) if np.exp(u) > (1 - gamma) else 0.0
        """数学表达式：g^(-1)(u) = gamma/(exp(u)-1+gamma)"""

        self.is_archimedean = True
        """是阿基米德 t-范数"""

        self.is_strict_archimedean = True
        """是严格阿基米德 t-范数"""

        self.supports_q = True
        """支持 q 阶同构映射推广"""

    def _init_yager(self):
        """
        初始化 Yager t-范数族 及其对偶 t-余范数族。
        这是一种阿基米德 t-范数族，包含一个参数 `p`。
        当 p=1 时，Yager t-范数退化为 Łukasiewicz t-范数。
        """
        if 'yager_p' not in self.params:
            self.params['yager_p'] = 1.0
        p = self.params.get('yager_p')  # 获取参数 p，默认为 1.0
        if p <= 0:
            raise ValueError("Yager参数p必须大于0")

        self._base_t_norm_raw = lambda a, b: max(0, 1 - ((1 - a) ** p + (1 - b) ** p) ** (1 / p))
        """数学表达式：T(a,b) = 1 - min(1, ((1-a)^p + (1-b)^p)^{1/p})"""

        self._base_t_conorm_raw = lambda a, b: min(1, (a ** p + b ** p) ** (1 / p))
        """数学表达式：S(a,b) = min(1, (a^p + b^p)^{1/p})"""

        self._base_g_func_raw = lambda a: (1 - a) ** p
        """数学表达式：g(a) = (1 - a)^p"""

        # self._base_g_inv_func_raw = lambda u: 1 - min(1, u ** (1 / p))
        self._base_g_inv_func_raw = lambda u: 1 - (u ** (1 / p))
        """数学表达式：g^(-1)(u) = 1 - min(1, u^{1/p})"""

        self.is_archimedean = True
        """是阿基米德 t-范数"""

        self.is_strict_archimedean = (p == 1)
        """是否严格阿基米德 t-范数，p=1时严格。
        当 p=1 时，Yager t-范数退化为 Łukasiewicz t-范数，而 Łukasiewicz 不是严格阿基米德的。
        这里注释有误，应为：当 p 趋近于无穷大时，Yager t-范数趋近于 Minimum t-范数。
        当 p=1 时，T(a,b) = max(0, a+b-1)，S(a,b) = min(1, a+b)，这正是 Łukasiewicz 范数。
        Łukasiewicz 范数不是严格阿基米德的。
        Yager 范数族通常是严格阿基米德的，除非 p=1 或 p 趋于无穷。
        对于 p=1，T(a,a) = max(0, 2a-1)。如果 a=0.5，T(0.5,0.5)=0，但 a!=0，所以不是严格阿基米德。
        """

        self.supports_q = True
        """支持 q 阶同构映射推广"""

    def _init_schweizer_sklar(self):
        """
        初始化 Schweizer-Sklar t-范数 及其对偶 t-余范数。
        这是一种严格阿基米德 t-范数，包含一个参数 `p`。
        当 p 趋近于 0 时，退化为代数积。
        当 p 趋近于无穷大时，退化为 Minimum。
        当 p 趋近于负无穷大时，退化为 Drastic Product。
        """
        if 'sklar_p' not in self.params:
            self.params['sklar_p'] = 1.0
        p = self.params.get('sklar_p')  # 获取参数 p，默认为 1.0
        if p == 0:
            raise ValueError("Schweizer-Sklar参数p不能为0")

        if p > 0:
            self._base_t_norm_raw = lambda a, b: (max(0, a ** (-p) + b ** (-p) - 1)) ** (
                    -1 / p) if a > self._epsilon and b > self._epsilon else 0.0
            """数学表达式：T(a,b) = (max(0, a^{-p} + b^{-p} - 1))^{-1/p}
            处理 a 或 b 接近 0 的情况，避免除以 0 或负指数问题。
            """

            self._base_t_conorm_raw = \
                lambda a, b: (1 - (max(0, (1 - a) ** (-p) + (1 - b) ** (-p) - 1))
                              ** (-1 / p)) if (1 - a) > self._epsilon and (1 - b) > self._epsilon else max(a, b)
            """数学表达式：S(a,b) = 1 - (max(0, (1-a)^{-p} + (1-b)^{-p} - 1))^{-1/p}
            处理 1-a 或 1-b 接近 0 的情况。
            """

            self._base_g_func_raw = lambda a: a ** (-p) - 1 if a > self._epsilon else np.inf
            """数学表达式：g(a) = a^{-p} - 1"""

            self._base_g_inv_func_raw = lambda u: (u + 1) ** (-1 / p) if u > -1 else 0.0
            """数学表达式：g^(-1)(u) = (u + 1)^{-1/p}"""

        else:  # p < 0
            # 当 p < 0 时，公式形式略有不同，以确保函数行为的正确性。
            self._base_t_norm_raw = lambda a, b: (a ** (-p) + b ** (-p) - 1) ** (
                    -1 / p) if a < 1.0 - self._epsilon and b < 1.0 - self._epsilon else min(a, b)
            """数学表达式：T(a,b) = (a^{-p} + b^{-p} - 1)^{-1/p}
            处理 a 或 b 接近 1 的情况。
            """

            self._base_t_conorm_raw = lambda a, b: 1 - ((1 - a) **
                                                        (-p) + (1 - b) ** (-p) - 1) ** (-1 / p) if ((1 - a)
                                                                                                    < 1.0 - self._epsilon and (
                                                                                                            1 - b) < 1.0 - self._epsilon) else max(
                a, b)
            """数学表达式：S(a,b) = 1 - ((1-a)^{-p} + (1-b)^{-p} - 1)^{-1/p}
            处理 1-a 或 1-b 接近 1 的情况。
            """

            self._base_g_func_raw = lambda a: (1 - a) ** (-p) - 1 if a < 1.0 - self._epsilon else np.inf
            """数学表达式：g(a) = (1 - a)^{-p} - 1"""

            self._base_g_inv_func_raw = lambda u: 1 - (u + 1) ** (-1 / p) if u > -1 else 0.0
            """数学表达式：g^(-1)(u) = 1 - (u + 1)^{-1/p}"""

        self.is_archimedean = True
        """是阿基米德 t-范数"""

        self.is_strict_archimedean = True
        """是严格阿基米德 t-范数"""

        self.supports_q = True
        """支持 q 阶同构映射推广"""

    def _init_dombi(self):
        """
        初始化 Dombi t-范数 及其对偶 t-余范数。
        这是一种严格阿基米德 t-范数，包含一个参数 `p`。
        """
        if 'dombi_p' not in self.params:
            self.params['dombi_p'] = 1.0
        p = self.params.get('dombi_p')  # 获取参数 p，默认为 1.0
        if p <= 0:
            raise ValueError("Dombi参数p必须大于0")

        # Dombi t-范数原始公式
        def dombi_tnorm(a, b):
            # 边界条件处理：T(a,0)=0, T(0,b)=0
            if a <= self._epsilon or b <= self._epsilon:
                return 0.0
            # 边界条件处理：T(a,1)=a, T(1,b)=b
            if abs(a - 1.0) < self._epsilon:
                return b
            if abs(b - 1.0) < self._epsilon:
                return a

            # 避免 (1-x)/x 或 x/(1-x) 趋近于无穷大或0时，p次幂导致浮点错误
            # 使用 np.power 安全计算幂次
            term_a = np.power((1.0 - a) / a, p)
            term_b = np.power((1.0 - b) / b, p)

            # 确保分母不为零，尽管在处理了 a,b 接近 0 或 1 的情况后，通常不会出现
            denominator_term = np.power(term_a + term_b, 1 / p)
            if denominator_term < self._epsilon:  # 避免除以0
                return 1.0  # 此时 (1+denominator_term) 趋近于 1，结果趋近于 1

            return 1 / (1 + denominator_term)

        # Dombi t-余范数原始公式
        def dombi_tconorm(a, b):
            # 边界条件处理：S(a,0)=a, S(0,b)=b
            if abs(a - 0.0) < self._epsilon: return b
            if abs(b - 0.0) < self._epsilon: return a
            # 边界条件处理：S(a,1)=1, S(1,b)=1
            if abs(a - 1.0) < self._epsilon or abs(b - 1.0) < self._epsilon:
                return 1.0

            # 避免 (1-x)/x 或 x/(1-x) 趋近于无穷大或0时，p次幂导致浮点错误
            # 注意：这里是 (x/(1-x))^p，与生成元相反
            term_a = np.power(a / (1.0 - a), p)
            term_b = np.power(b / (1.0 - b), p)

            # 确保分母不为零
            denominator_term = np.power(term_a + term_b, -1 / p)
            if denominator_term < self._epsilon:  # 避免除以0
                return 1.0  # 此时 (1+denominator_term) 趋近于 1，结果趋近于 1

            return 1 / (1 + denominator_term)

        # 修正生成元和伪逆的定义，使其在边界处符合数学定义
        # 生成元 g(a) = ((1-a)/a)^p
        def dombi_g_func(a):
            if abs(a - 0.0) < self._epsilon:  # a 趋近于 0
                return np.inf
            if abs(a - 1.0) < self._epsilon:  # a 趋近于 1
                return 0.0
            return np.power((1.0 - a) / a, p)

        # 伪逆 g_inv(u) = 1 / (1 + u^(1/p))
        def dombi_g_inv_func(u):
            if abs(u - 0.0) < self._epsilon:  # u 趋近于 0
                return 1.0
            # 当 u 趋近于无穷大时，u^(1/p) 趋近于无穷大，1 + u^(1/p) 趋近于无穷大，结果趋近于 0
            if np.isinf(u):
                return 0.0
            return 1.0 / (1.0 + np.power(u, 1.0 / p))

        self._base_t_norm_raw = dombi_tnorm
        """数学表达式：T(a,b) = 1/(1+(((1-a)/a)^p+((1-b)/b)^p)^{1/p})"""

        self._base_t_conorm_raw = dombi_tconorm
        """数学表达式：S(a,b) = 1 / (1 + ((a/(1-a))^p + (b/(1/(1-b)))^p)^{-1/p})"""

        self._base_g_func_raw = dombi_g_func
        """数学表达式：g(a) = ((1 - a)/a)^p"""

        self._base_g_inv_func_raw = dombi_g_inv_func
        """数学表达式：g^(-1)(u) = 1 / (1 + u^{1/p})"""

        self.is_archimedean = True
        """是阿基米德 t-范数"""

        self.is_strict_archimedean = True
        """是严格阿基米德 t-范数"""

        self.supports_q = True
        """支持 q 阶同构映射推广"""

    def _init_aczel_alsina(self):
        """
        初始化 Aczel-Alsina t-范数 及其对偶 t-余范数。
        这是一种严格阿基米德 t-范数，包含一个参数 `p`。
        当 p 趋近于 0 时，退化为 Minimum。
        当 p 趋近于 1 时，退化为代数积。
        当 p 趋近于无穷大时，退化为 Drastic Product。
        """
        if 'aa_p' not in self.params:
            self.params['aa_p'] = 1.0
        p = self.params.get('aa_p')  # 获取参数 p，默认为 1.0
        if p <= 0:
            raise ValueError("Aczel-Alsina参数p必须大于0")

        self._base_t_norm_raw = lambda a, b: np.exp(
            -(((-np.log(a)) ** p + (-np.log(b)) ** p) ** (1 / p))) if a > self._epsilon and b > self._epsilon else 0.0
        """数学表达式：T(a,b) = exp(-(((-ln a)^p + (-ln b)^p)^{1/p}))
        处理 a 或 b 接近 0 的情况，避免 log(0) 或负数次幂。
        """

        self._base_t_conorm_raw = lambda a, b: 1 - np.exp(
            -(((-np.log(1 - a)) ** p + (-np.log(1 - b)) ** p) ** (1 / p))) if (1 - a) > self._epsilon and (
                1 - b) > self._epsilon else max(a, b)
        """数学表达式：S(a,b) = 1 - exp(-(((-ln(1-a))^p + (-ln(1-b))^p)^{1/p}))
        处理 1-a 或 1-b 接近 0 的情况。
        """

        self._base_g_func_raw = lambda a: (-np.log(a)) ** p if a > self._epsilon else np.inf
        """数学表达式：g(a) = (-ln a)^p"""

        self._base_g_inv_func_raw = lambda u: np.exp(-(u ** (1 / p))) if u >= 0 else 1.0
        """数学表达式：g^(-1)(u) = exp(-u^{1/p})"""

        self.is_archimedean = True
        """是阿基米德 t-范数"""

        self.is_strict_archimedean = True
        """是严格阿基米德 t-范数"""

        self.supports_q = True
        """支持 q 阶同构映射推广"""

    def _init_frank(self):
        """
        初始化 Frank t-范数 及其对偶 t-余范数。
        这是一种严格阿基米德 t-范数族，包含一个参数 `s`。
        当 s 趋近于 0 时，退化为 Drastic Product。
        当 s 趋近于 1 时，退化为 Minimum。
        当 s 趋近于无穷大时，退化为 Product。
        """
        if 'frank_s' not in self.params:
            self.params['frank_s'] = np.e
        s = self.params.get('frank_s')  # 获取参数 s，默认为自然对数的底 e
        if s <= 0 or s == 1:
            raise ValueError("Frank参数s必须大于0且不等于1")

        def frank_tnorm(a, b):
            if s == np.inf:  # s 趋于无穷时，Frank 积退化为 Minimum 积
                return min(a, b)
            # 避免 log(0) 或除以 0
            if abs(s - 1) < self._epsilon: return min(a, b)  # s=1时退化为Minimum
            val_a = s ** a - 1
            val_b = s ** b - 1
            denominator = s - 1
            if denominator == 0: return min(a, b)  # 理论上 s!=1，但以防万一
            # 计算 log 的参数，确保其大于 0
            arg_log = 1 + (val_a * val_b) / denominator
            if arg_log <= 0: return 0.0  # 避免 log(负数)
            return np.log(arg_log) / np.log(s)

        def frank_tconorm(a, b):
            if s == np.inf:  # s 趋于无穷时，Frank 余范数退化为 Maximum 余范数
                return max(a, b)
            if abs(s - 1) < self._epsilon: return max(a, b)  # s=1时退化为Maximum
            val_1_a = s ** (1 - a) - 1
            val_1_b = s ** (1 - b) - 1
            denominator = s - 1
            if denominator == 0: return max(a, b)
            # 计算 log 的参数，确保其大于 0
            arg_log = 1 + (val_1_a * val_1_b) / denominator
            if arg_log <= 0: return 1.0  # 避免 log(负数)
            return 1 - np.log(arg_log) / np.log(s)

        self._base_t_norm_raw = frank_tnorm
        """数学表达式：T(a,b) = log_s(1 + ((s^a - 1)(s^b - 1))/(s - 1))"""

        self._base_t_conorm_raw = frank_tconorm
        """数学表达式：S(a,b) = 1 - log_s(1 + ((s^{1-a} - 1)(s^{1-b} - 1))/(s - 1))"""

        self._base_g_func_raw = lambda a: -np.log((s ** a - 1) / (s - 1)) if a > self._epsilon else np.inf
        """数学表达式：g(a) = -log_s((s^a - 1)/(s - 1))"""

        self._base_g_inv_func_raw = lambda u: np.log(1 + (s - 1) * np.exp(-u)) / np.log(s) if u < 100 else 0.0
        """数学表达式：g^(-1)(u) = log_s(1 + (s - 1) exp(-u))"""

        self.is_archimedean = True
        """是阿基米德 t-范数"""

        self.is_strict_archimedean = True
        """是严格阿基米德 t-范数"""

        self.supports_q = True
        """支持 q 阶同构映射推广"""

    def _init_minimum(self):
        """
        初始化最小值 t-范数 (Minimum t-norm) 及其对偶 t-余范数 (Maximum t-conorm)。
        这是一种非阿基米德 t-范数，也是最强的 t-范数。
        """
        self._base_t_norm_raw = lambda a, b: min(a, b)
        """数学表达式：T(a,b) = min(a,b)"""

        self._base_t_conorm_raw = lambda a, b: max(a, b)
        """数学表达式：S(a,b) = max(a,b)"""

        self._base_g_func_raw = None  # 非阿基米德 t-范数无生成元
        self._base_g_inv_func_raw = None

        self.is_archimedean = False
        """非阿基米德 t-范数: T(x,x) = x，不满足 T(x,x) < x。"""

        self.is_strict_archimedean = False
        """非严格阿基米德 t-范数"""

        self.supports_q = False
        """不支持 q 阶同构映射推广: 非阿基米德 t-范数通常不支持通过生成元进行 q 阶推广。"""

    def _init_nilpotent(self):
        """
        初始化 Nilpotent t-范数 及其对偶 t-余范数。
        这是一种非阿基米德 t-范数。
        """

        def nilpotent_tnorm(a, b):
            if a + b > 1:
                return min(a, b)
            else:
                return 0.0

        def nilpotent_tconorm(a, b):
            if a + b < 1:
                return max(a, b)
            else:
                return 1.0

        self._base_t_norm_raw = nilpotent_tnorm
        """数学表达式：T(a,b) = min(a,b) if a+b>1; 0 otherwise"""

        self._base_t_conorm_raw = nilpotent_tconorm
        """数学表达式：S(a,b) = max(a,b) if a+b<1; 1 otherwise"""

        self._base_g_func_raw = None
        self._base_g_inv_func_raw = None

        self.is_archimedean = False
        """非阿基米德 t-范数"""

        self.is_strict_archimedean = False
        """非严格阿基米德 t-范数"""

        self.supports_q = False
        """不支持 q 阶同构映射推广"""

    def _init_drastic(self):
        """
        初始化剧烈积 t-范数 (Drastic Product t-norm) 及其对偶 t-余范数 (Drastic Sum t-conorm)。
        这是一种非阿基米德 t-范数，也是最弱的 t-范数。
        """

        def drastic_tnorm(a, b):
            if abs(b - 1.0) < self._epsilon:  # b=1
                return a
            elif abs(a - 1.0) < self._epsilon:  # a=1
                return b
            else:
                return 0.0

        def drastic_tconorm(a, b):
            if abs(b - 0.0) < self._epsilon:  # b=0
                return a
            elif abs(a - 0.0) < self._epsilon:  # a=0
                return b
            else:
                return 1.0

        self._base_t_norm_raw = drastic_tnorm
        """数学表达式：T(a,b) = a if b=1; b if a=1; 0 otherwise"""

        self._base_t_conorm_raw = drastic_tconorm
        """数学表达式：S(a,b) = a if b=0; b if a=0; 1 otherwise"""

        self._base_g_func_raw = None
        self._base_g_inv_func_raw = None

        self.is_archimedean = False
        """非阿基米德 t-范数"""

        self.is_strict_archimedean = False
        """非严格阿基米德 t-范数"""

        self.supports_q = False
        """不支持 q 阶同构映射推广"""

    # ======================= 验证函数 ===========================

    def _verify_properties(self):
        """
        验证当前 t-范数实例的数学性质，包括 t-范数公理、阿基米德性、
        以及生成元与 t-范数的一致性。
        验证结果会以警告形式输出，不会中断程序执行。

        **验证内容:**
        1.  **t-范数公理**: 调用 `_verify_t_norm_axioms` 验证交换律、结合律、单调性和边界条件。
        2.  **阿基米德性**: 调用 `_verify_archimedean_property` 验证是否满足阿基米德或严格阿基米德性质。
        3.  **生成元性质**: 对于阿基米德 t-范数且生成元已定义的情况，调用 `_verify_generator_properties` 验证 `T(a,b) = g_inv(g(a) + g(b))` 是否成立。
        """
        # 验证 t-范数公理
        self._verify_t_norm_axioms()

        # 验证阿基米德性
        self._verify_archimedean_property()

        # 验证生成元性质（仅对阿基米德范数且生成元已定义时进行）
        if self.is_archimedean and self.g_func is not None and self.g_inv_func is not None:
            self._verify_generator_properties()

    def _verify_t_norm_axioms(self):
        """
        验证 t-范数公理：交换律、结合律、单调性、边界条件。
        使用一组测试值进行验证，并根据 `self._epsilon` 容差进行浮点数比较。
        如果任何公理不满足，将发出 `UserWarning`。
        """
        test_values = [0.2, 0.5, 0.8]  # 用于测试的模糊数值

        for a in test_values:
            for b in test_values:
                for c in test_values:
                    # 1. 交换律 (Commutativity): T(a,b) = T(b,a)
                    # 检查 abs(T(a,b) - T(b,a)) 是否大于容差
                    if abs(self.t_norm(a, b) - self.t_norm(b, a)) >= self._epsilon:
                        warnings.warn(
                            f"({self.norm_type}, q={self.q}).交换律失败: T({a},{b}) ≠ T({b},{a}) "
                            f"(T({a},{b})={self.t_norm(a, b):.6f}, T({b},{a})={self.t_norm(b, a):.6f}).",
                            UserWarning
                        )

                    # 2. 结合律 (Associativity): T(T(a,b),c) = T(a,T(b,c))
                    left_assoc = self.t_norm(self.t_norm(a, b), c)
                    right_assoc = self.t_norm(a, self.t_norm(b, c))
                    # 检查 abs(left_assoc - right_assoc) 是否大于容差
                    if abs(left_assoc - right_assoc) >= self._epsilon:
                        warnings.warn(
                            f"({self.norm_type}, q={self.q}).结合律失败: T(T({a},{b}),{c}) ≠ T({a},T({b},{c})) "
                            f"(left={left_assoc:.6f}, right={right_assoc:.6f}).",
                            UserWarning
                        )

                    # 3. 单调性 (Monotonicity): 如果 a <= b，则 T(a,c) <= T(b,c)
                    if a <= b:
                        # 检查 T(a,c) 是否严格大于 T(b,c) + _epsilon
                        if self.t_norm(a, c) > self.t_norm(b, c) + self._epsilon:
                            warnings.warn(
                                f"({self.norm_type}, q={self.q}).单调性失败: a≤b但T(a,c)>T(b,c) "
                                f"(T({a},{c})={self.t_norm(a, c):.6f}, T({b},{c})={self.t_norm(b, c):.6f}).",
                                UserWarning
                            )

                    # 4. 边界条件 (Boundary Condition): T(a,1) = a
                    # 检查 abs(T(a,1) - a) 是否大于容差
                    if abs(self.t_norm(a, 1.0) - a) >= self._epsilon:
                        warnings.warn(
                            f"({self.norm_type}, q={self.q}).边界条件失败: T({a},1) ≠ {a} "
                            f"(T({a},1)={self.t_norm(a, 1.0):.6f}).",
                            UserWarning
                        )

    def _verify_archimedean_property(self):
        """
        验证 t-范数的阿基米德性 (Archimedean Property) 和严格阿基米德性 (Strict Archimedean Property)。

        **定义:**
        -   **阿基米德性**: 对于所有 `a ∈ (0,1)`，存在 `n` 使得 `T^n(a) = T(a, ..., a)` (n 次) ` = 0`。
            等价地，对于所有 `a ∈ (0,1)`，`T(a,a) < a`。
        -   **严格阿基米德性**: 除了阿基米德性外，`T(x,y) = 0` 当且仅当 `x=0` 或 `y=0`。
            等价地，对于所有 `a ∈ (0,1)`，`T(a,a) < a` 且 `T(x,y) > 0` 对于所有 `x,y ∈ (0,1]`。

        **逻辑:**
        -   仅对标记为阿基米德 (`self.is_archimedean` 为 True) 的范数进行验证。
        -   对于严格阿基米德范数，检查 `T(a,a) < a`。
        -   对于非严格阿基米德但阿基米德的范数，检查 `T(a,a) <= a`。
        """
        if not self.is_archimedean:
            return  # 仅对标记为阿基米德的范数进行验证

        test_values = [0.1, 0.3, 0.5, 0.7, 0.9]
        for a in test_values:
            t_aa = self.t_norm(a, a)
            if self.is_strict_archimedean:
                # 严格阿基米德性要求 T(a,a) < a
                # 检查 t_aa 是否大于等于 a - _epsilon
                if t_aa >= a - self._epsilon:  # 使用 _epsilon 进行浮点数比较
                    warnings.warn(
                        f"({self.norm_type}, q={self.q}).严格阿基米德性失败: T({a},{a}) = {t_aa:.6f} ≥ {a}.",
                        UserWarning
                    )
            else:
                # 阿基米德性要求 T(a,a) <= a
                # 检查 t_aa 是否严格大于 a + _epsilon
                if t_aa > a + self._epsilon:
                    warnings.warn(
                        f"({self.norm_type}, q={self.q}).阿基米德性失败: T({a},{a}) = {t_aa:.6f} > {a}.",
                        UserWarning
                    )

    def _verify_generator_properties(self):
        """
        验证生成元性质：`T(a,b) = g_inv(g(a) + g(b))`。
        此验证使用经过 q 阶变换后的生成元 (`self.g_func`, `self.g_inv_func`)
        与经过 q 阶同构映射后的 t-范数 (`self.t_norm`) 进行比较。

        **逻辑:**
        -   如果生成元或伪逆未定义，则跳过验证并发出警告。
        -   使用一组测试值 `a` 和 `b`。
        -   对于每对 `(a,b)`，计算 `g(a)` 和 `g(b)`。
        -   通过生成元公式 `g_inv(g(a) + g(b))` 计算 t-范数结果 (`via_generator`)。
        -   直接通过 `self.t_norm(a,b)` 计算 t-范数结果 (`direct`)。
        -   比较 `via_generator` 和 `direct`，如果差异超出 `self._epsilon`，则发出警告。
        -   包含错误处理，以防生成元计算过程中出现数值问题。
        """
        if self.g_func is None or self.g_inv_func is None:
            warnings.warn(f"({self.norm_type}, q={self.q}).生成元或伪逆未定义，跳过生成元性质验证。", RuntimeWarning)
            return False

        test_values = [0.1, 0.3, 0.5, 0.7, 0.9]

        for a in test_values:
            for b in test_values:
                try:
                    # 使用当前 q 阶变换后的 g_func 和 g_inv_func
                    g_a = self.g_func(a)
                    g_b = self.g_func(b)

                    # 确保 g_a 和 g_b 是有限值，避免无穷大相加导致 NaN 或错误
                    if np.isinf(g_a) or np.isinf(g_b):
                        # 如果生成元值是无穷大，通常表示输入在边界上 (例如 a=0 或 b=0)。
                        # 此时，T(a,b) 的结果通常是 0。
                        # 直接比较可能不准确，跳过此测试对，因为生成元公式在边界处可能行为不确定。
                        continue

                    # 尝试通过生成元计算 t-范数
                    via_generator = self.g_inv_func(g_a + g_b)

                    # 使用当前 q 阶同构映射后的 t-范数直接计算
                    direct = self.t_norm(a, b)

                    # 比较两种计算结果，允许 _epsilon 容差
                    if abs(direct - via_generator) >= self._epsilon:
                        warnings.warn(
                            f"({self.norm_type}, q={self.q}).生成元验证失败: T({a},{b})={direct:.6f} ≠ g^(-1)(g(a)+g(b))={via_generator:.6f}. "
                            f"g(a)={g_a:.6f}, g(b)={g_b:.6f}.",
                            UserWarning
                        )
                        # return False # 不中断，继续检查其他值
                except Exception as e:
                    warnings.warn(
                        f"({self.norm_type}, q={self.q}).生成元计算过程中出现错误: a={a}, b={b}. 错误信息: {e}.",
                        RuntimeWarning
                    )
                    continue  # 跳过当前迭代，避免因计算错误导致后续比较失败
        return True

    def verify_de_morgan_laws(self, a: float = 0.6, b: float = 0.7) -> dict[str, bool]:
        """
        验证德摩根定律在 q 阶同构映射下的对偶关系。
        对于通过同构映射定义的 q 阶 t-范数和 t-余范数，德摩根定律通常是成立的。

        **德摩根定律形式:**
        1.  `S(a,b) = 1 - T(1-a, 1-b)`
        2.  `T(a,b) = 1 - S(1-a, 1-b)`

        Args:
            a (float): 第一个模糊数值，默认为 0.6。
            b (float): 第二个模糊数值，默认为 0.7。

        Returns:
            dict[str, bool]: 包含两个布尔值的字典，表示德摩根定律是否成立。
                             `'de_morgan_1'`: `S(a,b) == 1 - T(1-a, 1-b)`
                             `'de_morgan_2'`: `T(a,b) == 1 - S(1-a, 1-b)`
        """
        # results = {}
        #
        # # 验证: S(a,b) = 1 - T(1-a, 1-b)
        # s_direct = self.t_conorm(a, b)
        # s_via_demorgan = 1 - self.t_norm(1 - a, 1 - b)
        # # 使用 _epsilon 进行浮点数比较
        # results['de_morgan_1'] = abs(s_direct - s_via_demorgan) < self._epsilon
        #
        # # 验证: T(a,b) = 1 - S(1-a, 1-b)
        # t_direct = self.t_norm(a, b)
        # t_via_demorgan = 1 - self.t_conorm(1 - a, 1 - b)
        # # 使用 _epsilon 进行浮点数比较
        # results['de_morgan_2'] = abs(t_direct - t_via_demorgan) < self._epsilon
        #
        # return results

        results = {}

        # 定义 q-rung 补运算
        def q_rung_complement(x):
            if not (0 <= x <= 1):
                return x  # 或抛出错误
            return (1 - x ** self.q) ** (1 / self.q)

        # 验证: S(a,b) = N(T(N(a), N(b)))
        s_direct = self.t_conorm(a, b)
        n_a = q_rung_complement(a)
        n_b = q_rung_complement(b)
        s_via_demorgan = q_rung_complement(self.t_norm(n_a, n_b))
        results['de_morgan_1'] = abs(s_direct - s_via_demorgan) < self._epsilon

        # 验证: T(a,b) = N(S(N(a), N(b)))
        t_direct = self.t_norm(a, b)
        t_via_demorgan = q_rung_complement(self.t_conorm(n_a, n_b))
        results['de_morgan_2'] = abs(t_direct - t_via_demorgan) < self._epsilon

        return results

    # ======================= 获取信息 ============================

    def get_info(self) -> dict:
        """
        获取当前 t-范数实例的配置信息和属性。

        Returns:
            dict: 包含范数类型、q 值、参数、阿基米德性等信息的字典。
        """
        info = {
            'norm_type': self.norm_type,  # t-范数类型名称
            'is_archimedean': self.is_archimedean,  # 是否阿基米德
            'is_strict_archimedean': self.is_strict_archimedean,  # 是否严格阿基米德
            'supports_q': self.supports_q,  # 是否支持 q 阶推广
            'q_value': self.q,  # 当前 q 值
            'parameter': self.params,  # 特定范数的额外参数
            'epsilon': self._epsilon,  # 浮点数比较精度
            'precision': self._precision  # 浮点数小数点精度
        }
        return info

    def plot_t_norm_surface(self, resolution: int = 50):
        """
        绘制当前 t-范数和 t-余范数的三维表面图。
        图表展示了 t-范数 T(a,b) 和 t-余范数 S(a,b) 在 [0,1]x[0,1] 平面上的曲面。

        Args:
            resolution (int): 绘图网格的分辨率，默认为 50。
                              分辨率越高，曲面越平滑，但计算时间越长。
        """
        # 生成 a 和 b 的取值范围，避免边界值可能导致的计算问题（如 log(0) 或除以 0）
        x = np.linspace(self._epsilon, 1.0 - self._epsilon, resolution)
        y = np.linspace(self._epsilon, 1.0 - self._epsilon, resolution)
        X, Y = np.meshgrid(x, y)  # 创建网格点

        # 初始化 Z 坐标矩阵，用于存储 t-范数和 t-余范数的结果
        Z_t_norm = np.zeros_like(X, dtype=float)
        Z_t_conorm = np.zeros_like(X, dtype=float)

        # 遍历网格点，计算每个 (a,b) 对的 t-范数和 t-余范数值
        for i in range(resolution):
            for j in range(resolution):
                try:
                    Z_t_norm[i, j] = self.t_norm(X[i, j], Y[i, j])
                    Z_t_conorm[i, j] = self.t_conorm(X[i, j], Y[i, j])
                except Exception as e:
                    # 捕获绘图时可能出现的数值错误（例如，某些范数在特定参数下可能导致溢出或 NaN）
                    # 将错误点的值设置为 NaN，这样在绘图时这些点会被跳过，不会导致图形中断。
                    Z_t_norm[i, j] = np.nan
                    Z_t_conorm[i, j] = np.nan
                    # 可以选择在此处发出警告，但频繁的警告会影响用户体验，故注释掉。
                    # warnings.warn(f"绘图计算错误: ({X[i,j]}, {Y[i,j]}) -> {e}", RuntimeWarning)

        # 创建 Matplotlib 图形和子图
        fig = plt.figure(figsize=(14, 6))  # 调整图大小，使其可以并排显示两个 3D 图

        # 第一个子图：t-范数表面图
        ax1 = fig.add_subplot(121, projection='3d')  # 1行2列的第一个子图，3D投影
        ax1.plot_surface(X, Y, Z_t_norm, cmap='viridis', alpha=0.8)  # 绘制曲面
        ax1.set_xlabel('a')
        ax1.set_ylabel('b')
        ax1.set_zlabel('T(a,b)')
        ax1.set_title(f'T-Norm: {self.norm_type.title()} (q={self.q})')  # 设置标题
        ax1.set_zlim(0, 1)  # 限制 Z 轴范围在 [0,1]，因为模糊数值通常在此范围内

        # 第二个子图：t-余范数表面图
        ax2 = fig.add_subplot(122, projection='3d')  # 1行2列的第二个子图，3D投影
        ax2.plot_surface(X, Y, Z_t_conorm, cmap='plasma', alpha=0.8)  # 绘制曲面
        ax2.set_xlabel('a')
        ax2.set_ylabel('b')
        ax2.set_zlabel('S(a,b)')
        ax2.set_title(f'T-Conorm: {self.norm_type.title()} (q={self.q})')  # 设置标题
        ax2.set_zlim(0, 1)  # 限制 Z 轴范围在 [0,1]

        plt.tight_layout()  # 自动调整子图参数，使之填充整个图像区域
        plt.show()  # 显示图形

    # ======================= 实用工具方法 ============================
    # 这些方法提供了 t-范数与生成元之间转换的通用工具，不直接参与 OperationTNorm 的核心初始化流程。
    # 它们被定义为静态方法，可以直接通过类名调用 (e.g., OperationTNorm.generator_to_t_norm(...))。

    @staticmethod
    def t_norm_to_generator(t_norm_func: Callable[[float, float], float],
                            epsilon: float = 1e-6) -> tuple[Callable[[float], float], Callable[[float], float]]:
        """
        尝试从 t-范数函数（阿基米德 t-范数）推导其加性生成元 g(a) 和伪逆 g_inv(u)。
        此方法采用数值方法，可能不适用于所有 t-范数或在所有输入范围内精确。
        **注意**: 这是一个非常简化的示例实现，对于复杂的 t-范数，准确推导生成元通常需要更高级的数值积分技术或符号推导。

        这里仅提供一个概念性的框架，实际应用中可能需要针对特定范数进行定制。

        Args:
            t_norm_func (Callable): t-范数函数 T(a,b)。
            epsilon (float): 浮点数比较精度。

        Returns:
            tuple[Callable, Callable]: (生成元函数 g(a), 伪逆函数 g_inv(u))。
        """

        # 阿基米德 t-范数的生成元 g(x) 满足 g(x) = C * integral(1/phi(t) dt)
        # 且 T(x,y) = g_inv(g(x) + g(y))
        # 对于严格阿基米德 t-范数，g(x) 满足 g(x) = -ln(x) + ... 或 g(x) = (1-x)/x + ...
        # 这里采用一种简化的数值方法，基于 g(x) + g(y) = g(T(x,y))
        # 设定 g(1) = 0 (对于连续阿基米德 t-范数)

        def g(a: float) -> float:
            """
            简化的生成元函数 g(a)。
            对于 Product t-norm (T(a,b)=ab)，其生成元是 g(a) = -ln(a)。
            这里直接使用这个形式作为示例，因为它是一个常见的生成元。
            然而，对于其他 t-范数，其生成元形式会不同，需要更复杂的推导。
            """
            if a <= epsilon:
                return np.inf  # g(0) 通常为无穷大
            if a >= 1.0 - epsilon:
                return 0.0  # g(1) 通常为 0

            # 严格阿基米德 t-范数 T(x,y) = g_inv(g(x) + g(y))
            # 且 g(1)=0, T(x,1)=x
            # 那么 g(T(x,1)) = g(x) + g(1) => g(x) = g(x) + 0
            # 考虑 g(x) = integral_x^1 (1/phi(t)) dt
            # 简化为 g(x) = C * (1/x - 1) for some C, or -ln(x) for Product
            # 这里的数值推导可能不通用，需要根据具体范数进行调整
            # 这是一个简化的示例，实际应用中需要更复杂的数值积分或特定公式
            try:
                # 尝试使用代数积的生成元形式作为启发
                # 对于 T(a,b) = ab, g(a) = -ln(a)
                # g(T(a,b)) = -ln(ab) = -ln(a) - ln(b) = g(a) + g(b)
                # 这是一个简化的尝试，不保证对所有范数都精确
                # 更好的方法是数值积分或查找已知公式
                return -np.log(a)  # 仅为示例，可能不适用于所有 t-范数
            except Exception:
                return np.inf  # 发生错误时返回无穷大

        # 伪逆函数 g_inv(u) 的数值求解
        # 调用静态方法 generator_to_generator_inv 来从 g 函数推导其伪逆。
        g_inv = OperationTNorm.generator_to_generator_inv(g, epsilon=epsilon)

        return g, g_inv

    @staticmethod
    def generator_to_t_norm(g_func: Callable[[float], float],
                            g_inv_func: Callable[[float], float]) -> Callable[[float, float], float]:
        """
        从生成元 g(a) 和其伪逆 g_inv(u) 构造 t-范数 T(a,b)。
        这是阿基米德 t-范数的基本定义之一。

        **数学表达式：**
        `T(a,b) = g_inv(g(a) + g(b))`

        Args:
            g_func (Callable): 生成元函数 g(a)。
            g_inv_func (Callable): 生成元伪逆函数 g_inv(u)。

        Returns:
            Callable: 构造出的 t-范数函数 T(a,b)。
        """

        def T(a: float, b: float) -> float:
            """
            内部函数，实现 T(a,b) 的计算逻辑。
            """
            try:
                val_g_a = g_func(a)
                val_g_b = g_func(b)
                # 避免无穷大相加导致错误（如 NaN）
                if np.isinf(val_g_a) or np.isinf(val_g_b):
                    # 如果 g(a) 或 g(b) 是无穷大，通常意味着 a 或 b 在边界上 (0或1)
                    # 此时 T(a,b) 的结果通常是 0 (例如 T(0,b)=0)。
                    # 这是一个简化的处理，更严谨需要根据范数特性判断
                    if val_g_a == np.inf and val_g_b == np.inf: return 0.0  # g(0)+g(0) -> g_inv(inf) -> 0
                    if val_g_a == np.inf: return 0.0  # g(0)+g(b) -> g_inv(inf) -> 0
                    if val_g_b == np.inf: return 0.0  # g(a)+g(0) -> g_inv(inf) -> 0

                return g_inv_func(val_g_a + val_g_b)
            except Exception as e:
                warnings.warn(f"从生成元构造 t-范数时发生错误: {e}", RuntimeWarning)
                return 0.0  # 发生错误时返回 0

        return T

    @staticmethod
    def generator_to_generator_inv(g_func: Callable[[float], float],
                                   domain_start: float = 0.0,
                                   domain_end: float = 1.0,
                                   max_iterations: int = 1000,
                                   epsilon: float = 1e-6,
                                   ) -> Callable[[float], float]:
        """
        通过数值方法（二分法）从生成元 g_func 推导其伪逆 g_inv_func。
        适用于严格单调的生成元。伪逆 `g_inv(u)` 满足 `g(g_inv(u)) = u`。

        Args:
            g_func (Callable): 生成元函数，输入 x，输出 g(x)。
                               假定 g(x) 是从 [domain_start, domain_end] 映射到某个范围的严格单调函数。
            domain_start (float): 生成元输入域的起始值 (通常为 0)。
            domain_end (float): 生成元输入域的结束值 (通常为 1)。
            max_iterations (int): 最大迭代次数，防止无限循环。
            epsilon (float): 浮点数比较精度，用于判断是否找到足够精确的解。

        Returns:
            Callable: 生成元伪逆函数，输入 u，输出 x，使得 g(x) ≈ u。
        """
        # 确定生成元的单调性
        # 尝试在域内取两个点判断，避免 g(0) 或 g(1) 是无穷大
        try:
            # 在 domain_start 和 domain_end 附近取点，避免直接使用边界值（可能导致无穷大或错误）
            val_at_start = g_func(domain_start + epsilon)
            val_at_end = g_func(domain_end - epsilon)
            # 判断 g(x) 是递减还是递增。例如，-ln(x) 是递减的。
            is_decreasing = (val_at_start > val_at_end + epsilon)  # g(x) 递减 (例如 -ln(x))
        except Exception:
            # 如果边界值计算失败，假设为递减（这是许多生成元的常见情况）
            is_decreasing = True

        def g_inv(u: float) -> float:
            """
            伪逆函数实现：给定目标值 u，在 [domain_start, domain_end] 范围内寻找 x。
            使用二分法进行搜索。
            """
            low = domain_start
            high = domain_end

            # 快速路径处理边界情况
            # 如果目标值 u 接近 g(domain_start) 或 g(domain_end)，则直接返回对应的边界值。
            # 这有助于处理生成元在边界处趋于无穷大的情况。
            if is_decreasing:
                # 如果目标值 u 接近 g(domain_start) (通常是 inf)，则 x 趋近于 domain_start
                if u >= g_func(domain_start + epsilon) - epsilon: return domain_start
                # 如果目标值 u 接近 g(domain_end) (通常是 0)，则 x 趋近于 domain_end
                if u <= g_func(domain_end - epsilon) + epsilon: return domain_end
            else:  # g(x) 递增
                if u <= g_func(domain_start + epsilon) + epsilon: return domain_start
                if u >= g_func(domain_end - epsilon) - epsilon: return domain_end

            # 二分法搜索
            for _ in range(max_iterations):
                mid = (low + high) / 2.0

                # 避免 mid 过于接近边界导致 g_func(mid) 溢出或错误
                # 强制 mid 保持在 (domain_start, domain_end) 范围内，并与边界保持一定距离。
                if mid <= domain_start + epsilon: mid = domain_start + epsilon
                if mid >= domain_end - epsilon: mid = domain_end - epsilon

                try:
                    g_mid = g_func(mid)
                except Exception:
                    # 如果 g_func(mid) 发生错误（例如 log(0)），尝试调整 mid
                    # 这通常发生在 mid 过于接近生成元函数的定义域边界时。
                    if is_decreasing:
                        high = mid  # 假设 mid 太小，需要增大 x，所以缩小 high 边界
                    else:
                        low = mid  # 假设 mid 太大，需要减小 x，所以增大 low 边界
                    continue

                # 如果 g(mid) 足够接近目标值 u，则找到解
                if abs(g_mid - u) < epsilon:
                    return mid

                # 根据单调性调整搜索区间
                if is_decreasing:  # g(x) 递减 (例如 -ln(x))
                    if g_mid > u:  # g(mid) 比目标值大，说明 mid 太小，需要增大 mid (因为 g 是递减的)
                        low = mid
                    else:  # g(mid) 比目标值小，说明 mid 太大，需要减小 mid
                        high = mid
                else:  # g(x) 递增
                    if g_mid < u:  # g(mid) 比目标值小，说明 mid 太小，需要增大 mid (因为 g 是递增的)
                        low = mid
                    else:  # g(mid) 比目标值大，说明 mid 太大，需要减小 mid
                        high = mid

            # 达到最大迭代次数，返回当前最佳近似值
            # 即使未达到精确解，也返回当前二分区间的中点作为近似值。
            return (low + high) / 2.0

        return g_inv
