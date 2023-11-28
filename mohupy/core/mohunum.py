#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/11/26 下午1:37
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy
from typing import Union

import numpy as np

from .mohu import MohuQROFN, MohuQROIVFN, MohuQROHFN


class fuzznum(MohuQROFN, MohuQROIVFN, MohuQROHFN):

    def __init__(self, qrung, md, nmd):
        if isinstance(md, Union[int, float, np.int_, np.float_]) and \
                isinstance(nmd, Union[int, float, np.int_, np.float_]):
            super().__init__()
            MohuQROFN.__init__(self, qrung, md, nmd)

        elif isinstance(md, tuple) and isinstance(nmd, tuple):
            super().__init__()
            MohuQROIVFN.__init__(self, qrung, md, nmd)

        elif isinstance(md, Union[list, np.ndarray]) and isinstance(nmd, Union[list, np.ndarray]):
            super().__init__()
            MohuQROHFN.__init__(self, qrung, md, nmd)

        else:
            raise TypeError(f"Unknown data type, md:{type(md)} and nmd:{type(nmd)}")
