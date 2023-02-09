#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/9 下午8:31
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzPy

import fuzzpy_c.fuzzynumbers.qrungdhfe as qrungdhfe
import fuzzpy_c.fuzzynumbers.qrungifn as qrungifn
import fuzzpy_c.fuzzynumbers.qrungivfn as qrungivfn

from fuzzpy_c.config.dictionary import save_dict

d = {
    'qrungdhfe': {
        'type': qrungdhfe.qrungdhfe,
        'random': qrungdhfe.random,
        'convert_str': qrungdhfe.str_to_hfe,
        'intersection': qrungdhfe.intersection,
        'unions': qrungdhfe.unions,
        'algeb_multiply': qrungdhfe.algeb_multiply,
        'algeb_plus': qrungdhfe.algeb_plus,
        'eins_multiply': qrungdhfe.eins_multiply,
        'eins_plus': qrungdhfe.eins_plus,
        'pos': qrungdhfe.pos,
        'neg': qrungdhfe.neg,
        'zero': qrungdhfe.zero,
        # 'distance': qdfe_d,
        'generator': '',
    },
    'qrungifn': {
        'type': qrungifn.qrungifn,
        'random': qrungifn.random,
        'convert_str': qrungifn.str_to_fn,
        'intersection': qrungifn.intersection,
        'unions': qrungifn.unions,
        'algeb_multiply': qrungifn.algeb_multiply,
        'algeb_plus': qrungifn.algeb_plus,
        'eins_multiply': qrungifn.eins_multiply,
        'eins_plus': qrungifn.eins_plus,
        'pos': qrungifn.pos,
        'neg': qrungifn.neg,
        'zero': qrungifn.zero,
        # 'distance': qifn_d,
        'generator': '',
    },
    'qrungivfn': {
        'type': qrungivfn.qrungivfn,
        'random': qrungivfn.random,
        'convert_str': qrungivfn.str_to_ivfn,
        'intersection': qrungivfn.intersection,
        'unions': qrungivfn.unions,
        'algeb_multiply': qrungivfn.algeb_multiply,
        'algeb_plus': qrungivfn.algeb_plus,
        'eins_multiply': qrungivfn.eins_multiply,
        'eins_plus': qrungivfn.eins_plus,
        'pos': qrungivfn.pos,
        'neg': qrungivfn.neg,
        'zero': qrungivfn.zero,
        # 'distance': qivfn_d,
        'generator': '',
    }
}

if __name__ == '__main__':
    save_dict(d)
