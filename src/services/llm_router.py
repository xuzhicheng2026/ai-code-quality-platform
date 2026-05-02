"""
LLM 智能路由服务 - 根据任务类型智能选择最合适的模型
"""

import anthropic
import openai
from typing import Dict, List, Optional
from loguru import logger
from config import config


class ModelInfo:
    """模型信息"""

    CODE_REVIEW = ["claude", "gpt4"]
    SECURITY_ANALYSIS = ["claude", "gpt4"]
    PERFORMANCE_OPT = ["gpt4", "claude"]
    SIMPLE_ANALYSIS = ["deepseek", "claude"]
    CODE_COMPLETION = ["deepseek", "gpt4"]


class LLMRouter:
    """LLM 智能路由"""

    def __init__(self):
        self.clients = {}
        self._init_clients()

    def _init_clients(self):
        """初始化各模型客户端"""
        if config.ANTHROPIC_API_KEY:
            self.clients["anthropic"] = anthropic.Anthropic(
                api_key=config.ANTHROPIC_API_KEY
            )
            logger.info("Anthropic client initialized")

        if config.OPENAI_API_KEY:
            self.clients["openai"] = openai.OpenAI(
                api_key=config.OPENAI_API_KEY
            )
            logger.info("OpenAI client initialized")

    def route(self, task_type: str) -> str:
        """根据任务类型路由到合适的模型"""
        task_type_lower = task_type.lower()

        if "review" in task_type_lower or "code" in task_type_lower:
            return "claude"
        elif "security" in task_type_lower or "safe" in task_type_lower:
            return "claude"
        elif "performance" in task_type_lower or "optimize" in task_type_lower:
            return "gpt4"
        elif "simple" in task_type_lower or "basic" in task_type_lower:
            return "deepseek"
        else:
            return "claude"

    async def chat(
        self,
        messages: List[Dict],
        model: str = "claude",
        temperature: float = 0.3,
        max_tokens: int = 4096,
    ) -> str:
        """调用指定模型进行对话"""
        try:
            model_config = config.MODEL_CONFIGS.get(model, config.MODEL_CONFIGS["claude"])
            provider = model_config["provider"]

            if provider == "anthropic":
                return await self._chat_anthropic(messages, model_config, max_tokens)
            elif provider == "openai":
                return await self._chat_openai(messages, model_config, max_tokens)
            else:
                logger.error(f"Unknown provider: {provider}")
                return "Error: Unknown provider"

        except Exception as e:
            logger.error(f"LLM chat error: {e}")
            return f"Error: {str(e)}"

    async def _chat_anthropic(
        self, messages: List[Dict], model_config: Dict, max_tokens: int
    ) -> str:
        """调用 Anthropic 模型"""
        if "anthropic" not in self.clients:
            return "Error: Anthropic client not initialized"

        client = self.clients["anthropic"]
        response = client.messages.create(
            model=model_config["model"],
            max_tokens=max_tokens,
            messages=messages,
            temperature=model_config.get("temperature", 0.3),
        )
        return response.content[0].text

    async def _chat_openai(
        self, messages: List[Dict], model_config: Dict, max_tokens: int
    ) -> str:
        """调用 OpenAI 模型"""
        if "openai" not in self.clients:
            return "Error: OpenAI client not initialized"

        client = self.clients["openai"]
        response = client.chat.completions.create(
            model=model_config["model"],
            messages=messages,
            temperature=model_config.get("temperature", 0.3),
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content


# 全局路由实例
llm_router = LLMRouter()
