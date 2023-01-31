#  Copyright (c) yibocat 2023 All Rights Reserved
#  Date: 2023/1/31 上午11:12
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzyKit

from fuzzysets.sets import fuzzyset as fs
import library as fl


if __name__ == '__main__':
    s6 = "[[0.6,0.7],[0.1,0.]]"    # interval-valued number
    fl.qrungivfn_convert(s6, 2)
