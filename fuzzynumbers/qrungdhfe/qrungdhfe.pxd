# import numpy as np
# cimport numpy as np
# from libcpp cimport bool
# from ..Fuzzynum cimport Fuzzynum
#
# cdef class qrungdhfe(Fuzzynum):
#     cdef int __qrung
#     cdef str __parent
#     cdef double __score
#     cdef double __accuracy
#     cdef double __indeterminacy
#     cdef np.ndarray __md
#     cdef np.ndarray __nmd
#     cdef public:
#         int qrung
#         np.ndarray md
#         np.ndarray nmd
#         str parent
#         double score
#         double accuracy
#         double indeterminacy
#
#     cpdef set_md(self, value)
#     cpdef set_nmd(self, value)
#     cpdef isEmpty(self)
#     cpdef isEmpty_half(self)
#     cpdef isLegal(self)
#     cpdef comp(self)
#     cpdef qsort(self)
#     cpdef algeb_power(self, double l)
#     cpdef algeb_times(self, double l)
#     cpdef eins_power(self, double l)
#     cpdef eins_times(self, double l)