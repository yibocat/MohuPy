# UPDATE LOG

------
### 0.2.5-3-24.2024
1. 修复了字符转换bug，添加错误转换展示
2. 修复to_csv方法存在的bug

------
### 0.2.4-1-18.2024.2
1. 修复了读取数据的bug，添加了 header 和 index_col 参数在 load_csv() 方法中

------
### 0.2.4-1-17.2024
1. 修复了部分 bug
2. 修复了读取 csv 文件的 bug
3. 更新了一些方法不提示的错误

------
### version: 0.2.3-12-19.2023
1. 更新了适配的 Python 版本，适配的 Python 版本 'python >= 3.8'

------
### version: 0.2.2-12-17.2023
1. 更新了 `random` 模块中 `random.rand` 方法，对于 qrohfn 做了调整，加入了参数 minnum 和 maxnum，表示隶属度数量的最小限和最大限

------
### version: 0.2.2-12-01.2023
1. 更改了模糊数的比较规则，使用 score 得分值来进行比较
2. 修复了 Choquet integral 的计算问题
3. 修复了 `random.choice()` 存在的 bug(replace 参数问题)
4. 修复了 `str2fuzz()` 函数转换 `'qrohfn'` 类型时可能存在无法转换的 bug

------
### version: 0.2.1-11-30.2023
1. 修复了 `Fuzzarray.md` 和 `Fuzzarray.nmd` 存在的 bugs.
2. 修复了 `mtype='qrohfn'` 时的 `comp` 属性 bug.
3. 修复了 `mtype='qrohfn'` 的加法运算和乘法运算 bug.
4. 修复了 `fuzzset` 的一些 bugs：
   * `fuzzset(None)` 无法生成的情况已修复
   * `fuzzset` 高维数组被展开的情况已修复
5. 修复了 `fuzznum` 无法生成 `fuzznum(None)` 的情况
6. 更新了 requirements.txt 文件

------
# version: 0.2.0
**更新日期: 11.29.2023**

**主要更新内容**:
1. 重构核心代码，模糊集合类更新为 `Fuzzarray`，模糊数集合整合到一个模糊集类 `Fuzznum`；
2. 添加注册表，所有方法通过 `core.Registry()` 创建新字典，并保存到 `regedit` 文件下；
3. 重构 Archimedean 计算范数框架，整合到 `src` 文件下，并构建 Archimedean 注册表字典，可直接通过 mohupy.archimedeanDict 查看；
4. 构建 Library，注册好的方法通过 Library 调用；
5. 创建配置 config 文件夹(后续更新)，目前 config 仅包含 T 范数的转换配置，但尚未支持 Einstein 运算；
6. 废弃了原 `mohuset` 内容，部分方法名称发生变化
   * `str2num` -> `str2fuzz`
   * `asfuzzset` -> `asfuzzarray`
   * `is_valid` -> `isValid`
   * `is_empty` -> `isEmpty`
   * `max` -> `getmax`
   * `min` -> `getmin`
   * `sum` -> `getsum`
   * `prod` -> `getprod`

**Noting**: 0.2.0 版本修复了大部分以前遗留的 bugs，此外，0.2.0 版本以下的各版本不兼容

------
## version: 0.1.9-11.28.2023
1. 重构代码框架，重写了内核并命名为 base
2. 将模糊集类重命名为 `Fuzzarray`，并继承自 `mohuset`
3. 将模糊数类重命名为 `Fuzznum`，并继承自 `mohunum`
4. 将模糊数的构造公式重构代码: `fuzznum`和 `fuzzset`
5. 修复了众多 bugs，完善了基础框架
此外，为 0.2.0 的更新做好准备，目前 0.1.9 保留旧版本代码 mohuset 相关代码
该版本仅重构了底层`Fuzznum` 和 `Fuzzarray` 框架和计算逻辑，其余功能并未实现，
例如随机函数，构造函数等等

------
### version: 0.1.8-11.25.2023.3
1. 修复了 Choquet integral 的计算错误问题

------
### version: 0.1.8-11.25.2023
1. 修复了 Choquet integral 无法正常计算的 bug

------
### version: 0.1.8-11.24.2023
修复了一些 bugs

------
### version: 0.1.8-10.31.2023.2
1. 修复了减法运算和除法运算存在的缺陷，原论文中的方法有误
   > Reference: W. S. Du, “Research on arithmetic operations over generalized 
   > orthopair fuzzy sets,” Int. J. Intell. Syst., vol. 34, no. 5, pp. 709–732,
   > 2019, doi: 10.1002/int.22073.
