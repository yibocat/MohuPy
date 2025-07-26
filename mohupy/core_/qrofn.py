#  Copyright (c) yibocat 2025 All Rights Reserved
#  Python: 3.10.9
#  Date: 2025/7/8 22:54
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import copy

import numpy as np

from .strategy import ConfigStrategy
from .template import Template


class qROFNStrategy(ConfigStrategy):
    """
        q-rung orthopair fuzzy number(qROFN)：q接续对模糊数

        qROFN 的配置策略类，用于配置 qROFN 实例的属性
    """

    @property
    def type_name(self) -> str:
        """
            qROFN 的类型名称，定义为 'qrofn'
        """
        return 'qrofn'

    def configure(self, instance) -> None:
        """
            为 qROFN 类型配置属性
            q阶序对模糊数的属性包括：
                - q阶序对：q
                - 隶属度：md
                - 非隶属度：nmd
                - 维度：ndim（暂定）
                - 大小：size（暂定）
                - 形状：shape（暂定）
        """
        instance.qrung = 1
        instance.md = None
        instance.nmd = None
        instance.ndim = 0
        instance.size = 0
        instance.shape = ()


class qROFNNumber(Template):

    # def __init__(self, instance):
    #     super().__init__(instance)

    def report(self):
        return f'<{np.round(self.instance.md, 4)},{np.round(self.instance.nmd, 4)}>'

    def str(self):
        return f'<{np.round(self.instance.md, 4)},{np.round(self.instance.nmd, 4)}>'

    def initialize(self):
        if isinstance(self.instance.md, (float, int, np.int_, np.float64)) and \
                isinstance(self.instance.nmd, (float, int, np.int_, np.float64)):
            assert 0. <= self.instance.md <= 1. and 0. <= self.instance.nmd <= 1., \
                'ERROR: md and nmd must be betweenZERO and ONE'
            assert 0. <= self.instance.md ** self.instance.qrung + self.instance.nmd ** self.instance.qrung <= 1., \
                'ERROR: md ** qrung + nmd ** qrung must be between ZERO and ONE.'

            # md = np.round(self.instance.md, 6)
            # nmd = np.round(self.instance.nmd, 6)

    def score(self):
        return self.instance.md ** self.instance.qrung - self.instance.nmd ** self.instance.qrung

    def accuracy(self):
        return self.instance.md ** self.instance.qrung + self.instance.nmd ** self.instance.qrung

    def indeterminacy(self):
        acc = self.instance.md ** self.instance.qrung + self.instance.nmd ** self.instance.qrung
        if acc == np.round(1., 6):
            return np.round(0., 6)
        else:
            return (1. - acc) ** (1. / self.instance.qrung)

    def complement(self):
        newf = copy.deepcopy(self)
        newf.md = self.instance.nmd
        newf.nmd = self.instance.md
        return newf

    def validity(self):
        if 0. <= self.instance.md <= 1. and 0. <= self.instance.nmd <= 1. \
                and 0. <= self.instance.md ** self.instance.qrung + self.instance.nmd ** self.instance.qrung <= 1.:
            return True
        else:
            return False

    def empty(self):
        if self.instance.md is None and self.instance.nmd is None:
            return True
        else:
            return False

    def convert(self):
        return self.instance.md, self.instance.nmd

    def qsort(self):
        return self

    def unique(self):
        return self

    def normalize(self):
        return self
