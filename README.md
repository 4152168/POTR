# POTR (Predictive & Optimized Thinking Robot)
## 预测优化思维机器人 —— 让 AI 学会自我思考的工具
---

## English Introduction / 英语介绍

**POTR is a lightweight tool that enables AI to self-reflect and optimize its own outputs.**
By letting AI evaluate the depth of its answers and combining it with an information density metric, POTR automatically selects responses that are both concise and insightful.

POTR 是一个轻量级工具，使人工智能能够自我反思并优化自己的输出。通过让 AI 评估答案深度并结合信息密度指标，POTR 会自动选择既简洁又有洞察力的最佳答案。

---

## 功能 Features

### 自我评估（Self-Evaluation）

让 AI 对自己生成的多个答案进行“深度”打分（1–5 分）

### 智能筛选（Smart Selection）

综合答案长度与 AI 自评分，自动选出“既简洁又有料”的最佳答案

### 拒绝废话（Anti-Fluff Mechanism）

惩罚冗长空洞的回答，保留真正高信息密度的输出

---

## 快速开始 Quick Start

### 1. 安装依赖

```bash
pip install requests sentence-transformers numpy
```

### 2. 下载模型（以 Ollama 为例）

```bash
ollama pull deepseek-r1:8b   # 或替换为其他模型
```

### 3. 运行示例

```python
from potr import POTR

bot = POTR(model="deepseek-r1:8b")
question = "什么是意识？"#（这个地方你可以试着先列10个，然后如果是你要用的你模型跑更多的可以自定义（大方向都是差不多的））

best_answer = bot.think(question)
print(best_answer)
```

---

## 项目结构 Project Structure

```
POTR/
├── core/
│   ├── eve_plan.py           # 基础债务函数筛选（夏娃计划）
│   ├── secondary_screen.py   # 二次筛查（AI深度打分）
│   ├── info_density.py       # 信息密度计算与优化债务
│   └── final_screen.py       # 最终筛选器
│   └── pipeline.py           # 完整流程整合
├── analyze_default.py        # 统计分析脚本
├── config.py                 # 配置文件（模型名、超时等）
├── example_data.json         # 示例数据（106条测试问题）
├── README.md                 # 使用说明
└── LICENSE                   # GPL v3 协议
```

---

## 数据验证 Data Validation

基于 106 个哲学 / 科学问题的真实测试，POTR 成功区分：

* 冗长空洞的回答 → 惩罚
* 简洁准确的回答 → 保留
* 长但有深度的回答 → 因 AI 自评分高而保留

（详见 `example_data.json`）

---

## 许可证 License

GPL v3 – 使用者必须开源，并保留原作者信息。

---

## 作者 Author

郭维嘉 —— 中国独立开发者
