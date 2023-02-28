#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/21 上午4:11
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: Mohusets

import numpy as np
import warnings


from .memfunc import memfunc
from .function import (sigmf, trimf, zmf,
                       trapmf, smf, gaussmf,
                       gauss2mf, gbellmf)

# import mohusets.fuzzynumbers.qdhfe as hfe
# import mohusets.fuzzynumbers.qrungivfn as ivfn
# import mohusets.fuzzynumbers.qrungifn as ifn

# import mohusets.fuzzynumbers as fns
from ..fuzzynumbers import glb, zero


fdict = {'sigmf': sigmf,
         'trimf': trimf,
         'zmf': zmf,
         'trapmf': trapmf,
         'smf': smf,
         'gaussmf': gaussmf,
         'gauss2mf': gauss2mf,
         'gbellmf': gbellmf}


class fuzzgener(object):
    """
        This class is a fuzzy element generator base class, which contains
        the basic characteristics of the generator. First of all, various
        fuzzy elements can be generated according to the built-in 8 membership
        functions. Its principle is to obtain the corresponding fuzzy element
        value according to the membership function. In addition, fuzzy values
        can also be calculated by custom membership functions. This base class
        can also draw function graphs according to the given membership functions.

        Custom membership functions are adjusted according to the 'custom'
        attribute. When custom=True, 'func' is a custom membership function.
        The format of the custom membership function is as follows.
        This is just an example, because the function's range is not in
        the 0-1 interval, so the function is not perfect.
        ---------------------------------
        |   def func_test(x,*p):        |
        |       return p[0]*x + p[1]    |
        ---------------------------------
        Note that when 'custom==True', the attribute 'func' becomes a
        function. When 'custom==False', the attribute 'func' is the function
        name of a common membership function.

        Attributes
        ----------
            __qrung : int
                The q-rung of the fuzzy element.
                (e.g. qrung=3 indicates the intuitionistic fuzzy sets)
            __fuzze : str
                The fuzzy element type.
                (e.g. 'qrungdhfe', 'qrungivfn', 'qrungifn')
            __custom : bool
                Whether the membership function is customized.
                (default: False)
                Note: When changing this attribute, a warning will pop up to clear
                the original membership function and parameters.
            __mf : memfunc
                The membership function by memfunc.
            __nmf : memfunc
                The non-membership function by memfunc.
            __md_params : list
                The parameters of the membership function.
                (e.g. [[0.27,0.33],[0.45,0.66]]. This example has two membership
                functions because two sets of parameters are given.)
            __nmd_params : list
                The parameters of the non-membership function.
                (e.g. [[0.27,0.33],[0.45,0.66]]. This example has two non-membership
                functions because two sets of parameters are given.)
            __variable_start : float
                The start value of the variable.
            __variable_start: float
                the start of the independent variable
                (e.g. 0.)
            __variable_end: float
                the end of the independent variable
                (e.g. 1.)
            __linspace: int
                the number of points of the independent variable
                (e.g. 100)
            mfunc : str or function
                The membership function.
                (e.g. 'gaussmf',custom_func)
                When 'custom==False', 'mfunc' is of type str and belongs to the 8
                built-in membership functions. 'mfunc' is a custom membership
                function when 'custom==True'.
            nmfunc : str or function
                The non-membership function.
                (e.g. 'gaussmf',custom_func)
                When 'custom==False', 'nmfunc' is of type str and belongs to the 8
                built-in membership functions. 'nmfunc' is a custom membership
                function when 'custom==True'.

        Methods
        -------
            setvariable:
                set the start and end of the independent variable
                (e.g. memfunc.setvariable(0.1, 0.3, 100))
            plot:
                plot the membership function and the non-membership function.
                (e.g. memfunc.plot())
    """
    __qrung = 0
    __fuzze = ''
    __custom = False

    __mf = None
    __nmf = None

    __md_params = []
    __nmd_params = []

    __variable_start = 0.
    __variable_end = 1.
    __linspace = 100

    def __init__(self, qrung, fe, func, params, custom=False):
        """
            Initialize the fuzzy element generator.

            Parameters
            ----------
                qrung: int
                    The q-rung of the fuzzy element.
                    (e.g. qrung=3 indicates the intuitionistic fuzzy sets)
                fe: str
                    The fuzzy element type.
                    (e.g. 'qrungdhfe', 'qrungivfn', 'qrungifn')
                func: str or function
                    The membership function.
                    (e.g. 'gaussmf',custom_func)
                    When 'custom==False', 'func' is of type str and belongs to the 8
                    built-in membership functions. 'func' is a custom membership
                    function when 'custom==True'.
                params: list
                    The parameters of the membership function and non-membership function.
                    (e.g. [[[0.27,0.33],[0.45,0.66]],[[0.56,0.12],[0.44,0.78]].
                    This example has two membership functions and two non-membership
                    function because two sets of membership and non-membership func
                    parameters are given.)
                custom: bool
                    Whether the membership function is customized.
                    (default: False)
                    Note: When changing this attribute, a warning will pop up to clear
                    the original membership function and parameters.
        """
        d = glb.global_dict().keys()
        assert qrung > 0, 'q-rung must be >= 1'
        assert fe in d, 'fuzzy element type does not exist.'

        self.__qrung = qrung
        self.__fuzze = fe
        self.__custom = custom

        self.mfunc = func
        self.nmfunc = func
        self.__md_params = params[0]
        self.__nmd_params = params[1]

    def __repr__(self):
        """
            Print the fuzzy element generator information.
            This function is often used for program debugging.
        """
        info = 'Info:\n' + 'Q-rung: %d,\n' % self.__qrung + 'fuzzy element: %s\n' % self.__fuzze + \
               '--------------------\n' + \
               'Membership function:\n' + str(self.__mf) + '\n' + 'Non-Membership function:\n' + str(self.__nmf)
        return info

    def __str__(self):
        # """
        #     Print the fuzzy element generator information.
        #     This function is often used for output printing.
        # """
        # info = 'Info:\n' + 'Q-rung: %d,\n' % self.__qrung + 'fuzzy element: %s\n' % self.__fuzze + \
        #        '--------------------\n' + \
        #        'Membership function:\n' + str(self.__mf) + '\n' + 'Non-Membership function:\n' + str(self.__nmf)
        # return info
        return 'Successfully generated!'

    # Through the decorator, the private properties of this class can be accessed and
    # modified by subclasses. In addition, some restrictions have been added when modifying.
    @property
    def qrung(self):
        return self.__qrung

    @qrung.setter
    def qrung(self, qrung):
        assert qrung > 0, 'q-rung must be >= 1'
        assert type(qrung) == int, 'q-rung must be an integer.'
        self.__qrung = qrung

    @property
    def fuzze(self):
        return self.__fuzze

    @fuzze.setter
    def fuzze(self, fuzze):
        d = glb.global_dict().keys()
        if self.__custom:
            assert callable(fuzze), 'Custom fuzzy element must be a function.'
        else:
            assert fuzze in d, 'fuzzy element type does not exist.'
        self.__fuzze = fuzze

    @property
    def custom(self):
        return self.__custom

    # Modifying custom settings will clear membership functions and parameters, so use with caution.
    @custom.setter
    def custom(self, custom):
        assert type(custom) is bool, 'custom must be a boolean.'
        warnings.warn('Custom function transformations will clear the settings.')
        self.__md_params = []
        self.__nmd_params = []
        self.__mf = None
        self.__nmf = None
        self.__custom = custom

    @property
    def mf(self):
        return self.__mf

    @mf.setter
    def mf(self, mf):
        assert type(mf) is memfunc, 'Membership function must be a memfunc.'
        self.__mf = mf

    @property
    def nmf(self):
        return self.__nmf

    @nmf.setter
    def nmf(self, nmf):
        assert type(nmf) is memfunc, 'Non-Membership function must be a memfunc.'
        self.__nmf = nmf

    @property
    def md_params(self):
        return self.__md_params

    @md_params.setter
    def md_params(self, md_params):
        assert type(md_params) is list, 'Membership function parameters must be a list.'
        self.__md_params = md_params

    @property
    def nmd_params(self):
        return self.__nmd_params

    @nmd_params.setter
    def nmd_params(self, nmd_params):
        assert type(nmd_params) is list, 'Non-Membership function parameters must be a list.'
        self.__nmd_params = nmd_params

    @property
    def variable_start(self):
        return self.__variable_start

    @variable_start.setter
    def variable_start(self, variable_start):
        # assert type(variable_start) is float, 'variable_start must be a float.'
        self.__variable_start = variable_start

    @property
    def variable_end(self):
        return self.__variable_end

    @variable_end.setter
    def variable_end(self, variable_end):
        # assert type(variable_end) is float, 'variable_end must be a float.'
        self.__variable_end = variable_end

    @property
    def linspace(self):
        return self.__linspace

    @linspace.setter
    def linspace(self, linspace):
        self.__linspace = linspace

    def getinfo(self):
        print(self.__repr__())

    def setvariable(self, start, end, linspace):
        """
            Set the variable range of the independent variable. This
            function is used to generate the spatial extent of
            membership function instances.

            Args:
                start:  float
                    start of the variable range
                end:  float
                    end of the variable range
                linspace:  int
                    number of points in the variable range
        """
        self.__variable_start = start
        self.__variable_end = end
        self.__linspace = linspace

    def plot(self, figsize=(5, 3)):
        """
            Plot the membership function.
            Args:
                figsize: tuple, figure size, default=(5,3)
        """
        mf = self.__mf
        nmf = self.__nmf
        mf.setvariable(self.__variable_start, self.__variable_end, self.__linspace)
        nmf.setvariable(self.__variable_start, self.__variable_end, self.__linspace)
        mf.plot('mem func', figsize)
        nmf.plot('non-mem func', figsize)


