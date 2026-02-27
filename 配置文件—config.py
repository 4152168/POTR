# ================== POTR 项目配置文件 ==================
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "deepseek-r1:8b"           # 用于二次筛查的模型（可换 qwen2.5:7b-q4_0）
TIMEOUT = 60                            # 请求超时时间（秒）
TEMPERATURE = 0.2                       # 打分时温度（越低越稳定）

# 债务函数权重（夏娃计划）
LENGTH_WEIGHT = 0.3                      # 长度惩罚权重
RELEVANCE_WEIGHT = 0.7                   # 语义相关性权重

# 信息密度计算参数
DENSITY_BASE = 100                       # 密度公式中的缩放因子
NEW_DEBT_ORIG_WEIGHT = 0.7                # 新债务中原债务权重
NEW_DEBT_DENSITY_WEIGHT = 0.3              # 新债务中密度权重
# ======================================================
