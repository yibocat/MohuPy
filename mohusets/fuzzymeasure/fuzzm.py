#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/21 上午4:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets

import re
import numpy as np
from scipy.optimize import fsolve

from .math import lamda, subsets

import networkx

from . import hassenetworkx as hwx
from matplotlib import pyplot as plt


class fuzzm(object):
    __fs = None
    __meas = None
    __lambda = 0.
    __mobius = None
    __vector = np.array([])
    __table = None

    __dic = {
            'dirac': 'Dirac measure',
            'dual': 'dual fuzzy measure',
            'add': 'additive fuzzy measure',
            'symmetric': 'symmetric fuzzy measure',
            'lambda': 'lambda fuzzy measure'
        }

    def __init__(self, fs, meas='lambda', e=None, func=None, *args):
        # d = ['dirac', 'dual', 'add', 'symmetric', 'lambda']
        d = ['dirac', 'add', 'symmetric', 'lambda']
        assert meas in d, 'fuzzy measure does not exist.'
        self.__meas = meas
        self.__fs = np.asarray(fs)

        if meas == 'dirac':
            assert e is not None, 'e must be specified for dirac measure.'
            self.e = e
        if meas == 'add':
            assert np.round(fs.sum(), 5) == 1., 'set must sum to 1.'
        if meas == 'symmetric':
            if func is not None:
                self.func = func
                self.args = args
            else:
                self.func = None
                self.args = None
        if meas == 'lambda':
            self.__lambda = fsolve(lamda(self.__fs), np.array(-1))

    def __repr__(self):
        return 'Fuzzy measure: %s.' % self.__dic[self.__meas] + '\n' + \
            'The set: ' + str(self.__fs)

    def __call__(self, sub):
        if self.__meas == 'dirac':
            return self.__Dirac_measure(sub)
        if self.__meas == 'dual':
            return self.__dual_fuzz_meas(sub)
        if self.__meas == 'add':
            return self.__add_fuzz_meas(sub)
        if self.__meas == 'symmetric':
            return self.__symmetric_fuzz_meas(sub)
        if self.__meas == 'lambda':
            return self.__lambda_fuzz_measure(sub)

    @property
    def len(self):
        return self.__fs.size

    @property
    def set(self):
        return self.__fs

    def getlambda(self):
        assert self.__meas == 'lambda', 'the fuzzy measure must be lambda fuzzy measure.'
        return np.float_(self.__lambda)

    def __Dirac_measure(self, sub):
        """
            Dirac_measure(Bool fuzzy measure). The Dirac measure is a simple
            0-1 fuzzy measure. The element and subset must be a subset of the set.
            When the element is in the subset the Dirac measure is 1. Otherwise, the
            Dirac measure is 0.
            The Dirac measure is defined as:
            Parameters
            ----------
            sub: list or ndarray
                subset of the set
            Returns
            -------
            fuzzy measure: float
        """
        assert len(np.setdiff1d(self.e, self.__fs)) == 0, 'the element is not in the set'
        assert len(np.setdiff1d(sub, self.__fs)) == 0, 'the subset is not in the set'
        return np.float_(1) if self.e in sub else np.float_(0)

    def __dual_fuzz_meas(self, sub):
        """
            The dual fuzzy measure. 1 minus fuzzy measure of the complement of a subset.
            Parameters
            ----------
            sub: list or ndarray
                subset of the set
            Returns
            -------
                fuzzy measure: ndarray or float
        """
        assert len(np.setdiff1d(sub, self.__fs)) == 0, 'sub must be a subset of set.'
        return np.float_(1 - np.setdiff1d(self.__fs, sub))

    def __add_fuzz_meas(self, sub):
        """
            The additive measure.
            Parameters
            ----------
            sub: list or ndarray
                subset of the set
            Returns
            -------
                fuzzy measure: ndarray or float
        """
        assert len(np.setdiff1d(sub, self.__fs)) == 0, 'sub must be a subset of set.'
        # assert np.sum(self.__fs) == 1, 'set must sum to 1.'
        return np.float_(np.sum(sub))

    def __symmetric_fuzz_meas(self, sub):
        """
            Symmetric fuzz measure. The parameter 'func' indicates a monotone
            non-decreasing function and the parameter 'args' are passed to the
            function. In general, the argument to 'func' is the ratio of the
            number of elements in the subset to the number of elements in the
            set as a whole. When 'func' is not specified, the ratio is returned
            directly.
            Parameters
            ----------
            sub: list or ndarray
                The subset of the set.
            func: function, optional
                The function to be used.

            Returns
            -------
                The fuzz measure of the subset.
        """
        assert len(np.setdiff1d(sub, self.__fs)) == 0, 'sub must be a subset of set.'
        ratio = np.array(sub).size / np.array(self.__fs).size
        if self.func is None:
            return np.float_(ratio)
        else:
            return np.float_(self.func(ratio, self.args))

    def __lambda_fuzz_measure(self, sub):
        """
            The lambda fuzzy measure function.
            We have a subset of the fuzzy measure sets, then use the
            function to calculate the fuzzy measure of the subset.
            The parameter lambda can put in this function, but when
            this function is called, fsolve must be executed every
            time, which will greatly reduce the calculation efficiency.
            So the lambda is passed into the function as a parameter.

            Parameters
            ----------
                sub: ndarray or list
                    fuzzy density subset
            Returns
            -------
                float: fuzzy measure of the subset

            Examples
            --------
                In [1]: fuzz_den = np.array([0.4,0.25,0.37,0.2])
                In [2]: lambda_fuzzy_measure([0.25,0.37], fuzz_den, lambda)
                Out[2]: 0.5793
        """

        f = np.asarray(sub)
        assert len(np.setdiff1d(f, self.__fs)) == 0, 'ERROR! The subset is not an element of the set.'
        if np.round(self.__lambda, 5) == 0:
            return np.float_(f.sum())
        else:
            return np.float_((np.prod(1 + self.__lambda * f) - 1) / self.__lambda)

    def subsets(self):
        """
            Computes all subsets of a set

            Returns
            -------
            subsets: list
                all subsets of a collection
        """
        ans = []
        n = 1 << len(self.__fs)
        for i in range(n):
            res = np.array([])
            num = i
            idx = 0
            while num:
                if num & 1:
                    res = np.append(res, self.__fs[idx])
                num >>= 1
                idx += 1
            ans.append(res)
        return np.asarray(ans, dtype=object)

    def meas_table(self):
        """
            Show all subsets and their fuzzy measure values
            Returns
            -------
            self.__table: ndarray
                fuzzy measure table
        """
        ss = self.subsets()
        fmeas = np.array([])
        for s in ss:
            fmeas = np.append(fmeas, self.__call__(s))
        self.__table = np.stack((ss, fmeas), axis=1)
        return self.__table

    def mobius_table(self):
        """
            Fuzzy measure table of Möbius Representation
            Returns
            -------
            self.__mobius: ndarray
                fuzzy measure table of Möbius Representation
        """
        ss = self.subsets()
        fmeas = np.array([])
        for s in ss:
            fmeas = np.append(fmeas, self.mobius_transform(s))
        self.__mobius = np.stack((ss, fmeas), axis=1)
        return self.__mobius

    def mobius_transform(self, A):
        """
            Mobius transform of the fuzzy measure

            Parameters
            ----------
            A: ndarray or list
                fuzzy measure set

            Returns
            -------
            A: ndarray or list
                mobius transform of a fuzzy measure set
        """
        # meas = self.__init__()
        trans = np.array([])
        for B in subsets(A):
            ceof = (-1) ** np.setdiff1d(A, B).size
            trans = np.append(trans, ceof * self(B))
        return np.sum(trans)

    def zeta_transform(self, A):
        """
            The Möbius transformation is invertible, and one recovers
            μ by using its inverse, called Zeta transform.

            Note: the zeta_transform is equal to the fuzzy measure value.
            In other words, zeta_transform(A) equals self.__call__(A),
            where A is a subset of the fuzzy measure set.

            Examples:
            --------
                In [1]: s = np.array([0.4,0.25,0.37,0.2])
                In [2]: x = fuzzm(s)
                In [3]: x.zeta_transform([0.4,0.25])==x([0.4,0.25])
                Out[3]: True

            Parameters
            ----------
            A: list or ndarray
                subset of the set

            Returns
            -------
            zeta: numpy.float_
                Zeta transform of Möbius Representation
        """
        mm = np.array([])
        for t in subsets(A):
            mm = np.append(mm, self.mobius_transform(t))
        return np.sum(mm)

    def vector(self):
        """
            Returns the vector representation of the fuzzy measure
            Returns
            -------
            v: numpy.float_
                vector representation of the fuzzy measure
        """
        for x in self.subsets():
            self.__vector = np.append(self.__vector, self.__call__(x))
        return self.__vector

    def subdicts(self, chara='C', reserve=4):
        """
            Returns the dictionary representation of the fuzzy measure power set
            Parameters
            ----------
                chara: str
                    character representation of the fuzzy measure
                reserve: int
                    Keep 'reserve' digits after the decimal point

            Returns
            -------
                d: dict
                    dictionary representation of the fuzzy measure
        """
        def _subsets(nums):
            ans = []
            n = 1 << len(nums)
            for i in range(n):
                res = []
                num = i
                idx = 0
                while num:
                    if num & 1:
                        res.append(nums[idx])
                    num >>= 1
                    idx += 1
                ans.append(str(res))
            return ans

        def _conversion(sttr):
            tss = re.findall(r'\w\d', sttr)
            sp = tss[0]
            for i in tss[1:]:
                sp += ','+i
            return sp

        n = self.__fs.size
        attributes = []
        for i in range(n):
            attributes.append(chara+str(i+1))

        subset_attributes = _subsets(attributes)
        fuzzy_measure = np.round(self.vector(), reserve).tolist()

        sub_att = ['{}']
        for t in subset_attributes[1:]:
            sub_att.append(_conversion(t))

        subbs = dict(zip(sub_att, fuzzy_measure))
        return subbs

    def dicts(self, chara='C'):
        """
            Returns the dictionary representation of the fuzzy measure
            Parameters
            ----------
                chara: str
                    character representation of the fuzzy measure

            Returns
            -------
                d: dict
                    dictionary representation of the fuzzy measure
        """
        n = self.__fs.size
        attributes = []
        for i in range(n):
            attributes.append(chara+str(i+1))

        fuzzdd = dict(zip(attributes, self.__fs))

        return fuzzdd

    def hasse_diagram(self, node_char='C', node_size=85000, save_path=None, figsize=(18, 12), fontsize=9, transparency=0.55):
        def _search_subset(pattern, st):
            """
                判断子集，在画 hasse 图时的边有用
            """
            if re.search(pattern, st) is not None or pattern == '{}':
                return True
            else:
                return False
        t = self                                    # 创建一个模糊测度对象
        dd = t.subdicts(chara=node_char)            # 得到模糊测度字典

        keys = []                                   # 模糊测度字典的键列表
        for i in dd.keys():
            keys.append(i)

        values = np.array([])                       # 模糊测度字典的值列表
        for j in dd.values():
            values = np.append(values, j)

        def value(v):
            return (v/np.sum(values))*node_size

        subset_relationships = [(s1+'\n'+str(dd[s1]), s2+'\n'+str(dd[s2]))
                                for s1 in dd.keys() for s2 in dd.keys()
                                if ((s1 != s2) and _search_subset(s1, s2))]   # 得到所有子集间的关系，即 hasse 的边

        Graph = networkx.DiGraph()
        Graph.add_nodes_from([s+'\n'+str(dd[s]) for s in dd])
        Graph.add_edges_from(subset_relationships)
        hwx.transitivity_elimination(Graph)
        # Plotting with automated / default layering
        plt.figure(figsize=figsize)
        networkx.draw_networkx(Graph,
                               node_size=[value(dd[node]) for node in keys],
                               pos=hwx.layout(Graph),
                               alpha=transparency,
                               font_size=fontsize,
                               font_family='Times New Roman',
                               font_weight='bold',
                               font_color='black')

        plt.axis('off')
        if save_path is not None:
            try:
                plt.savefig(save_path, bbox_inches='tight')
                print('Saved successfully!')
            except IOError:
                print('Save failed:')
        plt.show()
