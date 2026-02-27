# POTR (Predictive & Optimized Thinking Robot)
## 预测优化思维机器人 —— 让AI学会自我思考的工具

POTR 是一个轻量级工具，它让 AI 对自己的输出进行反思和优化。通过让 AI 自我评估答案的深度，并结合信息密度指标，POTR 能自动筛选出既简洁又有深度的最佳回答。
**English Introduction**  
POTR is a lightweight tool that enables AI to self-reflect and optimize its own outputs. By letting AI evaluate the depth of its answers and combining it with an information density metric, POTR automatically selects responses that are both concise and insightful.

---

## 它能做什么

- **自我评估**：让 AI 对自己生成的多个答案进行“深度”打分（1–5分）
- **智能筛选**：综合答案长度和 AI 自评分，自动选出“既简洁又有料”的最佳答案
- **拒绝废话**：惩罚冗长空洞的回答，保留真正有价值的信息

---

## 快速开始

### 1. 安装依赖
pip install requests sentence-transformers numpy

###2. 下载模型（以 Ollama 为例）
bash
ollama pull deepseek-r1:8b   # 或替换为其他模型

###3. 运行示例
from potr import POTR
bot = POTR(model="deepseek-r1:8b")
question = "什么是意识？"
best_answer = bot.think(question)
print(best_answer)


文件名	作用
eve_plan.py	→基础债务函数筛选（夏娃计划）
secondary_screen.py	→二次筛查：让 AI 给答案打深度分
info_density.py	→信息密度计算与优化债务
pipeline.py	→完整流程整合
analyze_default.py	→统计脚本，分析默认3分的分布
config.py	→配置文件（模型名、超时等）
example_data.json	→示例数据（10条）
README.md	→本文件
LICENSE	GPL →协议

数据验证
基于 106 个哲学/科学问题的真实测试，POTR 成功区分了：
冗长空洞的回答 → 惩罚
简洁准确的回答 → 保留
长但有深度的回答 → 因 AI 自评分高而保留
（具体数据见 example_data.json）

许可证
GPL v3 – 使用者必须开源，必须保留原作者信息。
作者：郭维嘉 —— 中国独立开发者
