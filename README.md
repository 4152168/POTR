# POTR（Predictive & Optimized Thinking Robot）# POTR（预测优化思考机器人）POTR（预测优化思维机器人）
——让AI学会自我思考的工具。
# POTR
POTR 是一个让 AI 学会自我反思和优化的轻量级工具。它通过让 AI 对自己的输出进行二次评估，并引入“信息密度”指标，从而在保持回答简洁的同时，保留有深度的内容。
POTR (Predictive &amp;   &雏形;   &雏形;amp; Optimized Thinking Robot) &amp;   &雏形;   &雏形;ndash; a lightweight tool that enables AI to self-assess its responses and select concise, insightful answers using self-scoring and information density.POTR (Predictive & Optimized Thinking Robot) POTR （Predictive &;amp;;;;）&；这是一种轻量级的工具，使人工智能能够自我评估其回答，并使用自我评分和信息密度选择简洁、有洞察力的答案。POTR（预测优化思维机器人）

## 它能做什么
- **自我评估**：让 AI 对自己生成的多个答案进行“深度”打分（1-5分）
- **智能筛选**：综合答案长度和 AI 自评分，自动选出“既简洁又有料”的最佳答案
- **拒绝废话**：惩罚冗长空洞的回答，保留真正有价值的信息

## 开始
### 安装依赖
pip install requests sentence-transformers numpyPIP安装请求句子-变压器numpy

#下载模型（以 Ollama 为例）
bash
ollama pull qwen2.5:7b-q4_0奥拉玛拉qwen2.5:7b-q4_0

#运行示例
from potr import POTR   从波特导入波特

bot = POTR(model="qwen2.5:7b-q4_0")bot = POTR（model="qwen2.5:7b-q4_0"）bot = POTR(model="qwen2.5:7b-q4_0")bot = POTR（model="qwen2.5:7b-q4_0"）
question = "什么是意识？"   question = "什么是意识？"question = "什么是意识？"   question = "什么是意识？"
best_answer = bot.think(question)Best_answer = bot.think（问题）Best_answer = bot。think（问题）Best_answer = bot_think（问题）
print(best_answer)   打印(best_answer)打印（best_answer） （best_answer）

#文件说明
core.py – 核心筛选逻辑（长度 + 语义相似度）
self_assess.py – AI 自我评估模块（让 AI 给自己的答案打分）self_assess.py – AI 自我评估模块（让 AI 给自己的答案打分）self_assess.py – AI 自我评估模块（让 AI 给自己的答案打分）self_assess.py – AI 自我评估模块（让 AI 给自己的答案打分）
density.py – 信息密度计算   density.py – 信息密度计算density.py – 信息密度计算   density.py – 信息密度计算
pipeline.py – 把上面三个串起来的完整流程

#数据验证
基于 106 个哲学/科学问题的真实测试，POTR 成功区分了：
冗长空洞的回答 → 惩罚
简洁准确的回答 → 保留
长但有深度的回答 → 因 AI 自评分高而保留
（具体数据见 example_data.json）

许可证
GPL v3 – 用了必须开源，必须保留作者信息。
作者：郭维嘉——来自中国的一名独立开发者。
