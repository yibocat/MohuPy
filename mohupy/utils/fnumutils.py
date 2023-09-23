

#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/9/21 下午8:25
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

import re
from ..config import import_cupy_lib

from ..mohunums import mohunum

np = import_cupy_lib()


def rand_num(q=1, mtype='fn'):
    """
        Generate a random fuzzy number.

        Parameters
        ----------
            q : int
            mtype : str
                The type of fuzzy number
                Optional: 'fn','ivfn'

        Returns
        -------
            mohunum
    """
    if mtype == 'fn':
        newfn = mohunum(q, 0., 0.)
        newfn._mohunum__MEMSHIP_KEY = False
        while True:
            newfn.md = np.random.rand(1)
            newfn.nmd = np.random.rand(1)
            if newfn.md ** q + newfn.nmd ** q <= 1:
                break
        newfn._mohunum__MEMSHIP_KEY = True
        return newfn
    if mtype == 'ivfn':
        newfn = mohunum(q, [0., 0.], [0., 0.])
        newfn._mohunum__MEMSHIP_KEY = False
        while True:
            newfn.md = [np.random.rand(1)[0], np.random.rand(1)[0]]
            newfn.nmd = [np.random.rand(1)[0], np.random.rand(1)[0]]
            if newfn.is_valid():
                break
        newfn._mohunum__MEMSHIP_KEY = True
        return newfn

    raise ValueError('ERROR: Error mtype of fuzzy number.')


def str_to_mohunum(s: str, q, mtype='fn'):
    """
        Convert a string to a fuzzy number.

        Parameters
        ----------
            s : str
            q : int
            mtype: str
                The type of fuzzy number
                Optional: 'fn','ivfn'

        Returns
        -------
            mohunum

        Notes: When the input data is 0, it should be set to 0.
        Q-rung fuzzy convert function accepts the form: [x,x]
    """
    if mtype == 'fn':
        newfn = mohunum(q, 0., 0.)
        t = re.findall(r'^\[(\d.*?\d)]$', s)
        assert len(t) == 1, \
            'ERROR: data format error.'
        x = re.findall(r'\d.?\d*', t[0])
        assert len(x) == 2, \
            'ERROR: data format error.'
        newfn._mohunum__MEMSHIP_KEY = False
        newfn.md = np.asarray(float(x[0]))
        newfn.nmd = np.asarray(float(x[1]))
        newfn._mohunum__MEMSHIP_KEY = True
        assert newfn.is_valid(), \
            'ERROR: The data format is correct, but the data is invalid.'
        return newfn
    if mtype == 'ivfn':
        newfn = mohunum(q, [0., 0.], [0., 0.])
        t2 = re.findall(r'\[(\d.*?\d)]', s)
        assert len(t2) == 2, \
            'ERROR: data format error.'
        md = re.findall(r'\d.?\d*', t2[0])
        nmd = re.findall(r'\d.?\d*', t2[1])
        assert len(md) == 2 and len(nmd) == 2, \
            'ERROR: data format error.'

        m = [float(md[0]), float(md[1])]
        n = [float(nmd[0]), float(nmd[1])]
        newfn._mohunum__MEMSHIP_KEY = False
        newfn.md = m
        newfn.nmd = n
        newfn._mohunum__MEMSHIP_KEY = True
        assert newfn.is_valid(), \
            'ERROR: Invalid data! Illegal Q-rung interval-valued fuzzy number.'
        return newfn
    raise ValueError('ERROR: Error type of fuzzy number.')


def distance(d1: mohunum, d2: mohunum, l: (int, np.int_), indeterminacy=True):
    """
        The generalized distance function for two fuzzy elements.
        The parameter 'l' is the generalized distance function parameter.
        'l=1' indicates the Hamming distance and 'l=2' indicates the
        Euclidean distance.

        Parameters
        ----------
            d1 : mohunum
                The first fuzzy number.
            d2 : mohunum
                The second fuzzy number.
            l : int, np.int_
                The generalized distance function parameter.
                'l=1' indicates the Hamming distance and 'l=2' indicates
                the Euclidean distance.
            indeterminacy : bool
                If True, the indeterminacy of the two fuzzy numbers will be considered.
                If False, the indeterminacy of the two fuzzy numbers will not be considered.

        Returns
        -------
            float
                The generalized distance between of two fuzzy numbers.

        References
        ----------
            [1] J. S, “Ordering of interval-valued Fermatean fuzzy sets and its
                applications,” Expert Syst Appl, vol. 185, p. 115613, 2021,
                doi: 10.1016/j.eswa.2021.115613.
            [2] Z. Xu, “A method based on distance measure for interval-valued
                intuitionistic fuzzy group decision-making,” Inform Sciences,
                vol. 180, no. 1, pp. 181–190, 2010, doi: 10.1016/j.ins.2009.09.005.

        Example
        -------
            In [1]: f1 = mohunum(2, 0.5, 0.45)
            In [2]: f2 = mohunum(2, 0.67, 0.2)
            In [3]: distance(f1, f2, 2)
            Out[3]: 0.18342903259844126

    """
    assert d1.qrung == d2.qrung, \
        'ERROR: The q rung of two fuzzy numbers must be equal.'
    assert d1.mtype == d2.mtype, \
        'ERROR: The type of two fuzzy numbers must be same.'
    assert l > 0, \
        'ERROR: The value of l must be greater than 0.'
    mtype = d1.mtype
    q = d1.qrung
    pi1 = d1.indeterminacy
    pi2 = d2.indeterminacy
    pi = np.fabs(pi1 ** q - pi2 ** q) ** l
    if mtype == 'fn':
        if indeterminacy:
            return (0.5 * (np.fabs(d1.md ** q - d2.md ** q) ** l +
                           np.fabs(d1.nmd ** q - d2.nmd ** q) ** l + pi)) ** (1 / l)
        else:
            return (0.5 * (np.fabs(d1.md ** q - d2.md ** q) ** l +
                           np.fabs(d1.nmd ** q - d2.nmd ** q) ** l)) ** (1 / l)
    if mtype == 'ivfn':
        if indeterminacy:
            return 0.25 * (
                    np.fabs(d1.md[0] ** q - d2.md[0] ** q) ** l +
                    np.fabs(d1.md[1] ** q - d2.md[1] ** q) ** l +
                    np.fabs(d1.nmd[0] ** q - d2.nmd[0] ** q) ** l +
                    np.fabs(d1.nmd[1] ** q - d2.nmd[1] ** q) ** l + pi) ** (1 / l)
        else:
            return 0.25 * (
                    np.fabs(d1.md[0] ** q - d2.md[0] ** q) ** l +
                    np.fabs(d1.md[1] ** q - d2.md[1] ** q) ** l +
                    np.fabs(d1.nmd[0] ** q - d2.nmd[0] ** q) ** l +
                    np.fabs(d1.nmd[1] ** q - d2.nmd[1] ** q) ** l) ** (1 / l)
    raise ValueError('ERROR: Error type of fuzzy number.')
