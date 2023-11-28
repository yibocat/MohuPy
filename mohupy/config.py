#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/11/28 下午3:50
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
import numpy as np


# import GPUtil
#
# gpu = GPUtil.getGPUs()
# if len(gpu) > 0:
#     __USE_GPU = True
# else:
#     __USE_GPU = False
#
#
# # def set_gpu_mode(enable_gpu):
# #     global __USE_GPU
# #     if len(gpu) > 0:
# #         __USE_GPU = enable_gpu
# #     else:
# #         # print('No GPU found. Use CPU mode.')
# #         __USE_GPU = False
# #
# #
# # def get_gpu_mode():
# #     if __USE_GPU:
# #         print("Using GPU mode.")
# #     else:
# #         print("Using CPU mode.")
#
#
# def import_py_lib():
#     # gpus = GPUtil.getGPUs()
#     # if len(gpus) > 0:
#     #     if __USE_GPU:
#     #         try:
#     #             import cupy as array_lib
#     #             set_gpu_mode(True)
#     #         except ImportError:
#     #             import numpy as array_lib
#     #             set_gpu_mode(False)
#     #     else:
#     #         set_gpu_mode(False)
#     #         import numpy as array_lib
#     # else:
#     #     set_gpu_mode(False)
#     #     import numpy as array_lib
#     import numpy as array_lib
#     return array_lib
#
#
# def import_df_lib():
#     # gpus = GPUtil.getGPUs()
#     # if len(gpus) > 0:
#     #     if __USE_GPU:
#     #         try:
#     #             import cudf as array_lib
#     #             set_gpu_mode(True)
#     #         except ImportError:
#     #             import pandas as array_lib
#     #             set_gpu_mode(False)
#     #     else:
#     #         set_gpu_mode(False)
#     #         import pandas as array_lib
#     # else:
#     #     set_gpu_mode(False)
#     #     import pandas as array_lib
#     import pandas as array_lib
#     return array_lib

class Approx:
    round = 6

    ZERO_1 = np.float_(1e-1)
    ZERO_2 = np.float_(1e-2)
    ZERO_3 = np.float_(1e-3)
    ZERO_4 = np.float_(1e-4)
    ZERO_5 = np.float_(1e-5)
    ZERO_6 = np.float_(1e-6)
    ZERO_7 = np.float_(1e-7)
    ZERO_8 = np.float_(1e-8)
    ZERO_9 = np.float_(1e-9)
    ZERO_10 = np.float_(1e-10)
    ZERO_16 = np.float_(1e-16)

    ONE_1 = np.float_(1 - 1e-1)
    ONE_2 = np.float_(1 - 1e-2)
    ONE_3 = np.float_(1 - 1e-3)
    ONE_4 = np.float_(1 - 1e-4)
    ONE_5 = np.float_(1 - 1e-5)
    ONE_6 = np.float_(1 - 1e-6)
    ONE_7 = np.float_(1 - 1e-7)
    ONE_8 = np.float_(1 - 1e-8)
    ONE_9 = np.float_(1 - 1e-9)
    ONE_10 = np.float_(1 - 1e-10)
    ONE_16 = np.float_(1 - 1e-16)

    approx_dict = {
        1: (ONE_1, ZERO_1),
        2: (ONE_2, ZERO_2),
        3: (ONE_3, ZERO_3),
        4: (ONE_4, ZERO_4),
        5: (ONE_5, ZERO_5),
        6: (ONE_6, ZERO_6),
        7: (ONE_7, ZERO_7),
        8: (ONE_8, ZERO_8),
        9: (ONE_9, ZERO_9),
        10: (ONE_10, ZERO_10),
        16: (ONE_16, ZERO_16),
    }


def approx(a):
    Approx.round = a
