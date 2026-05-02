"""
AI Code Quality Platform - 配置管理
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """应用配置"""

    # API 配置
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    # LLM API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")

    # 模型配置
    MODEL_CONFIGS = {
        "claude": {
            "provider": "anthropic",
            "model": "claude-3-sonnet-20240229",
            "temperature": 0.3,
            "max_tokens": 4096,
        },
        "gpt4": {
            "provider": "openai",
            "model": "gpt-4-turbo-preview",
            "temperature": 0.3,
            "max_tokens": 4096,
        },
        "deepseek": {
            "provider": "deepseek",
            "model": "deepseek-coder",
            "temperature": 0.3,
            "max_tokens": 4096,
        },
    }

    # 路由策略
    ROUTING_STRATEGY = os.getenv("ROUTING_STRATEGY", "intelligent")
    MAX_RETRIES = 3
    TIMEOUT = 60

    # 日志配置
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")


config = Config()
