import json
import numpy as np
from collections import defaultdict

INPUT_FILE = "phase1_results_with_ai_scores.json"

def analyze():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total_answers = 0
    default_count = 0
    default_by_question = defaultdict(int)
    lengths_default = []
    lengths_other = []

    for item in data:
        for cand in item['candidates']:
            total_answers += 1
            source = cand.get('score_source', 'unknown')
            if source == 'default':
                default_count += 1
                default_by_question[item['question']] += 1
                lengths_default.append(len(cand['answer']))
            else:
                lengths_other.append(len(cand['answer']))

    default_ratio = default_count / total_answers * 100
    print(f"总答案数: {total_answers}")
    print(f"默认3分数量: {default_count}")
    print(f"默认3分占比: {default_ratio:.2f}%")

    if default_by_question:
        sorted_q = sorted(default_by_question.items(), key=lambda x: x[1], reverse=True)
        print("\n默认分最多的5个问题:")
        for q, cnt in sorted_q[:5]:
            print(f"  {q[:50]}... : {cnt}个")

    print(f"\n默认答案平均长度: {np.mean(lengths_default) if lengths_default else 0:.1f}")
    print(f"正常答案平均长度: {np.mean(lengths_other) if lengths_other else 0:.1f}")

    if default_ratio <= 10:
        print("\n✅ 默认比例 ≤10%，可接受，可进入下一步。")
    else:
        print("\n❌ 默认比例 >10%，建议优化模型或超时设置。")

if __name__ == "__main__":
    analyze()
