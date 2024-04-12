#  Copyright (c) yibocat 2024 All Rights Reserved
#  Python: 3.10.9
#  Date: 2024/4/12 下午3:33
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from ...tensor import Fuzztensor


def tensor_savez(x: Fuzztensor, filename: str):
    """
    将 Fuzztensor 保存为 np.npz 形式的文件
    :param x:
    :param filename:
    :return:
    """
    from ..lib import TensorSavez
    TensorSavez(x)(filename)


def tensor_loadz(filename: str) -> Fuzztensor:
    """
    从一个 Fuzztensor 的 np.npz 文件中读取 Fuzztensor
    :param filename:    文件名称
    :return:            Fuzztensor
    """
    from ..lib import TensorLoadz
    return TensorLoadz()(filename)


def tensor_to_csv(x: Fuzztensor, filename: str, header=None, index_col=None):
    from ..lib import TensorToCSV
    TensorToCSV(x, header, index_col)(filename)


def tensor_from_csv(filename: str, qrung, header='infer', index_col=0) -> Fuzztensor:
    from ..lib import TensorLoadCSV
    return TensorLoadCSV(qrung, header, index_col)(filename)
