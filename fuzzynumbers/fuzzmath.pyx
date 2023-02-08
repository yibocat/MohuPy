
from config import load_dict
d = load_dict(False)

cpdef double generalized_distance(d1, d2, double l=1., double t=1., indeterminacy=True):
    assert l > 0, 'ERROR: Generalized distance parameter error, parameter must be > 0.'
    assert d1.__class__.__name__ == d2.__class__.__name__ and \
            d1.__class__.__name__ in d, 'The two fuzzy element types are not the same or are incorrect.'

    cdef str typ
    typ = d1.__class__.__name__
    if typ == 'qrungdhfe':
        return d[typ]['distance'](d1, d2, l, t, indeterminacy)
    else:
        return d[typ]['distance'](d2, d1, l, indeterminacy)
