#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/10/1 下午9:57
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import mohupy as mp

if __name__ == '__main__':
    t1 = mp.random(3, 'qrofn', 3,5)
    t2 = mp.random(3, 'qrofn', 5,4)
    print(t1@t2)
