import numpy as np
from scipy.optimize import fsolve


class fuzzm(object):
    __fs = None
    __meas = None
    __lambda = 0.

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
        dic = {
            'dirac': 'Dirac measure',
            'dual': 'dual fuzzy measure',
            'add': 'additive fuzzy measure',
            'symmetric': 'symmetric fuzzy measure',
            'lambda': 'lambda fuzzy measure'
        }

        return 'Fuzzy measure: %s.' % dic[self.__meas] + '\n' + \
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

    def getlambda(self):
        if self.__meas == 'lambda':
            return np.float_(self.__lambda)
        else:
            return None

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
        ss = self.subsets()
        fmeas = np.array([])
        for s in ss:
            fmeas = np.append(fmeas, self.__call__(s))
        t = np.stack((ss, fmeas), axis=1)
        # t = dict(zip(ss, fmeas))

        return t


def lamda(sets):
    """
        The equation for computing the lambda fuzzy measure
        parameter, which returns an anonymous function.

        The calculation of lambda needs to use optimize.fsolve
        optimization calculation of the scipy library, because
        the equation is a high-order nonlinear equation.

        The initial value of lambda optimization calculation
        is usually 1, as shown in the example below.

        Parameters
        ----------
            sets: ndarray or list
                fuzzy density list: fuzzy measures for single elements

        Returns
        -------
            function: anonymous function
                Equation of lambda fuzzy measure parameter

        Examples
        --------
            In [1]: x = np.array([0.4,0.25,0.37,0.2])
            In [2]: scipy.optimize.fsolve(lamda(x), np.array(-1))
            Out[2]: array(-0.4403)
    """
    return lambda lam: np.prod(1 + lam * sets) - lam - 1
