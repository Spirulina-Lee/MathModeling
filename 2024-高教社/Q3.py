import numpy as np
import matplotlib.pyplot as plt
from itertools import product
import pandas as pd
from matplotlib import rcParams

# 配置中文字体
rcParams['font.sans-serif'] = ['SimHei']
rcParams['axes.unicode_minus'] = False

# 零配件和半成品及成品数据
parts_data = {
    '零件A': {'次品率': 0.1, '单价': 2, '检测费': 1},
    '零件B': {'次品率': 0.1, '单价': 8, '检测费': 1},
    '零件C': {'次品率': 0.1, '单价': 12, '检测费': 2},
    '零件D': {'次品率': 0.1, '单价': 2, '检测费': 1},
    '零件E': {'次品率': 0.1, '单价': 8, '检测费': 1},
    '零件F': {'次品率': 0.1, '单价': 12, '检测费': 2},
    '零件G': {'次品率': 0.1, '单价': 8, '检测费': 1},
    '零件H': {'次品率': 0.1, '单价': 12, '检测费': 2},
}

sub_assemblies = {
    '组件A': {'次品率': 0.1, '组装费': 8, '检测费': 4, '拆解费': 6},
    '组件B': {'次品率': 0.1, '组装费': 8, '检测费': 4, '拆解费': 6},
    '组件C': {'次品率': 0.1, '组装费': 8, '检测费': 4, '拆解费': 6},
}

finished_product = {
    '产品': {'次品率': 0.1, '组装费': 8, '检测费': 6, '拆解费': 10, '售价': 200, '退换损失': 40}
}

# 成本计算函数
def estimate_total_cost(parts, subs, final, inspect_parts, inspect_subs, inspect_final, dismantle_final, dismantle_subs):
    cost_sum = 0
    combined_defective_rate = 1

    # 计算零配件成本
    for idx, (part, part_info) in enumerate(parts.items()):
        part_cost = part_info['单价']
        defect_rate = part_info['次品率']
        if inspect_parts[idx]:
            defect_rate *= 0.5
            part_cost += part_info['检测费']

        cost_sum += part_cost
        combined_defective_rate *= (1 - defect_rate)

    # 计算半成品成本
    for idx, (sub, sub_info) in enumerate(subs.items()):
        sub_cost = sub_info['组装费']
        defect_rate = sub_info['次品率']
        if inspect_subs[idx]:
            defect_rate *= 0.5
            sub_cost += sub_info['检测费']

        cost_sum += sub_cost
        combined_defective_rate *= (1 - defect_rate)

        if dismantle_subs[idx]:
            cost_sum += sub_info['拆解费']

    # 计算成品成本
    final_defective_rate = final['产品']['次品率'] * (0.5 if inspect_final else 1)
    final_cost = final['产品']['组装费']

    if inspect_final:
        final_cost += final['产品']['检测费']

    cost_sum += final_cost
    combined_defective_rate = 1 - (combined_defective_rate * (1 - final_defective_rate))

    # 添加调换损失和拆解费用
    replacement_loss = final['产品']['退换损失'] * combined_defective_rate
    cost_sum += replacement_loss

    if dismantle_final:
        cost_sum += final['产品']['拆解费']

    return cost_sum, combined_defective_rate

# 生成所有策略的组合
part_options = list(product([True, False], repeat=8))
sub_options = list(product([True, False], repeat=3))
final_options = list(product([True, False], repeat=2))
dismantle_sub_options = list(product([True, False], repeat=3))

strategy_info = []
outcomes = []

# 描述策略
def describe_strategy(inspect_parts, inspect_subs, inspect_final, dismantle_final, dismantle_subs):
    desc = ""
    for idx, inspect in enumerate(inspect_parts):
        desc += f"检测零件 {idx + 1}，" if inspect else f"不检测零件 {idx + 1}，"
    for idx, inspect in enumerate(inspect_subs):
        desc += f"检测组件 {idx + 1}，" if inspect else f"不检测组件 {idx + 1}，"
    desc += "检测成品，" if inspect_final else "不检测成品，"
    desc += "拆解成品，" if dismantle_final else "不拆解成品，"
    for idx, dismantle in enumerate(dismantle_subs):
        desc += f"拆解组件 {idx + 1}，" if dismantle else f"不拆解组件 {idx + 1}，"
    return desc

# 计算每种策略的结果
strategy_id = 1
for part_comb in part_options:
    for sub_comb in sub_options:
        for final_comb in final_options:
            for dismantle_sub_comb in dismantle_sub_options:
                inspect_parts = part_comb
                inspect_subs = sub_comb
                inspect_final = final_comb[0]
                dismantle_final = final_comb[1]
                dismantle_subs = dismantle_sub_comb

                total_cost, defective_rate = estimate_total_cost(parts_data, sub_assemblies, finished_product,
                                                                inspect_parts, inspect_subs, inspect_final,
                                                                dismantle_final, dismantle_subs)

                strategy_desc = describe_strategy(inspect_parts, inspect_subs, inspect_final, dismantle_final,
                                                  dismantle_subs)
                outcomes.append([strategy_id, strategy_desc, total_cost, defective_rate])
                strategy_id += 1

# 转换为DataFrame
df_strategies = pd.DataFrame(outcomes, columns=['策略编号', '策略描述', '总成本', '成品次品率'])

# 保存到Excel
df_strategies.to_excel('策略结果.xlsx', index=False)
print("策略已保存到文件 '策略结果.xlsx'。")

# 绘制成本和次品率图表
plt.figure(figsize=(10, 6))
plt.bar(df_strategies['策略编号'], df_strategies['总成本'], color='lightblue', label="总成本")
plt.xlabel("策略编号")
plt.ylabel("总成本 (元)")
plt.title("策略的总成本比较")
plt.grid(axis='y')
plt.legend()
plt.show()

plt.figure(figsize=(10, 6))
plt.scatter(df_strategies['策略编号'], df_strategies['成品次品率'], color='coral', label="成品次品率")
plt.xlabel("策略编号")
plt.ylabel("成品次品率")
plt.title("策略的成品次品率比较")
plt.grid(True)
plt.legend()
plt.show()
