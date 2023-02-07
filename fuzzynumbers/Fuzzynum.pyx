cdef class Fuzzynum:

    def __init__(self):
        pass

    cpdef double score(self):
        pass

    cpdef double accuracy(self):
        pass

    cpdef double indeterminacy(self):
        pass

    cpdef isEmpty(self):
        pass

    cpdef isEmpty_half(self):
        pass

    cpdef isLegal(self):
        pass

    cpdef complement(self):
        pass