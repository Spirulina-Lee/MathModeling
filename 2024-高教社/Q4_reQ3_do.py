import numpy as np
import pandas as pd

# 读取策略结果文件（假设前面的代码已生成了策略结果）
# 如果你有已生成的结果可以直接从df中读取，否则用 pd.read_excel('策略结果.xlsx') 读取
df = pd.read_excel('re策略结果.xlsx')

# 提取总成本和成品次品率两列
data = df[['总成本', '成品次品率']].values


# 第一步：数据标准化（这里采用极差标准化）
def normalize(data):
    min_vals = np.min(data, axis=0)
    max_vals = np.max(data, axis=0)
    norm_data = (data - min_vals) / (max_vals - min_vals)
    return norm_data


norm_data = normalize(data)


# 第二步：计算熵值
def calculate_entropy(norm_data):
    # 防止计算时出现log(0)，将0替换为一个极小值
    norm_data = np.where(norm_data == 0, 1e-12, norm_data)

    # 计算每个策略在各指标下的占比
    proportion = norm_data / np.sum(norm_data, axis=0)

    # 计算熵值
    k = 1 / np.log(len(norm_data))
    entropy = -k * np.sum(proportion * np.log(proportion), axis=0)

    return entropy


entropy = calculate_entropy(norm_data)


# 第三步：计算权重
def calculate_weights(entropy):
    d = 1 - entropy  # 熵越大，d值越小，权重越小
    weights = d / np.sum(d)  # 归一化权重
    return weights


weights = calculate_weights(entropy)

# 打印熵值和权重
print("各个指标的熵值为：", entropy)
print("各个指标的权重为：", weights)


# 第四步：计算综合评价值（加权得分）
def calculate_evaluation(norm_data, weights):
    evaluation = np.dot(norm_data, weights)
    return evaluation


evaluation_scores = calculate_evaluation(norm_data, weights)

# 将评价值添加到DataFrame中
df['评价值'] = evaluation_scores

# 根据评价值排序，评价值越小越好
df = df.sort_values(by='评价值')

# 保存新的策略结果到Excel
df.to_excel('re带评价值的策略结果.xlsx', index=False)
print("策略结果已保存到 're带评价值的策略结果.xlsx' 文件中。")

# 打印最优策略
best_strategy = df.iloc[0]  # 获取评价值最小的策略
print("最优策略为：")
print(best_strategy)
