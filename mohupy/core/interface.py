#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/10/15 下午2:02
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy


class Memoize:
    """
        Memory unit dictionary, a dictionary used to dynamically
        record fuzzy parent classes
    """

    def __init__(self, f):
        self.f = f
        self.memo = {}

    def __call__(self, args):
        self.memo.clear()
        return self.memo.setdefault(args, self.f(args))


@Memoize
def mohuParent(base):
    class mohunum(base):
        def __init__(self, qrung, md, nmd):
            base.__init__(self, qrung, md, nmd)

        def __repr__(self):
            return base.__repr__(self)

        def __str__(self):
            return base.__str__(self)

        @property
        def score(self):
            return base.score(self)

        @property
        def acc(self):
            return base.acc(self)

        @property
        def ind(self):
            return base.ind(self)

        @property
        def comp(self):
            return base.comp(self)

        @property
        def T(self):
            return base.T(self)

        def is_valid(self):
            return base.is_valid(self)

        def isEmpty(self):
            return base.isEmpty(self)

        def convert(self):
            return base.convert(self)

        def reshape(self, *n):
            from ..utils import asfuzzset
            if n == (1,):
                return asfuzzset([self])
            raise ValueError(f'cannot reshape mohunum of size {self.size} to {n}')

    return mohunum


import shutil


def download_template(destination_path):
    """
        Template download method, used to download fuzzy number templates
    """
    source_path = '../mohupy/core/template.py'
    shutil.copyfile(source_path, destination_path)
    print('Download successful!')
