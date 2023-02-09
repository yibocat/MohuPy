
from dictionary import save_dict
import fuzzynumbers.qrungdhfe
import fuzzynumbers.qrungifn
import fuzzynumbers.qrungivfn

from fuzzynumbers.__fuzzmath import qdfe_d, qifn_d, qivfn_d

d = {
    'qrungdhfe': {
        'type': fuzzynumbers.qrungdhfe.qrungdhfe,
        'random': fuzzynumbers.qrungdhfe.random,
        'convert_str': fuzzynumbers.qrungdhfe.str_to_hfe,
        'intersection': fuzzynumbers.qrungdhfe.intersection,
        'unions': fuzzynumbers.qrungdhfe.unions,
        'algeb_multiply': fuzzynumbers.qrungdhfe.algeb_multiply,
        'algeb_plus': fuzzynumbers.qrungdhfe.algeb_plus,
        'eins_multiply': fuzzynumbers.qrungdhfe.eins_multiply,
        'eins_plus': fuzzynumbers.qrungdhfe.eins_plus,
        'pos': fuzzynumbers.qrungdhfe.pos,
        'neg': fuzzynumbers.qrungdhfe.neg,
        'zero': fuzzynumbers.qrungdhfe.zero,
        'distance': qdfe_d,
        'generator': '',
    },
    'qrungifn': {
        'type': fuzzynumbers.qrungifn.qrungifn,
        'random': fuzzynumbers.qrungifn.random,
        'convert_str': fuzzynumbers.qrungifn.str_to_fn,
        'intersection': fuzzynumbers.qrungifn.intersection,
        'unions': fuzzynumbers.qrungifn.unions,
        'algeb_multiply': fuzzynumbers.qrungifn.algeb_multiply,
        'algeb_plus': fuzzynumbers.qrungifn.algeb_plus,
        'eins_multiply': fuzzynumbers.qrungifn.eins_multiply,
        'eins_plus': fuzzynumbers.qrungifn.eins_plus,
        'pos': fuzzynumbers.qrungifn.pos,
        'neg': fuzzynumbers.qrungifn.neg,
        'zero': fuzzynumbers.qrungifn.zero,
        'distance': qifn_d,
        'generator': '',
    },
    'qrungivfn': {
        'type': fuzzynumbers.qrungivfn.qrungivfn,
        'random': fuzzynumbers.qrungivfn.random,
        'convert_str': fuzzynumbers.qrungivfn.str_to_ivfn,
        'intersection': fuzzynumbers.qrungivfn.intersection,
        'unions': fuzzynumbers.qrungivfn.unions,
        'algeb_multiply': fuzzynumbers.qrungivfn.algeb_multiply,
        'algeb_plus': fuzzynumbers.qrungivfn.algeb_plus,
        'eins_multiply': fuzzynumbers.qrungivfn.eins_multiply,
        'eins_plus': fuzzynumbers.qrungivfn.eins_plus,
        'pos': fuzzynumbers.qrungivfn.pos,
        'neg': fuzzynumbers.qrungivfn.neg,
        'zero': fuzzynumbers.qrungivfn.zero,
        'distance': qivfn_d,
        'generator': '',
    }
}

if __name__ == '__main__':
    save_dict(d)
