import requests
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import time
import random

# ========== 配置参数 ==========
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "deepseek-r1:8b"   # 可替换为 qwen2.5:7b-q4_0 以加快速度（或者你自己的模型）
TIMEOUT = 60
LENGTH_WEIGHT = 0.3            # 债务函数中长度惩罚的权重
DENSITY_BASE = 100              # 信息密度计算基数（本脚本未使用，但保留）
ORIGINAL_WEIGHT = 0.7           # 优化债务权重（本脚本未使用，但保留）

# ========== 初始化模型 ==========
encoder = SentenceTransformer('paraphrase-MiniLM-L3-v2')

# ========== 提问模板 ==========
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

# ========== 核心函数 ==========
def generate_real_answer(prompt):
    """调用真实模型生成答案"""
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
    """债务函数：值越小越好"""
    if not answer:
        return 999.0
    # 长度惩罚（假设200字为基准）
    length_penalty = len(answer) / 200.0
    # 语义相似度惩罚
    q_emb = encoder.encode(question)
    a_emb = encoder.encode(answer)
    sim = np.dot(q_emb, a_emb) / (np.linalg.norm(q_emb) * np.linalg.norm(a_emb))
    relevance = (sim + 1) / 2   # 映射到0-1
    relevance_debt = 1 - relevance
    # 加权合并
    debt = LENGTH_WEIGHT * length_penalty + (1 - LENGTH_WEIGHT) * relevance_debt
    return float(debt)

def generate_candidates(question, num_candidates=5):
    """为单个问题生成多个候选答案，并计算债务"""
    candidates = []
    for i in range(num_candidates):
        prompt = ANGLE_TEMPLATES[i % len(ANGLE_TEMPLATES)].format(question)
        answer = generate_real_answer(prompt)
        time.sleep(0.3)   # 避免请求过快
        debt = calculate_debt(question, answer)
        candidates.append({
            "prompt": prompt,
            "answer": answer,
            "debt": debt
        })
    return candidates

def run_eve(questions, output_file="phase1_results.json"):
    """对问题列表执行夏娃计划，保存结果到文件"""
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
            # 临时保存
            with open("phase1_partial.json", "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"夏娃计划完成，结果已保存到 {output_file}")
    return results

if __name__ == "__main__":
    # 测试用法
    with open("questions.txt", "r", encoding="utf-8") as f:
        qlist = [line.strip() for line in f if line.strip()]
    run_eve(qlist[:5])   # 先试5个
