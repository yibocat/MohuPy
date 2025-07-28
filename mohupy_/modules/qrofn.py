#  Copyright (c) yibocat 2025 All Rights Reserved
#  Python: 3.10.9
#  Date: 2025/7/27 00:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
from typing import Optional, Dict, Any, Union

from mohupy_.core.base import FuzznumStrategy, FuzznumTemplate
from mohupy_.core.triangular import OperationTNorm


class QROFNStrategy(FuzznumStrategy):
    mtype = 'qrofn'
    md: Optional[float] = None
    nmd: Optional[float] = None

    def __init__(self):
        super().__init__()

        self.add_attribute_validator('md',
                                     lambda x: x is None or isinstance(x, (int, float)) and 0 <= x <= 1)
        self.add_attribute_validator('nmd',
                                     lambda x: x is None or isinstance(x, (int, float)) and 0 <= x <= 1)

        # 添加变更回调
        self.add_change_callback('md', self._on_membership_change)
        self.add_change_callback('nmd', self._on_membership_change)

    def _fuzz_constraint(self):
        # 模糊约束条件
        if self.md is not None and self.nmd is not None and self.md ** self.q + self.nmd ** self.q > 1 :
            raise ValueError(f"md^q + nmd^q = {self.md ** self.q + self.nmd ** self.q} > 1, violates fuzzy number constraints")

    def _on_membership_change(self, attr_name: str, old_value: Any, new_value: Any) -> None:
        """隶属度或非隶属度变更时的回调函数。

        此回调函数在 `md` 或 `nmd` 属性被设置时触发。它会检查模糊数约束条件
        `md + nmd <= 1`，如果违反则发出警告。
        """
        if new_value is not None and hasattr(self, 'md') and hasattr(self, 'nmd'):
            # 只有当新值不为 None，并且实例上同时存在 'md' 和 'nmd' 属性时才执行后续检查。
            # 这确保了在对象初始化过程中，当属性可能尚未完全设置时，不会触发不完整的检查。
            self._fuzz_constraint()

    def _validate(self) -> None:
        # 计算结果验证，所以一般情况下一旦 attribute_validator 验证成功，计算结果就是正确的
        # 该方法用于加强验证
        super()._validate()
        self._fuzz_constraint()

    def add(self, other_strategy: 'QROFNStrategy', tnorm: OperationTNorm) -> Dict[str, Any]:

        new_md = tnorm.t_conorm(self.md, other_strategy.md)
        new_nmd = tnorm.t_norm(self.nmd, other_strategy.nmd)

        return {'md': new_md, 'nmd': new_nmd, 'q': self.q}

    def mul(self, other_strategy: 'QROFNStrategy', tnorm: OperationTNorm) -> Dict[str, Any]:

        new_md = tnorm.t_norm(self.md, other_strategy.md)
        new_nmd = tnorm.t_conorm(self.nmd, other_strategy.nmd)

        return {'md': new_md, 'nmd': new_nmd, 'q': self.q}

    def tim(self, other_operand: Union[int, float], tnorm: OperationTNorm) -> Dict[str, Any]:

        md = tnorm.f_inv_func(other_operand * tnorm.f_func(self.md))
        nmd = tnorm.g_inv_func(other_operand * tnorm.g_func(self.nmd))

        return {'md': md, 'nmd': nmd, 'q': self.q}

    def pow(self, other_operand: Union[int, float], tnorm: OperationTNorm) -> Dict[str, Any]:

        md = tnorm.g_inv_func(other_operand * tnorm.g_func(self.md))
        nmd = tnorm.f_inv_func(other_operand * tnorm.f_func(self.nmd))

        return {'md': md, 'nmd': nmd, 'q': self.q}


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

    @property
    def score(self):
        return self.instance.md ** self.instance.q - self.instance.nmd ** self.instance.q
