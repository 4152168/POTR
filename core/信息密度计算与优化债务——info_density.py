import   进口   进口json json
from   从 config import   进口 DENSITY_BASE, ORIGINAL_WEIGHT

def calculate_density(answer, ai_score):
    """计算信息密度"""
    length = len(answer)
    if   如果 length == 0:
        return   返回 0.0
    density = ai_score * DENSITY_BASE / (length + 10)   # +10 防止除零
    return   返回 round(density, 4)

def optimize_debt(original_debt, density):
    """根据信息密度计算优化后的债务"""
    # 密度越低，其倒数越大，惩罚越重
    density_component = 1.0 / (density + 0.01)
    new_debt = ORIGINAL_WEIGHT * original_debt + (1 - ORIGINAL_WEIGHT) * density_component
    return   返回 round(new_debt, 4)

def run_density(input_file, output_file):
    """读取二次筛查结果，添加 info_density 和 new_debt 字段"""
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for   为 item in   在 data:
        for   为 cand in   在 item['candidates']:
            ai_score = cand.get('ai_depth_score', 3)
            answer = cand.get('answer', '')
            density = calculate_density(answer, ai_score)
            new_debt = optimize_debt(cand.get('debt', 0), density)
            cand['info_density'] = density
            cand['new_debt'] = new_debt

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False   假, indent=2)
    print(f"信息密度计算完成，结果已保存到 {output_file}")

if如果__name__ == "__main__"   如果； __name__ == "__main__":
    run_density("phase1_results_with_ai_scores.json", "phase1_results_with_density.json")