class dhfegener(fuzzgener):
    """
        Q-rung dual hesitant fuzzy element fuzzgener. As a subclass of fuzzgener,
        this class inherits most of the properties of the parent class, and can
        access the private properties of the parent class through the decorator
        set by the parent class. By inputting qrung, type of fuzzy element,
        membership function, parameters and user-defined settings, the fuzzgener
        can finally calculate a Q-rung dual hesitant fuzzy element satisfying
        the condition.

        Attributes:
            mfunc: str or function
                membership function
            nmfunc: str or function
                non-membership function
            __mfnum: int
                number of membership function parameters.
            __nmfnum: int
                number of non-membership function parameters.

        Methods:
            generate: function
                generate a Q-rung dual hesitant fuzzy element satisfying
                the condition.
    """

    # membership function
    # #non-membership function
    mfunc = None
    nmfunc = None

    __mfnum = -1
    __nmfnum = -1

    def __init__(self, qrung, func, params, custom=False):
        fe = 'qrungdhfe'
        super(dhfegener, self).__init__(qrung, fe, func, params, custom)
        self.__mfnum = len(params[0])
        self.__nmfnum = len(params[1])

        self.mf = memfunc(self.mfunc, self.md_params, self.custom)
        self.nmf = memfunc(self.nmfunc, self.nmd_params, self.custom)

    def __call__(self, x, y):
        return self.generate(x, y)

    @property
    def mfnum(self):
        return self.__mfnum

    @property
    def nmfnum(self):
        return self.__nmfnum

    def generate(self, x, y):
        assert self.variable_start <= x <= self.variable_end, \
            'The independent variable x is not in the range of %d and %d' % (
                self.variable_start, self.variable_end)
        assert self.variable_start <= y <= self.variable_end, \
            'The independent variable y is not in the range of %d and %d' % (
                self.variable_start, self.variable_end)

        dhfe = zero('qrungdhfe', self.qrung)
        md = self.mf(x)
        nmd = self.nmf(y)
        dhfe.set_md(md)
        dhfe.set_nmd(nmd)
        if dhfe.isLegal():
            return dhfe
        else:
            raise ValueError('The fuzzy element is not valid.')


