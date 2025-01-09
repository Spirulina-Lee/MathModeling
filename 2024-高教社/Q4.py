import numpy as np
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportion_confint
from tqdm import tqdm

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体字体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号


# 自适应抽样检测函数，用于直接点估计次品率
def adaptive_sampling(true_defective_rate, alpha, max_samples=1000):
    n = 0  # 当前抽取的样本数
    defective_count = 0  # 次品数量

    while n < max_samples:
        sample = np.random.binomial(1, true_defective_rate)
        defective_count += sample
        n += 1
        current_defective_rate = defective_count / n

        ci_lower, ci_upper = proportion_confint(defective_count, n, alpha=alpha, method='beta')

        # 判断是否满足接受或拒绝的条件
        if ci_upper < true_defective_rate:
            return "接收该批次", n, current_defective_rate
        elif ci_lower > true_defective_rate:
            return "拒绝该批次", n, current_defective_rate

    return "无法确定", n, current_defective_rate


# 蒙特卡洛模拟函数，使用点估计
def monte_carlo_simulation(detected_defective_rate, alpha, max_samples=1000, num_simulations=1000):
    estimated_defective_rate_list = []
    for _ in tqdm(range(num_simulations)):
        # 使用检测到的次品率作为 "真实次品率" 来生成数据
        decision, _, estimated_defective_rate = adaptive_sampling(detected_defective_rate, alpha, max_samples)

        # 记录每次模拟中的次品率估计
        estimated_defective_rate_list.append(estimated_defective_rate)

    return estimated_defective_rate_list


# 可视化结果
def plot_simulation_results(defective_rate_list_5, defective_rate_list_10, defective_rate_list_20, filename):
    fig, ax = plt.subplots()

    # 绘制三种次品率的直方图
    ax.hist(defective_rate_list_5, bins=30, alpha=0.5, label="5% 样品率")
    ax.hist(defective_rate_list_10, bins=30, alpha=0.5, label="10% 样品率")
    ax.hist(defective_rate_list_20, bins=30, alpha=0.5, label="20% 样品率")

    # 输出平均值
    avg_5 = np.mean(defective_rate_list_5)
    avg_10 = np.mean(defective_rate_list_10)
    avg_20 = np.mean(defective_rate_list_20)

    print(f'5% 样品率对应的真实次品率: {avg_5:.4f}')
    print(f'10% 样品率对应的真实次品率: {avg_10:.4f}')
    print(f'20% 样品率对应的真实次品率: {avg_20:.4f}')

    # 设置图表细节
    ax.set_xlabel('估计的次品率')
    ax.set_ylabel('频率')
    ax.set_title('不同检测次品率的估计次品率分布')
    ax.legend()

    # 保存图像
    plt.savefig(filename, dpi=500, transparent=True)  # 高分辨率保存图片
    plt.show()


# 参数设定
num_simulations = 1000  # 模拟次数
max_samples = 1000

# 设置后验检测到的次品率
detected_defective_rates = [0.05, 0.10, 0.20]
alpha = 0.05  # 95% 的置信度

# 分别进行蒙特卡洛模拟
estimated_defective_rate_list_5 = monte_carlo_simulation(detected_defective_rates[0], alpha, max_samples,
                                                         num_simulations)
estimated_defective_rate_list_10 = monte_carlo_simulation(detected_defective_rates[1], alpha, max_samples,
                                                          num_simulations)
estimated_defective_rate_list_20 = monte_carlo_simulation(detected_defective_rates[2], alpha, max_samples,
                                                          num_simulations)

# 绘制结果
plot_simulation_results(estimated_defective_rate_list_5, estimated_defective_rate_list_10,
                        estimated_defective_rate_list_20, 'point_estimate_real_defective_rate.png')
