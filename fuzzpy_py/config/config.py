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
import fuzzpy_py.fuzzyelement
from fuzzpy_py.fuzzyelement.__fuzzyElemmath import qhfeDistance, qfnDistance, qivfnDistance
from fuzzpy_py.fuzzyelement.IVFNumbers import (qrungivfn, randomIVFN, str_to_ivfn)
from fuzzpy_py.fuzzyelement.FNumbers import (qrungfn, randomFN, str_to_fn)
from fuzzpy_py.fuzzyelement.DHFElements import (qrunghfe, randomQHF, str_to_hfe)
from fuzzpy_py.generator import DHFEGenerator, FNGenerator, IVFNGenerator

d = {
    'qrunghfe': {
        'type': qrunghfe,
        'random': randomQHF,
        'generator': DHFEGenerator,
        'convert_str': str_to_hfe,
        'intersection': fuzzpy_py.fuzzyelement.DHFElements.intersection,
        'unions': fuzzpy_py.fuzzyelement.DHFElements.unions,
        'algeb_multiply': fuzzpy_py.fuzzyelement.DHFElements.algeb_multiply,
        'algeb_plus': fuzzpy_py.fuzzyelement.DHFElements.algeb_plus,
        'eins_multiply': fuzzpy_py.fuzzyelement.DHFElements.eins_multiply,
        'eins_plus': fuzzpy_py.fuzzyelement.DHFElements.eins_plus,
        'pos': fuzzpy_py.fuzzyelement.DHFElements.pos,
        'neg': fuzzpy_py.fuzzyelement.DHFElements.neg,
        'zero': fuzzpy_py.fuzzyelement.DHFElements.zero,
        'distance': qhfeDistance,
    },
    'qrungfn': {
        'type': qrungfn,
        'random': randomFN,
        'generator': FNGenerator,
        'convert_str': str_to_fn,
        'intersection': fuzzpy_py.fuzzyelement.FNumbers.intersection,
        'unions': fuzzpy_py.fuzzyelement.FNumbers.unions,
        'algeb_multiply': fuzzpy_py.fuzzyelement.FNumbers.algeb_multiply,
        'algeb_plus': fuzzpy_py.fuzzyelement.FNumbers.algeb_plus,
        'eins_multiply': fuzzpy_py.fuzzyelement.FNumbers.eins_multiply,
        'eins_plus': fuzzpy_py.fuzzyelement.FNumbers.eins_plus,
        'pos': fuzzpy_py.fuzzyelement.FNumbers.pos,
        'neg': fuzzpy_py.fuzzyelement.FNumbers.neg,
        'zero': fuzzpy_py.fuzzyelement.FNumbers.zero,
        'distance': qfnDistance,
    },
    'qrungivfn': {
        'type': qrungivfn,
        'random': randomIVFN,
        'generator': IVFNGenerator,
        'convert_str': str_to_ivfn,
        'intersection': fuzzpy_py.fuzzyelement.IVFNumbers.intersection,
        'unions': fuzzpy_py.fuzzyelement.IVFNumbers.unions,
        'algeb_multiply': fuzzpy_py.fuzzyelement.IVFNumbers.algeb_multiply,
        'algeb_plus': fuzzpy_py.fuzzyelement.IVFNumbers.algeb_plus,
        'eins_multiply': fuzzpy_py.fuzzyelement.IVFNumbers.eins_multiply,
        'eins_plus': fuzzpy_py.fuzzyelement.IVFNumbers.eins_plus,
        'pos': fuzzpy_py.fuzzyelement.IVFNumbers.pos,
        'neg': fuzzpy_py.fuzzyelement.IVFNumbers.neg,
        'zero': fuzzpy_py.fuzzyelement.IVFNumbers.zero,
        'distance': qivfnDistance,
    }
}

if __name__ == '__main__':
    save_dict(d)
