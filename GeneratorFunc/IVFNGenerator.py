from matplotlib import pyplot as plt
from IVFNumbers import QrungIVFN
from .generateMF import *


class IVFNGenerator(object):
    qrung = 0
    customFunc = False

    _variable_start = 0
    _variable_end = 1
    _linspace = 100

    def __init__(self, q, customFunc=False):
        self.qrung = q
        self.upp_mfpara = []
        self.low_mfpara = []
        self.upp_nmfpara = []
        self.low_nmfpara = []

        self.customFunc = customFunc

        if not self.customFunc:
            self.MFunc = ''
            self.NMFunc = ''
            self.mf = _memshipFunc(self.MFunc, self.low_mfpara, self.upp_mfpara)
            self.nmf = _memshipFunc(self.NMFunc, self.low_nmfpara, self.upp_nmfpara)
        else:
            self.MFunc = None
            self.NMFunc = None
            self.mf = _customMemFunc(self.MFunc, self.low_mfpara, self.upp_mfpara)
            self.nmf = _customMemFunc(self.NMFunc, self.low_nmfpara, self.upp_nmfpara)

    def __repr__(self):
        return 'Membership function:\n' + str(self.mf) + '\n' + 'Non-Membership function:\n' + str(self.nmf)

    def MFgeneratorSetting(self, MFunc, low_MF_para, upp_MF_para):
        if not self.customFunc:
            assert MFunc == 'sigmf' or MFunc == 'trimf' or MFunc == 'zmf' or \
                   MFunc == 'smf' or MFunc == 'gaussmf' or MFunc == 'gauss2mf' or MFunc == 'gbellmf' or MFunc == 'trapmf', \
                'ERROR! Wrong membership function!'
            self.MFunc = MFunc
            self.low_mfpara = low_MF_para
            self.upp_mfpara = upp_MF_para
        else:
            self.MFunc = MFunc
            self.low_mfpara = low_MF_para
            self.upp_mfpara = upp_MF_para
            assert hasattr(self.MFunc, '__call__'), 'ERROR:The MFunc is not a function!'

    def NMFgeneratorSetting(self, NMFunc, low_NMF_para, upp_NMF_para):
        if not self.customFunc:
            assert NMFunc == 'sigmf' or NMFunc == 'trimf' or NMFunc == 'zmf' or \
                   NMFunc == 'smf' or NMFunc == 'gaussmf' or NMFunc == 'gauss2mf' or NMFunc == 'gbellmf' or NMFunc == 'trapmf', \
                'ERROR! Wrong membership function!'
            self.NMFunc = NMFunc
            self.low_nmfpara = low_NMF_para
            self.upp_nmfpara = upp_NMF_para
        else:
            self.NMFunc = NMFunc
            self.low_nmfpara = low_NMF_para
            self.upp_nmfpara = upp_NMF_para
            assert hasattr(self.NMFunc, '__call__'), 'ERROR:The NMFunc is not a function!'

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
            assert self.MFunc != '' and self.NMFunc != '' and self.low_mfpara != [] and self.upp_mfpara != [] \
                   and self.low_nmfpara != [] and self.upp_nmfpara != [], \
                'Membership function or parameter or number of function has not been set! Please set the membership and non-membership function first.'
            self.mf = _memshipFunc(self.MFunc, self.low_mfpara, self.upp_mfpara)
            self.nmf = _memshipFunc(self.NMFunc, self.low_nmfpara, self.upp_nmfpara)
        else:
            assert hasattr(self.MFunc, '__call__') and hasattr(self.NMFunc,
                                                               '__call__'), 'ERROR:The MFunc and NMFunc are not function type!'
            self.mf = _customMemFunc(self.MFunc, self.low_mfpara, self.upp_mfpara)
            self.nmf = _customMemFunc(self.NMFunc, self.low_nmfpara, self.upp_nmfpara)

        self.mf.setvariable(self._variable_start, self._variable_end, self._linspace)
        self.nmf.setvariable(self._variable_start, self._variable_end, self._linspace)

        print(self.__repr__())

    def MF_NMF_Plot(self):
        x = np.linspace(self._variable_start, self._variable_end, self._linspace)
        mf = self.mf
        nmf = self.nmf

        mf.MF_Plot('Membership func')
        nmf.MF_Plot('Non-Membership func')

    def generator(self, x, y):
        assert self._variable_start <= x <= self._variable_end, 'The independent variable x is not in the range of %d and %d' % (
            self._variable_start, self._variable_end)
        assert self._variable_start <= y <= self._variable_end, 'The independent variable y is not in the range of %d and %d' % (
            self._variable_start, self._variable_end)

        newIVFN = QrungIVFN(self.qrung,0,0,0,0)
        MD = self.mf.calculate_MD(x)
        NMD = self.nmf.calculate_MD(y)

        assert np.max(MD)**self.qrung+np.max(NMD)**self.qrung<=1,'The MD^'+str(self.qrung)+'+NMD^'+str(self.qrung)+'<=1 and >=0. Please reset the parameters'
        assert np.min(MD)**self.qrung+np.min(NMD)**self.qrung>=0,'The MD^'+str(self.qrung)+'+NMD^'+str(self.qrung)+'<=1 and >=0. Please reset the parameters'

        newIVFN.mdl = MD[0]
        newIVFN.mdu = MD[1]
        newIVFN.nmdl = NMD[0]
        newIVFN.nmdu = NMD[1]

        return newIVFN


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
            upp_para: 表示隶属函数上限的参数数组
            low_para: 表示隶属函数下限的参数数组
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
    upp_para = []
    low_para = []

    _variable_start = 0
    _variable_end = 1
    _linspace = 100

    def __init__(self, memFunc, low_para, upp_para):
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
        assert len(upp_para) == len(low_para), 'ERROR: Arguments to the same function must be equal.'
        if memFunc == 'sigmf' or memFunc == 'zmf' or memFunc == 'smf' or memFunc == 'gaussmf':
            assert type(upp_para) == tuple and type(
                low_para) == tuple, 'ERROR:The %s function\'s parameter type is error!Parameter type should be tuple!' % memFunc
            assert len(upp_para) == 2 and len(
                low_para) == 2, 'ERROR:The number of the %s function is error!The number of parameters should be 2' % memFunc
        elif memFunc == 'gauss2mf':
            assert type(upp_para) == tuple and type(
                low_para) == tuple, 'ERROR:The %s function\'s parameter type is error!Parameter type should be tuple!' % memFunc
            assert len(upp_para) == 4 and len(
                low_para) == 4, 'ERROR:The number of the %s function is error!The number of parameters should be 4' % memFunc
        elif memFunc == 'gbellmf':
            assert type(upp_para) == tuple and type(
                low_para) == tuple, 'ERROR:The %s function\'s parameter type is error!Parameter type should be tuple!' % memFunc
            assert len(upp_para) == 3 and len(
                low_para) == 3, 'ERROR:The number of the %s function is error!The number of parameters should be 3' % memFunc
        elif memFunc == 'trimf':
            assert type(upp_para) == list and type(
                low_para) == list, 'ERROR:The %s function\'s parameter type is error!Parameter type should be list!' % memFunc
            assert len(upp_para) == 3 and len(
                low_para) == 3, 'ERROR:The number of the %s function is error!The number of parameters should be 3' % memFunc
        elif memFunc == 'trapmf':
            assert type(upp_para) == list and type(
                low_para) == list, 'ERROR:The %s function\'s parameter type is error!Parameter type should be list!' % memFunc
            assert len(upp_para) == 4 and len(
                low_para) == 4, 'ERROR:The number of the %s function is error!The number of parameters should be 4' % memFunc
        else:
            assert memFunc == '', 'ERROR!Wrong function name!'

        self.memFunc = memFunc
        self.upp_para = upp_para
        self.low_para = low_para

    def __repr__(self):
        """
            打印隶属函数信息
        """
        return 'Function: %s\nLower limit membership parameter: ' % self.memFunc + str(
            self.low_para) + '\nUpper limit membership parameter: ' + str(self.upp_para)

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
            生成函数隶属度,首先生成隶属度下限，再生成隶属度上限
        """

        y_low = 0
        if self.memFunc == 'sigmf':
            y_low = sigmf(x, self.low_para[0], self.low_para[1]) - self._min_generateMF()[0]
        if self.memFunc == 'zmf':
            y_low = zmf(x, self.low_para[0], self.low_para[1]) - self._min_generateMF()[0]
        if self.memFunc == 'smf':
            y_low = smf(x, self.low_para[0], self.low_para[1]) - self._min_generateMF()[0]
        if self.memFunc == 'gaussmf':
            y_low = gaussmf(x, self.low_para[0], self.low_para[1]) - self._min_generateMF()[0]
        if self.memFunc == 'gauss2mf':
            y_low = gauss2mf(x, self.low_para[0], self.low_para[1], self.low_para[2], self.low_para[3]) - \
                    self._min_generateMF()[0]
        if self.memFunc == 'gbellmf':
            y_low = gbellmf(x, self.low_para[0], self.low_para[1], self.low_para[2]) - self._min_generateMF()[0]
        if self.memFunc == 'trimf':
            y_low = trimf(x, self.low_para) - self._min_generateMF()[0]
        if self.memFunc == 'trapmf':
            y_low = trapmf(x, self.low_para) - self._min_generateMF()[0]

        y_upp = 0
        if self.memFunc == 'sigmf':
            y_upp = sigmf(x, self.upp_para[0], self.upp_para[1]) - self._min_generateMF()[1]
        if self.memFunc == 'zmf':
            y_upp = zmf(x, self.upp_para[0], self.upp_para[1]) - self._min_generateMF()[1]
        if self.memFunc == 'smf':
            y_upp = smf(x, self.upp_para[0], self.upp_para[1]) - self._min_generateMF()[1]
        if self.memFunc == 'gaussmf':
            y_upp = gaussmf(x, self.upp_para[0], self.upp_para[1]) - self._min_generateMF()[1]
        if self.memFunc == 'gauss2mf':
            y_upp = gauss2mf(x, self.upp_para[0], self.upp_para[1], self.upp_para[2], self.upp_para[3]) - \
                    self._min_generateMF()[1]
        if self.memFunc == 'gbellmf':
            y_upp = gbellmf(x, self.upp_para[0], self.upp_para[1], self.upp_para[2]) - self._min_generateMF()[1]
        if self.memFunc == 'trimf':
            y_upp = trimf(x, self.upp_para) - self._min_generateMF()
        if self.memFunc == 'trapmf':
            y_upp = trapmf(x, self.upp_para) - self._min_generateMF()

        # assert y_upp.all>y_low.all, 'ERROR: The upper membership limit must be greater than the lower membership limit. Select a new set of parameters.'
        return [y_low, y_upp]

    def _min_generateMF(self):
        """
            计算隶属函数在当前自变量范围下的最小值
            该函数的作用是将隶属函数沿 与轴向下平移最小值个单位，保证隶属度函数的值 <= 1
            可以理解为函数的系数
            先计算下限最小值，再计算上限最小值，最后返回 list
        """
        x = np.linspace(self._variable_start, self._variable_end, self._linspace)

        min_mf_low = 0
        if self.memFunc == 'sigmf':
            min_mf_low = min(sigmf(x, self.low_para[0], self.low_para[1]))
        if self.memFunc == 'zmf':
            min_mf_low = min(zmf(x, self.low_para[0], self.low_para[1]))
        if self.memFunc == 'smf':
            min_mf_low = min(smf(x, self.low_para[0], self.low_para[1]))
        if self.memFunc == 'gaussmf':
            min_mf_low = min(gaussmf(x, self.low_para[0], self.low_para[1]))
        if self.memFunc == 'gauss2mf':
            min_mf_low = min(gauss2mf(x, self.low_para[0], self.low_para[1], self.low_para[2], self.low_para[3]))
        if self.memFunc == 'gbellmf':
            min_mf_low = min(gbellmf(x, self.low_para[0], self.low_para[1], self.low_para[2]))
        if self.memFunc == 'trimf':
            min_mf_low = min(trimf(x, self.low_para))
        if self.memFunc == 'trapmf':
            min_mf_low = min(trapmf(x, self.low_para))

        min_mf_upp = 0
        if self.memFunc == 'sigmf':
            min_mf_upp = min(sigmf(x, self.upp_para[0], self.upp_para[1]))
        if self.memFunc == 'zmf':
            min_mf_upp = min(zmf(x, self.upp_para[0], self.upp_para[1]))
        if self.memFunc == 'smf':
            min_mf_upp = min(smf(x, self.upp_para[0], self.upp_para[1]))
        if self.memFunc == 'gaussmf':
            min_mf_upp = min(gaussmf(x, self.upp_para[0], self.upp_para[1]))
        if self.memFunc == 'gauss2mf':
            min_mf_upp = min(gauss2mf(x, self.upp_para[0], self.upp_para[1], self.upp_para[2], self.upp_para[3]))
        if self.memFunc == 'gbellmf':
            min_mf_upp = min(gbellmf(x, self.upp_para[0], self.upp_para[1], self.upp_para[2]))
        if self.memFunc == 'trimf':
            min_mf_upp = min(trimf(x, self.upp_para))
        if self.memFunc == 'trapmf':
            min_mf_upp = min(trapmf(x, self.upp_para))

        return [min_mf_low, min_mf_upp]

    def _max_generateMF(self):
        """
            计算上下限隶属函数在自变量范围内的最大值
        """
        x = np.linspace(self._variable_start, self._variable_end, self._linspace)
        max_mf_low = max(self._generateMF(x)[0])
        max_mf_upp = max(self._generateMF(x)[1])
        return [max_mf_low, max_mf_upp]

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
        # for j in range(1):
        plt.plot(x, y[0], label=st + ':Lower limit of membership')
        plt.plot(x, y[1], label=st + ':Upper limit of membership')
        plt.grid(linestyle='-.')
        plt.legend()
        plt.show()

    def calculate_MD(self, x):
        """
            通过上限隶属度函数和下限隶属度函数计算隶属度
        """
        y = self._generateMF(x)
        if y[0] > y[1]:
            y[0], y[1] = y[1], y[0]
        return np.array(y)


class _customMemFunc(object):
    ArbFunc = None
    upp_para = []
    low_para = []

    _variable_start = 0
    _variable_end = 1
    _linspace = 100

    def __init__(self, ArbFunc, low_para, upp_para):
        assert hasattr(ArbFunc, '__call__') or ArbFunc is None, 'ERROR: The membership function has to be a function!'
        assert len(upp_para) == len(low_para), 'ERROR: Arguments to the same function must be equal.'
        self.ArbFunc = ArbFunc
        self.low_para = np.asarray(low_para)
        self.upp_para = np.asarray(upp_para)

    def __repr__(self):
        """
            打印隶属函数信息
        """
        return 'Function: %s\nLower limit membership parameter: ' % self.ArbFunc.__name__ + str(
            self.low_para) + '\nUpper limit membership parameter: ' + str(self.upp_para)

    def setvariable(self, start, end, linspace):
        """
            设置自变量变化范围，返回一个 start-end ，间隔为 linspace 的 array
            该函数用来生成隶属函数实例的空间范围
        """
        self._variable_start = start
        self._variable_end = end
        self._linspace = linspace

    def _generateMF(self, x):
        y_low = self.ArbFunc(x, *self.low_para) - self._min_generateMF()[0]
        y_upp = self.ArbFunc(x, *self.upp_para) - self._min_generateMF()[1]
        return [y_low, y_upp]

    def _min_generateMF(self):
        """
            计算隶属函数在当前参数和当前自变量范围下的最小值
            该函数的作用是将隶属函数沿 y 轴方向向下平移最小值个单位，保证隶属函数的值 <= 1
            可以理解为该函数的系数
        """
        min_mf_low, min_mf_upp = [], []
        x = np.linspace(self._variable_start, self._variable_end, self._linspace)
        min_mf_low = min(self.ArbFunc(x, *self.low_para))
        min_mf_upp = min(self.ArbFunc(x, *self.upp_para))
        return [min_mf_low, min_mf_upp]

    def _max_generateMF(self):
        """
            计算上下限隶属函数在自变量范围内的最大值
        """
        x = np.linspace(self._variable_start, self._variable_end, self._linspace)
        max_mf_low = max(self._generateMF(x)[0])
        max_mf_upp = max(self._generateMF(x)[1])
        return [max_mf_low, max_mf_upp]

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
        # for j in range(1):
        plt.plot(x, y[0], label=st + ':Lower limit of membership')
        plt.plot(x, y[1], label=st + ':Upper limit of membership')
        plt.grid(linestyle='-.')
        plt.legend()
        plt.show()

    def calculate_MD(self, x):
        """
            通过上限隶属度函数和下限隶属度函数计算隶属度
        """
        y = self._generateMF(x)
        if y[0] > y[1]:
            y[0], y[1] = y[1], y[0]
        return np.array(y)
