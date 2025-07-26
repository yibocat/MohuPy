<img src="https://github.com/yibocat/MohuPy/blob/master/assets/MohuPy-2.png?raw=true" alt="MohuPy-2" style="zoom: 67%;" />

# MohuPy

简体中文 | [English](https://github.com/yibocat/MohuPy/blob/master/README.md)

MohuPy 是一个模糊数学计算工具包，包括代数范数下的 q 阶序对模糊数（*q-rofn*）、区间值 q 阶序对模糊数（*iv-q-rofn*）和 q 阶序对犹豫模糊数（*q-rohfn*）的运算，并提供模糊向量的高阶运算和自动微分以及模糊数的计算图模型，可用于处理不规则模糊计算、模糊决策相关问题、一般高阶模糊计算问题以及复杂模糊函数的微分导数计算问题。

## 特点

- *q-rofn*、*iv-q-rofn*、*q-rohfn* 集与矩阵和向量的加、减、乘、除；
- 高维模糊数运算、矩阵运算和向量运算；
- *q-rofn*的模糊张量运算与自动微分，*q-rofn*的模糊计算图模型；
- 非加性测度的表示，莫比乌斯变换，非加性测度的计算；
- 非加性测度集函数的导数、Shannon熵、Sugeno积分、Choquet积分和Shilkret积分；
- 八种常用的隶属函数。
- 高阶模糊集与模糊向量的基本用法，包括任意随机形状、保存、加载、最大最小和等。

## 安装


```shell
pip install mohupy
```

## 要求

1. python >= 3.10
2. numpy >= 1.24
3. scipy >= 1.10.0
4. matplotlib >= 3.8.0
5. pandas >= 1.5.0
6. networkx >= 3.1.0

## 开始使用

### 1. 创建模糊数

导入包很简单，只需

```python
import mohupy as mp
```

然后，创建一个 *3-rofn* <0.7,0.4>，如下所示：

`````python
x = mp.fuzznum(3, 0.7, 0.4)
print(x)
`````

然后会显示如下内容：

`````python
<0.7,0.4>
`````

如果需要检查 <0.7,0.4> 的得分、隶属度和非隶属度，可以编写如下代码查看：

`````python
print(x.score)
print(x.md, x.nmd)
`````

`````python
0.2789999999999999
0.7 0.4
`````

注：初始模糊数类型为 *q-rofn*，模糊数类型可通过全局变量函数 `mp.config.set_mtype()` 调整，而模糊数类型可以用 `.mtype` 表示，其中 `.mtype='qrofn'` 表示 *q-rofn*，`.mtype='ivfn'` 表示 *iv-q-rofn*，`.mtype='qrohfn'` 表示 *q-rohfn*。

`````python
mp.config.set_mtype('ivfn')
print(mp.config.Config.mtype)
`````

`````python
'ivfn'
`````

### 3. 模糊集（向量）

可以使用 `mp.fuzzset()` 创建一个空的模糊集（向量），从而创建模糊向量。

`````python
y = mp.fuzzset()
print(y)
`````

`````python
Fuzzarray([], qrung=None, mtype=qrofn)
`````

需要注意的是，这是一个空的初始化模糊集（向量），即表示模糊数的 `qrung = None` 是一个空值，可以在后续操作中赋值。例如，可以创建一个随机 *iv-1-rofn* 模糊矩阵：

```````python
mp.config.set_mtype('ivfn')
fuzzy_matrix = mp.rand_fuzz(5,2)
fuzzy_matrix
```````

```python
Fuzzarray([[<[0.1211 0.3985],[0.0445 0.5733]> <[0.1978 0.6394],[0.1696 0.3151]>]
           [<[0.3597 0.5338],[0.3082 0.3306]> <[0.3761 0.5476],[0.0515 0.372 ]>]
           [<[0.437  0.5267],[0.3074 0.3981]> <[0.2731 0.4707],[0.2992 0.4142]>]
           [<[0.0881 0.3158],[0.1707 0.5903]> <[0.1358 0.6692],[0.1511 0.2643]>]
           [<[0.0571 0.1164],[0.363  0.4567]> <[0.0259 0.0657],[0.2901 0.6906]>]], qrung=1, mtype=ivfn)
```

而且，直接在 `fuzzy_matrix` 上进行计算非常简单。例如，其平方可以如下计算

```python
fuzzy_matrix ** 2
```

```python
Fuzzarray([[<[0.0147 0.1588],[0.087  0.8179]> <[0.0391 0.4088],[0.3105 0.5309]>]
           [<[0.1294 0.285 ],[0.5214 0.5519]> <[0.1414 0.2998],[0.1003 0.6056]>]
           [<[0.191  0.2774],[0.5203 0.6377]> <[0.0746 0.2216],[0.5088 0.6568]>]
           [<[0.0078 0.0997],[0.3123 0.8321]> <[0.0184 0.4479],[0.2794 0.4588]>]
           [<[0.0033 0.0136],[0.5942 0.7049]> <[0.0007 0.0043],[0.4961 0.9043]>]], qrung=1, mtype=ivfn)
```

### 4. 模糊张量与自动微分

需要注意的是，目前的模糊张量仅支持 *q-rofn* 这一种模糊数类型，现有文献中对 *iv-q-rofn* 和 *q-rohfn* 的描述不足。模糊张量可以通过函数 `tensor = mp.Fuzztensor()` 创建。比如，随机生成一个二维模糊张量，并针对特定函数 f(x) = 0.2 x 求关于 x 的导数。

`````python
x = mp.rand_tensor(5,2)
fx = 0.2 * x
fx.backward()
print(x)
print(fx)
print(x.grad)
`````

```python
Fuzztensor([[<0.0293,0.3409> <0.1657,0.4683>]
            [<0.142,0.3044> <0.6446,0.2342>]
            [<0.7509,0.0453> <0.0425,0.0003>]
            [<0.8818,0.1123> <0.2809,0.6213>]
            [<0.3699,0.4671> <0.1744,0.081>]], qrung=1, mtype=qrofn)

Fuzztensor([[<0.0059,0.8063> <0.0356,0.8592>]
            [<0.0302,0.7883> <0.1869,0.748>]
            [<0.2427,0.5385> <0.0086,0.1925>]
            [<0.3476,0.6458> <0.0638,0.9092>]
            [<0.0882,0.8588> <0.0376,0.6049>]], qrung=1, mtype=qrofn)

Fuzztensor([[<0.2,0.8> <0.2,0.8>]
            [<0.2,0.8> <0.2,0.8>]
            [<0.2,0.8> <0.2,0.8>]
            [<0.2,0.8> <0.2,0.8>]
            [<0.2,0.8> <0.2,0.8>]], qrung=1, mtype=qrofn)
```

### 5. 模糊测度

MohuPy 还包含非加性测度计算包，主要的模糊测度包括 Dirac 测度、Additive 测度、Symmetric 测度、lambda 模糊测度等，此外还包括 Shapley 指数、Banzhaf 指数和模糊测度 Shannon 熵。在非加性测度积分方面，包括 Choquet 积分、Sugeno 积分和 Shilkret 积分。以数组 [0.4, 0.25, 0.37, 0.2] 为例，该数组在 lambda 模糊测度下的字典表示如下

```py
measure = [0.4,0.25,0.37,0.2]
mp.dict_rep(measure, mp.lambda_meas, measure)
```

```python
{'{}': -0.0,
 'C1': 0.4,
 'C2': 0.25,
 'C1,C2': 0.60597,
 'C3': 0.37,
 'C1,C3': 0.704836,
 'C2,C3': 0.579272,
 'C1,C2,C3': 0.877251,
 'C4': 0.2,
 'C1,C4': 0.564776,
 'C2,C4': 0.427985,
 'C1,C2,C4': 0.752608,
 'C3,C4': 0.537418,
 'C1,C3,C4': 0.842768,
 'C2,C3,C4': 0.728261,
 'C1,C2,C3,C4': 1.0}
```

特别地，哈斯图还可以用来查看数组在lambda模糊测度下的测度值。

```python
mp.hasse_diagram(measure, mp.lambda_meas)
```

<img src="https://github.com/yibocat/MohuPy/blob/master/assets/hasse%20diagram.png?raw=true" alt="hasse diagram" style="zoom:67%;" />

如果计算这个数组的Choquet积分，可以通过下面的代码计算

```python
mp.integral.choquet(measure, mp.lambda_meas)
```

```python
0.34044280478185107
```

### 6. 模糊图

模糊数的点图可以很方便的看到模糊数在模糊区域中的位置，另外还可以看到模糊数的加法区域、减法区域、乘法区域和除法区域。MohuPy 内置了绘图方法，而且非常容易写。例如，画一个 *3-rofn* <0.7,0.4> 并画出它的各个操作区域，可以这样写：

```python
x = mp.fuzznum(3, 0.7,0.4)
mp.fuzz_plot(x)
```

<img src="https://github.com/yibocat/MohuPy/blob/master/assets/fuzzyplot.png?raw=true" alt="fuzzyplot" style="zoom:67%;" />

分别查看模糊数的每个域并编写代码，

```python
mp.fuzz_plot(x, add=True)
mp.fuzz_plot(x, sub=True)
mp.fuzz_plot(x, mul=True)
mp.fuzz_plot(x, div=True)
```

| <img src="https://github.com/yibocat/MohuPy/blob/master/assets/add.png?raw=true" alt="add" style="zoom:67%;" /> | <img src="https://github.com/yibocat/MohuPy/blob/master/assets/sub.png?raw=true" alt="sub" style="zoom:67%;" /> |
| :--------------------------------------------------------: | ---------------------------------------------------------- |
| <img src="https://github.com/yibocat/MohuPy/blob/master/assets/mul.png?raw=true" alt="mul" style="zoom:67%;" /> | <img src="https://github.com/yibocat/MohuPy/blob/master/assets/div.png?raw=true" alt="div" style="zoom:67%;" /> |

甚至可以画出一个模糊集所有模糊数的分布，以15个随机 *iv-2-qrofns* 为例，

```python
mp.config.set_mtype('ivfn')
x = mp.rand_fuzz(15,qrung=2)
mp.fuzz_plot(x, alpha=0.1)
```

<img src="https://github.com/yibocat/MohuPy/blob/master/assets/15ivfn.png?raw=true" alt="15ivfn" style="zoom:67%;" />

## 待办事项

 - [x] 采用模糊注册表框架
 - [x] q-Rung 序对对犹豫模糊集
 - [x] 添加更多阿基米德范数运算和注册（Einstein、Frank、Hamacher）
 - [x] 模糊函数的梯度和自动微分
 - [x] 将模糊数和模糊集的运算集成到计算图模型中
 - [ ] 隶属度函数与非隶属度函数的模糊隶属度生成器

## 更新日志

更新日志： [Log](https://github.com/yibocat/MohuPy/blob/master/update.md)

## 联系方式

email: yibocat@yeah.net

## 许可证

[MIT](https://github.com/yibocat/MohuPy/blob/master/LICENSE)