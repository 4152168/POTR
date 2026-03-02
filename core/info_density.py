import json
import math
from config import DENSITY_BASE, ORIGINAL_WEIGHT

def calculate_density(answer, ai_score, original_debt):
    length = len(answer)
    if length == 0:
        return 0.0, float('inf')
    density = ai_score * DENSITY_BASE / (math.log(length + 10) * 10)
    density = round(density, 4)
    new_debt = ORIGINAL_WEIGHT * original_debt + (1 - ORIGINAL_WEIGHT) * (1 / (density + 0.01))
    new_debt = round(new_debt, 4)
    return density, new_debt

def run_density(input_file, output_file):
    """供 pipeline 调用的主函数"""
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        for cand in item['candidates']:
            ai_score = cand.get('ai_depth_score', 3)
            orig_debt = cand.get('debt', 0)
            answer = cand.get('answer', '')
            density, new_debt = calculate_density(answer, ai_score, orig_debt)
            cand['info_density'] = density
            cand['new_debt'] = new_debt

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"信息密度计算完成，结果已保存到 {output_file}")

if __name__ == "__main__":
    run_density("phase1_results_with_ai_scores.json", "phase1_results_with_density.json")
