#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/21 上午4:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets

import mohusets.fuzzynumbers.fuzz_global as glb

glb._init()

import mohusets.fuzzynumbers.qrungdhfe as hfe
import mohusets.fuzzynumbers.qrungifn as ifn
import mohusets.fuzzynumbers.qrungivfn as ivfn

dict_dhfe = {'type': hfe.qrungdhfe}
dict_ifn = {'type': ifn.qrungifn}
dict_ivfn = {'type': ivfn.qrungivfn}

from mohusets.fuzzynumbers.__fuzzmath import qdfe_d, qifn_d, qivfn_d

dict_dhfe['random'] = hfe.random
dict_ifn['random'] = ifn.random
dict_ivfn['random'] = ivfn.random

dict_dhfe['convert_str'] = hfe.str_to_hfe
dict_ifn['convert_str'] = ifn.str_to_fn
dict_ivfn['convert_str'] = ivfn.str_to_ivfn

dict_dhfe['intersection'] = hfe.intersection
dict_ifn['intersection'] = ifn.intersection
dict_ivfn['intersection'] = ivfn.intersection

dict_dhfe['unions'] = hfe.unions
dict_ifn['unions'] = ifn.unions
dict_ivfn['unions'] = ivfn.unions

dict_dhfe['algeb_multiply'] = hfe.algeb_multiply
dict_ifn['algeb_multiply'] = ifn.algeb_multiply
dict_ivfn['algeb_multiply'] = ivfn.algeb_multiply

dict_dhfe['algeb_plus'] = hfe.algeb_plus
dict_ifn['algeb_plus'] = ifn.algeb_plus
dict_ivfn['algeb_plus'] = ivfn.algeb_plus

dict_dhfe['eins_multiply'] = hfe.eins_multiply
dict_ifn['eins_multiply'] = ifn.eins_multiply
dict_ivfn['eins_multiply'] = ivfn.eins_multiply

dict_dhfe['eins_plus'] = hfe.eins_plus
dict_ifn['eins_plus'] = ifn.eins_plus
dict_ivfn['eins_plus'] = ivfn.eins_plus

dict_dhfe['pos'] = hfe.pos
dict_ifn['pos'] = ifn.pos
dict_ivfn['pos'] = ivfn.pos

dict_dhfe['neg'] = hfe.neg
dict_ifn['neg'] = ifn.neg
dict_ivfn['neg'] = ivfn.neg

dict_dhfe['zero'] = hfe.zero
dict_ifn['zero'] = ifn.zero
dict_ivfn['zero'] = ivfn.zero

dict_dhfe['distance'] = qdfe_d
dict_ifn['distance'] = qifn_d
dict_ivfn['distance'] = qivfn_d

glb.global_set('qrungdhfe', dict_dhfe)
glb.global_set('qrungifn', dict_ifn)
glb.global_set('qrungivfn', dict_ivfn)
