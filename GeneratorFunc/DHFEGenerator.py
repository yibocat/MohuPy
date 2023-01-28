from matplotlib import pyplot as plt

from DHFElements import HQrungF
from .generateMF import *


class DHFEGenerator(object):
    """
        对偶犹豫模糊元素生成器父类

        ================================================================
        说明：
            这是一个对偶犹豫模糊元素生成器，利用对偶犹豫模糊隶属度函数生成器生成，有两种方式：
                1. 使用内建的 8 种隶属函数
                2. 自定义隶属函数，属性 customFunc 来区分使用哪种隶属函数
        属性：
            qrung: 表示创建哪种对偶犹豫模糊元素。若 qrung=1 表示对偶犹豫模糊元素；qrung=2 表示对偶犹豫毕达哥拉斯模糊元素；qrung=3 表示对偶犹豫费马模糊元素
            customFunc 表示自定义函数开关，用来选择哪种隶属函数。若为 False 则使用内建的 8 种隶属函数；若为 True 则使用自定义隶属函数
            _variable_start,_variable_end,_linspace 为三个私有属性，表示自变量范围和自变量间隔
            MF_parameter 表示隶属度参数列表
            NMF_parameter 表示非隶属度参数列表
            numMFC 表示隶属函数个数
            numNMFC 表示非隶属度函数个数
            MFunc, NMFunc:  当 customFunc 为 False 时，MFunc 和 NMFunc 表示内建隶属函数的函数名，‘str’类型
                            当 customFunc 为 True 时，MFunc 和 NMFunc 表示自定义函数本身，‘Function’ 类型

            mf 表示生成的隶属函数集合，MemshipFC 类型或 CustomMemshipFC 类型
            nmf 表示生成的非隶属函数集合，MemshipFC 类型或 CustomMemshipFC 类型
        方法：
            MFgeneratorSet(self,MFunc,MFnum,MFparas) 表示隶属函数设置
            NMFgeneratorSet(self,NMFunc,NMFnum,NMFparas) 表示非隶属函数设置
            set_Variable: 设置自变量范围和间隔
            generator_function: 生成隶属度和非隶属度函数
            MF_NMF_Plot: 画出隶属度和非隶属度的曲线图
            generator_DHFE: 生成 DHFE
        步骤：
            1. 先初始化，创建一个对偶犹豫模糊元素生成器
            2. 设置隶属度函数和非隶属度函数，使用 MFgeneratorSet 和 NMFgeneratorSet 方法
            3. 设置自变量范围和间隔
            4. 生成 DHFE
            注意：步骤不可打乱
    """
    qrung = 0
    customFunc = False  # 自定义函数开关，False 表示使用内建函数，True 表示使用自定义函数，默认为 False

    _variable_start = 0
    _variable_end = 1
    _linspace = 100

    numMFC = 0
    numNMFC = 0

    def __init__(self, q, customFunc=False):
        self.qrung = q

        self.MF_parameters = []
        self.NMF_parameters = []

        self.customFunc = customFunc
        if self.customFunc:
            self.MFunc = None
            self.NMFunc = None
            self.mf = _customMemFunc(self.MFunc, self.MF_parameters, self.numMFC)
            self.nmf = _customMemFunc(self.NMFunc, self.NMF_parameters, self.numNMFC)
        else:
            self.MFunc = ''
            self.NMFunc = ''
            self.mf = _memshipFunc(self.MFunc, self.NMF_parameters, self.numMFC)
            self.nmf = _memshipFunc(self.NMFunc, self.NMF_parameters, self.numNMFC)

    def __repr__(self):
        return 'Membership function:\n' + str(self.mf) + '\n' + 'Non-Membership function:\n' + str(self.nmf)

    def MFgeneratorSettings(self, MFunc, MFnum, MFparas):
        """
            隶属函数设置:
            先判断是否为自定义函数，查看 customFunc 属性
            MFunc:  当不是自定义函数时，str 类型，表示函数的名称
                    当是自定义函数时，function 类型，表示函数本身
            MFnum:  表示隶属函数的个数
            MFparas:表示参数列表
        """
        if self.customFunc:
            self.MFunc = MFunc
            self.numMFC = MFnum
            self.MF_parameters = MFparas
            assert len(
                self.MF_parameters) == self.numMFC, 'The number of MFCs has not been set or does not match the number of parameters.'
        else:
            assert MFunc == 'sigmf' or MFunc == 'trimf' or MFunc == 'zmf' or MFunc == 'smf' or MFunc == 'gaussmf' or MFunc == 'gauss2mf' or MFunc == 'gbellmf' or MFunc == 'trapmf', \
                'ERROR! Wrong membership function!'
            self.MFunc = MFunc
            self.numMFC = MFnum
            self.MF_parameters = MFparas
            assert len(
                self.MF_parameters) == self.numMFC, 'The number of MFCs has not been set or does not match the number of parameters.'

    def NMFgeneratorSettings(self, NMFunc, NMFnum, NMFparas):
        """
            非隶属函数设置:
            先判断是否为自定义函数，查看 customFunc 属性
            NMFunc:  当不是自定义函数时，str 类型，表示函数的名称
                     当是自定义函数时，function 类型，表示函数本身
            NMFnum:  表示非隶属函数的个数
            NMFparas:表示参数列表
        """
        if self.customFunc:
            self.NMFunc = NMFunc
            self.numNMFC = NMFnum
            self.NMF_parameters = NMFparas
            assert len(
                self.NMF_parameters) == self.numNMFC, 'The number of MFCs has not been set or does not match the number of parameters.'
        else:
            assert NMFunc == 'sigmf' or NMFunc == 'trimf' or NMFunc == 'zmf' or NMFunc == 'smf' or NMFunc == 'gaussmf' or NMFunc == 'gauss2mf' or NMFunc == 'gbellmf' or NMFunc == 'trapmf', \
                'ERROR! Wrong non-membership function!'
            self.NMFunc = NMFunc
            self.numNMFC = NMFnum
            self.NMF_parameters = NMFparas
            assert len(
                self.NMF_parameters) == self.numNMFC, 'The number of NMFCs has not been set or does not match the number of parameters.'

    def setVariable(self, start, end, linspace):
        """
            设置自变量范围和间隔
            start:  自变量起始值
            end:  自变量终止值
            linspace: 自变量间隔

            该函数可以用来调整图像的显示范围
        """
        self._variable_start = start
        self._variable_end = end
        self._linspace = linspace

    def generatorFunc(self):
        """
            生成隶属度和非隶属度函数
            首先设置参数，然后设置环境
        """
        if self.customFunc:
            assert hasattr(self.MFunc, '__call__') and hasattr(self.NMFunc,
                                                               '__call__'), 'ERROR:The MFunc and NMFunc are not function type!'
            self.mf = _customMemFunc(self.MFunc, self.MF_parameters, self.numMFC)
            self.nmf = _customMemFunc(self.NMFunc, self.NMF_parameters, self.numNMFC)
        else:
            assert self.MFunc != '' and self.NMFunc != '' and \
                   self.MF_parameters != [] and self.NMF_parameters != [] \
                   and self.numMFC != 0 and self.numNMFC != 0, 'Membership function or parameter or number of function has not been set! Please set the membership and non-membership function first.'
            self.mf = _memshipFunc(self.MFunc, self.MF_parameters, self.numMFC)
            self.nmf = _memshipFunc(self.NMFunc, self.NMF_parameters, self.numNMFC)

        self.mf.setvariable(self._variable_start, self._variable_end, self._linspace)
        self.nmf.setvariable(self._variable_start, self._variable_end, self._linspace)

        print(self.__repr__())

    def MF_NMF_Plot(self):
        """
            画图，分别画出隶属度和非隶属度的曲线图
        """
        # x = np.linspace(self._variable_start, self._variable_end, self._linspace)
        mf = self.mf
        nmf = self.nmf

        mf.MF_Plot('Membership func')
        nmf.MF_Plot('Non-Membership func')

    def generator(self, x, y):
        """
        生成 Q 阶序对犹豫模糊元素
            x:  隶属函数自变量取值
            y:  非隶属函数自变量取值
        """
        assert self._variable_start <= x <= self._variable_end, 'The independent variable x is not in the range of %d and %d' % (
            self._variable_start, self._variable_end)
        assert self._variable_start <= y <= self._variable_end, 'The independent variable y is not in the range of %d and %d' % (
            self._variable_start, self._variable_end)

        newDHFE = HQrungF(self.qrung, [], [])
        md = self.mf.calculate_MD(x)
        nmd = self.nmf.calculate_MD(y)
        assert np.max(md) ** self.qrung + np.max(nmd) ** self.qrung <= 1, 'The MD^' + str(self.qrung) + '+NMD^' + str(
            self.qrung) + '<=1 and >=0. Please reset the parameters'
        assert np.min(md) ** self.qrung + np.min(nmd) ** self.qrung >= 0, 'The MD^' + str(self.qrung) + '+NMD^' + str(
            self.qrung) + '<=1 and >=0. Please reset the parameters'
        newDHFE.md = md
        newDHFE.nmd = nmd

        return newDHFE


