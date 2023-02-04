#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/2 上午1:58
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzyKit

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

__dict_file = '../config/dictionary.pkl'


def load_dict(info=True):
    if info:
        print('Loading configuration file...')
    with open(__dict_file, 'rb') as f:
        dicts = pickle.load(f)
    if info:
        print('Loaded successfully!')
    return dicts


def save_dict(dd):
    print('Saving configuration file...')
    with open(__dict_file, 'wb') as f:
        pickle.dump(dd, f)
    print('Saved successfully!')
