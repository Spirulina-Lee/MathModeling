import itertools

# 定义所有决策的组合 (16种可能的组合)
decisions_combinations = list(itertools.product([0, 1], repeat=4))

# 根据表格中的数据重新定义情景参数
scenarios_corrected = [
    {'defective_rate_1': 0.10, 'defective_rate_2': 0.10, 'purchase_1': 4, 'purchase_2': 18,
     'inspect_1': 2, 'inspect_2': 3, 'assemble_cost': 6, 'inspect_product': 3,
     'market_price': 56, 'exchange_loss': 6, 'disassembly_cost': 5, 'product_failure_rate': 0.10},

    {'defective_rate_1': 0.20, 'defective_rate_2': 0.20, 'purchase_1': 4, 'purchase_2': 18,
     'inspect_1': 2, 'inspect_2': 3, 'assemble_cost': 6, 'inspect_product': 3,
     'market_price': 56, 'exchange_loss': 6, 'disassembly_cost': 5, 'product_failure_rate': 0.20},

    {'defective_rate_1': 0.10, 'defective_rate_2': 0.10, 'purchase_1': 4, 'purchase_2': 18,
     'inspect_1': 2, 'inspect_2': 3, 'assemble_cost': 6, 'inspect_product': 3,
     'market_price': 56, 'exchange_loss': 30, 'disassembly_cost': 5, 'product_failure_rate': 0.10},

    {'defective_rate_1': 0.20, 'defective_rate_2': 0.20, 'purchase_1': 4, 'purchase_2': 18,
     'inspect_1': 1, 'inspect_2': 1, 'assemble_cost': 6, 'inspect_product': 2,
     'market_price': 56, 'exchange_loss': 30, 'disassembly_cost': 5, 'product_failure_rate': 0.20},

    {'defective_rate_1': 0.10, 'defective_rate_2': 0.20, 'purchase_1': 4, 'purchase_2': 18,
     'inspect_1': 8, 'inspect_2': 1, 'assemble_cost': 6, 'inspect_product': 2,
     'market_price': 56, 'exchange_loss': 10, 'disassembly_cost': 5, 'product_failure_rate': 0.10},

    {'defective_rate_1': 0.05, 'defective_rate_2': 0.05, 'purchase_1': 4, 'purchase_2': 18,
     'inspect_1': 2, 'inspect_2': 3, 'assemble_cost': 6, 'inspect_product': 3,
     'market_price': 56, 'exchange_loss': 10, 'disassembly_cost': 40, 'product_failure_rate': 0.05}
]

