    penalty: 惩罚项，可为 'l1' or 'l2'。'netton-cg', 'sag', 'lbfgs' 只支持 'l2'。

        'l1' 正则化的损失函数不是连续可导的，而 'netton-cg', 'sag', 'lbfgs' 这三种算法需要损失函数的一阶或二阶连续可导。
        调参时如果主要是为了解决过拟合，选择 'l2' 正则化就够了。若选择 'l2' 正则化还是过拟合，可考虑 'l1' 正则化。
        若模型特征非常多，希望一些不重要的特征系数归零，从而让模型系数化的话，可使用 'l1' 正则化。

    dual: 选择目标函数为原始形式还是对偶形式。

    将原始函数等价转化为一个新函数，该新函数称为对偶函数。对偶函数比原始函数更易于优化。

    tol: 优化算法停止的条件。当迭代前后的函数差值小于等于 tol 时就停止。
    C: 正则化系数。其越小，正则化越强。
    fit_intercept: 选择逻辑回归模型中是否会有常数项 𝑏。
    intercept_scaling:
    class_weight: 用于标示分类模型中各种类型的权重，{class_label: weight} or 'balanced'。

        'balanced': 类库根据训练样本量来计算权重。某种类型的样本量越多，则权重越低。
        若误分类代价很高，比如对合法用户和非法用户进行分类，可适当提高非法用户的权重。
        样本高度失衡的。如合法用户 9995 条，非法用户 5 条，可选择 'balanced'，让类库自动提高非法用户样本的权重。

    random_state: 随机数种子。
    solver: 逻辑回归损失函数的优化方法。

        'liblinear': 使用坐标轴下降法来迭代优化损失函数。
        'lbfgs': 拟牛顿法的一种。利用损失函数二阶导数矩阵即海森矩阵来迭代优化损失函数。
        'newton-cg': 牛顿法的一种。同上。
        'sag': 随机平均梯度下降。每次迭代仅仅用一部分的样本来计算梯度，适合于样本数据多的时候。
        多元逻辑回归有 OvR(one-vs-rest) 和 MvM(many-vs-many) 两种，而 MvM 一般比 OvR 分类相对准确一些。但是，'liblinear' 只支持 OvR。

    max_iter: 优化算法的迭代次数。
    multi_class: 'ovr' or 'multinomial'。'multinomial' 即为 MvM。

        若是二元逻辑回归，二者区别不大。
        对于 MvM，若模型有 T 类，每次在所有的T类样本里面选择两类样本出来，把所有输出为该两类的样本放在一起，进行二元回归，得到模型参数，一共需要 T(T-1)/2 次分类。

    verbose：控制是否 print 训练过程。
    warm_start:
    n_jobs: 用 cpu 的几个核来跑程序。