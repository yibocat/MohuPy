#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/21 上午4:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets
from mohusets.generator.memfunc import memfunc

fdict = ['sigmf', 'trimf', 'zmf', 'trapmf', 'smf', 'gaussmf', 'gauss2mf', 'gbellmf']
params = [
    [[13, 0.23], [11, 0.41]],                           # sigmf parameters: 2mf
    [[0.22, 0.31, 0.56], [0.44, 0.59, 0.71]],           # trimf parameters: 2mf
    [[0.22, 0.61], [0.57, 0.93]],                       # zmf parameters: 2mf
    [[0.2, 0.3, 0.4, 0.5], [0.2, 0.4, 0.6, 0.8]],       # trapmf parameters: 2mf
    [[0.3, 0.55], [0.61, 0.77]],                        # smf parameters: 2mf
    [[0.35, 0.11], [0.22, 0.16]],                       # gaussmf parameters: 2mf
    [[0.33, 0.51, 0.46, 0.71], [0.10, 0.63, 0.22, 0.71]],   # gauss2mf parameters: 2mf
    [[0.44, 0.31, 0.6], [0.33, 0.71, 0.28]],  # gbellmf parameters: 1mf and 1nmf
]
if __name__ == '__main__':
    i = 3
    f = memfunc(fdict[i], params[i])
    print(f)
    f.plot()