# 成本计算函数，计算利润、次品率，并返回详细的成本分项
def calculate_profit_and_defective_rate_detailed(scenario, decision, quantity_part1=1000, quantity_part2=1000, sub_decision_str=None):
    d1, d2 = scenario['defective_rate_1'], scenario['defective_rate_2']
    c1, c2 = scenario['purchase_1'], scenario['purchase_2']
    i1, i2 = scenario['inspect_1'], scenario['inspect_2']
    ac = scenario['assemble_cost']
    ip = scenario['inspect_product']
    mp = scenario['market_price']
    el = scenario['exchange_loss']
    dc = scenario['disassembly_cost']
    product_failure_rate = scenario['product_failure_rate']

    # 解析决策组合 (d1检测, d2检测, 成品检测, 拆解)
    detect_part1, detect_part2, detect_product, disassemble = decision

    # 1. 固定采购成本：无论是否检测，所有零配件都先买回来
    purchase_cost_part1 = c1 * quantity_part1
    purchase_cost_part2 = c2 * quantity_part2
    purchase_cost = purchase_cost_part1 + purchase_cost_part2

    # 2. 零配件1检测成本
    if detect_part1:
        inspect_cost_part1 = i1 * quantity_part1  # 检测所有的零件，无论是否合格
        part1_defective_rate = 0  # 检测后次品率变为0
        good_quantity_part1 = quantity_part1 * (1 - d1)  # 只留下合格的零件1
        # 检测的零件直接丢弃
        quantity_part1 = good_quantity_part1  # 更新数量
    else:
        inspect_cost_part1 = 0  # 不检测时无检测费用
        part1_defective_rate = d1  # 不检测次品率保持原样

    # 3. 零配件2检测成本
    if detect_part2:
        inspect_cost_part2 = i2 * quantity_part2  # 检测所有的零件，无论是否合格
        part2_defective_rate = 0  # 检测后次品率变为0
        good_quantity_part2 = quantity_part2 * (1 - d2)  # 只留下合格的零件2
        # 检测的零件直接丢弃
        quantity_part2 = good_quantity_part2  # 更新数量
    else:
        inspect_cost_part2 = 0  # 不检测时无检测费用
        part2_defective_rate = d2  # 不检测次品率保持原样

    # 4. 装配逻辑：根据两个零件的质量情况决定成品次品率
    if detect_part1 and detect_part2:
        total_quantity = min(good_quantity_part1, good_quantity_part2)  # 两个零件都合格时，用最少的
        product_defective_rate = product_failure_rate  # 仅考虑装配失败的次品率
    elif detect_part1 and not detect_part2:
        total_quantity = good_quantity_part1  # 零件1合格的数量
        product_defective_rate = part2_defective_rate + (1 - part2_defective_rate) * product_failure_rate  # 考虑未检测零件的次品率
    elif not detect_part1 and detect_part2:
        total_quantity = good_quantity_part2  # 零件2合格的数量
        product_defective_rate = part1_defective_rate + (1 - part1_defective_rate) * product_failure_rate  # 考虑未检测零件的次品率
    else:
        total_quantity = min(quantity_part1, quantity_part2)  # 两个零件都可能次品
        # 如果任意一个零件次品，成品必然是次品
        product_defective_rate = 1 - (1 - part1_defective_rate) * (1 - part2_defective_rate)
        # 如果两个零件都是合格的，考虑装配失败的次品率
        product_defective_rate += (1 - product_defective_rate) * product_failure_rate

    # 5. 装配成本：无论装配是否生成次品，装配都需要费用
    assemble_cost = total_quantity * ac  # 实际装配成本

    # 6. 成品检测逻辑
    if detect_product:
        # 如果成品被检测，次品进入拆解
        product_cost = ip * total_quantity  # 检测所有成品
        defective_quantity = total_quantity * product_defective_rate  # 检测出次品的数量
        sold_quantity = total_quantity * (1 - product_defective_rate)  # 售出的正品数量
        total_sales = sold_quantity * mp  # 只有合格成品进入市场
        product_sale_loss = 0  # 检测后无销售损失
    else:
        # 如果不检测，次品直接进入市场
        product_cost = 0  # 不检测时无检测费用
        sold_quantity = total_quantity * (1 - product_defective_rate)  # 售出的正品数量
        total_sales = sold_quantity * mp  # 售出的正品销售额
        # 换货损失 = 调换损失（次品流入市场）
        product_sale_loss = product_defective_rate * el * total_quantity  # 换货损失=调换损失
        defective_quantity = total_quantity * product_defective_rate  # 流入市场的次品

    # 打印主序列中的正品售出数量和对应的销售额
    print(f"主序列售出正品数量: {sold_quantity:.2f}, 对应销售额: {total_sales:.2f}")

    # 7. 计算进入子序列的正品零件：正品零件总数 - 已生产的正品成品个数
    total_good_part1 = quantity_part1 * (1 - part1_defective_rate)  # 零件1的总正品数量
    total_good_part2 = quantity_part2 * (1 - part2_defective_rate)  # 零件2的总正品数量
    # 未被使用的正品零件个数
    unused_good_part1 = total_good_part1 - sold_quantity
    unused_good_part2 = total_good_part2 - sold_quantity
    # 进入子序列的正品零件数为两个正品零件中较少的那个
    good_parts_for_subsequence = min(unused_good_part1, unused_good_part2)

    # 8. 换货后的拆解逻辑：如果选择拆解
    if disassemble == 1:
        disassembly_cost = defective_quantity * dc  # 拆解所有次品的费用
        # 如果不检测，流入市场的次品也进入拆解
        if not detect_product:
            disassembly_cost += product_defective_rate * total_quantity * dc  # 流入市场的次品拆解
    else:
        disassembly_cost = 0  # 没有拆解则无拆解费用

    # 9. 拆解后的子决策：子序列继承主序列的零件检测和装配结果
    if disassemble == 1 and defective_quantity > 0:
        # 根据主序列的检测结果判断子序列中的零件
        if detect_part1 and detect_part2:
            # 主序列检测了零件，子序列只有因装配失败的正品零件
            sub_defective_rate_1 = 0  # 子序列中的零件都是正品
            sub_defective_rate_2 = 0
        else:
            # 主序列未检测，子序列可能有次品零件
            sub_defective_rate_1 = d1  # 继承主序列的次品率
            sub_defective_rate_2 = d2

        # 拆解后的子决策：零部件检测决策相反，成品检测决策保持原决策或取反
        new_decision_part1 = 1 - detect_part1
        new_decision_part2 = 1 - detect_part2

        # 子决策，保留成品检测决策不变或取反
        new_decision_combinations = [(new_decision_part1, new_decision_part2, detect_product, 0),  # 保持成品检测决策
                                     (new_decision_part1, new_decision_part2, 1 - detect_product, 0)]  # 取反成品检测决策

        sub_results = []
        for sub_decision in new_decision_combinations:
            sub_decision_str = f"{''.join(map(str, decision))}|{''.join(map(str, sub_decision))}"
            # 子决策计算时根据主序列继承次品率
            sub_result = calculate_profit_and_defective_rate_detailed(
                {
                    'defective_rate_1': sub_defective_rate_1,
                    'defective_rate_2': sub_defective_rate_2,
                    'purchase_1': c1,
                    'purchase_2': c2,
                    'inspect_1': i1,
                    'inspect_2': i2,
                    'assemble_cost': ac,
                    'inspect_product': ip,
                    'market_price': mp,
                    'exchange_loss': el,
                    'disassembly_cost': dc,
                    'product_failure_rate': product_failure_rate
                },
                sub_decision,
                quantity_part1=good_parts_for_subsequence,  # 使用计算出的剩余正品零件数量
                quantity_part2=good_parts_for_subsequence,
                sub_decision_str=sub_decision_str
            )
            sub_result['purchase_cost'] = 0  # 子决策没有采购成本

            # 子决策中的逻辑调整：
            # 如果子决策再次检测，次品被丢弃；如果不检测，次品进入市场，产生换货损失
            if sub_decision[2]:  # 成品再次检测
                sub_result['exchange_loss'] = 0  # 检测后不会有次品进入市场
            else:
                # 不检测，次品进入市场，计算换货损失（包括调换损失）
                defective_rate = sub_result['product_defective_rate']
                sub_result['exchange_loss'] = defective_rate * el * good_parts_for_subsequence  # 只算调换损失

            sub_results.append(sub_result)

        # 打印子序列中的正品售出数量和对应的销售额
        for sub_result in sub_results:
            sub_decision_str = sub_result.get('decision_str')
            print(f"子序列 {sub_decision_str} -> 售出正品数量: {sub_result['total_sales'] / mp:.2f}, 对应销售额: {sub_result['total_sales']:.2f}")

        # 获取子分支中最佳利润方案
        best_sub_result = max(sub_results, key=lambda x: x['profit'])

        # 将子分支的成本、销售和利润与主决策相加
        total_sales += best_sub_result['total_sales']  # 加上子分支的销售收入
        disassembly_cost += best_sub_result['disassembly_cost']  # 加上子分支的拆解费用
        assemble_cost += best_sub_result['assemble_cost']  # 加上子分支的装配费用
        inspect_cost_part1 += best_sub_result['inspect_cost_part1']  # 加上子分支的零件1检测费用
        inspect_cost_part2 += best_sub_result['inspect_cost_part2']  # 加上子分支的零件2检测费用
        product_cost += best_sub_result['product_cost']  # 加上子分支的成品检测费用
        product_sale_loss += best_sub_result['exchange_loss']  # 子分支的换货损失
        sub_decision_str = best_sub_result.get('decision_str', sub_decision_str)

    # 总成本：采购成本 + 检测成本 + 装配成本 + 拆解成本 + 换货损失
    total_cost = (purchase_cost + inspect_cost_part1 + inspect_cost_part2 +
                  assemble_cost + product_cost + disassembly_cost + product_sale_loss)

    # 利润 = 销售收入 - 成本
    profit = total_sales - total_cost

    # 返回详细的成本分项
    return {
        'profit': profit,
        'product_defective_rate': product_defective_rate,
        'total_cost': total_cost,
        'total_sales': total_sales,
        'purchase_cost': purchase_cost,
        'inspect_cost_part1': inspect_cost_part1,
        'inspect_cost_part2': inspect_cost_part2,
        'assemble_cost': assemble_cost,
        'product_cost': product_cost,
        'disassembly_cost': disassembly_cost,
        'exchange_loss': product_sale_loss,
        'decision_str': sub_decision_str or ''.join(map(str, decision))
    }

