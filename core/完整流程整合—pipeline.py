import os
import json
import time
from config import MODEL_NAME, TIMEOUT

# 各模块导入
from eve_plan import run_eve
from secondary_screen import run_secondary
from info_density import run_density
from final_screen import final_selection

# ========== 流程控制开关 ==========
RUN_EVE = True               # 是否运行夏娃计划（生成基础数据）
RUN_SECONDARY = True          # 是否运行二次筛查（添加AI深度分）
RUN_DENSITY = True            # 是否运行信息密度计算
RUN_FINAL = True              # 是否运行最终筛选
# ==================================

# 文件路径配置
QUESTIONS_FILE = "questions.txt"                     # 输入问题列表
EVE_OUTPUT = "phase1_results.json"                   # 夏娃计划输出
SECONDARY_OUTPUT = "phase1_results_with_ai_scores.json"  # 二次筛查输出
DENSITY_OUTPUT = "phase1_results_with_density.json"       # 信息密度输出
FINAL_OUTPUT = "final_results.json"                       # 最终筛选输出

def check_file_exists(filepath, description):
    """检查文件是否存在，不存在则打印警告"""
    if not os.path.exists(filepath):
        print(f"⚠️ 警告：{description} 文件 {filepath} 不存在，将跳过相关步骤。")
        return False
    return True

def run_pipeline():
    """执行完整的 POTR 处理流程"""
    print("=" * 50)
    print("POTR 完整流程启动")
    print(f"模型：{MODEL_NAME}，超时：{TIMEOUT}秒")
    print("=" * 50)

    # ---------- 1. 夏娃计划 ----------
    if RUN_EVE:
        print("\n[步骤1] 夏娃计划：基础债务函数筛选")
        if not check_file_exists(QUESTIONS_FILE, "问题列表"):
            print("❌ 缺少问题列表，流程终止。")
            return
        with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
            questions = [line.strip() for line in f if line.strip()]
        print(f"读取到 {len(questions)} 个问题。")
        run_eve(questions, output_file=EVE_OUTPUT)
    else:
        print("\n[步骤1] 夏娃计划已跳过。")

    # ---------- 2. 二次筛查 ----------
    if RUN_SECONDARY:
        print("\n[步骤2] 二次筛查：AI 深度打分")
        if check_file_exists(EVE_OUTPUT, "夏娃计划结果"):
            run_secondary(EVE_OUTPUT, SECONDARY_OUTPUT)
        else:
            print("❌ 缺少夏娃计划结果，跳过二次筛查。")
    else:
        print("\n[步骤2] 二次筛查已跳过。")

    # ---------- 3. 信息密度计算 ----------
    if RUN_DENSITY:
        print("\n[步骤3] 信息密度计算与债务优化")
        if check_file_exists(SECONDARY_OUTPUT, "二次筛查结果"):
            run_density(SECONDARY_OUTPUT, DENSITY_OUTPUT)
        else:
            print("❌ 缺少二次筛查结果，跳过信息密度计算。")
    else:
        print("\n[步骤3] 信息密度计算已跳过。")

    # ---------- 4. 最终筛选 ----------
    if RUN_FINAL:
        print("\n[步骤4] 最终筛选：基于优化债务选出最佳答案")
        if check_file_exists(DENSITY_OUTPUT, "信息密度计算结果"):
            final_selection()
        else:
            print("❌ 缺少信息密度计算结果，跳过最终筛选。")
    else:
        print("\n[步骤4] 最终筛选已跳过。")

    print("\n" + "=" * 50)
    print("POTR 流程执行完毕！")
    print("最终结果文件：", FINAL_OUTPUT)
    print("=" * 50)

if __name__ == "__main__":
    run_pipeline()
