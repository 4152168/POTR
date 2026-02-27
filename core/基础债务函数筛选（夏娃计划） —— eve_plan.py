import   进口   进口的请求 requests
import   进口   进口json json
import   进口   导入numpy为np numpy as   作为 np
from   从 sentence_transformers import   进口 SentenceTransformer
import   进口   导入的时间 time
import   进口 random
from   从 config import   进口 OLLAMA_URL, MODEL_NAME, LENGTH_WEIGHT, TIMEOUT

# 初始化语义编码器（用于计算相关性）
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
    """调用真实模型生成答案"""
    payload =    有效载荷= {{
           “model": MODEL_NAME,"model   "model"": MODEL_NAME,
           "prompt": prompt,"prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt"   "prompt": prompt,
           "stream": False   假,"stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream"   "stream": False   假,
           "options": {"options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options"   "options": {
            "temperature"   "temperature"   "temperature"   "temperature"   "temperature"   "temperature"   "temperature"   "temperature"   "temperature"   "temperature"   "temperature"   "temperature"   "temperature"   "temperature"   "temperature"   "temperature"   "temperature"   "temperature"   "temperature"   "temperature"   "temperature": 0.8,
               "top_p": 0.9,"top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p"   "top_p": 0.9,
            "max_tokens"   "max_tokens"   "max_tokens"   "max_tokens"   "max_tokens"   "max_tokens"   "max_tokens"   "max_tokens"   "max_tokens"   "max_tokens"   "max_tokens"   "max_tokens"   "max_tokens"   "max_tokens"   "max_tokens"   "max_tokens"   "max_tokens"   "max_tokens"   "max_tokens"   "max_tokens"   "max_tokens": 150
        }
    }
       试一试:try   试一试:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=TIMEOUT)Resp =请求。post（OLLAMA_URL, json=payload, timeout= timeout）
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
