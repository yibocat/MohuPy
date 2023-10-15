# UPDATE LOG

------
## version: 0.1.5-10.15.2023
1. 新增了模糊类型注册表，通过运行 `mp.download_template` 方法下载模糊数模板
2. 优化了模糊数结构， `qrofn` 和 `ivfn` 父类调整为 `fuzzNum`，并且基于工厂函数动态继承
3. 优化了 `mohuset` 类，运算方法代码，修复了一些 bugs

### 计划：
- [ ] 添加阿基米德范数注册表
- [ ] 添加随机函数注册表
- [ ] 添加 q-rung orthopair hesitant fuzzy number 类型

------
## version: 0.1.4-10.6.2023
1. 修复了`mohuset` 和`mohunum` 绝对值计算 bugs
2. 修复了 `mohunum` 的比较运算(`mohunum` 与 `mohuset` 的比较)

------
## version: 0.1.3-10.2.2023
1. 增加了 `mohusets` 的比较运算
2. 增加了 `mohunum` reshape 方法和 T 属性
3. 修复了 `MohuBase` 的 `max`,`min`,`mean`和`sum` 方法，添加了 `axis` 参数
4. 修复了 `mohuset` 的一些 bugs。

------
## version: 0.1.2-10.1.2023
1. 重构代码框架，将 `mohuset` 和 `mohunum` 放入 `core`；
2. 完善了 `mohuset` 与 `mohunum` 的运算规则，支持复杂运算，包括 数数运算，数集运算等；
3. 完善了 `mohuset` 的最大最小值平均值功能，添加了 `axis` 参数；
4. 修改了 q-rofn 的字符表示，由 `fn` 换成 `qrofn`。
5. 添加了注册表，将两种模糊集合 `MohuQROFN` 和 `MohuQROIVFN` 进行注册
6. 更新 README


