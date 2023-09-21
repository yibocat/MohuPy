#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/24 下午9:30
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets

class global_config:
    # global GLOBALS_DICT
    def __init__(self):
        self.GLOBALS_DICT = {}

    def global_set(self, name, value):
        try:
            self.GLOBALS_DICT[name] = value
            return True
        except KeyError:
            return False

    def global_get(self, name):
        try:
            return self.GLOBALS_DICT[name]
        except KeyError:
            return "Not Found"

    def global_dict(self):
        return self.GLOBALS_DICT


from .fuzzy_element import qrungifn
from .fuzzymath import (intersection, unions,
                        algeb_multiply, algeb_plus,
                        eins_multiply, eins_plus)
from .toolkit import (random, str_to_fn, pos, neg, zero)

config = global_config()
dic = dict()
dic['type'] = qrungifn
dic['intersection'] = intersection
dic['unions'] = unions
dic['algeb_multiply'] = algeb_multiply
dic['algeb_plus'] = algeb_plus
dic['eins_multiply'] = eins_multiply
dic['eins_plus'] = eins_plus
dic['random'] = random
dic['convert_str'] = str_to_fn
dic['pos'] = pos
dic['neg'] = neg
dic['zero'] = zero

config.global_set('qrungifn', dic)
