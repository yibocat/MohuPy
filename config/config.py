#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/2 下午4:34
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzyKit

"""
    Manually update the fuzzy set configuration file
"""

from dictionary import save_dict
import fuzzyelement
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
        'algebraicmultiplication': fuzzyelement.DHFElements.algebraicmultiplication,
        'algebraicplus': fuzzyelement.DHFElements.algebraicplus,
        'einsteinmultiplication': fuzzyelement.DHFElements.einsteinmultiplication,
        'einsteinplus': fuzzyelement.DHFElements.einsteinplus,
        'pos': fuzzyelement.DHFElements.pos,
        'neg': fuzzyelement.DHFElements.neg,
        'zero': fuzzyelement.DHFElements.zero,
    },
    'qrungfn': {
        'type': qrungfn,
        'random': randomFN,
        'generator': FNGenerator,
        'convert_str': str_to_fn,
        'intersection': fuzzyelement.FNumbers.intersection,
        'unions': fuzzyelement.FNumbers.unions,
        'algebraicmultiplication': fuzzyelement.FNumbers.algebraicmultiplication,
        'algebraicplus': fuzzyelement.FNumbers.algebraicplus,
        'einsteinmultiplication': fuzzyelement.FNumbers.einsteinmultiplication,
        'einsteinplus': fuzzyelement.FNumbers.einsteinplus,
        'pos': fuzzyelement.FNumbers.pos,
        'neg': fuzzyelement.FNumbers.neg,
        'zero': fuzzyelement.FNumbers.zero,
    },
    'qrungivfn': {
        'type': qrungivfn,
        'random': randomIVFN,
        'generator': IVFNGenerator,
        'convert_str': str_to_ivfn,
        'intersection': fuzzyelement.IVFNumbers.intersection,
        'unions': fuzzyelement.IVFNumbers.unions,
        'algebraicmultiplication': fuzzyelement.IVFNumbers.algebraicmultiplication,
        'algebraicplus': fuzzyelement.IVFNumbers.algebraicplus,
        'einsteinmultiplication': fuzzyelement.IVFNumbers.einsteinmultiplication,
        'einsteinplus': fuzzyelement.IVFNumbers.einsteinplus,
        'pos': fuzzyelement.IVFNumbers.pos,
        'neg': fuzzyelement.IVFNumbers.neg,
        'zero': fuzzyelement.IVFNumbers.zero,
    }
}

if __name__ == '__main__':
    save_dict(d)
