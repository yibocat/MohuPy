#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/1 下午5:37
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzyKit

import numpy as np
import pandas as pd

from config import load_dict


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
            qrung: the Q-rung of the element
            collection: the collection of elements in the fuzzy set
            __elements_num: the number of elements in the fuzzy set
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
            randint: Randomly generate multidimensional fuzzy sets
            score: Calculate the score value of each element of n-dimensional fuzzy set
            reshape: Reshaping of Fuzzy Sets
            display_matrix: Display the matrix representation of the fuzzy set
            savez: Save the set and information of the fuzzy set to a file
            loadz: Load the set and information of the fuzzy set from a file
            savecsv: Save the 2-dimension matrix of the fuzzy set to a CSV file
            loadcsv: Load the 2-dimension matrix of the fuzzy set from a CSV file
    """
    qrung = None
    collection = np.array([])
    __elements_num = 0
    __dict = None
    __shape = None

    def __init__(self, qrung, t):
        dictionary = load_dict(False)
        assert t in dictionary, 'ERROR: created type does not exist!'
        self.collection = np.array([])
        self.qrung = qrung
        self.__dict = dictionary[t]
        self.__elements_num = 0
        self.__shape = None

    def __repr__(self):
        return \
                'Collection information\n' \
                '----------------------------------------\n' \
                'fuzzy set type:            %s\n' % self.__dict['type'].__name__ + \
                'Q-rung:                    %s\n' % self.qrung + \
                'the set shape:             ' + str(self.__shape) + '\n' + \
                'elements number:           %s\n' % self.__elements_num

    @property
    def dict(self):
        return self.__dict

    @property
    def elements_num(self):
        return self.__elements_num

    @property
    def list(self):
        return self.collection.tolist()

    @property
    def shape(self):
        self.__shape = self.collection.shape
        return self.__shape

    @property
    def isEmpty(self):
        return self.__elements_num == 0

    def append(self, x):
        """
            Adds an element to a collection.

            Before adding an element, first verify that the element is eligible for
            the fuzzy set. In other words, verify Q-rung consistency and fuzzy type
            consistency. It should be noted that after adding elements, the number
            of collection elements needs to be +1.

            Parameters:
                x: the fuzzy element to be added

        """
        assert x.qrung == self.qrung, 'ERROR: Q-rung for adding elements differs from set.'
        assert x.__class__ == self.__dict['type'], 'ERROR: Cannot add different types of fuzzy elements!'
        self.collection = np.append(x, self.collection)
        self.__elements_num += 1

    def remove(self, x):
        """
            Removes an element from a collection by value.

            First determine whether the value is in the set. After deleting the
            element, the set will become a one-dimensional fuzzy collection. To adjust
            the shape, call the reshape method.

            Parameters:
                x: the element to be deleted
        """
        assert x in self.collection, 'ERROR: element is not in the set.'
        self.collection = np.delete(self.collection, np.where(self.collection == x))
        self.__elements_num -= 1

    def pop(self, i):
        """
            Removes an element from a collection by index.

            Parameters
        """
        self.collection = np.delete(self.collection, i)
        self.__elements_num -= 1

    def random(self, n, m=5):
        """
            Randomly generate a one-dimensional fuzzy set.

            First find the parent class of the current collection element, and give
            the parameters of the random function according to the type of the parent
            class (fuzzy collection). The reason for this is that because there is a
            big difference between hesitant fuzzy sets and random functions of fuzzy
            sets. The random function of the hesitant fuzzy element contains two
            parameters, while the fuzzy set contains only one parameter. In addition,
            in order to unify random methods and construct random fuzzy sets, a
            dictionary registry is used to store all types of fuzzy set configurations,
            and then the dictionary type is used to call random functions.

            Parameters:
                n: the number of elements in the fuzzy set
                m: the number of the element of the membership and non-membership degree
                    collection of the dual hesitant fuzzy set. The default value is set to 5

            Returns:
                the fuzzy set
        """
        self.__elements_num = 0
        self.collection = np.array([])
        father = None

        for base in self.__dict['type'].__bases__:
            father = base.__name__
        if father == 'DhFuzzy':
            args = [self.qrung, m]
        else:
            args = [self.qrung]
        for i in range(n):
            self.append(self.__dict['random'](*args))

        self.__shape = self.collection.shape
        return self

    def randint(self, *n, num=5):
        """
            Generate a fuzzy set of arbitrary dimensions.

            The idea of this function is very simple. First, the number of all elements
            in the set is given according to the shape set by the parameters. Then call
            the random method to randomly generate a one-dimensional set containing the
            given number. Finally, resize the collection according to the given shape.

            Parameters:
                n: the shape parameters of the collection. It can be 2-dimensional,
                    3-dimensional or even multidimensional.
                    For example, *n = [3,3,5] is a 3*3*5 3-dimensional fuzzy set.
                num: the number of the element of the membership and non-membership degree
                    collection of the dual hesitant fuzzy set. The default value is set to 5

            Returns:
                the fuzzy set

        """

        self.__elements_num = 0
        shape = n
        self.__elements_num = np.prod(n)
        self.random(self.__elements_num, num)
        self.reshape(shape)
        self.__shape = shape
        return self

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
        self.reshape(self.__elements_num)
        slist = np.asarray([self.collection[i].score for i in range(len(self.collection))])
        self.reshape(shape)
        return slist.reshape(shape)

    def reshape(self, *x):
        """
            Reshapes the collection according to the given shape.

            Parameters:
                x: the shape parameters of the collection. It can be 2-dimensional,
                    3-dimensional or even multidimensional.
                    For example, *n = [3,3,5] is a 3*3*5 3-dimensional fuzzy set.
                    This method is similar to numpy.random.
            Returns:
                the fuzzy set
        """
        self.collection = self.collection.reshape(*x)
        self.__elements_num = self.collection.size
        self.__shape = self.collection.shape
        return self

    def display_matrix(self):
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
                    [[np.round(self.collection[i].md, 4),
                      np.round(self.collection[i].nmd, 4)]])
        else:
            for i in range(self.__shape[0]):
                a = []
                for j in range(self.__shape[1]):
                    a.append(
                        [np.round(self.collection[i, j].md, 4),
                         np.round(self.collection[i, j].nmd, 4)])
                matrix.append(a)
        return pd.DataFrame(matrix)

    def savez(self, path):
        """
            Save the fuzzy set to a.npz file.

            This method not only saves the fuzzy set, but also saves the relevant
            information of the fuzzy set.
            Specific storage content:
                1. The collection of the fuzzy set
                2. The qrung of the fuzzy set
                3. The shape of the fuzzy set

            Parameters:
                path: the path to save the fuzzy set
                    Note: No need to add suffix, this method will automatically save to
                    npz compressed file.
        """
        print("Saving...")
        collection = self.collection
        qrung = self.qrung
        shape = self.__shape
        np.savez_compressed(path, collection=collection, qrung=qrung, shape=shape)
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
        self.collection = fuzzset['collection']
        self.qrung = fuzzset['qrung']
        self.__shape = fuzzset['shape']
        self.__elements_num = self.collection.size
        print('Loaded!')
        return self

    def savecsv(self, path):
        """
            Save the fuzzy set to a.csv file.

            This method only saves the fuzzy set, and does not save the related
            information of the set.

            Parameters:
                path: the path to save the fuzzy set
        """
        print('Saving...')
        mat = self.display_matrix()
        mat.to_csv(path)
        print('Saved!')

    def loadcsv(self, path):
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
        print('Loading...')
        m = pd.read_csv(path, index_col=0)
        m = np.array(m)

        try:
            self.__dict['convert_str'](m[0, 0], self.qrung)
        except Exception as e:
            print(e, 'The fuzzy data format does not match the created fuzzy set element format')

        for i in range(len(m)):
            for j in range(len(m[i])):
                m[i][j] = self.__dict['convert_str'](m[i, j], self.qrung)

        matrix = np.asarray(m)
        self.__shape = matrix.shape
        self.__elements_num = matrix.size
        self.collection = matrix
        print('Loaded!')
        return self
