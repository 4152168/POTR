import json
import numpy as np

INPUT_FILE = "phase1_results_with_density.json"
OUTPUT_FILE = "final_results.json"

def final_selection():
    # 读取数据
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    final_results = []
    for item in data:
        question = item['question']
        candidates = item['candidates']

        # 收集每个候选的 new_debt 值
        new_debts = [c.get('new_debt', float('inf')) for c in candidates]

        # 找到债务最小的索引
        best_idx = np.argmin(new_debts)

        # 构造最终结果条目（可保留所有候选，也可只存最佳）
        final_item = {
            "question": question,
            "best_index": int(best_idx),
            "best_answer": candidates[best_idx]['answer'],
            "best_new_debt": candidates[best_idx]['new_debt'],
            # 可选：保留原始候选列表，方便对比
            "candidates": candidates
        }
        final_results.append(final_item)

    # 保存最终结果
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_results, f, ensure_ascii=False, indent=2)

    print(f"最终筛选完成，结果已保存到 {OUTPUT_FILE}")
    print(f"共处理 {len(final_results)} 个问题")

if __name__ == "__main__":
    final_selection()
