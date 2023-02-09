#  Copyright (c) yibocat 2023 All Rights Reserved
#  Python: 3.10.9
#  Date: 2023/2/1 下午5:37
#  Author: yibow
#  Email: yibocat@yeah.net
#  Software: FuzzPy

from matplotlib import pyplot as plt
from fuzzyelement.FNumbers import qrungfn
from .generateMF import *


class FNGenerator(object):
    """
        Q阶模糊数生成器

        ================================================================

        说明：
            这是一个Q阶模糊数生成器，利用Q阶模糊隶属函数生成器生成，有两种方式：
                1. 使用内建的 8 种隶属函数
                2. 自定义隶属函数，属性 customFunc 来区分使用哪种隶属函数
        属性：
            qrung: 表示创建哪种对偶犹豫模糊元素。若 qrung=1 表示直觉模糊数，qrung=2 表示毕达哥拉斯模糊数；qrung=3 表示费马模糊数
            customFunc: 表示自定义函数开关，用来选择哪种隶属函数。若为 False 则使用内建的 8 种隶属函数；若为 True 则使用自定义隶属函数
            _variable_start,_variable_end,_linspace: 为三个私有属性，表示自变量范围和自变量间隔
            MF_parameter:表示隶属度参数列表
            NMF_parameter:表示非隶属度参数列表
            MFunc, NMFunc:  当 customFunc 为 False 时，MFunc 和 NMFunc 表示内建隶属函数的函数名，‘str’类型
                            当 customFunc 为 True 时，MFunc 和 NMFunc 表示自定义函数本身，‘Function’ 类型
            mf:表示生成的隶属函数，MemshipFC 类型或 CustomMemshipFC 类型
            nmf:表示生成的非隶属函数，MemshipFC 类型或 CustomMemshipFC 类型
        方法：
            MFgeneratorSetting(self,MFunc,MFnum,MFparas) 表示隶属函数设置
            NMFgeneratorSetting(self,NMFunc,NMFnum,NMFparas) 表示非隶属函数设置
            setVariable: 设置自变量范围和间隔
            generatorFunc: 生成隶属度和非隶属度函数
            MF_NMF_Plot: 画出隶属度和非隶属度的曲线图
            generator: 生成Q阶模糊数
        步骤（注意：步骤不可打乱）：
            1. 先初始化，创建一个Q阶模糊数生成器
            2. 设置隶属度函数和非隶属度函数，使用 MFgeneratorSetting 和 NMFgeneratorSetting 方法
            3. 设置自变量范围和间隔
            4. 生成 FN
    """
    qrung = 0
    customFunc = False

    _variable_start = 0
    _variable_end = 1
    _linspace = 100

    def __init__(self, q, customFunc=False):
        self.qrung = q

        self.MF_parameter = []
        self.NMF_parameter = []

        self.customFunc = customFunc
        if not self.customFunc:
            self.MFunc = ''
            self.NMFunc = ''
            self.mf = _memshipFunc(self.MFunc, self.MF_parameter)
            self.nmf = _memshipFunc(self.NMFunc, self.NMF_parameter)
        else:
            self.MFunc = None
            self.NMFunc = None
            self.mf = _customMemFunc(self.MFunc, self.MF_parameter)
            self.nmf = _customMemFunc(self.NMFunc, self.NMF_parameter)

    def __repr__(self):
        return 'Membership function:\n' + str(self.mf) + '\n' + 'Non-Membership function:\n' + str(self.nmf)

    def MFgeneratorSettings(self, MFunc, MFparas):
        """
            隶属函数设置:
            先判断是否为自定义函数，查看 customFunc 属性
            MFunc:  当不是自定义函数时，str 类型，表示函数的名称
                    当是自定义函数时，function 类型，表示函数本身
            MFparas:表示参数
        """
        if self.customFunc:
            self.MFunc = MFunc
            self.MF_parameter = MFparas
            assert hasattr(self.MFunc, '__call__'), 'ERROR:The MFunc is not a function!'
        else:
            assert MFunc == 'sigmf' or MFunc == 'trimf' or MFunc == 'zmf' or MFunc == 'smf' or MFunc == 'gaussmf' or MFunc == 'gauss2mf' or MFunc == 'gbellmf' or MFunc == 'trapmf', \
                'ERROR! Wrong membership function!'
            self.MFunc = MFunc
            self.MF_parameter = MFparas

    def NMFgeneratorSettings(self, NMFunc, NMFparas):
        """
            非隶属函数设置:
            先判断是否为自定义函数，查看 customFunc 属性
            NMFunc:  当不是自定义函数时，str 类型，表示函数的名称
                     当是自定义函数时，function 类型，表示函数本身
            NMFparas:表示参数
        """
        if self.customFunc:
            self.NMFunc = NMFunc
            self.NMF_parameter = NMFparas
            assert hasattr(self.NMFunc, '__call__'), 'ERROR:The NMFunc is not a function!'
        else:
            assert NMFunc == 'sigmf' or NMFunc == 'trimf' or NMFunc == 'zmf' or NMFunc == 'smf' or NMFunc == 'gaussmf' or NMFunc == 'gauss2mf' or NMFunc == 'gbellmf' or NMFunc == 'trapmf', \
                'ERROR! Wrong membership function!'
            self.NMFunc = NMFunc
            self.NMF_parameter = NMFparas

    def setVariable(self, start, end, linspace):
        """
            设置自变量表示范围
            start 表示开始
            end 表示结束
            linspace 表示间隔

            该函数可以用来调整图像的显示范围
        """
        self._variable_start = start
        self._variable_end = end
        self._linspace = linspace

    def generatorFunc(self):
        """
            隶属度函数与非隶属度函数生成器
            首先设置参数
            其次设置环境
        """

        if not self.customFunc:
            assert self.MFunc != '' and self.NMFunc != '' and self.MF_parameter != [] and self.NMF_parameter != [], \
                'Membership function or parameter or number of function has not been set! Please set the membership and non-membership function first.'
            self.mf = _memshipFunc(self.MFunc, self.MF_parameter)
            self.nmf = _memshipFunc(self.NMFunc, self.NMF_parameter)
        else:
            assert hasattr(self.MFunc, '__call__') and hasattr(self.NMFunc,
                                                               '__call__'), 'ERROR:The MFunc and NMFunc are not function type!'
            self.mf = _customMemFunc(self.MFunc, self.MF_parameter)
            self.nmf = _customMemFunc(self.NMFunc, self.NMF_parameter)

        self.mf.setvariable(self._variable_start, self._variable_end, self._linspace)
        self.nmf.setvariable(self._variable_start, self._variable_end, self._linspace)

        print(self.__repr__())

    def MF_NMF_Plot(self):
        """
            画图，分别画出隶属度和非隶属度的曲线图
        """
        # np.linspace(self._variable_start, self._variable_end, self._linspace)
        mf = self.mf
        nmf = self.nmf

        mf.MF_Plot('Membership func')
        nmf.MF_Plot('Non-Membership func')

    def generator(self, x, y):
        """
            生成模糊元素
            x 表示隶属函数的自变量取值
            y 表示非隶属函数的自变量取值
        """

        assert self._variable_start <= x <= self._variable_end, 'The independent variable x is not in the range of %d and %d' % (
            self._variable_start, self._variable_end)
        assert self._variable_start <= y <= self._variable_end, 'The independent variable y is not in the range of %d and %d' % (
            self._variable_start, self._variable_end)

        newFN = qrungfn(self.qrung, 0., 0.)
        md = self.mf.calculate_MD(x)
        nmd = self.nmf.calculate_MD(y)
        assert np.max(md) ** self.qrung + np.max(nmd) ** self.qrung <= 1, 'The MD^' + str(self.qrung) + '+NMD^' + str(
            self.qrung) + '<=1 and >=0. Please reset the parameters'
        assert np.min(md) ** self.qrung + np.min(nmd) ** self.qrung >= 0, 'The MD^' + str(self.qrung) + '+NMD^' + str(
            self.qrung) + '<=1 and >=0. Please reset the parameters'
        newFN.md = md
        newFN.nmd = nmd

        return newFN


