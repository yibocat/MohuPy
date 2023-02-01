#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/1 下午5:37
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzyKit

from fuzzysets.sets import fuzzyset as fs
import library as fl


if __name__ == '__main__':
    s6 = "[[0.6,0.7],[0.1,0.]]"    # interval-valued number
    fl.qrungivfn_convert(s6, 2)
