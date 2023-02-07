cdef class Fuzzynum:

    cpdef double score(self)
    cpdef double accuracy(self)
    cpdef double indeterminacy(self)
    cpdef isEmpty(self)
    cpdef isEmpty_half(self)
    cpdef isLegal(self)
    cpdef complement(self)