# 对每个情景计算24种决策的详细结果
detailed_results = []
for index, scenario in enumerate(scenarios_corrected):
    print(f"\n情景 {index + 1} 的24种决策详情:")
    scenario_result = []
    for decision in decisions_combinations:
        result = calculate_profit_and_defective_rate_detailed(scenario, decision)
        decision_str = result['decision_str']
        print(f"决策 {decision_str} -> 总成本: {result['total_cost']:.2f}, 销售额: {result['total_sales']:.2f}, 利润: {result['profit']:.2f}, 次品率: {result['product_defective_rate']:.2%}")
        print(f"详细成本: 采购成本: {result['purchase_cost']:.2f}, 零件1检测成本: {result['inspect_cost_part1']:.2f}, "
              f"零件2检测成本: {result['inspect_cost_part2']:.2f}, 装配成本: {result['assemble_cost']:.2f}, "
              f"成品检测成本: {result['product_cost']:.2f}, 拆解成本: {result['disassembly_cost']:.2f}, "
              f"换货损失: {result['exchange_loss']:.2f}")
        scenario_result.append(result)
    detailed_results.append(scenario_result)

# 打印最佳策略
print("\n最佳策略:")

optimal_profit_decisions = []
for result in detailed_results:
    best_decision = max(result, key=lambda x: x['profit'])
    print(
        f"情景 {best_decision['decision_str']} -> 总成本: {best_decision['total_cost']:.2f}, 销售额: {best_decision['total_sales']:.2f}, 利润: {best_decision['profit']:.2f}, 次品率: {best_decision['product_defective_rate']:.2%}")
    print(f"详细成本: 采购成本: {best_decision['purchase_cost']:.2f}, 零件1检测成本: {best_decision['inspect_cost_part1']:.2f}, "
          f"零件2检测成本: {best_decision['inspect_cost_part2']:.2f}, 装配成本: {best_decision['assemble_cost']:.2f}, "
          f"成品检测成本: {best_decision['product_cost']:.2f}, 拆解成本: {best_decision['disassembly_cost']:.2f}, "
          f"换货损失: {best_decision['exchange_loss']:.2f}")
    optimal_profit_decisions.append(best_decision)
