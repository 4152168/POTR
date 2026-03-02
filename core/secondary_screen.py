import json
import requests
import time
import re
from config import OLLAMA_URL, MODEL_NAME, TIMEOUT

def batch_score(question, answers):
    prompt = f"""请为下面5个答案的“内容深度”打分（1-5分，5分最高）。
只输出5个数字，用空格隔开。

问题：{question}

1.{answers[0]}
2.{answers[1]}
3.{answers[2]}
4.{answers[3]}
5.{answers[4]}

分数："""
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "top_p": 0.9,
            "max_tokens": 10
        }
    }
    try:
        print(f"正在请求 Ollama: {MODEL_NAME}")
        resp = requests.post(OLLAMA_URL, json=payload, timeout=TIMEOUT)
        resp.raise_for_status()
        result = resp.json()
        text = result.get('response', '').strip()
        print(f"原始响应: {text}")
        nums = re.findall(r'\d+', text)
        if len(nums) >= 5:
            return [int(n) for n in nums[:5]], 'ai'
        else:
            print(f"返回数字不足5个，实际得到: {text}")
            return None, None
    except requests.exceptions.Timeout:
        print(f"请求超时（{TIMEOUT}秒），请考虑增加 TIMEOUT 或使用更快的模型")
        return None, None
    except Exception as e:
        print(f"批量请求失败: {type(e).__name__}: {e}")
        return None, None

def run_secondary(input_file, output_file):
    print(f"开始读取文件: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"成功读取 {len(data)} 个问题")

    for idx, item in enumerate(data):
        question = item['question']
        answers = [c['answer'] for c in item['candidates']]
        print(f"处理第 {idx+1}/{len(data)} 个问题: {question[:30]}...")
        scores, source = batch_score(question, answers)
        if scores and len(scores) == 5:
            for i, cand in enumerate(item['candidates']):
                cand['ai_depth_score'] = scores[i]
                cand['score_source'] = source
            print(f"得分: {scores}")
        else:
            print(f"问题 {question[:30]} 打分失败，使用默认3分")
            for cand in item['candidates']:
                cand['ai_depth_score'] = 3
                cand['score_source'] = 'default'
        time.sleep(1)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"二次筛查完成，结果已保存到 {output_file}")

if __name__ == "__main__":
    run_secondary("phase1_results.json", "phase1_results_with_ai_scores.json")
