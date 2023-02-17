import fuzzynumbers.config
import fuzzynumbers.fuzz_global as glb

__all__ = []
get_dict = glb.global_dict()
get_variable = glb.global_get
set_variable = glb.global_set
__all__ += ['get_dict', 'get_variable', 'set_variable']

qrungdhfe = glb.global_get('qrungdhfe')['type']
qrungifn = glb.global_get('qrungifn')['type']
qrungivfn = glb.global_get('qrungivfn')['type']

__all__ += ['qrungdhfe', 'qrungifn', 'qrungivfn']

from .qrungdhfe.toolkit import str_to_hfe
from .qrungifn.toolkit import str_to_fn
from .qrungivfn.toolkit import str_to_ivfn

__all__ += ['str_to_hfe', 'str_to_fn', 'str_to_ivfn']

from .fuzzmath import (generalized_distance, random,
                       intersection, unions,
                       algeb_multiply, algeb_plus,
                       eins_multiply, eins_plus,
                       pos, neg, zero,
                       normal)

from .tools import dh_fn_min, dh_fn_max, dh_fn_mean

__all__ += ['generalized_distance', 'random', 'intersection', 'unions',
            'algeb_multiply', 'algeb_plus', 'eins_multiply', 'eins_plus',
            'pos', 'neg', 'zero']

__all__ += ['dh_fn_min', 'dh_fn_max', 'dh_fn_mean', 'normal']
