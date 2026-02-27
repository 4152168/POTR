import json
from eve_plan import run_eve
from secondary_screen import run_secondary
from info_density import run_density

def run_pipeline(questions_file="questions.txt", final_output="final_results.json"):
    """执行完整POTR流程：夏娃计划 → 二次筛查 → 信息密度"""
    # 1. 夏娃计划
    from eve_plan import run_eve
    with open(questions_file, "r", encoding="utf-8") as f:
        questions = [line.strip() for line in f if line.strip()]
    eve_results = run_eve(questions, output_file="phase1_results.json")

    # 2. 二次筛查
    run_secondary("phase1_results.json", "phase1_results_with_ai_scores.json")

    # 3. 信息密度
    run_density("phase1_results_with_ai_scores.json", final_output)

    print(f"完整流程结束，最终结果已保存到 {final_output}")

if __name__ == "__main__":
    run_pipeline()
