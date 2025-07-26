#  Copyright (c) yibocat 2025 All Rights Reserved
#  Python: 3.10.9
#  Date: 2025/7/8 20:10
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy


from .base import Attribute
from .fuzzy import fuzz_directory
from .fuzznums import Fuzznum
from .fuzzarray import Fuzzarray


class Report(Attribute):
    def function(self, x):
        if isinstance(x, Fuzznum):
            if x.md is None and x.nmd is None:
                return f'<>'
            else:
                return fuzz_directory[x.mtype](x.qrung, x.md, x.nmd).report()
        if isinstance(x, Fuzzarray):
            p = str(x.array).replace('\n', '\n' + ' ' * 10)
            return f'Fuzzarray({p}, qrung={x.qrung}, mtype={x.mtype})'
        raise TypeError(f'ERROR: The type ({type(x)}) of fuzzy element is not supported.')


class Str(Attribute):
    def function(self, x):
        if isinstance(x, Fuzznum):
            return fuzz_directory[x.mtype](x.qrung, x.md, x.nmd).str()
        if isinstance(x, Fuzzarray):
            return str(x.array)
        raise TypeError(f'ERROR: The type ({type(x)}) of fuzzy element is not supported.')


class Score(Attribute):
    def function(self, x):
        if isinstance(x, Fuzznum):
            return fuzz_directory[x.mtype](x.qrung, x.md, x.nmd).score()
        if isinstance(x, Fuzzarray):
            # TODO: 模糊集
            pass
        raise TypeError(f'ERROR: The type ({type(x)}) of fuzzy element is not supported.')


class Accuracy(Attribute):
    def function(self, x):
        if isinstance(x, Fuzznum):
            return fuzz_directory[x.mtype](x.qrung, x.md, x.nmd).accuracy()
        if isinstance(x, Fuzzarray):
            # TODO: 模糊集
            pass
        raise TypeError(f'ERROR: The type ({type(x)}) of fuzzy element is not supported.')


class Indeterminacy(Attribute):
    def function(self, x):
        if isinstance(x, Fuzznum):
            return fuzz_directory[x.mtype](x.qrung, x.md, x.nmd).indeterminacy()
        if isinstance(x, Fuzzarray):
            # TODO: 模糊集
            pass


class Complement(Attribute):
    def function(self, x):
        if isinstance(x, Fuzznum):
            return fuzz_directory[x.mtype](x.qrung, x.md, x.nmd).complement()
        if isinstance(x, Fuzzarray):
            # TODO: 模糊集
            pass
        raise TypeError(f'ERROR: The type ({type(x)}) of fuzzy element is not supported.')
