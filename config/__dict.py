#  Copyright (c) yibocat 2023 All Rights Reserved
#  Date: 2023/1/31 上午10:56
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzyKit

"""
    The fuzzy element type regedit stores some existing
    fuzzy set configuration information.
"""
from fuzzyelement.DHFElements import qrunghfe, randomQHF, str_to_hfe
from fuzzyelement.FNumbers import qrungfn, randomFN, str_to_fn
from fuzzyelement.IVFNumbers import qrungivfn, randomIVFN, str_to_ivfn

from generator.DHFEGenerator import DHFEGenerator
from generator.FNGenerator import FNGenerator
from generator.IVFNGenerator import IVFNGenerator

__dict = {
    'qrunghfe': {
        'type': qrunghfe,
        'random': randomQHF,
        'generator': DHFEGenerator,
        'convert_str': str_to_hfe},
    'qrungfn': {
        'type': qrungfn,
        'random': randomFN,
        'generator': FNGenerator,
        'convert_str': str_to_fn},
    'qrungivfn': {
        'type': qrungivfn,
        'random': randomIVFN,
        'generator': IVFNGenerator,
        'convert_str': str_to_ivfn}
}
