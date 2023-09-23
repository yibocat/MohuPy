#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/9/23 下午4:29
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import GPUtil

gpu = GPUtil.getGPUs()
if len(gpu) > 0:
    __USE_GPU = True
else:
    __USE_GPU = False


def set_gpu_mode(enable_gpu):
    global __USE_GPU
    if len(gpu) > 0:
        __USE_GPU = enable_gpu
    else:
        # print('No GPU found. Use CPU mode.')
        __USE_GPU = False


def get_gpu_mode():
    if __USE_GPU:
        print("Using GPU mode.")
    else:
        print("Using CPU mode.")


def import_cupy_lib():
    gpus = GPUtil.getGPUs()
    if len(gpus) > 0:
        if __USE_GPU:
            try:
                import cupy as array_lib
                set_gpu_mode(True)
            except ImportError:
                import numpy as array_lib
                set_gpu_mode(False)
        else:
            set_gpu_mode(False)
            import numpy as array_lib
    else:
        set_gpu_mode(False)
        import numpy as array_lib
    return array_lib


def import_cudf_lib():
    gpus = GPUtil.getGPUs()
    if len(gpus) > 0:
        if __USE_GPU:
            try:
                import cudf as array_lib
                set_gpu_mode(True)
            except ImportError:
                import pandas as array_lib
                set_gpu_mode(False)
        else:
            set_gpu_mode(False)
            import pandas as array_lib
    else:
        set_gpu_mode(False)
        import pandas as array_lib
    return array_lib
