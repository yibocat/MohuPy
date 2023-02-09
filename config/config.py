#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/2 下午4:34
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzPy

"""
    Manually update the fuzzy set configuration file
"""

from dictionary import save_dict
import fuzzyelement
from fuzzyelement.__fuzzyElemmath import qhfeDistance, qfnDistance, qivfnDistance
from fuzzyelement.IVFNumbers import (qrungivfn, randomIVFN, str_to_ivfn)
from fuzzyelement.FNumbers import (qrungfn, randomFN, str_to_fn)
from fuzzyelement.DHFElements import (qrunghfe, randomQHF, str_to_hfe)
from generator import DHFEGenerator, FNGenerator, IVFNGenerator

d = {
    'qrunghfe': {
        'type': qrunghfe,
        'random': randomQHF,
        'generator': DHFEGenerator,
        'convert_str': str_to_hfe,
        'intersection': fuzzyelement.DHFElements.intersection,
        'unions': fuzzyelement.DHFElements.unions,
        'algeb_multiply': fuzzyelement.DHFElements.algeb_multiply,
        'algeb_plus': fuzzyelement.DHFElements.algeb_plus,
        'eins_multiply': fuzzyelement.DHFElements.eins_multiply,
        'eins_plus': fuzzyelement.DHFElements.eins_plus,
        'pos': fuzzyelement.DHFElements.pos,
        'neg': fuzzyelement.DHFElements.neg,
        'zero': fuzzyelement.DHFElements.zero,
        'distance': qhfeDistance,
    },
    'qrungfn': {
        'type': qrungfn,
        'random': randomFN,
        'generator': FNGenerator,
        'convert_str': str_to_fn,
        'intersection': fuzzyelement.FNumbers.intersection,
        'unions': fuzzyelement.FNumbers.unions,
        'algeb_multiply': fuzzyelement.FNumbers.algeb_multiply,
        'algeb_plus': fuzzyelement.FNumbers.algeb_plus,
        'eins_multiply': fuzzyelement.FNumbers.eins_multiply,
        'eins_plus': fuzzyelement.FNumbers.eins_plus,
        'pos': fuzzyelement.FNumbers.pos,
        'neg': fuzzyelement.FNumbers.neg,
        'zero': fuzzyelement.FNumbers.zero,
        'distance': qfnDistance,
    },
    'qrungivfn': {
        'type': qrungivfn,
        'random': randomIVFN,
        'generator': IVFNGenerator,
        'convert_str': str_to_ivfn,
        'intersection': fuzzyelement.IVFNumbers.intersection,
        'unions': fuzzyelement.IVFNumbers.unions,
        'algeb_multiply': fuzzyelement.IVFNumbers.algeb_multiply,
        'algeb_plus': fuzzyelement.IVFNumbers.algeb_plus,
        'eins_multiply': fuzzyelement.IVFNumbers.eins_multiply,
        'eins_plus': fuzzyelement.IVFNumbers.eins_plus,
        'pos': fuzzyelement.IVFNumbers.pos,
        'neg': fuzzyelement.IVFNumbers.neg,
        'zero': fuzzyelement.IVFNumbers.zero,
        'distance': qivfnDistance,
    }
}

if __name__ == '__main__':
    save_dict(d)
