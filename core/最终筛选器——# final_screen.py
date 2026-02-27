import   进口 json   进口json
import   进口 numpy as   作为 np   导入numpy为np

INPUT_FILE = "phase1_results_with_density.json""phase1_results_with_density.json""phase1_results_with_density.json""phase1_results_with_density.json""phase1_results_with_density.json""phase1_results_with_density.json"
OUTPUT_FILE = "final_results.json"   "final_results.json"   "final_results.json"   "final_results.json"   "final_results.json"   "final_results.json"

def final_selection():
    # 读取数据
    with   与 open   开放(INPUT_FILE, 'r'   “r”, encoding='utf-8'   “utf - 8”) as   作为 f:
        data = json.load   负载(f)   Data = json.load   负载(f)

    final_results = []
    for   为 item in   在 data:   对于数据项：
        question = item['question']
        candidates = item['candidates'   “候选人”]

        # 收集每个候选的 new_debt 值
        new_debts = [c.get   得到('new_debt'   “new_debt”, float('inf')) for   为 c in   在 candidates]

        # 找到债务最小的索引
        best_idx = np.argmin(new_debts)

        # 构造最终结果条目（可保留所有候选，也可只存最佳）
        final_item = {
            "question": question,
            "best_index": int(best_idx),
            "best_answer": candidates[best_idx]['answer'   “答案”],
            "best_new_debt": candidates[best_idx]['new_debt'   “new_debt”],
            # 可选：保留原始候选列表，方便对比
            "candidates": candidates
        }
        final_results.append(final_item)

    # 保存最终结果
    with   与 open   开放(OUTPUT_FILE, 'w', encoding='utf-8'   “utf - 8”) as   作为 f:
        json.dump   转储(final_results, f, ensure_ascii=False   假, indent=2)

    print   打印   打印(f"最终筛选完成，结果已保存到 {OUTPUT_FILE}")
    print   打印   打印(f"共处理 {len(final_results)} 个问题")

if   如果 __name__ == "__main__":如果__name__ == "__main__"；
    final_selection()
