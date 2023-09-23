#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/9/21 下午8:25
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: MohuPy

from .config import import_cupy_lib, import_cudf_lib
from matplotlib import pyplot as plt

np = import_cupy_lib()
pd = import_cudf_lib()


class mohuset(object):
    """
        Mohuset class is a fuzzy set class of fuzzy number. This class contains two
            type of fuzzy numbers(currently): q-rung orthopair fuzzy number and q-rung
            orthopair interval-valued fuzzy number. The fuzzy set here can not only be
            regarded as a set, but also as a high-order fuzzy vector or high-order
            fuzzy tensor. It includes not only logical operations on sets, but also
            high-order mathematical operations.

        Private Attributes
        -----------------
            __qrung : int       The q-rung of the fuzzy set.
            __shape : tuple     The shape of the fuzzy set
            __mtype : str       The type of the fuzzy set. Mainly the type of fuzzy
                                set elements
            __ndim : int        The dimension of the fuzzy set.
            __size : int        The size of the fuzzy set.
            __set : np.ndarray  The set of the fuzzy set.

        Public Attributes
        -----------------
            qrung : int         The q-rung of the fuzzy set.

            mtype : str         The type of the fuzzy set. Mainly the type of fuzzy

            ndim : int          The dimension of the fuzzy set.

            size : int          The size of the fuzzy set.

            set : np.ndarray    The set of the fuzzy set.

            shape : tuple       The shape of the fuzzy set.

            md: np.ndarray      The membership degree matrix of the fuzzy set.

            nmd: np.ndarray     The non-membership degree matrix of the fuzzy set.

            mat: pd.DataFrame   The set matrix of the fuzzy set.

            score: np.ndarray   The score matrix of the fuzzy set.

            T: mohuset.T        The transpose of the fuzzy set.


        Methods
        --------------
            __getitem__(self, item):    Return the element of the fuzzy set. This
                method treats the fuzzy set class as a higher-order tensor. Return a
                fuzzy number directly through the coordinates.

            __len__(self):              Return the size of the fuzzy set.

            __repr__(self):             Return a string representation of the fuzzy set.

            __str__(self):              Return a string representation of the fuzzy set.

            __add__(self, other):       Add two fuzzy sets.

            __sub__(self, other):       Subtract two fuzzy sets.

            __mul__(self, other):       Multiply two fuzzy sets.

            __truediv__(self, other):   Divide two fuzzy sets.

            __pow__(self, other):       Raise to the power of two fuzzy sets.

            __matmul__(self, other):    Matrix multiplication of two fuzzy sets.


            setter(self, s, shape, ndim, size):
                                        Set the fuzzy set's set, shape, ndim and size.

            random(self, *n):           Generate a random fuzzy set with *n shape.

            ravel(self):                Reshapes the fuzzy set to a 1-dimensional array.

            append(self, other):        Append a fuzzy number to the fuzzy set.

            remove(self, other):        Remove a fuzzy number from the fuzzy set.

            pop(self, i):               Remove a fuzzy number from the fuzzy set by index.

            reshsape(self, *n):         Reshapes the fuzzy set to a *n shape set.

            clear(self):                Clear the fuzzy set.

            max(self):                  Return the maximum element of the fuzzy set.

            min(self):                  Return the minimum element of the fuzzy set.

            fmax(self):                 Return the maximum element of the fuzzy set with func.

            fmin(self):                 Return the minimum element of the fuzzy set with func.

            sum(self):                  Return the sum of all elements of the fuzzy set.

            savez(self, path):          Save the fuzzy set to a .npz file.

            loadz(self, path):          Load the fuzzy set from a.npz file.

            plot(self):                 Plot all fuzzy element of the fuzzy set.

    """
    __qrung = None
    __shape = None
    __mtype = None
    __ndim = None
    __size = 0
    __set = np.array([], dtype=object)

    def __init__(self, q=None, mtype='fn'):
        if q is not None or mtype is None:
            assert q > 0, \
                'ERROR: qrung must be greater than 0.'
            self.__qrung = q
            self.__mtype = mtype
            self.__set = np.array([], dtype=object)
            self.__shape = None
            self.__ndim = 0
            self.__size = 0
        else:
            pass

    def __repr__(self):
        return np.array_repr(self.__set) + \
            '\n mtype=%s, qrung=%s, shape=%s, size=%s' \
            % (self.__mtype, self.__qrung, self.__shape, self.__size)

    def __str__(self):
        return str(self.__set)

    def __getitem__(self, item):
        return self.__set[item]

    def __len__(self):
        return self.__size

    @property
    def qrung(self):
        return self.__qrung

    @property
    def mtype(self):
        return self.__mtype

    @property
    def shape(self):
        return self.__shape

    @property
    def ndim(self):
        return self.__ndim

    @property
    def size(self):
        return self.__size

    @property
    def set(self):
        return self.__set

    @property
    def md(self):
        def __md(x):
            if x.mtype == 'fn':
                return x.md
            if x.mtype == 'ivfn':
                return np.array(x.md, dtype=list)

        vec_func = np.vectorize(__md)
        return vec_func(self.__set)

    @property
    def nmd(self):
        def __nmd(x):
            if x.mtype == 'fn':
                return x.nmd
            if x.mtype == 'ivfn':
                return np.array(x.nmd, dtype=list)

        vec_func = np.vectorize(__nmd)
        return vec_func(self.__set)

    @property
    def mat(self):
        """
            Display the matrix of the fuzzy set.

            Note that this method only exhibits 1- and 2-dimensional fuzzy sets.
            Since this method is based on pandas.DataFrame, it does not support
            high-dimensional display for the time being.

            Parameters
            ----------

            Returns
            -------
                the matrix of the fuzzy set
        """
        assert self.__ndim == 1 or self.__ndim == 2, \
            'ERROR: Only 1- and 2-dimensional fuzzy sets are supported.'
        return pd.DataFrame(self.__set.tolist())

    @property
    def score(self):
        """
            Display the score value of the fuzzy set.

            The scores of all elements of the fuzzy set are calculated under the
            premise that the shape of the fuzzy set is consistent. In other words,
            the method calculates the score value of each blurred element while
            keeping the shape unchanged.

            Parameters
            ----------

            Returns
            -------
                The score of the fuzzy set
        """
        shape = self.__shape
        scoreset = self.__set.ravel()
        slist = np.asarray([scoreset[i].score for i in range(len(scoreset))])
        self.__set.reshape(shape)
        return slist.reshape(shape)

    @property
    def T(self):
        """
            Display the transposed matrix of the fuzzy set.

            Parameters
            ----------

            Returns
            -------
                The transposed matrix of the fuzzy set
        """
        st = self.__set
        s = st.T

        newset = mohuset(self.__qrung, self.__mtype)
        newset.__set = s
        newset.__shape = s.shape
        newset.__ndim = s.ndim
        newset.__size = s.size

        del st, s
        return newset

    def __add__(self, other):
        if isinstance(other, mohuset):
            assert other.mtype == self.__mtype, \
                'ERROR: The two fuzzy sets must be of the same type.'
            assert other.qrung == self.__qrung, \
                'ERROR: The two fuzzy sets must be of the same Q-rung.'
            assert other.shape == self.__shape, \
                'ERROR: The two fuzzy sets must be of the same shape.'
            assert other.ndim == self.__ndim, \
                'ERROR: The two fuzzy sets must be of the same ndim.'
            assert other.size == self.__size, \
                'ERROR: The two fuzzy sets must be of the same size.'

            newset = mohuset(self.__qrung, self.__mtype)
            newset.__set = self.__set + other.__set
            newset.__shape = self.__shape
            newset.__ndim = self.__ndim
            newset.__size = self.__size
            return newset
        if other.__class__.__name__ == 'mohunum':
            assert other.mtype == self.__mtype, \
                'ERROR: The fuzzy number and set must be of the same type.'
            assert other.qrung == self.__qrung, \
                'ERROR: The fuzzy number and set must be of the same Q-rung.'

            newset = mohuset(self.__qrung, self.__mtype)
            newset.__set = self.__set + other
            newset.__shape = self.__shape
            newset.__ndim = self.__ndim
            newset.__size = self.__size
            return newset
        raise TypeError('ERROR: Unsupported type.')

    def __sub__(self, other):
        """
            Subtract two fuzzy sets.

            Parameters
            ----------
                other: the fuzzy set to be subtracted

            Returns
            -------
                the fuzzy set that is the difference of the two fuzzy sets

            Notes
            -----
                Subtraction is not currently applicable to interval-valued
                q-rung orthopair fuzzy sets.
        """
        if self.__mtype == 'fn':
            if isinstance(other, mohuset):
                assert other.mtype == self.__mtype, \
                    'ERROR: The two fuzzy sets must be of the same type.'
                assert other.qrung == self.__qrung, \
                    'ERROR: The two fuzzy sets must be of the same Q-rung.'
                assert other.shape == self.__shape, \
                    'ERROR: The two fuzzy sets must be of the same shape.'
                assert other.ndim == self.__ndim, \
                    'ERROR: The two fuzzy sets must be of the same ndim.'
                assert other.size == self.__size, \
                    'ERROR: The two fuzzy sets must be of the same size.'

                newset = mohuset(self.__qrung, self.__mtype)
                newset.__set = self.__set - other.__set
                newset.__shape = self.__shape
                newset.__ndim = self.__ndim
                newset.__size = self.__size
                return newset
            if other.__class__.__name__ == 'mohunum':
                if self.__mtype == 'fn':
                    assert other.mtype == self.__mtype, \
                        'ERROR: The fuzzy number and set must be of the same type.'
                    assert other.qrung == self.__qrung, \
                        'ERROR: The fuzzy number and set must be of the same Q-rung.'

                    newset = mohuset(self.__qrung, self.__mtype)
                    newset.__set = self.__set - other
                    newset.__shape = self.__shape
                    newset.__ndim = self.__ndim
                    newset.__size = self.__size
                    return newset
        if self.__mtype == 'ivfn':
            raise ValueError('ERROR: Fuzzy numbers of \'ivfn\' '
                             'do not currently support subtraction.')
        raise TypeError('ERROR: Unsupported type.')

    def __mul__(self, other):
        """
            Multiply two fuzzy sets.

            Parameters
            ----------
                other: the fuzzy set to be multiplied

            Returns
            -------
                the fuzzy set that is the product of the two fuzzy sets
        """
        if isinstance(other, mohuset):
            assert other.mtype == self.__mtype, \
                'ERROR: The two fuzzy sets must be of the same type.'
            assert other.qrung == self.__qrung, \
                'ERROR: The two fuzzy sets must be of the same Q-rung.'
            assert other.shape == self.__shape, \
                'ERROR: The two fuzzy sets must be of the same shape.'
            assert other.ndim == self.__ndim, \
                'ERROR: The two fuzzy sets must be of the same ndim.'
            assert other.size == self.__size, \
                'ERROR: The two fuzzy sets must be of the same size.'

            newset = mohuset(self.__qrung, self.__mtype)
            newset.__set = self.__set * other.__set
            newset.__shape = self.__shape
            newset.__ndim = self.__ndim
            newset.__size = self.__size
            return newset
        if other.__class__.__name__ == 'mohunum':
            assert other.mtype == self.__mtype, \
                'ERROR: The fuzzy number and set must be of the same type.'
            assert other.qrung == self.__qrung, \
                'ERROR: The fuzzy number and set must be of the same Q-rung.'

            newset = mohuset(self.__qrung, self.__mtype)
            newset.__set = self.__set * other
            newset.__shape = self.__shape
            newset.__ndim = self.__ndim
            newset.__size = self.__size
            return newset
        if isinstance(other, (float, np.float_, int, np.int_)):
            assert 0 < other <= 1, \
                'ERROR: The value must be between 0 and 1.'
            newset = mohuset(self.__qrung, self.__mtype)
            newset.__set = self.__set * other
            newset.__shape = self.__shape
            newset.__ndim = self.__ndim
            newset.__size = self.__size
            return newset

    def __rmul__(self, other):
        """
            Multiply two fuzzy sets.

            Parameters
            ----------
                other: the fuzzy set to be multiplied

            Returns
            -------
                the fuzzy set that is the product of the two fuzzy sets
        """
        if isinstance(other, mohuset):
            assert other.mtype == self.__mtype, \
                'ERROR: The two fuzzy sets must be of the same type.'
            assert other.qrung == self.__qrung, \
                'ERROR: The two fuzzy sets must be of the same Q-rung.'
            assert other.shape == self.__shape, \
                'ERROR: The two fuzzy sets must be of the same shape.'
            assert other.ndim == self.__ndim, \
                'ERROR: The two fuzzy sets must be of the same ndim.'
            assert other.size == self.__size, \
                'ERROR: The two fuzzy sets must be of the same size.'

            newset = mohuset(self.__qrung, self.__mtype)
            newset.__set = other.__set * self.__set
            newset.__shape = self.__shape
            newset.__ndim = self.__ndim
            newset.__size = self.__size
            return newset
        if other.__class__.__name__ == 'mohunum':
            assert other.mtype == self.__mtype, \
                'ERROR: The fuzzy number and set must be of the same type.'
            assert other.qrung == self.__qrung, \
                'ERROR: The fuzzy number and set must be of the same Q-rung.'

            newset = mohuset(self.__qrung, self.__mtype)
            newset.__set = other * self.__set
            newset.__shape = self.__shape
            newset.__ndim = self.__ndim
            newset.__size = self.__size
            return newset
        if isinstance(other, (float, np.float_, int, np.int_)):
            assert 0 < other <= 1, \
                'ERROR: The value must be between 0 and 1.'
            newset = mohuset(self.__qrung, self.__mtype)
            newset.__set = other * self.__set
            newset.__shape = self.__shape
            newset.__ndim = self.__ndim
            newset.__size = self.__size
            return newset

    def __truediv__(self, other):
        """
            Divide two fuzzy sets.

            Parameters
            ----------
                other: the fuzzy set to be divided

            Returns
            -------
                the fuzzy set that is the quotient of the two fuzzy sets

            Notes
            -----
                Division is not currently applicable to interval-valued
                q-rung orthopair fuzzy sets.
        """
        if self.__mtype == 'fn':
            if isinstance(other, mohuset):
                assert other.mtype == self.__mtype, \
                    'ERROR: The two fuzzy sets must be of the same type.'
                assert other.qrung == self.__qrung, \
                    'ERROR: The two fuzzy sets must be of the same Q-rung.'
                assert other.shape == self.__shape, \
                    'ERROR: The two fuzzy sets must be of the same shape.'
                assert other.ndim == self.__ndim, \
                    'ERROR: The two fuzzy sets must be of the same ndim.'
                assert other.size == self.__size, \
                    'ERROR: The two fuzzy sets must be of the same size.'
                newset = mohuset(self.__qrung, self.__mtype)
                newset.__set = self.__set / other.__set
                newset.__shape = self.__shape
                newset.__ndim = self.__ndim
                newset.__size = self.__size
                return newset
            if other.__class__.__name__ == 'mohunum':
                assert other.mtype == self.__mtype, \
                    'ERROR: The fuzzy number and set must be of the same type.'
                assert other.qrung == self.__qrung, \
                    'ERROR: The fuzzy number and set must be of the same Q-rung.'
                newset = mohuset(self.__qrung, self.__mtype)
                newset.__set = self.__set / other
                newset.__shape = self.__shape
                newset.__ndim = self.__ndim
                newset.__size = self.__size
                return newset
            if isinstance(other, (float, np.float_)):
                assert other >= 1, \
                    'ERROR: The value must be greater than 1.'
                newset = mohuset(self.__qrung, self.__mtype)
                newset.__set = self.__set / other
                newset.__shape = self.__shape
                newset.__ndim = self.__ndim
                newset.__size = self.__size
                return newset
        if self.__mtype == 'ivfn':
            raise ValueError('ERROR: Fuzzy numbers of \'ivfn\' '
                             'do not currently support subtraction.')
        raise TypeError('ERROR: Unsupported type.')

    def __pow__(self, power, modulo=None):
        """

        """
        assert isinstance(power, (float, np.float_)), \
            'ERROR: The power must be a float.'
        assert 0 < power <= 1, \
            'ERROR: The value must be between 0 and 1.'

        newset = mohuset(self.__qrung, self.__mtype)
        newset.__set = self.__set ** power
        newset.__shape = self.__shape
        newset.__ndim = self.__ndim
        newset.__size = self.__size
        return newset

    def __matmul__(self, other):
        """
            Matrix multiplication of two fuzzy sets.

            Parameters
            ----------
                other: the fuzzy set to be multiplied

            Returns
            -------
                the fuzzy set that is the product of the two fuzzy sets
        """
        assert isinstance(other, mohuset), \
            'ERROR: The fuzzy set must be a fuzzy set.'
        assert self.__ndim == other.__ndim == 2, \
            'ERROR: The matrix ndim must be 2.'
        assert self.__shape[1] == other.__shape[0], \
            'ERROR: Incompatible shapes for matrix multiplication.'
        assert self.__qrung == other.__qrung, \
            'ERROR: The Q-rung of the two fuzzy sets must match.'
        assert self.__mtype == other.__mtype, \
            'ERROR: The two fuzzy sets must be of the same type.'

        newset = mohuset(self.__qrung, self.__mtype)
        fs = np.dot(self.__set, other.__set)
        newset.__set = fs
        newset.__shape = fs.shape
        newset.__ndim = fs.ndim
        newset.__size = fs.size
        return newset

    def setter(self, s, shape, ndim, size):
        """
            Set the fuzzy set.
            Functions that can modify the shape of fuzzy sets

            Parameters
            ----------
                s:      np.ndarray
                        The fuzzy set of the mohuset.
                shape:  tuple
                        The shape of the fuzzy set.
                ndim:   int
                        The ndim of the fuzzy set.
                size:   int
                        The size of the fuzzy set.

            Returns
            -------
                mohuset
                The modified fuzzy set
        """
        self.__set = s
        self.__shape = shape
        self.__ndim = ndim
        self.__size = size

        return self

    def random(self, *n):
        """
            Randomly generate a *n-shaped fuzzy set.

            Parameters
            ----------
                n: the shape of the fuzzy set

            Returns
            -------
                A *n-shaped fuzzy set
        """
        if self.__mtype is None and self.__qrung is None:
            self.__mtype = 'fn'
            self.__qrung = 1

        from .utils.fnumutils import rand_num
        def __random(dummy):
            return rand_num(mtype=self.__mtype, q=self.__qrung)

        vec_func = np.vectorize(__random)
        result = np.empty(n)
        result = vec_func(result)
        return self.setter(result, result.shape, result.ndim, result.size)

        # self.__size = 0
        # self.__set = np.array([])
        # from .utils.fnumutils import rand_num
        # for i in range(np.prod(n)):
        #     self.append(rand_num(mtype=self.__mtype, q=self.__qrung))
        # self.reshape(*n)
        # self.__ndim = len(n)
        # return self

    def ravel(self):
        """
            Reshapes the fuzzy set to a 1-dimensional array.
        """
        self.__set = self.__set.ravel()
        self.__shape = self.__set.shape
        self.__ndim = 1
        return self

    def append(self, x):
        """
            Append a fuzzy number to the fuzzy set.

            Before adding an element, first verify that the element is eligible for
            the fuzzy set. In other words, verify Q-rung consistency and fuzzy type
            consistency. It should be noted that after adding elements, the number
            of set elements needs to be +1.

            Parameters
            ----------
                x: the fuzzy element to be added

            Returns
            -------
                None
        """
        if self.__mtype is not None and self.__qrung is not None:
            assert x.qrung == self.__qrung, \
                'ERROR: qrung mismatch.'
            assert x.mtype == self.__mtype, \
                'ERROR: Fuzzy type mismatch.'
            self.__set = np.append(self.__set, x)
            self.__size += 1
            self.__shape = self.__set.shape
            self.__ndim = self.__set.ndim
        else:
            self.__mtype = x.mtype
            self.__set = np.append(self.__set, x)
            self.__qrung = x.qrung
            self.__shape = self.__set.shape
            self.__ndim = self.__set.ndim
            self.__size += 1

    def remove(self, x):
        """
            Remove a fuzzy number from the fuzzy set.

            First determine whether the value is in the set. After deleting the
            element, the set will become a one-dimensional fuzzy set. To adjust
            the shape, call the reshape method.

            Parameters
            ----------
                x: the fuzzy element to be removed

            Returns
            -------
                None
        """
        assert self.__size == 0, \
            'ERROR: Cannot remove, the set is empty.'
        assert x in self.__set, \
            'ERROR: Fuzzy element not in set.'
        self.__set = np.delete(self.__set, np.where(self.__set == x))
        self.__size -= 1
        self.__shape = self.__set.shape
        self.__ndim = self.__set.ndim

    def pop(self, i):
        """
            Removes an element from a set by index.

            Parameters
            ----------
                i: the index of the fuzzy element to be removed

            Returns
            -------
                None
        """
        self.__set = np.delete(self.__set, i)
        self.__size -= 1
        self.__shape = self.__set.shape
        self.__ndim = self.__set.ndim

    def reshape(self, *shape):
        """
            Reshape the fuzzy set according to the given shape.

            Parameters
            ----------
                shape:  the new shape of the fuzzy set. It can be 2-dimensional,
                        3-dimensional or even multidimensional.
                        For example, *n = [3,3,5] is a 3*3*5 3-dimensional fuzzy set.
                        This method is similar to numpy.random.
            Returns
            -------
                mohuset: the reshaped fuzzy set
        """
        self.__set = self.__set.reshape(*shape)
        self.__shape = self.__set.shape
        self.__ndim = self.__set.ndim
        return self

    def clear(self):
        """
            Clears the fuzzy set.
            This method is not recommended to be used. Make sure the data is saved
            before using this method.
        """
        self.__size = 0
        self.__set = np.array([], dtype=object)
        self.__mtype = None
        self.__qrung = None
        self.__ndim = None
        self.__shape = None
        return self

    def max(self, show=True):
        """
            Returns the maximum fuzzy number in the fuzzy set.

            Parameters
            ----------
                show: whether to display the maximum fuzzy number

            Returns
            -------
                The maximum fuzzy number
        """
        if self.__mtype == 'fn':
            index = np.unravel_index(np.argmax(self.__set), self.__shape)
            if show:
                print(index)
            return self.__set[index]
        if self.__mtype == 'ivfn':
            index = np.unravel_index(np.argmax(self.score), self.__shape)
            if show:
                print(index)
            return self.__set[index]
        raise ValueError('ERROR: Fuzzy set type not supported.')

    def min(self, show=True):
        """
            Returns the minimum fuzzy number in the fuzzy set.

            Parameters
            ----------
                show: whether to display the minimum fuzzy number

            Returns
            -------
                The minimum fuzzy number
        """
        if self.__mtype == 'fn':
            index = np.unravel_index(np.argmin(self.__set), self.__shape)
            if show:
                print(index)
            return self.__set[index]
        if self.__mtype == 'ivfn':
            index = np.unravel_index(np.argmin(self.score), self.__shape)
            if show:
                print(index)
            return self.__set[index]
        raise ValueError('ERROR: Fuzzy set type not supported.')

    def fmax(self, func, *args, show=True):
        """
            Compute the fuzzy elements using a custom function and then find the
            maximum value in the matrix. Here func can be seen as a substitute
            for the scoring function.

            Parameters
            ----------
                func: the custom function
                args: the arguments of the custom function
                show: whether to print the maximum element. Defaults to true

            Returns
            -------
                mohunum: the maximum element in the fuzzy set

            Note
            ----
                This function is often used as an innovation of the score function.
        """
        slist = func(self.__set, *args)
        index = np.unravel_index(np.argmax(slist), slist.shape)
        if show:
            print(index)
        return self.__set[index]

    def fmin(self, func, *args, show=True):
        """
            Compute the fuzzy elements using a custom function and then find the
            minimum value in the matrix. Here func can be seen as a substitute
            for the scoring function.

            Parameters
            ----------
                func: the custom function
                args: the arguments of the custom function
                show: whether to print the minimum element. Defaults to true

            Returns
            -------
                mohunum: the minimum element in the fuzzy set

            Note
            ----
                This function is often used as an innovation of the score function.
        """
        slist = func(self.__set, *args)
        index = np.unravel_index(np.argmin(slist), slist.shape)
        if show:
            print(index)
        return self.__set[index]

    def sum(self):
        """
            Returns the sum of the fuzzy set.

            Returns
            -------
                The sum of the fuzzy set
        """
        return np.sum(self.__set)

    def savez(self, path):
        """
            Save the fuzzy set to a.npz file.

            This method not only saves the fuzzy set, but also saves the relevant
            information of the fuzzy set.
            Specific storage content:
                1. The set of the fuzzy set
                2. The qrung of the fuzzy set
                3. The shape of the fuzzy set

            Parameters
            ----------
                path: the path of the.npz file

            Returns
            -------
                Bool: True if the save was successful
        """

        np.savez_compressed(path,
                            set=self.__set,
                            mtype=self.__mtype,
                            qrung=self.__qrung,
                            shape=self.__shape,
                            ndim=self.__ndim,
                            size=self.__size)

    def loadz(self, path):
        """
        Load the fuzzy set from a.npz file.

        This method not only loads the fuzzy set, but also loads the relevant
        information of the fuzzy set.
        Specific storage content:
            1. The set of the fuzzy set
            2. The qrung of the fuzzy set
            3. The shape of the fuzzy set

        Parameters
        ----------
            path: the path of the.npz file

        Returns
        -------
            Bool: True if the load was successful
        """

        mset = np.load(path, allow_pickle=True)
        self.__set = mset['set']
        self.__mtype = mset['mtype']
        self.__qrung = mset['qrung']
        self.__shape = tuple(mset['shape'])
        self.__ndim = mset['ndim']
        self.__size = mset['size']

    def plot(self, color='red', alpha=0.3):
        q = self.__qrung
        x = np.linspace(0, 1, 1000)

        plt.gca().spines['top'].set_linewidth(False)
        plt.gca().spines['bottom'].set_linewidth(True)
        plt.gca().spines['left'].set_linewidth(True)
        plt.gca().spines['right'].set_linewidth(False)
        plt.axis([0, 1.1, 0, 1.1])
        plt.axhline(y=0)
        plt.axvline(x=0)

        if self.__mtype == 'fn':
            md = self.md
            nmd = self.nmd

            plt.scatter(md, nmd, color=color, marker='.', alpha=alpha)

        if self.__mtype == 'ivfn':
            def __plot(x):
                md = x.md
                nmd = x.nmd
                plt.fill([md[0], md[1], md[1], md[0]],
                         [nmd[1], nmd[1], nmd[0], nmd[0]],
                         color=color, alpha=alpha)

            plot_func = np.vectorize(__plot)
            plot_func(self.__set)

        y = (1 - x ** q) ** (1 / q)
        plt.plot(x, y)
        plt.show()