------
### version: 0.1.8-10.31.2023
1. 修复了 `qrofn` 的比较运算 `>=` 和 `<=`存在的 bug.
2. 添加了近似值设置 `mp.Approx.round`，用来给定模糊数的近似，默认为 6（小数点后 6 位）。
使用 `mp.Approx.round = 6` 来对全局近似值进行更改
3. 修复了减法运算和除法运算存在的缺陷
   > Reference: W. S. Du, “Research on arithmetic operations over generalized 
   > orthopair fuzzy sets,” Int. J. Intell. Syst., vol. 34, no. 5, pp. 709–732,
   > 2019, doi: 10.1002/int.22073.
4. 对所有运算添加了近似，模糊数其实并不需要非常精确，保证一定的精度即可
------
### version: 0.1.8-10.30.2023
1. 添加了广播方法 `broadcast_to` 和 `squeeze`
2. 添加了 `random.seed()` 方法

------
## version: 0.1.8-10.26.2023
1. 重构了 `mohunum` 和 `mohuset` 的运算法则，结构更加清晰明了，便于后续维护。
2. 修复了模糊向量的运算及模糊集合，模糊数广播。
3. 修复了一些计算 bugs。

------
### version: 0.1.7-10.25.2023
1. 增加了 `isscalar` 方法
2. 修复了 `fuzzset` 存在的 bug
3. 重新设置了打印格式

------
### version: 0.1.7-10.24.2023
1. 对 `mohunum` 添加了 `flatten()` 方法
2. 修复了 `fuzzset` 方法存在的 bug

------
## version: 0.1.7-10.24.2023
1. 添加了常量设置 `constant`
2. 修复了一些 bug
3. 更新了 0.1.6-10.22.2023 遗留的一些问题

------
### version: 0.1.6-10.22.2023
1. 添加 `zeros_like`,`poss_like`,`negs_like` 和 `full_like` 方法
2. 修复了 `random.choice` 方法存在的一些 bugs。
3. 更换模糊数方法名称：`mohunum`->`fuzznum`
4. 增加模糊集合方法 `fuzzset`，用于创建一个模糊集
5. 更换模糊数基类名称：`fuzzNum` -> `mohunum`
   > 注意：模糊集合基类为 `mohuset`，模糊集合创建方法为 `fuzzset()`， 模糊数基类为 `mohunum`， 模糊数创建方法为 `fuzznum()` 
6. 取消了动态继承

------
## version: 0.1.6-10.18.2023
1. 完善了 `qrohfn` 的所有功能
2. 修复了一些 bugs

------
### version: 0.1.5-10.17.2023
1. 完善了 `qrohfn` 的功能，并注册
   1. 构造函数(zeros, poss, negs)
   2. 距离公式
   3. 随机公式
   4. 字符转换
2. 优化了代码结构
3. 修复了一些 bugs

------
### version: 0.1.5-10.16.2023
1. 优化了结构，设置了注册表
   1. 模糊类型注册表
   2. 模糊距离注册表
   3. 模糊画图注册表
   4. 转换字符注册表
   5. 随机注册表
2. 添加了 **Q 阶序对犹豫模糊数** 类型（识别字符：`qrohfn`）
3. 修复了一些 bugs（ plot 方法）

------
## version: 0.1.5-10.15.2023
1. 新增了模糊类型注册表，通过运行 `mp.download_template` 方法下载模糊数模板
2. 优化了模糊数结构， `qrofn` 和 `ivfn` 父类调整为 `mohunum`，并且基于工厂函数动态继承
3. 优化了 `mohuset` 类，运算方法代码，修复了一些 bugs

### 计划：
- [ ] 添加阿基米德范数注册表
- [ ] 添加随机函数注册表
- [ ] 添加 q-rung orthopair hesitant fuzzy number 类型

------
## version: 0.1.4-10.6.2023
1. 修复了`mohuset` 和`fuzznum` 绝对值计算 bugs
2. 修复了 `fuzznum` 的比较运算(`fuzznum` 与 `mohuset` 的比较)

------
## version: 0.1.3-10.2.2023
1. 增加了 `mohusets` 的比较运算
2. 增加了 `fuzznum` reshape 方法和 T 属性
3. 修复了 `MohuBase` 的 `max`,`min`,`mean`和`sum` 方法，添加了 `axis` 参数
4. 修复了 `mohuset` 的一些 bugs。

------
## version: 0.1.2-10.1.2023
1. 重构代码框架，将 `mohuset` 和 `fuzznum` 放入 `core`；
2. 完善了 `mohuset` 与 `fuzznum` 的运算规则，支持复杂运算，包括 数数运算，数集运算等；
3. 完善了 `mohuset` 的最大最小值平均值功能，添加了 `axis` 参数；
4. 修改了 q-rofn 的字符表示，由 `fn` 换成 `qrofn`。
5. 添加了注册表，将两种模糊集合 `MohuQROFN` 和 `MohuQROIVFN` 进行注册
6. 更新 README


