"""
    This file is a fuzzy set configuration information IO file, which stores
    the existing fuzzy set configuration information into the pkl file. The
    storage format is a dictionary type. The stored configuration information
    dictionary is as follows:

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

    The dictionary here is a nested dictionary. Each key is a fuzzy element
    type description. The value is a dictionary containing configuration
    information.
    Currently, contains the following configuration information:

    type:   type, the type of Fuzzy Sets
    random: function,  function for randomly generating fuzzy elements'
    generator: type, membership function generator
    convert_str: function, function for converting string to fuzzy element
"""
import pickle
# from dictionary import save_dict

# from fuzzpy import fuzzynumbers
import fuzzynumbers.qrungdhfe
import fuzzynumbers.qrungifn
import fuzzynumbers.qrungivfn

from fuzzynumbers.__fuzzmath import qdfe_d, qifn_d, qivfn_d
from generator import dhfegener, ifngener, ivfngener

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
        'fuzzgener': dhfegener,
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
        'fuzzgener': ifngener,
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
        'fuzzgener': ivfngener,
    }
}


def load_dict(dic, info=True):
    if info:
        print('Loading configuration file...')
    with open(dic, 'rb') as f:
        dicts = pickle.load(f)
    if info:
        print('Loaded successfully!')
    return dicts


def save_dict(dic):
    print('Saving configuration file...')
    with open(dic, 'wb') as f:
        pickle.dump(d, f)
    print('Saved successfully!')

