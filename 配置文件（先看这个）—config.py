# POTR 项目配置文件

# Ollama 服务地址
OLLAMA_URL = "http://localhost:11434/api/generate"

# 默认模型（根据你实际下载的模型名修改）
MODEL_NAME = "deepseek-r1:8b"   # 可换成 qwen2.5:7b-q4_0 等

# 请求超时时间（秒）
TIMEOUT = 120

# 夏娃计划中长度惩罚的权重（相关性惩罚权重为 1 - LENGTH_WEIGHT）
LENGTH_WEIGHT = 0.2

# 信息密度计算基数（数值越大密度值越大）
DENSITY_BASE = 100

# 优化债务中原始债务的权重（信息密度倒数权重为 1 - ORIGINAL_WEIGHT）
ORIGINAL_WEIGHT = 0.15
