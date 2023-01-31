#  Copyright (c) yibocat 2023 All Rights Reserved
#  Date: 2023/1/30 下午8:25
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzyKit
import copy

import numpy as np
import pandas as pd

from fuzzyelement.FNumbers import qrungfn
from fuzzyelement.IVFNumbers import qrungivfn
from fuzzyelement.DHFElements import qrunghfe
from library.random import randomFN
from library.random import randomQHF
from library.random import randomIVFN

from config.__dict import __dict as dic


class fuzzyset(object):
    """
            Fuzzy set class. General operations on fuzzy sets, including
            adding fuzzy elements, deleting fuzzy elements, random fuzzy
            sets, etc.
            First, a dictionary of fuzzy element types is given. According
            to different types of fuzzy elements, different fuzzy sets are
            constructed, including Q-rung fuzzy sets, Q-rung interval
            valued fuzzy sets and Q-rung dual hesitant fuzzy sets.
            To initialize a fuzzy set, two parameters need to be passed in,
            namely Q-rung and fuzzy element type. It should be noted that:
            the type of fuzzy element must be included in the dictionary.

            After initialization, the fuzzy set object can be used to
            add fuzzy elements, delete fuzzy elements, random fuzzy sets,
            etc.

            Attributes:
                qrung: the Q-rung of the element
                type: the type of the fuzzy element
                __elements_num: the number of elements in the fuzzy set
                collection: the collection of elements in the fuzzy set
                __dict: Dictionary of Fuzzy Set Kinds
                list: the list of elements in the fuzzy set

            Methods:
                append: add a fuzzy element to the fuzzy set
                delete: delete a fuzzy element from the fuzzy set
                deleteI: delete a fuzzy element from the fuzzy set by index
                random: generate a random fuzzy set
                __repr__: print the fuzzy set information
                isEmpty: whether the fuzzy set is empty
                check_dict: check the dictionary of elements kinds
        """
    qrung = None
    collection = np.array([])
    type = None
    __elements_num = 0
    __dict = dic
    __shape = None

    def __init__(self, qrung, t):
        assert t in self.__dict, 'ERROR: created type does not exist!'
        self.collection = np.array([])
        self.qrung = qrung
        self.type = self.__dict[t]
        self.__elements_num = 0
        self.__shape = None

    def __repr__(self):
        return \
                'Collection information\n' \
                '----------------------------------------\n' \
                'type of the set:           %s\n' % self.type.__name__ + \
                'Q-rung:                    %s\n' % self.qrung + \
                'shape of the set:          ' + str(self.__shape) + '\n' + \
                'number of elements:        %s\n' % self.__elements_num

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
        assert x.qrung == self.qrung, 'ERROR: Q-rung for adding elements differs from set.'
        assert x.__class__ == self.type, 'ERROR: Cannot add different types of fuzzy elements!'
        self.collection = np.append(x, self.collection)
        self.__elements_num += 1

    def remove(self, x):
        assert x in self.collection, 'ERROR: element is not in the set.'
        self.collection = np.delete(self.collection, np.where(self.collection == x))
        self.__elements_num -= 1

    def pop(self, i):
        self.collection = np.delete(self.collection, i)
        self.__elements_num -= 1

    def random(self, n, m=5):
        self.__elements_num = 0
        self.collection = np.array([])

        for i in range(n):
            if self.type == qrungfn:
                self.append(randomFN(self.qrung))
            if self.type == qrungivfn:
                self.append(randomIVFN(self.qrung))
            if self.type == qrunghfe:
                self.append(randomQHF(self.qrung, m))

    def randint(self, *n, num=5):
        self.__elements_num = 0
        self.__shape = n
        self.__elements_num = np.prod(n)
        self.random(self.__elements_num, num)
        self.reshape(self.__shape)

    def getScore(self):
        shape = self.__shape
        self.reshape(self.__elements_num)
        slist = np.asarray([self.collection[i].score for i in range(len(self.collection))])
        self.reshape(shape)
        return slist.reshape(shape)

    def reshape(self, *x):
        self.collection = self.collection.reshape(*x)
        self.__elements_num = self.collection.size
        self.__shape = self.collection.shape
        return self

    def display_matrix(self):
        assert len(self.__shape) <= 2, 'The dimension of the shape must be less than or ' \
                                       'equal to 2. If you still want to display, please ' \
                                       'use the \'reshape()\' function to convert.'
        matrix = []
        print(self.__shape)
        for i in range(self.__shape[0]):
            a = []
            for j in range(self.__shape[1]):
                a.append(
                    [np.round(self.collection[i, j].md, 4),
                     np.round(self.collection[i, j].nmd, 4)])
            matrix.append(a)
        return pd.DataFrame(matrix)

    def save(self):
        pass

    def load(self):
        pass
