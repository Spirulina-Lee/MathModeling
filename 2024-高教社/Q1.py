import numpy as np
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportion_confint
from tqdm import tqdm
from matplotlib.font_manager import FontProperties

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号


# 进行蒙特卡洛模拟函数
def adaptive_sampling(p0, alpha, max_samples=1000):
    n = 0  # 当前抽取的样本数
    defective_count = 0  # 次品数量

    while n < max_samples:
        sample = np.random.binomial(1, p0)
        defective_count += sample
        n += 1
        current_defective_rate = defective_count / n

        ci_lower, ci_upper = proportion_confint(defective_count, n, alpha=alpha, method='beta')

        if ci_upper < p0:
            return "接收该批次", n, current_defective_rate
        elif ci_lower > p0:
            return "拒绝该批次", n, current_defective_rate

    return "无法确定", n, current_defective_rate


# 蒙特卡洛模拟
def monte_carlo_simulation(p0, alpha, max_samples=1000, num_simulations=1000):
    samples_list = []
    for _ in tqdm(range(num_simulations)):
        decision, samples, _ = adaptive_sampling(p0, alpha, max_samples)
        if decision != "无法确定":
            samples_list.append(samples)
    return samples_list


# 可视化
def plot_simulation_results(simulation1, simulation2, color1, color2, label1, label2, filename):
    fig, ax = plt.subplots()

    # 绘制两次蒙特卡洛模拟的散点图
    x1 = np.arange(len(simulation1))
    x2 = np.arange(len(simulation2))
    ax.scatter(x1, simulation1, color=color1, label=label1, alpha=0.5)
    ax.scatter(x2, simulation2, color=color2, label=label2, alpha=0.5)

    # 计算平均值
    avg_simulation1 = np.mean(simulation1)
    avg_simulation2 = np.mean(simulation2)

    # 输出拟合值到控制台
    print(f'{label1} 平均样本数: {avg_simulation1:.2f}')
    print(f'{label2} 平均样本数: {avg_simulation2:.2f}')

    # 绘制拟合线
    ax.axhline(y=avg_simulation1, color=color1, linestyle='--', label=f'{label1} 平均样本数')
    ax.axhline(y=avg_simulation2, color=color2, linestyle='--', label=f'{label2} 平均样本数')

    # 图表细节
    ax.set_xlabel('模拟次数')
    ax.set_ylabel('样本数')
    ax.set_title('蒙特卡洛模拟样本数')
    ax.legend()

    # 设置背景透明
    fig.patch.set_alpha(0)

    # 保存高分辨率透明图片
    plt.savefig(filename, dpi=500, transparent=True)  # 高分辨率 dpi=500


# 参数设定
p0 = 0.1  # 标称次品率
num_simulations = 1000  # 模拟次数
max_samples = 1000

# 在 95% 的置信度下，拒收次品率超过标称值的批次
alpha_for_reject = 0.05
simulation1_1 = monte_carlo_simulation(p0, alpha_for_reject, max_samples, num_simulations)  # 第一次模拟
simulation1_2 = monte_carlo_simulation(p0, alpha_for_reject, max_samples, num_simulations)  # 第二次模拟

# 在 90% 的置信度下，接收次品率不超过标称值的批次
alpha_for_accept = 0.10
simulation2_1 = monte_carlo_simulation(p0, alpha_for_accept, max_samples, num_simulations)  # 第一次模拟
simulation2_2 = monte_carlo_simulation(p0, alpha_for_accept, max_samples, num_simulations)  # 第二次模拟

# 绘制并保存两种情况下的图
plot_simulation_results(simulation1_1, simulation1_2, '#BDD4FC', '#FFE89C', '95% 置信度第一次', '95% 置信度第二次',
                        'monte_carlo_simulation_reject.png')
plot_simulation_results(simulation2_1, simulation2_2, '#BDD4FC', '#FFE89C', '90% 置信度第一次', '90% 置信度第二次',
                        'monte_carlo_simulation_accept.png')
