#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/1 下午5:37
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzyKit

# from fuzzyelement.DHFElements import qrunghfe


# def dhfwa(sets, weight):
#     """
#
#     """
#     q = sets[0].qrung
#
#     dlist = []
#     if weight.sum() == 0:
#         for i in range(len(sets)):
#             dlist.append(sets[i])
#     else:
#         assert len(sets) == len(weight), 'The number of sets is not equal to the number of weight!'
#         for i in range(len(sets)):
#             dlist.append(sets[i].Fast_Algebraic_Times(weight[i]))
#
#     if q == 1:
#         aggDHFE = DHIFE([0], [1])
#     elif q == 2:
#         aggDHFE = DHPFE([0], [1])
#     else:
#         aggDHFE = DHFFE([0], [1])
#     for agg in dlist:
#         aggDHFE = DHFFE_Algebraic_Plus(agg, aggDHFE)
#     return aggDHFE
