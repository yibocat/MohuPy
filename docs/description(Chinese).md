## MohuPy

1. Q 阶序对模糊数，Q 阶序对区间值模糊数
   1. 定义
   2. 加法，减法，乘法，除法，幂次和比较运算（运算符重载）
   3. 交并运算
   4. 合法性判断，判空，转换，Q 阶序对模糊数的平面图
   5. 随机函数，模糊数字符转换
   6. 广义 Q 阶序对模糊距离
   7. 爱因斯坦加，爱因斯坦乘，爱因斯坦倍，爱因斯坦幂 
2. Q 阶序对模糊集合，Q 阶序对区间值模糊集合
   1. 基于 Numpy（CuPy）框架的 Q 阶序对模糊集合和 Q 阶序对区间值模糊集合
   2. 隶属度矩阵，非隶属度矩阵，得分矩阵，转置矩阵
   3. Q 阶序对模糊高阶加法，减法，乘法，除法和幂次运算
   4. 高阶随机，添加元素，删除元素，移除元素，清空，求和
   5. 最大值，最小值，f 函数最大值，f 函数最小值
   6. 保存 .npz 文件，加载 ,npz 文件，保存 .csv 文件， 加载 .csv 文件
   7. Q阶序对模糊集合和 Q阶序对区间值模糊集合的模糊数分布图
   8. 自定义函数模糊集合运算，随机提取模糊数
   9. Q 阶序对模糊向量点积，内积，外积，自定义函数运算，笛卡尔和，笛卡尔积
   10. Q 阶序对模糊高阶点积，内积，自定义函数运算，笛卡尔和，笛卡尔积
   11. 构造高阶 Q 阶序对全零模糊集合，正理想高阶模糊集合，负理想高阶模糊集合，任意模糊数高阶模糊集合
3. 函数
   1. 8 个常用函数：sigmf 函数, 三角形函数，Z 形函数，梯形函数，S 形函数，高斯函数，双高斯函数，广义贝尔函数
   2. 隶属函数与非隶属函数生成器
4. 模糊测度
   1. 狄拉克测度（布尔模糊测度）
   2. 加性模糊测度
   3. 堆成模糊测度
   4. lambda 模糊测度
   5. 莫比乌斯表示
   6. Zeta 表示
   7. 向量表示
   8. 字典表示
   9. 模糊测度哈斯图
5. 模糊测度指标
   1. 集函数的导数
   2. Shapley 值
   3. Banzhaf 值
   4. 香浓熵
6. 模糊测度积分
   1. Choquet 积分
   2. Sugeno 积分
   3. Shilkret 积分
7. 杂项
   1. 数据集合正太分布 k-s 检验
   2. 数据集合随机划分为两个集合
   3. 阿基米德 T 范数与阿基米德 T 余范数

## 待开发的功能：
1. Q阶序对模糊数的相似性度量，模糊熵度量
2. 广义模糊集合距离，相似度度量
3. [ ] 适配 GPU，采用 CuPy
4. [ ] 添加基于 PyTorch 或 TensorFlow 的模糊框架，已适配深度学习开发
5. [ ] Numpy 和 CuPy 进行张量计算存在缺陷，考虑适配 PyTorch 和 TensorFlow
6. [ ] 基于 MohuPy 的 Q 阶序对模糊神经网络
7. [ ] 添加 Q 阶序对犹豫模糊集的计算