class ivfngener(fuzzgener):
    """
        Qrung interval intuitionistic fuzzy number fuzzgener. As a subclass of fuzzgener,
        this class inherits most of the properties of the parent class, and can
        access the private properties of the parent class through the decorator
        set by the parent class. By inputting qrung, type of fuzzy element,
        membership function, parameters and user-defined settings, the fuzzgener
        can finally calculate a Q-rung interval intuitionistic fuzzy number
        satisfying the condition.

        Attributes:
            mfunc: str or function
                membership function
            nmfunc: str or function
                non-membership function
            __mfnum: int
                number of membership function parameters.
                Note that the number of parameters must be 2 and can not be modified
            __nmfnum: int
                number of non-membership function parameters.
                Note that the number of parameters must be 2 and can not be modified
        Methods:
            generate: function
                generate a Q-rung dual hesitant fuzzy element satisfying
                the condition.
    """
    # membership function
    # #non-membership function
    mfunc = None
    nmfunc = None

    __mfnum = 2
    __nmfnum = 2

    def __init__(self, qrung, func, params, custom=False):
        fe = 'qrungivfn'
        super(ivfngener, self).__init__(qrung, fe, func, params, custom)
        assert self.__mfnum == len(params[0]), 'membership function parameter setting error. ' \
                                               'There can only be two set of parameters'
        assert self.__nmfnum == len(params[1]), 'non-membership function parameter setting error. ' \
                                                'There can only be two set of parameters'

        self.mf = memfunc(self.mfunc, self.md_params, self.custom)
        self.nmf = memfunc(self.nmfunc, self.nmd_params, self.custom)

    def __call__(self, x, y):
        return self.generate(x, y)

    @property
    def mfnum(self):
        return self.__mfnum

    @property
    def nmfnum(self):
        return self.__nmfnum

    def generate(self, x, y):
        assert self.variable_start <= x <= self.variable_end, \
            'The independent variable x is not in the range of %d and %d' % (
                self.variable_start, self.variable_end)
        assert self.variable_start <= y <= self.variable_end, \
            'The independent variable y is not in the range of %d and %d' % (
                self.variable_start, self.variable_end)

        ivf = zero('qrungivfn', self.qrung)
        md = np.sort(self.mf(x))
        nmd = np.sort(self.nmf(y))
        ivf.set_md(md)
        ivf.set_nmd(nmd)
        if ivf.isLegal():
            return ivf
        else:
            raise ValueError('The fuzzy element is not valid.')


