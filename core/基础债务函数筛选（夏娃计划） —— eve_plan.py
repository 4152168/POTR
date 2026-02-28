import requests
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import time
from config import OLLAMA_URL, MODEL_NAME, LENGTH_WEIGHT, TIMEOUT

encoder = SentenceTransformer('paraphrase-MiniLM-L3-v2')

# 提问角度模板（保证答案多样性）
ANGLE_TEMPLATES = [
    "{} 请用一句话回答。",
    "{} 请从哲学角度解释。",
    "{} 请用比喻说明。",
    "{} 请给出具体例子。",
    "{} 如果反过来想会怎样？",
    "用最简单的话说：{}",
    "详细解释一下：{}",
    "你觉得{}和宇宙常数κ有什么关系？",
]

def generate_real_answer(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.8,
            "top_p": 0.9,
            "max_tokens": 150
        }
    }
    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=TIMEOUT)
        return resp.json()['response'].strip()
    except Exception as e:
        print(f"生成答案失败: {e}")
        return ""

def calculate_debt(question, answer):
    if not answer:
        return 999.0
    length_penalty = len(answer) / 200.0
    q_emb = encoder.encode(question)
    a_emb = encoder.encode(answer)
    sim = np.dot(q_emb, a_emb) / (np.linalg.norm(q_emb) * np.linalg.norm(a_emb))
    relevance = (sim + 1) / 2
    relevance_debt = 1 - relevance
    debt = LENGTH_WEIGHT * length_penalty + (1 - LENGTH_WEIGHT) * relevance_debt
    return float(debt)

def generate_candidates(question, num_candidates=5):
    candidates = []
    for i in range(num_candidates):
        prompt = ANGLE_TEMPLATES[i % len(ANGLE_TEMPLATES)].format(question)
        answer = generate_real_answer(prompt)
        time.sleep(0.3)
        debt = calculate_debt(question, answer)
        candidates.append({
            "prompt": prompt,
            "answer": answer,
            "debt": debt
        })
    return candidates

def run_eve(questions, output_file="phase1_results.json"):
    """供 pipeline 调用的主函数"""
    results = []
    for idx, q in enumerate(questions):
        print(f"处理第 {idx+1}/{len(questions)} 个问题: {q[:30]}...")
        candidates = generate_candidates(q)
        best_idx = np.argmin([c["debt"] for c in candidates])
        results.append({
            "question": q,
            "candidates": candidates,
            "best_index": int(best_idx),
            "best_answer": candidates[best_idx]["answer"]
        })
        if (idx + 1) % 10 == 0:
            with open("phase1_partial.json", "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"夏娃计划完成，结果已保存到 {output_file}")
    return results

if __name__ == "__main__":
    # 测试用
    with open("questions.txt", "r", encoding="utf-8") as f:
        qlist = [line.strip() for line in f if line.strip()]
    run_eve(qlist[:2])