class _memshipFunc(object):
    """
        隶属度或非隶属度函数类，将各种隶属度函数整理成一个集合类，方便计算对偶犹豫模糊可能隶属度和可能非隶属度

        ----------------------------------------------------------------

        属性：
            memFunc: 表示隶属度函数名称，共有 8 种隶属度函数，分别是：
                sigmf(x,a,b)          基本 Sigmoid 激活函数      a 表示偏差或偏移量，b表示激活区域(越大越平坦)
                trimf(x,[a,b,c])      三角函数                  [a,b,c]表示三角的三点组成的数组，满足 a<=b<=c
                zmf(x,a,b)            Z-函数                    形状如 Z，a 表示函数做变化，b 表示函数右变化，满足 a<=b
                trapmf(x,[a,b,c,d])   梯形函数                  [a,b,c,d]表示梯形的四个点，满足 a<=b<=c<=d
                smf(x,a,b)            S-函数                    a 表示从 0 开始爬升的点，b 表示趋于 1 的稳定的点
                gaussmf(x,a,b)        高斯函数                  a 表示均值或中心值，b 表示标准差的高斯参数
                gauss2mf(x,a,b,c,d)   双结合高斯函数             a 表示第一个高斯函数的均值，b 表示第一个高斯函数标准差的高斯参数，c 和 d 分别表示第二个高斯函数的参数
                gbellmf(x,a,b,c)      广义贝尔函数               a 表示宽度，b 表示斜率，c 表示偏差或中心点

                注意：memFunc 只能是一种隶属函数，不支持多种函数，即 memFunc 不为数组
            parameter: 表示函数的参数数组
                parameter[(a,b),(a,b)] 为 tuple 类型的有2个的参数数组，适用 sigmf,zmf,smf,gaussmf
                parameter[[a,b,c],[a,b,c]] 为 list 类型的有3个参数的参数数组，适用 trimf
            numFunc: 表示函数个个数，也表示可能隶属度的个数。例如一个对偶犹豫模糊元素的隶属度有 3 个可能的值，则意味着 numFunc = 3

            _variable_start,_variable_end,_linspace: 表示函数的自变量范围，start 为起始自变量值，end 为终止自变量，linspace 为数间隔。
                默认为(0,1,100)，表示自变量范围 0-1，总共有 100 个数。
                属性为私有属性，外部不可调用，但可以通过 setvariable() 方法修改
        方法:
            setvariable(self,start,end,linspace):  设置自变量范围和间隔
            _min_generateMF(self):                 计算 self 设置好的自变量范围和参数下的范围内函数最小值，目的是被隶属度函数减去以标准化隶属度函数
            _generateMF(self,x):                   生成隶属度集合
            MF_Plot(self):                         画出设置的隶属度函数曲线，方便观察
            calculate_MD(self,x):                  计算 x 的隶属度，返回一个长度为 numFunc 的 array 类型的数组，即可能隶属度或非隶属度
    """
    memFunc = ''
    parameter = []

    _variable_start = 0
    _variable_end = 1
    _linspace = 100

    def __init__(self, memFunc, parameter):
        """
            Set membership conditions：
            ===============================================
            Parameter:
                sigmf:   (a,b)      ->tuple /
                trimf:   [a,b,c]    ->list  /
                zmf:     (a,b)      ->tuple /
                trapmf:  [a,b,c,d]  ->list  /
                smf:     (a,b)      ->tuple /
                gaussmf: (a,b)      ->tuple /
                gauss2mf:(a,b,c,d)  ->tuple /
                gbellmf: (a,b,c)    ->tuple /
        """
        if memFunc == 'sigmf' or memFunc == 'zmf' or memFunc == 'smf' or memFunc == 'gaussmf':
            assert type(
                parameter) == tuple, 'ERROR:The %s function\'s parameter type is error!Parameter type should be tuple! ' % memFunc
            assert len(
                parameter) == 2, 'ERROR:The number of the %s function is error!The number of parameters should be 2 ' % memFunc
        elif memFunc == 'gauss2mf':
            assert type(
                parameter) == tuple, 'ERROR:The %s function\'s parameter type is error!Parameter type should be tuple! ' % memFunc
            assert len(
                parameter) == 4, 'ERROR:The number of the %s function is error!The number of parameters should be 4 ' % memFunc
        elif memFunc == 'gbellmf':
            assert type(
                parameter) == tuple, 'ERROR:The %s function\'s parameter type is error!Parameter type should be tuple! ' % memFunc
            assert len(
                parameter) == 3, 'ERROR:The number of the %s function is error!The number of parameters should be 3 ' % memFunc
        elif memFunc == 'trimf':
            assert type(
                parameter) == list, 'ERROR:The %s function\'s parameter type is error!Parameter type should be list! ' % memFunc
            assert len(
                parameter) == 3, 'ERROR:The number of the %s function is error!The number of parameters should be 3 ' % memFunc
        elif memFunc == 'trapmf':
            assert type(
                parameter) == list, 'ERROR:The %s function\'s parameter type is error!Parameter type should be list! ' % memFunc
            assert len(
                parameter) == 4, 'ERROR:The number of the %s function is error!The number of parameters should be 4 ' % memFunc
        else:
            assert memFunc == '', 'ERROR!Wrong function name!'

        self.memFunc = memFunc
        self.parameter = parameter

    def __repr__(self):
        """
            打印隶属函数信息
        """
        return 'Function: %s, parameter: %s' % (self.memFunc, self.parameter)

    def setvariable(self, start, end, linspace):
        """
            设置自变量变化范围，返回一个 start-end ，间隔为 linspace 的 array
            该函数用来生成隶属函数实例的空间范围
        """
        self._variable_start = start
        self._variable_end = end
        self._linspace = linspace

    def _generateMF(self, x):
        """
            生成函数隶属度
        """
        y = 0
        if self.memFunc == 'sigmf':
            y = sigmf(x, self.parameter[0], self.parameter[1]) - self._min_generateMF()
        if self.memFunc == 'zmf':
            y = zmf(x, self.parameter[0], self.parameter[1]) - self._min_generateMF()
        if self.memFunc == 'smf':
            y = smf(x, self.parameter[0], self.parameter[1]) - self._min_generateMF()
        if self.memFunc == 'gaussmf':
            y = gaussmf(x, self.parameter[0], self.parameter[1]) - self._min_generateMF()
        if self.memFunc == 'gauss2mf':
            y = gauss2mf(x, self.parameter[0], self.parameter[1], self.parameter[2],
                         self.parameter[3]) - self._min_generateMF()
        if self.memFunc == 'gbellmf':
            y = gbellmf(x, self.parameter[0], self.parameter[1], self.parameter[2]) - self._min_generateMF()
        if self.memFunc == 'trimf':
            y = trimf(x, self.parameter) - self._min_generateMF()
        if self.memFunc == 'trapmf':
            y = trapmf(x, self.parameter) - self._min_generateMF()
        return y

    def _min_generateMF(self):
        """
            计算隶属度函数在当前参数和当前自变量范围下的最小值
            该函数的作用是将隶属函数沿 y 轴方向向下平移最小值个单位，保证隶属度函数的值<=1
            可以理解为函数的系数
        """
        x = np.linspace(self._variable_start, self._variable_end, self._linspace)
        min_mf = 0
        if self.memFunc == 'sigmf':
            min_mf = min(sigmf(x, self.parameter[0], self.parameter[1]))
        if self.memFunc == 'zmf':
            min_mf = min(zmf(x, self.parameter[0], self.parameter[1]))
        if self.memFunc == 'smf':
            min_mf = min(smf(x, self.parameter[0], self.parameter[1]))
        if self.memFunc == 'gaussmf':
            min_mf = min(gaussmf(x, self.parameter[0], self.parameter[1]))
        if self.memFunc == 'gauss2mf':
            min_mf = min(gauss2mf(x, self.parameter[0], self.parameter[1], self.parameter[2], self.parameter[3]))
        if self.memFunc == 'gbellmf':
            min_mf = min(gbellmf(x, self.parameter[0], self.parameter[1], self.parameter[2]))
        if self.memFunc == 'trimf':
            min_mf = min(trimf(x, self.parameter))
        if self.memFunc == 'trapmf':
            min_mf = min(trapmf(x, self.parameter))
        return min_mf

    def _max_generateMF(self):
        """
            计算隶属函数在自变量范围内的最大值
        """
        x = np.linspace(self._variable_start, self._variable_end, self._linspace)
        max_mf = max(self._generateMF(x))
        return max_mf

    def get_min_generateMF(self):
        """
            获取自变量范围内各个隶属函数的最小值
            注意：这里的最小值是原隶属函数的最小值，即还没有向下平移过的隶属度最小值
                平移后的隶属度最小值均为 0!
        """
        return self._min_generateMF()

    def get_max_generateMF(self):
        """
            获取自变量范围内各个隶属函数的最大值
        """
        return self._max_generateMF()

    def MF_Plot(self, st):
        """
            画出隶属度曲线图，方便设置可能隶属度
        """
        x = np.linspace(self._variable_start, self._variable_end, self._linspace)
        y = self._generateMF(x)
        plt.figure(figsize=(8, 5))
        plt.plot(x, y, label=st + ': ' + self.memFunc)
        plt.grid(linestyle='-.')
        plt.legend()
        plt.show()

    def calculate_MD(self, x):
        """
            通过隶属度方程，计算隶属度集合
        """
        y = self._generateMF(x)
        return np.array(y)


