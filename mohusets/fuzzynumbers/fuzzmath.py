#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/21 上午4:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets

import mohusets.fuzzynumbers.config
from . import fuzz_global as glb


def generalized_distance(d1, d2, l=1., t=1., indeterminacy=True):
    """
        Generalized distance between two fuzzy elements.

        Parameters
        ----------
        d1 : fuzzynumbers.
            First fuzzy element.
        d2 : fuzzynumbers.
            Second fuzzy element.
        l : float, optional
            Likelihood parameter. The default is 1.0.
        t : float, optional
            Transitivity parameter. The default is 1.0.
        indeterminacy : bool, optional
            If True, the indeterminacy of the two fuzzy elements is considered. The default is True.

        Returns
        -------
        float
            Generalized distance between two fuzzy elements.

        Examples
        --------
            In [1]: import fuzzynumbers
            In [2]: x1 = fuzzynumbers.qrungdhfe(3, [0.5,0.6], [0.3,0.7])
            In [3]: x2 = fuzzynumbers.qrungdhfe(3, [0.4,0.1], [0.8])
            In [4]: fuzzynumbers.generalized_distance(x1, x2)
            Out[4]: 0.327
    """
    assert l > 0., 'ERROR: Generalized distance parameter error, parameter must be > 0.'
    assert d1.__class__.__name__ == d2.__class__.__name__, 'the two fuzzy element types are not same.'
    assert d1.__class__.__name__ in glb.global_dict(), 'the fuzzy element type does not exist.'

    typ = d1.__class__.__name__
    if typ == 'qrungdhfe':
        return glb.global_get(typ)['distance'](d1, d2, l, t, indeterminacy)
    else:
        return glb.global_get(typ)['distance'](d2, d1, l, indeterminacy)


def random(q, fn, n=5):
    """
        Generate a random element from a fuzzy element.

        Parameters
        ----------
        fn : str
            Fuzzy element type.
        q : int
            Q-rung of the fuzzy element.
        n : int, optional
            Number of membership or non-membership degree. The default is 5. Only works for qrungdhfe.

        Returns
        -------
        fuzzynumbers.
            Random element.
    """
    assert fn in glb.global_dict(), 'the fuzzy element type does not exist.'

    if fn == 'qrungdhfe':
        return glb.global_get(fn)['random'](q, n)
    else:
        return glb.global_get(fn)['random'](q)


def intersection(fn1, fn2):
    """
        Intersection of two fuzzy elements.

        Parameters
        ----------
        fn1 : fuzzynumbers.
            First fuzzy element.
        fn2 : fuzzynumbers.
            Second fuzzy element.

        Returns
        -------
        fuzzynumbers.
            Intersection of two fuzzy elements.
    """
    assert fn1.__class__.__name__ in glb.global_dict(), 'the fuzzy element type does not exist.'
    assert fn2.__class__.__name__ in glb.global_dict(), 'the fuzzy element type does not exist.'
    assert fn1.__class__.__name__ == fn2.__class__.__name__, 'the two fuzzy element types are not same.'

    return glb.global_get(fn1.__class__.__name__)['intersection'](fn1, fn2)


def unions(fn1, fn2):
    """
        Union of two fuzzy elements.

        Parameters
        ----------
        fn1 : fuzzynumbers.
            First fuzzy element.
        fn2 : fuzzynumbers.
            Second fuzzy element.

        Returns
        -------
        fuzzynumbers.
            Union of two fuzzy elements.
    """
    assert fn1.__class__.__name__ in glb.global_dict(), 'the fuzzy element type does not exist.'
    assert fn2.__class__.__name__ in glb.global_dict(), 'the fuzzy element type does not exist.'
    assert fn1.__class__.__name__ == fn2.__class__.__name__, 'the two fuzzy element types are not same.'

    return glb.global_get(fn1.__class__.__name__)['unions'](fn1, fn2)


def algeb_multiply(fn1, fn2):
    """
        Multiplication of two fuzzy elements.

        Parameters
        ----------
        fn1 : fuzzynumbers.
            First fuzzy element.
        fn2 : fuzzynumbers.
            Second fuzzy element.

        Returns
        -------
        fuzzynumbers.
            Multiplication of two fuzzy elements.
    """
    assert fn1.__class__.__name__ in glb.global_dict(), 'the fuzzy element type does not exist.'
    assert fn2.__class__.__name__ in glb.global_dict(), 'the fuzzy element type does not exist.'
    assert fn1.__class__.__name__ == fn2.__class__.__name__, 'the two fuzzy element types are not same.'

    return glb.global_get(fn1.__class__.__name__)['algeb_multiply'](fn1, fn2)


