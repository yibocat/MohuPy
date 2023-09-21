#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/21 上午4:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets

import mohusets.fuzzynumbers.fuzz_global as glb

glb._init()

from .qdhfe import config as cfg1
from .qifn import config as cfg2
from .qivfn import config as cfg3

from .__fuzzmath import qdfe_d, qifn_d, qivfn_d

dict_dhfe = cfg1.global_dict()
dict_ifn = cfg2.global_dict()
dict_ivfn = cfg3.global_dict()

dict_dhfe['qrungdhfe']['distance'] = qdfe_d
dict_ifn['qrungifn']['distance'] = qifn_d
dict_ivfn['qrungivfn']['distance'] = qivfn_d

glb.global_set('qrungdhfe', dict_dhfe['qrungdhfe'])
glb.global_set('qrungifn', dict_ifn['qrungifn'])
glb.global_set('qrungivfn', dict_ivfn['qrungivfn'])