class ifngener(fuzzgener):
    """
        Qrung intuitionistic fuzzy number fuzzgener. As a subclass of fuzzgener,
        this class inherits most of the properties of the parent class, and can
        access the private properties of the parent class through the decorator
        set by the parent class. By inputting qrung, type of fuzzy element,
        membership function, parameters and user-defined settings, the fuzzgener
        can finally calculate a Q-rung intuitionistic fuzzy number satisfying
        the condition.

        Attributes:
            mfunc: str or function
                membership function
            nmfunc: str or function
                non-membership function
            __mfnum: int
                number of membership function parameters.
                Note that the number of parameters must be 1 and can not be modified
            __nmfnum: int
                number of non-membership function parameters.
                Note that the number of parameters must be 1 and can not be modified
        Methods:
            generate: function
                generate a Q-rung dual hesitant fuzzy element satisfying
                the condition.
    """
    # membership function
    # #non-membership function
    mfunc = None
    nmfunc = None

    __mfnum = 1
    __nmfnum = 1

    def __init__(self, qrung, func, params, custom=False):
        fe = 'qrungifn'
        super(ifngener, self).__init__(qrung, fe, func, params, custom)
        assert self.__mfnum == len(params[0]), 'membership function parameter setting error. ' \
                                               'There can only be one set of parameters'
        assert self.__nmfnum == len(params[1]), 'non-membership function parameter setting error. ' \
                                                'There can only be one set of parameters'

        self.mf = memfunc(self.mfunc, self.md_params, self.custom)
        self.nmf = memfunc(self.nmfunc, self.nmd_params, self.custom)

    def __call__(self, x, y):
        return self.generate(x, y)

    @property
    def mfnum(self):
        return self.__mfnum

    @property
    def nmfnum(self):
        return self.__nmfnum

    def generate(self, x, y):
        assert self.variable_start <= x <= self.variable_end, \
            'The independent variable x is not in the range of %d and %d' % (
                self.variable_start, self.variable_end)
        assert self.variable_start <= y <= self.variable_end, \
            'The independent variable y is not in the range of %d and %d' % (
                self.variable_start, self.variable_end)

        fn = zero('qrungifn', self.qrung)
        md = np.sort(self.mf(x))
        nmd = np.sort(self.nmf(y))
        fn.set_md(md)
        fn.set_nmd(nmd)
        if fn.isLegal():
            return fn
        else:
            raise ValueError('The fuzzy element is not valid.')