def algeb_plus(fn1, fn2):
    """
        Addition of two fuzzy elements.

        Parameters
        ----------
        fn1 : fuzzynumbers.
            First fuzzy element.
        fn2 : fuzzynumbers.
            Second fuzzy element.

        Returns
        -------
        fuzzynumbers.
            Addition of two fuzzy elements.
    """
    assert fn1.__class__.__name__ in glb.global_dict(), 'the fuzzy element type does not exist.'
    assert fn2.__class__.__name__ in glb.global_dict(), 'the fuzzy element type does not exist.'
    assert fn1.__class__.__name__ == fn2.__class__.__name__, 'the two fuzzy element types are not same.'

    return glb.global_get(fn1.__class__.__name__)['algeb_plus'](fn1, fn2)


def eins_multiply(fn1, fn2):
    """
        Einstein multiplication of two fuzzy elements.

        Parameters
        ----------
        fn1 : fuzzynumbers.
            First fuzzy element.
        fn2 : fuzzynumbers.
            Second fuzzy element.

        Returns
        -------
        fuzzynumbers.
            Multiplication of two fuzzy elements.
    """
    assert fn1.__class__.__name__ in glb.global_dict(), 'the fuzzy element type does not exist.'
    assert fn2.__class__.__name__ in glb.global_dict(), 'the fuzzy element type does not exist.'
    assert fn1.__class__.__name__ == fn2.__class__.__name__, 'the two fuzzy element types are not same.'

    return glb.global_get(fn1.__class__.__name__)['eins_multiply'](fn1, fn2)


def eins_plus(fn1, fn2):
    """
        Einstein addition of two fuzzy elements.

        Parameters
        ----------
        fn1 : fuzzynumbers.
            First fuzzy element.
        fn2 : fuzzynumbers.
            Second fuzzy element.

        Returns
        -------
        fuzzynumbers.
            Addition of two fuzzy elements.
    """
    assert fn1.__class__.__name__ in glb.global_dict(), 'the fuzzy element type does not exist.'
    assert fn2.__class__.__name__ in glb.global_dict(), 'the fuzzy element type does not exist.'
    assert fn1.__class__.__name__ == fn2.__class__.__name__, 'the two fuzzy element types are not same.'

    return glb.global_get(fn1.__class__.__name__)['eins_plus'](fn1, fn2)


def pos(fn, q):
    """
        Positive element of a fuzzy element.

        Parameters
        ----------
        fn : str
            Fuzzy element type.
        q : int
            Q-rung of the fuzzy element.

        Returns
        -------
        fuzzynumbers.
            Positive element of a fuzzy element.
    """
    assert fn in glb.global_dict(), 'the fuzzy element type does not exist.'
    return glb.global_get(fn)['pos'](q)


def neg(fn, q):
    """
        Negative element of a fuzzy element.

        Parameters
        ----------
        fn : str
            Fuzzy element type.
        q : int
            Q-rung of the fuzzy element.

        Returns
        -------
        fuzzynumbers.
            Negative element of a fuzzy element.
    """
    assert fn in glb.global_dict(), 'the fuzzy element type does not exist.'
    return glb.global_get(fn)['neg'](q)


def zero(fn, q):
    """
        Zero element of a fuzzy element.

        Parameters
        ----------
        fn : str
            Fuzzy element type.
        q : int
            Q-rung of the fuzzy element.

        Returns
        -------
        fuzzynumbers.
            Zero element of a fuzzy element.
    """
    assert fn in glb.global_dict(), 'the fuzzy element type does not exist.'
    return glb.global_get(fn)['zero'](q)


from .__fuzzmath import normalization


def normal(d1, d2, t=1):
    """
        Normalization of two fuzzy elements.
        Normalization is mainly aimed at dual hesitant fuzzy elements.
        The parameter 't' is the risk factor of normalization process, which in
        the interval [0, 1]. 't=1' indicates optimistic normalization and
        't=0' indicates pessimistic normalization.\n
        Parameters
        ----------
        d1 : fuzzynumbers.qrungdhfe
            First fuzzy element.
        d2 : fuzzynumbers.qrungdhfe
            Second fuzzy element.
        t : float, optional
            T-value of the fuzzy element. The default is 1.

        Returns
        -------
        fuzzynumbers.
            Normalization of two fuzzy elements.
    """
    assert d1.__class__.__name__ == d2.__class__.__name__, 'the two fuzzy element types are not same.'
    assert d1.__class__.__name__ in glb.global_dict(), 'the fuzzy element type does not exist.'
    assert d1.__class__.__name__ == 'qrungdhfe', 'the fuzzy element type is not qrungdhfe.'

    return normalization(d1, d2, t)
