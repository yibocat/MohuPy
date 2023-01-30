#  Copyright (c) yibocat 2023 All Rights Reserved
#  Date: 2023/1/30 下午8:25
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzyKit
import numpy as np
from FNumbers import qrungfn
from IVFNumbers import qrungivfn
from DHFElements import qrunghfe
from Lib.random import randomFN
from Lib.random import randomQHF
from Lib.random import randomIVFN


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
    collection = None
    type = None
    __elements_num = 0
    __dict = {'qrunghfe': qrunghfe, 'qrungfn': qrungfn, 'qrungivfn': qrungivfn}

    def __init__(self, q, t):
        assert t in self.__dict, 'ERROR: created type does not exist!'
        self.collection = np.array([])
        self.qrung = q
        self.type = self.__dict[t]

    def __repr__(self):
        return  'Collection information\n'\
                '----------------------------------------\n'\
                'number of elements:        %s\n' % self.__elements_num + \
                'Q-rung:                    %s\n' % self.qrung + \
                'type of the set:           %s\n' % self.type.__name__

    @property
    def dict(self):
        return self.__dict

    @property
    def elements_num(self):
        return self.__elements_num

    @property
    def list(self):
        return self.collection.tolist()

    def append(self, x):
        assert x.qrung == self.qrung, 'ERROR: Q-rung for adding elements differs from set.'
        assert x.__class__ == self.type, 'ERROR: Cannot add different types of fuzzy elements!'
        self.collection = np.append(self.collection, x)
        self.__elements_num += 1
        return self

    def delete(self, x):
        assert x in self.collection, 'ERROR: element is not in the set.'
        self.collection = np.delete(self.collection, np.where(self.collection == x))
        self.__elements_num -= 1

    def deleteI(self, i):
        self.collection = np.delete(self.collection, i)
        self.__elements_num -= 1

    def isEmpty(self):
        return self.__elements_num == 0

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

    def check_dict(self):
        for x in self.__dict:
            print(x, self.__dict[x])

    def save(self):
        pass

    def load(self):
        pass


