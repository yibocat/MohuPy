#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/12 下午1:52
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from ...core import Fuzzarray


def fuzz_savez(x: Fuzzarray, filename: str):
    from ..lib import Savez
    Savez(x)(filename)


def fuzz_loadz(filename: str) -> Fuzzarray:
    from ..lib import Loadz
    return Loadz()(filename)


def fuzz_to_csv(x: Fuzzarray, filename:str, header=None, index_col=None):
    from ..lib import ToCSV
    ToCSV(x, header, index_col)(filename)


def fuzz_from_csv(filename:str, qrung, header='infer', index_col=0) -> Fuzzarray:
    from ..lib import LoadCSV
    return LoadCSV(qrung, header, index_col)(filename)
