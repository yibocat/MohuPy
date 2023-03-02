#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/21 上午4:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets

import copy

import numpy as np
import pandas as pd

from ..fuzzynumbers import glb


class fuzzyset(object):
    """
        Fuzzy set class. General operations on fuzzy sets, including adding fuzzy
        elements, deleting fuzzy elements, random fuzzy sets, etc. First, a dictionary
        of fuzzy element types is given. According to different types of fuzzy
        elements, different fuzzy sets are constructed, including Q-rung fuzzy
        sets, Q-rung interval valued fuzzy sets and Q-rung dual hesitant fuzzy sets.
        To initialize a fuzzy set, two parameters need to be passed in, namely Q-rung
        and fuzzy element type. It should be noted that: the type of fuzzy element
        must be included in the dictionary.

        After initialization, the fuzzy set object can be used to add fuzzy elements,
        delete fuzzy elements, random fuzzy sets, etc.

        Attributes:
            __qrung: the Q-rung of the element
            __set: the set of elements in the fuzzy set
            __size: the number of elements in the fuzzy set
            __dict: dictionary of current fuzzy set types
            __shape: Shape of fuzzy data set

            list: the list of elements in the fuzzy set

        Methods:
            __repr__: print the fuzzy set information

            isEmpty: whether the set is empty
            append: add a fuzzy element to the fuzzy set
            remove: delete a fuzzy element from the fuzzy set
            pop: delete a fuzzy element from the fuzzy set by index
            random: Randomly generate a one-dimensional fuzzy set
            rand: Randomly generate multidimensional fuzzy sets
            score: Calculate the score value of each element of n-dimensional fuzzy set
            elementFunc: Apply a function to all elements of the fuzzy set
            reshape: Reshaping of Fuzzy Sets
            mat: Display the matrix representation of the fuzzy set
            savez: Save the set and information of the fuzzy set to a file
            loadz: Load the set and information of the fuzzy set from a file
            savecsv: Save the 2-dimension matrix of the fuzzy set to a CSV file
            loadcsv: Load the 2-dimension matrix of the fuzzy set from a CSV file
    """
    __qrung = None
    __set = np.array([])
    __size = 0
    __dict = None
    __shape = None
    __type = None
    __ndim = None

    def __init__(self, qrung=None, ftype=None):
        dictionary = glb.global_dict()
        if qrung is not None and ftype is not None:
            assert ftype in dictionary, 'ERROR: fuzzy set type does not exist.'
            self.__type = ftype
            self.__set = np.array([])
            self.__qrung = qrung
            self.__dict = dictionary[ftype]
            self.__size = 0
            self.__shape = None
            self.__ndim = None
        else:
            pass

    def __repr__(self):
        return \
                'Collection information\n' \
                '----------------------------------------\n' \
                'fuzzy set type:            %s\n' % self.__type + \
                'Q-rung:                    %s\n' % self.__qrung + \
                'the set shape:             ' + str(self.__shape) + '\n' + \
                'elements number:           %s\n' % self.__size

    def __str__(self):
        return \
                'Collection information\n' \
                '----------------------------------------\n' \
                'fuzzy set type:            %s\n' % self.__type + \
                'Q-rung:                    %s\n' % self.__qrung + \
                'the set shape:             ' + str(self.__shape) + '\n' + \
                'elements number:           %s\n' % self.__size

    @property
    def ftype(self):
        return self.__type

    @property
    def qrung(self):
        return self.__qrung

    @property
    def set(self):
        return self.__set

    @property
    def size(self):
        return self.__size

    @property
    def dict(self):
        return self.__dict

    @property
    def shape(self):
        return self.__shape

    @property
    def isempty(self):
        return self.__size == 0

    @property
    def list(self):
        return self.__set.tolist()

    @property
    def ndim(self):
        self.__ndim = len(self.__shape)
        return self.__ndim

    @property
    def mat(self):
        """
            Display the matrix of the fuzzy set.

            Note that this method only exhibits 1- and 2-dimensional fuzzy sets.
            Since this method is based on pandas.DataFrame, it does not support
            high-dimensional display for the time being.

            Parameters:

            Returns:
                the matrix of the fuzzy set
        """
        assert 0 < len(self.__shape) <= 2, \
            'The dimension of the shape must be less than or ' \
            'equal to 2. If you still want to display, please ' \
            'use the \'reshape()\' function to convert.'
        matrix = []

        if len(self.__shape) == 1:
            for i in range(self.__shape[0]):
                matrix.append(
                    [[np.round(self.__set[i].md, 4),
                      np.round(self.__set[i].nmd, 4)]])
        else:
            for i in range(self.__shape[0]):
                a = []
                for j in range(self.__shape[1]):
                    a.append(
                        [np.round(self.__set[i, j].md, 4),
                         np.round(self.__set[i, j].nmd, 4)])
                matrix.append(a)
        return pd.DataFrame(matrix)

    @property
    def score(self):
        """
            Calculate the score of the fuzzy set.

            The scores of all elements of the fuzzy set are calculated under the premise
            that the shape of the fuzzy set is consistent. In other words, the method
            calculates the score value of each blurred element while keeping the shape unchanged.

            Returns:
                the score of the fuzzy set
        """
        shape = self.__shape
        self.ravel()
        slist = np.asarray([self.__set[i].score for i in range(len(self.__set))])
        self.reshape(shape)
        return slist.reshape(shape)

    def append(self, x):
        """
            Adds an element to a set.

            Before adding an element, first verify that the element is eligible for
            the fuzzy set. In other words, verify Q-rung consistency and fuzzy type
            consistency. It should be noted that after adding elements, the number
            of set elements needs to be +1.

            Parameters:
                x: the fuzzy element to be added

        """

        if self.__type is not None:
            assert x.qrung == self.__qrung, 'ERROR: Q-rung for adding elements differs from set.'
            assert x.__class__ == self.__dict['type'], 'ERROR: Cannot add different types of fuzzy elements!'
            self.__set = np.append(self.__set, x)
            self.__size += 1
            self.__shape = self.__set.shape
        else:
            self.__type = x.__class__.__name__
            self.__dict = glb.global_get(self.__type)
            # self.__dict = fns.get_dict[self.__type]
            self.__set = np.append(self.__set, x)
            self.__qrung = x.qrung
            self.__shape = self.__set.shape
            self.__size += 1

    def remove(self, x):
        """
            Removes an element from a set by value.

            First determine whether the value is in the set. After deleting the
            element, the set will become a one-dimensional fuzzy set. To adjust
            the shape, call the reshape method.

            Parameters:
                x: the element to be deleted
        """
        assert x in self.__set, 'ERROR: element is not in the set.'
        self.__set = np.delete(self.__set, np.where(self.__set == x))
        self.__size -= 1
        self.__shape = self.__set.shape

    def pop(self, i):
        """
            Removes an element from a set by index.

            Parameters
        """
        self.__set = np.delete(self.__set, i)
        self.__size -= 1
        self.__shape = self.__set.shape

    def elementfunc(self, func, *args):
        """
            Apply a function to all elements of the fuzzy set.

            Usually we need to directly perform a unified function operation on all elements
            of the fuzzy set. This function can be our custom function, so we need a method
            to apply the custom function to each element.

            Parameters:
                func: the function to be applied to all elements of the fuzzy set
                *args: the parameters of the function.
        """
        shape = self.__shape
        self.ravel()
        slist = np.asarray([func(self.__set[i], *args) for i in range(len(self.__set))])
        self.reshape(shape)
        return slist.reshape(shape)

    def random(self, n, num=5):
        """
            Randomly generate a one-dimensional fuzzy set.

            First find the parent class of the current set element, and give
            the parameters of the random function according to the type of the parent
            class (fuzzy set). The reason for this is that because there is a
            big difference between hesitant fuzzy sets and random functions of fuzzy
            sets. The random function of the hesitant fuzzy element contains two
            parameters, while the fuzzy set contains only one parameter. In addition,
            in order to unify random methods and construct random fuzzy sets, a
            dictionary registry is used to store all types of fuzzy set configurations,
            and then the dictionary type is used to call random functions.

            Parameters:
                n: the number of elements in the fuzzy set
                num: the number of the element of the membership and non-membership degree
                    set of the dual hesitant fuzzy set. The default value is set to 5

            Returns:
                the fuzzy set
        """
        self.__size = 0
        self.__set = np.array([])

        # for base in self.__dict['type'].__bases__:
        #     father = base.__name__

        if self.__type == 'qrungdhfe':
            args = [self.__qrung, num]
        else:
            args = [self.__qrung]
        for i in range(n):
            self.append(self.__dict['random'](*args))

        self.__shape = self.__set.shape
        return self

    def rand(self, *n, num=5):
        """
            Generate a fuzzy set of arbitrary dimensions.

            The idea of this function is very simple. First, the number of all elements
            in the set is given according to the shape set by the parameters. Then call
            the random method to randomly generate a one-dimensional set containing the
            given number. Finally, resize the set according to the given shape.

            Parameters:
                n: the shape parameters of the set. It can be 2-dimensional,
                    3-dimensional or even multidimensional.
                    For example, *n = [3,3,5] is a 3*3*5 3-dimensional fuzzy set.
                num: the number of the element of the membership and non-membership degree
                    set of the dual hesitant fuzzy set. The default value is set to 5

            Returns:
                the fuzzy set

        """

        self.__size = 0
        # self.__set = np.array([])
        shape = n
        self.random(np.prod(n), num)
        self.reshape(shape)
        self.__shape = shape
        self.__size = self.__set.size
        return self

    def reshape(self, *x):
        """
            Reshapes the set according to the given shape.

            Parameters:
                x: the shape parameters of the set. It can be 2-dimensional,
                    3-dimensional or even multidimensional.
                    For example, *n = [3,3,5] is a 3*3*5 3-dimensional fuzzy set.
                    This method is similar to numpy.random.
            Returns:
                the fuzzy set
        """
        self.__set = self.__set.reshape(*x)
        # self.__size = self.__set.size
        self.__shape = self.__set.shape
        return self

    def ravel(self):
        """
            Reshapes the set to a 1-dimensional array.
        """
        self.__set = self.__set.ravel()
        # self.__size = self.__set.size
        self.__shape = self.__set.shape
        return self

    def poss(self, *n):
        """
             Generates a high-dimensional fuzzy set with a positive ideal solution.
             This means that the degrees of membership are all 1 and the degrees of
             non-membership are all 0.

             Parameters:
                 n: the shape parameters of the set. It can be 2-dimensional,
                    3-dimensional or even multidimensional.
                     For example, *n = [3,3,5] is a 3*3*5 3-dimensional fuzzy set.
        """
        assert self.__size == 0, 'The fuzzy set is not empty. This set ' \
                                 'already has data, please clear the data first.'
        self.__size = 0
        self.__set = np.array([])
        shape = n
        for i in range(np.prod(n)):
            self.append(self.__dict['pos'](self.__qrung))
        self.reshape(shape)
        self.__shape = shape
        self.__size = self.__set.size
        return self

    def negs(self, *n):
        """
            Generates a high-dimensional fuzzy set with a negative ideal solution.
             This means that the degrees of membership are all 0 and the degrees of
             non-membership are all 1.

             Parameters:
                 n: the shape parameters of the set. It can be 2-dimensional,
                    3-dimensional or even multidimensional.
                     For example, *n = [3,3,5] is a 3*3*5 3-dimensional fuzzy set.
        """
        assert self.__size == 0, 'The fuzzy set is not empty. This set ' \
                                 'already has data, please clear the data first.'
        self.__size = 0
        self.__set = np.array([])
        shape = n
        for i in range(np.prod(n)):
            self.append(self.__dict['neg'](self.__qrung))
        self.reshape(shape)
        self.__shape = shape
        self.__size = self.__set.size
        return self

    def zeros(self, *n):
        """
            Generate a high-dimensional fuzzy set whose membership degree and
            non-membership degree are both 0.

            Parameters:
                 n: the shape parameters of the set. It can be 2-dimensional,
                    3-dimensional or even multidimensional.
                     For example, *n = [3,3,5] is a 3*3*5 3-dimensional fuzzy set.
        """
        assert self.__size == 0, 'The fuzzy set is not empty. This set ' \
                                 'already has data, please clear the data first.'
        self.__size = 0
        self.__set = np.array([])
        shape = n
        for i in range(np.prod(n)):
            self.append(self.__dict['zero'](self.__qrung))
        self.reshape(shape)
        self.__shape = shape
        self.__size = self.__set.size
        return self

    def clear(self):
        """
            Clears the fuzzy set.
            This method is not recommended to be used. Make sure the data is saved
            before using this method.
        """
        self.__size = 0
        self.__set = np.array([])
        self.__type = None
        self.__shape = None
        self.__dict = None
        self.__qrung = None
        return self

    def max(self, show=True):
        """
            Returns the maximum element of the fuzzy set.

            Parameters:
                show: whether to print the maximum element. Defaults to true
            Returns:
                the maximum element of the fuzzy set
        """
        score_mat = self.score
        index = np.unravel_index(np.argmax(score_mat), score_mat.shape)
        if show:
            print(index)
        return self.__set[index]

    def fmax(self, func, *args, show=True):
        """
            Compute the fuzzy elements using a custom function and then find the
            maximum value in the matrix. Here func can be seen as a substitute
            for the scoring function.

            Parameters:
                func: custom function
                *args: arguments for the custom function
                show: whether to print the maximum element. Defaults to true

            Returns:
                the maximum element of the fuzzy set
        """
        f_mat = self.elementfunc(func, *args)
        index = np.unravel_index(np.argmax(f_mat), f_mat.shape)
        if show:
            print(index)
        return self.__set[index]

    def min(self, show=True):
        """
            Returns the minimum element of the fuzzy set.

            Parameters:
                 show: whether to print the minimum element. Defaults to true
            Returns:
                the minimum element of the fuzzy set
        """
        score_mat = self.score
        index = np.unravel_index(np.argmin(score_mat), score_mat.shape)
        if show:
            print(index)
        return self.__set[index]

    def fmin(self, func, *args, show=True):
        """
            Compute the fuzzy elements using a custom function and then find the
            minimum value in the matrix. Here func can be seen as a substitute
            for the scoring function.

            Parameters:
                func: custom function
                *args: arguments for the custom function
                show: whether to print the maximum element. Defaults to true

            Returns:
                the minimum element of the fuzzy set
        """
        f_mat = self.elementfunc(func, *args)
        index = np.unravel_index(np.argmin(f_mat), f_mat.shape)
        if show:
            print(index)
        return self.__set[index]

    def sum(self, norm='algeb_plus'):
        newf = copy.deepcopy(self)
        newf = newf.ravel()
        newE = self.__dict['neg'](self.__qrung)
        for e in newf.set:
            newE = self.__dict[norm](newE, e)
        del newf
        return newE

    def savez(self, path):
        """
            Save the fuzzy set to a.npz file.

            This method not only saves the fuzzy set, but also saves the relevant
            information of the fuzzy set.
            Specific storage content:
                1. The set of the fuzzy set
                2. The qrung of the fuzzy set
                3. The shape of the fuzzy set

            Parameters:
                path: the path to save the fuzzy set
                    Note: No need to add suffix, this method will automatically save to
                    npz compressed file.
        """
        print("Saving...")
        collection = self.__set
        ftype = self.__type
        qrung = self.__qrung
        shape = self.__shape
        dicts = self.__dict
        np.savez_compressed(path+'.npz', set=collection, ftype=ftype, qrung=qrung, shape=shape, dict=dicts)
        print('Saved!')

    def loadz(self, path):
        """
            Load the fuzzy set from a.npz file.

            This method not only loads the fuzzy set, but also loads the relevant
            information of the set.

            Parameters:
                path: the path to load the fuzzy set
                    Note: No need to add suffix, this method will automatically load from
                    npz compressed file.
        """
        print("Loading...")
        file = path + '.npz'

        fuzzset = np.load(file, allow_pickle=True)
        self.__qrung = fuzzset['qrung']
        self.__set = fuzzset['set']
        self.__shape = fuzzset['shape']
        self.__type = fuzzset['ftype']
        self.__dict = fuzzset['dict'].tolist()
        self.__size = self.__set.size
        print('Loaded!')
        return self

    def savecsv(self, path, show=False):
        """
            Save the fuzzy set to a.csv file.

            This method only saves the fuzzy set, and does not save the related
            information of the set.

            Parameters:
                path: the path to save the fuzzy set
                show: Print save information option
        """
        if show:
            print('Saving...')
        s = []
        for i in range(self.__shape[0]):
            u = []
            for j in range(self.__shape[1]):
                u.append(list(self.__set[i, j].convert()))
            s.append(u)
        s = pd.DataFrame(s)
        s.to_csv(path)
        if show:
            print('Saved!')
            print(s)
        return s

    def loadcsv(self, path, show=False):
        """
            Load the fuzzy set from a.csv file.

            This method is used to load a fuzzy set table with unknown information. It
            is necessary to judge the content of the fuzzy table during loading. When
            initializing a fuzzy set, Q-rung and fuzzy set type are given, so it is necessary
            to judge whether a fuzzy set meets these two conditions. This method will only
            load when the fuzzy set table is equal to or satisfied with the initial fuzzy set
            condition.

            parameter
                path: the path to load the fuzzy set.
        """
        if show:
            print('Loading...')
        m = pd.read_csv(path, index_col=0)
        m = np.asarray(m)
        if show:
            print(m)
        # try:
        self.__dict['convert_str'](m[0, 0], self.__qrung)
        # except Exception as e:
        #     print(e, 'The fuzzy data format does not match the created fuzzy set element format')

        for i in range(len(m)):
            for j in range(len(m[i])):
                try:
                    m[i][j] = self.__dict['convert_str'](m[i, j], self.__qrung)
                except Exception as e:
                    print(e, 'error element:(%d,%d)' % (i+1, j+1))
                    return None

        matrix = np.asarray(m)
        self.__shape = matrix.shape
        self.__size = matrix.size
        self.__set = matrix
        if show:
            print('Loaded!')

    def sort(self):
        pass
