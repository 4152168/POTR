# config.py
# POTR 项目配置文件

# Ollama 服务地址
OLLAMA_URL = "http://localhost:11434/api/generate"OLLAMA_URL = "http://localhost:11434/api/generate""http://localhost:11434/api/generate""http://localhost:11434/api/generate""http://localhost:11434/api/generate""http://localhost:11434/api/generate""http://localhost:11434/api/generate""http://localhost:11434/api/generate"

# 默认使用的模型（可根据需要修改）
MODEL_NAME = "deepseek-r1:8b"   # 推荐替换为 qwen2.5:7b-q4_0 以加快速度

# 超时设置（秒）
TIMEOUT = 60

# 债务函数权重（长度惩罚占比，相关性惩罚占比为 1-LENGTH_WEIGHT）
LENGTH_WEIGHT = 0.3

# 信息密度计算基数
DENSITY_BASE = 100

# 优化债务的权重（原始债务权重，信息密度倒数权重为 1-ORIGINAL_WEIGHT）
ORIGINAL_WEIGHT = 0.7
