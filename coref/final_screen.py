import json
import numpy as np

def run_final(input_file, output_file):
    """从输入文件读取数据，用 new_debt 选出最佳答案，保存到输出文件"""
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    final_results = []
    for item in data:
        question = item['question']
        candidates = item['candidates']
        new_debts = [c.get('new_debt', float('inf')) for c in candidates]
        best_idx = np.argmin(new_debts)
        final_item = {
            "question": question,
            "best_index": int(best_idx),
            "best_answer": candidates[best_idx]['answer'],
            "best_new_debt": candidates[best_idx]['new_debt'],
            "candidates": candidates   # 保留全部候选，方便对比
        }
        final_results.append(final_item)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_results, f, ensure_ascii=False, indent=2)
    print(f"最终筛选完成，结果已保存到 {output_file}")
    print(f"共处理 {len(final_results)} 个问题")

if __name__ == "__main__":
    run_final("phase1_results_with_density.json", "final_results.json")