class _customMemFunc(object):
    """
        自定义隶属函数生成器

        ----------------------------------------------------------------

        说明：
            MemshipFC 隶属函数生成器包含了 8 种基本隶属函数，而该生成器可以创建自定义隶属函数和非隶属函数
            注意：自建函数时，使用如下方法
            ---------------------------------
            |   def func_test(x,*p):        |
            |       return p[0]*x + p[1]    |
            ---------------------------------
            参数以 list 类型传入，表示为参数列表，然后在函数中使用列表元素的形式表示参数
        属性:
            ArbFunc: 表示自定义隶属函数方法，类型为‘function’
            parameter: 表示函数的参数列表
                parameter=[[2,4,5],[1,4,7],[2,6,3]] 表示为：有三个隶属函数，且参数列表分别为 [2,4,5],[1,4,7],[2,6,3] 的隶属函数
            numFunc: 表示自定义隶属函数的个数，例如对于一个犹豫模糊集，定义了 3 个隶属函数，那么该值为 3

        方法:
            setvariable(self,start,end,linspace):  设置自变量范围和间隔
            _min_generateMF(self):                 计算 self 设置好的自变量范围和参数下的范围内函数最小值，目的是被隶属度函数减去以标准化隶属度函数
            _generateMF(self,x):                   生成隶属度集合
            MF_Plot(self):                         画出设置的隶属度函数曲线，方便观察
            calculate_MD(self,x):                  计算 x 的隶属度，返回一个长度为 numFunc 的 array 类型的数组，即可能隶属度或非隶属度
    """
    parameter = []
    ArbFunc = None

    _variable_start = 0
    _variable_end = 1
    _linspace = 100

    def __init__(self, ArbFunc, parameter):
        assert hasattr(ArbFunc, '__call__') or ArbFunc is None, 'ERROR: The membership function has to be a function!'
        assert type(
            parameter) == list, 'ERROR:The custom function\'s parameter type is error! Parameter type should be list!'

        self.ArbFunc = ArbFunc
        self.parameter = np.asarray(parameter)

    def __repr__(self):
        """
            打印隶属函数信息
        """
        return 'Function : %s, parameters: %s' % (self.ArbFunc.__name__, self.parameter)

    def setvariable(self, start, end, linspace):
        """
            设置自变量变化范围，返回一个 start-end ，间隔为 linspace 的 array
            该函数用来生成隶属函数实例的空间范围
        """
        self._variable_start = start
        self._variable_end = end
        self._linspace = linspace

    def _generateMF(self, x):
        """
            生成函数的隶属度，组成一个列表集合
        """
        return self.ArbFunc(x, *self.parameter) - self._min_generateMF()

    def _min_generateMF(self):
        """
            计算隶属函数在当前参数和当前自变量范围下的最小值
            该函数的作用是将隶属函数沿 y 轴方向向下平移最小值个单位，保证隶属函数的值 <= 1
            可以理解为该函数的系数
        """
        x = np.linspace(self._variable_start, self._variable_end, self._linspace)
        min_mf = min(self.ArbFunc(x, *self.parameter))
        return min_mf

    def _max_generateMF(self):
        """
            计算隶属函数在自变量范围内的最大值
        """
        x = np.linspace(self._variable_start, self._variable_end, self._linspace)
        return max(self._generateMF(x))

    def get_min_generateMF(self):
        """
            获取自变量范围内各个隶属函数的最小值
            注意：这里的最小值是原隶属函数的最小值，即还没有向下平移过的隶属度最小值
                平移后的隶属度最小值均为 0!
        """
        return self._min_generateMF()

    def get_max_generateMF(self):
        """
            获取自变量范围内各个隶属函数的最大值
        """
        return self._max_generateMF()

    def MF_Plot(self, st):
        """
            画出隶属度曲线图，方便设置可能隶属度
        """
        x = np.linspace(self._variable_start, self._variable_end, self._linspace)
        y = self._generateMF(x)
        plt.figure(figsize=(8, 5))
        plt.plot(x, y, label=st + ': ' + self.ArbFunc.__name__)
        plt.grid(linestyle='-.')
        plt.legend()
        plt.show()

    def calculate_MD(self, x):
        """
            通过隶属度方程，计算隶属度集合
        """
        y = self._generateMF(x)
        return np.array(y)
