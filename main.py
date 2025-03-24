import math
import itertools


def get_float_input(prompt):
    """获取用户输入并转换为浮点数，如果输入无效则提示重新输入"""
    while True:
        try:
            return round(float(input(prompt)), 2)
        except ValueError:
            print("输入无效，请输入一个数字！")


def two_floor_three_ceil(number):
    integer_part = math.floor(number)  # 获取整数部分
    decimal_part = number - integer_part  # 获取小数部分

    if decimal_part < 0.2:
        return integer_part  # 小数部分小于 0.2，舍去
    else:
        return math.ceil(number)  # 小数部分大于或等于 0.2，进位


def getScore(
    living: float,
    material_attack: float,
    material_defense: float,
    magic_attack: float,
    magic_defense: float,
):
    """计算资质得分"""
    return math.floor(
        (living + material_attack) * 0.625
        + (material_defense + magic_attack + magic_defense) * 1.25
    )


if __name__ == "__main__":
    # 获取所有输入并转换为浮点数
    # living_upper = get_float_input("输入生命上限: ")
    # living_curr = get_float_input("输入当前生命值: ")
    # living_unit = get_float_input("输入一个果子可以增加的生命值: ")
    # material_attack_upper = get_float_input("输入物理攻击上限: ")
    # material_attack_curr = get_float_input("输入当前物理攻击: ")
    # material_attack_unit = get_float_input("输入一个果子可以增加的物理攻击: ")
    # magic_attack_upper = get_float_input("输入法术攻击上限: ")
    # magic_attack_curr = get_float_input("输入当前法术攻击: ")
    # magic_attack_unit = get_float_input("输入一个果子可以增加的法术攻击: ")
    # magic_defense_upper = get_float_input("输入法术防御上限: ")
    # magic_defense_curr = get_float_input("输入当前法术防御: ")
    # magic_defense_unit = get_float_input("输入一个果子可以增加的法术防御: ")
    # material_defense_upper = get_float_input("输入物理防御上限: ")
    # material_defense_curr = get_float_input("输入当前物理防御: ")
    # material_defense_unit = get_float_input("输入一个果子可以增加的物理防御: ")

    living_upper = 57.2
    living_curr = 56.68
    living_unit = 0.52
    material_attack_upper = 9.73
    material_attack_curr = 9.56
    material_attack_unit = 0.09

    magic_attack_upper = 2.77
    magic_attack_curr = 2.69
    magic_attack_unit = 0.02

    magic_defense_upper = 3.2
    magic_defense_curr = 2.93
    magic_defense_unit = 0.03
    material_defense_upper = 3.9
    material_defense_curr = 3.57
    material_defense_unit = 0.04

    # 计算各项值
    living = 20 - two_floor_three_ceil(round((living_upper - living_curr) / living_unit, 2))
    material_attack = 20 - two_floor_three_ceil(
        round((material_attack_upper - material_attack_curr) / material_attack_unit, 2)
    )
    magic_attack = 20 - two_floor_three_ceil(
        round((magic_attack_upper - magic_attack_curr) / magic_attack_unit, 2)
    )

    print(
        (magic_attack_upper - magic_attack_curr) / magic_attack_unit,
        round((magic_attack_upper - magic_attack_curr) / magic_attack_unit, 2),
        two_floor_three_ceil(
            round((magic_attack_upper - magic_attack_curr) / magic_attack_unit, 2)
        ),
    )

    magic_defense = 20 - two_floor_three_ceil(
        round((magic_defense_upper - magic_defense_curr) / magic_defense_unit, 2)
    )
    material_defense = 20 - two_floor_three_ceil(
        round((material_defense_upper - material_defense_curr) / material_defense_unit, 2)
    )

    print(
        f"当前数值：生命{living} 物攻{material_attack} 法攻{magic_attack} 法防{magic_defense} 物防{material_defense}"
    )

    # 计算总分并向下取整
    score = getScore(living, material_attack, material_defense, magic_attack, magic_defense)
    print("当前得分:", score)
    if score >= 90:
        print("恭喜，您的艾比资质已经达到 90 分！")

    # 根据各项数值计算是否能在 6 个资质果内达到 90 分
    # 每个属性的候选果子数量
    upper_boundary = 18
    living_candidate = max(upper_boundary - living, 0)
    material_attack_candidate = max(upper_boundary - material_attack, 0)
    material_defense_candidate = max(upper_boundary - material_defense, 0)
    magic_attack_candidate = max(upper_boundary - magic_attack, 0)
    magic_defense_candidate = max(upper_boundary - magic_defense, 0)

    # 生成所有可能的候选组合（每个属性使用的果子数量）
    candidates = {
        "living": living_candidate,
        "material_attack": material_attack_candidate,
        "material_defense": material_defense_candidate,
        "magic_attack": magic_attack_candidate,
        "magic_defense": magic_defense_candidate,
    }

    # 为每个属性生成可能的果子使用数量（0到最大值，不超过候选值）
    ranges = []
    for key in candidates:
        max_val = candidates[key]
        ranges.append(range(0, max_val + 1))  # 包含 0 到 max_val

    # 生成所有组合的笛卡尔积，并筛选出总使用数 ≤6 的组合
    valid_combinations = []
    for combo in itertools.product(*ranges):
        total_used = sum(combo)
        if total_used <= 6:
            valid_combinations.append(combo)

    # 存储所有符合条件的组合及其得分
    results = []
    for combo in valid_combinations:
        # 分配果子到各属性
        l_add, ma_add, md_add, mgc_add, mgd_add = combo

        # 计算新属性值
        new_living = living + l_add
        new_material_attack = material_attack + ma_add
        new_material_defense = material_defense + md_add
        new_magic_attack = magic_attack + mgc_add
        new_magic_defense = magic_defense + mgd_add

        # 计算新分数
        new_score = getScore(
            new_living,
            new_material_attack,
            new_material_defense,
            new_magic_attack,
            new_magic_defense,
        )
        if new_score >= 90:
            # 构建输出字符串，只显示非零的果子数量
            output = []
            if l_add > 0:
                output.append(f"生命果: {l_add}")
            if ma_add > 0:
                output.append(f"物攻果: {ma_add}")
            if mgc_add > 0:
                output.append(f"法攻果: {mgc_add}")
            if mgd_add > 0:
                output.append(f"法防果: {mgd_add}")
            if md_add > 0:
                output.append(f"物防果: {md_add}")

            # 存储结果
            results.append(
                {"total_used": sum(combo), "output": "  ".join(output), "new_score": new_score}
            )

    # 按总果子数排序
    results.sort(key=lambda x: x["total_used"])

    # 输出排序后的结果
    if results:
        print("\n找到可行组合（按总果子数排序）：")
        for result in results:
            print(
                f"  总果子数: {result['total_used']}  {result['output']}  新得分: {result['new_score']}"
            )
    else:
        print("\n无法在 6 个资质果内达到 90 分！")