class _memshipFunc(object):
    """
        隶属度或非隶属度函数类，将各种隶属度函数整理成一个集合类，方便计算对偶犹豫模糊可能隶属度和可能非隶属度
        =====================================================================================
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
    numFunc = 0

    _variable_start = 0
    _variable_end = 1
    _linspace = 100

    def __init__(self, memFunc, parameter, numFunc):
        """
            Set membership conditions：
            ===============================================
            Parameter:
                sigmf:   (a,b)     ->[(a,b)]     ->tuple /
                trimf:   [a,b,c]   ->[[a,b,c]]   ->list  /
                zmf:     (a,b)     ->[(a,b)]     ->tuple /
                trapmf:  [a,b,c,d] ->[[a,b,c,d]] ->list
                smf:     (a,b)     ->[(a,b)]     ->tuple /
                gaussmf: (a,b)     ->[(a,b)]     ->tuple /
                gauss2mf:(a,b,c,d) ->[(a,b,c,d)] ->tuple /
                gbellmf: (a,b,c)   ->[(a,b,c)]   ->tuple /
        """
        assert len(parameter) == numFunc, \
            'ERROR!The number of parameters is not equal to numFunc! numFunc=%d means you should create %d sets of parameters' % (
                numFunc, numFunc)
        if memFunc == 'sigmf' or memFunc == 'zmf' or memFunc == 'smf' or memFunc == 'gaussmf':
            for para in parameter:
                assert type(
                    para) == tuple, 'ERROR:The %s function\'s parameter type is error!Parameter type should be tuple!' % memFunc
                assert len(
                    para) == 2, 'ERROR:The number of the %s function is error!The number of parameters should be 2' % memFunc
        elif memFunc == 'gauss2mf':
            for para in parameter:
                assert type(
                    para) == tuple, 'ERROR:The %s function\'s parameter type is error!Parameter type should be tuple!' % memFunc
                assert len(
                    para) == 4, 'ERROR:The number of the %s function is error!The number of parameters should be 4' % memFunc
        elif memFunc == 'gbellmf':
            for para in parameter:
                assert type(
                    para) == tuple, 'ERROR:The %s function\'s parameter type is error!Parameter type should be tuple!' % memFunc
                assert len(
                    para) == 3, 'ERROR:The number of the %s function is error!The number of parameters should be 3' % memFunc
        elif memFunc == 'trimf':
            for para in parameter:
                assert type(
                    para) == list, 'ERROR:The %s function\'s parameter type is error!Parameter type should be list!' % memFunc
                assert len(
                    para) == 3, 'ERROR:The number of the %s function is error!The number of parameters should be 3' % memFunc
        elif memFunc == 'trapmf':
            for para in parameter:
                assert type(
                    para) == list, 'ERROR:The %s function\'s parameter type is error!Parameter type should be list!' % memFunc
                assert len(
                    para) == 4, 'ERROR:The number of the %s function is error!The number of parameters should be 4' % memFunc
        else:
            assert memFunc == '', 'ERROR!Wrong function name!'

        self.memFunc = memFunc
        self.parameter = parameter
        self.numFunc = numFunc

    def __repr__(self):
        """
            Print information of membership function.
        """
        s = ''
        for i in range(self.numFunc):
            s += 'Function %d: %s, parameter:%s \n' % (i + 1, self.memFunc, self.parameter[i])
        return s

    def setvariable(self, _variable_start, _variable_end, _linspace):
        """
            设置自变量变化范围，返回一个 start-end ，间隔为 linspace 的 array。该函数用来生成隶属函数实例的空间范围
            self._variable_start = _variable_start
            self._variable_end = _variable_end
            self._linspace = _linspace
            :param _variable_start:     the start position of the variable
            :param _variable_end:       the end position of the variable
            :param _linspace:           the linspace of the variable
            :return:None
        """
        self._variable_start = _variable_start
        self._variable_end = _variable_end
        self._linspace = _linspace

    def _generateMF(self, x):
        """
            生成各函数的隶属度，组成一个列表集合
        """
        y = []
        for i in range(self.numFunc):
            if self.memFunc == 'sigmf':
                y.append(sigmf(x, self.parameter[i][0], self.parameter[i][1]) - self._min_generateMF()[i])
            if self.memFunc == 'zmf':
                y.append(zmf(x, self.parameter[i][0], self.parameter[i][1]) - self._min_generateMF()[i])
            if self.memFunc == 'smf':
                y.append(smf(x, self.parameter[i][0], self.parameter[i][1]) - self._min_generateMF()[i])
            if self.memFunc == 'gaussmf':
                y.append(gaussmf(x, self.parameter[i][0], self.parameter[i][1]) - self._min_generateMF()[i])
            if self.memFunc == 'gauss2mf':
                y.append(gauss2mf(x, self.parameter[i][0], self.parameter[i][1], self.parameter[i][2],
                                  self.parameter[i][3]) - self._min_generateMF()[i])
            if self.memFunc == 'gbellmf':
                y.append(gbellmf(x, self.parameter[i][0], self.parameter[i][1], self.parameter[i][2]) -
                         self._min_generateMF()[i])
            if self.memFunc == 'trimf':
                y.append(trimf(x, self.parameter[i]) - self._min_generateMF()[i])
            if self.memFunc == 'trapmf':
                y.append(trapmf(x, self.parameter[i]) - self._min_generateMF()[i])
        return y

    def _min_generateMF(self):
        """
            计算隶属度函数在当前参数和当前自变量范围下的最小值
            该函数的作用是将隶属函数沿 y 轴方向向下平移最小值个单位，保证隶属度函数的值<=1
            可以理解为函数的系数
        """
        min_mf = []
        x = np.linspace(self._variable_start, self._variable_end, self._linspace)
        for i in range(self.numFunc):
            if self.memFunc == 'sigmf':
                min_mf.append(min(sigmf(x, self.parameter[i][0], self.parameter[i][1])))
            if self.memFunc == 'zmf':
                min_mf.append(min(zmf(x, self.parameter[i][0], self.parameter[i][1])))
            if self.memFunc == 'smf':
                min_mf.append(min(smf(x, self.parameter[i][0], self.parameter[i][1])))
            if self.memFunc == 'gaussmf':
                min_mf.append(min(gaussmf(x, self.parameter[i][0], self.parameter[i][1])))
            if self.memFunc == 'gauss2mf':
                min_mf.append(min(gauss2mf(x, self.parameter[i][0], self.parameter[i][1], self.parameter[i][2],
                                           self.parameter[i][3])))
            if self.memFunc == 'gbellmf':
                min_mf.append(min(gbellmf(x, self.parameter[i][0], self.parameter[i][1], self.parameter[i][2])))
            if self.memFunc == 'trimf':
                min_mf.append(min(trimf(x, self.parameter[i])))
            if self.memFunc == 'trapmf':
                min_mf.append(min(trapmf(x, self.parameter[i])))
        return min_mf

    def _max_generateMF(self):
        """
            计算隶属函数在自变量范围内的最大值
        """
        x = np.linspace(self._variable_start, self._variable_end, self._linspace)
        y = self._generateMF(x)

        max_mf = []
        for i in range(self.numFunc):
            max_mf.append(max(y[i]))

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
        for j in range(self.numFunc):
            plt.plot(x, y[j], label=st + ': ' + self.memFunc + '_%d' % (j + 1))
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
        自建隶属函数生成器
        ========================================================================================
        说明：
            MemshipFC 隶属函数生成器包含了 8 种基本的隶属函数，而该生成器可以创建自定义隶属函数和非隶属函数
            注意：自建函数时，使用如下方法
            ---------------------------------
            |   def func_test(x,*p):        |
            |       return p[0]*x + p[1]    |
            ---------------------------------
            参数以 list 类型传入，表示为参数列表，然后在函数中使用列表元素的形式表示参数
        ========================================================================================
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
    numFunc = 0
    ArbFunc = None  # custom function

    _variable_start = 0
    _variable_end = 1
    _linspace = 100

    def __init__(self, ArbFunc, parameter, numFunc):
        assert len(parameter) == numFunc, 'ERROR!The number of parameters is not equal to numFunc! ' \
                                          'numFunc=%d means you should create %d sets of parameters ' % (
                                              numFunc, numFunc)
        assert hasattr(ArbFunc, '__call__') or ArbFunc is None, 'ERROR: The membership function has to be a function!'
        for para in parameter:
            assert type(
                para) == list, 'ERROR:The custom function\'s parameter type is error! Parameter type should be list!'

        self.ArbFunc = ArbFunc
        self.parameter = np.asarray(parameter)
        self.numFunc = numFunc

    def __repr__(self):
        """
            Print information of membership function.
        """
        s = ''
        for i in range(self.numFunc):
            s += 'Function %d: %s, parameter:%s \n' % (i + 1, self.ArbFunc.__name__, self.parameter[i])
        return s

    def setvariable(self, start, end, linspace):
        """
            设置自变量变化范围，返回一个 start-end ，间隔为 linspace 的 array
            该函数用来生成隶属函数实例的空间范围
            参数以 list 类型传入，表示为参数列表，然后在函数中使用列表元素的格式表示参数

            参数说明：
                start: 自变量的起始值
                end: 自变量的终止值
                linspace: 自变量的间隔
        """
        self._variable_start = start
        self._variable_end = end
        self._linspace = linspace

    def _generateMF(self, x):
        """
            生成函数的隶属度，组成一个列表集合
            参数以 list 类型传入，表示为参数列表，然后在函数中使用列表元素的形式表示参数

            参数说明：
                x: 自变量的值
        """
        y = []
        for i in range(self.numFunc):
            y.append(self.ArbFunc(x, *self.parameter[i]) - self._min_generateMF()[i])
            # y.append(self.ArbFunc(x, *self.parameter[i]))
        return y

    def _min_generateMF(self):
        """
            计算隶属函数在当前参数和当前自变量范围下的最小值
            该函数的作用是将隶属函数沿 y 轴方向向下平移最小值个单位，保证隶属函数的值 <= 1, 可以理解为该函数的系数
        """
        min_mf = []
        x = np.linspace(self._variable_start, self._variable_end, self._linspace)
        for i in range(self.numFunc):
            min_mf.append(min(self.ArbFunc(x, *self.parameter[i])))
        return min_mf

    def _max_generateMF(self):
        """
            计算隶属函数在自变量范围内的最大值
        """
        max_mf = []
        x = np.linspace(self._variable_start, self._variable_end, self._linspace)
        y = self._generateMF(x)

        for i in range(self.numFunc):
            max_mf.append(max(y[i]))
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

            参数说明：
                st: String  图片标题
        """
        x = np.linspace(self._variable_start, self._variable_end, self._linspace)
        y = self._generateMF(x)
        plt.figure(figsize=(8, 5))
        for j in range(self.numFunc):
            plt.plot(x, y[j], label=st + ': ' + self.ArbFunc.__name__ + '_%d' % (j + 1))
        plt.grid(linestyle='-.')
        plt.legend()
        plt.show()

    def calculate_MD(self, x):
        """
            通过隶属度方程，计算隶属度集合

            参数说明：
                x: 要计算的自变量，也就是确定值
        """
        y = self._generateMF(x)
        return np.array(y)
