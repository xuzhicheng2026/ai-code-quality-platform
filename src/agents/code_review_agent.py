"""
代码审查 Agent - 自动化代码审查和质量分析
"""

from typing import Dict, List
from loguru import logger
from src.services.llm_router import llm_router


class CodeReviewAgent:
    """代码审查 Agent"""

    SYSTEM_PROMPT = """你是一位资深的代码审查专家，擅长发现代码中的问题并提供改进建议。
请分析提供的代码，识别：
1. 代码规范问题
2. 潜在的 Bug
3. 代码风格问题
4. 可优化的地方
5. 最佳实践建议

请以结构化的 JSON 格式返回分析结果。"""

    def __init__(self):
        self.name = "CodeReviewAgent"
        logger.info(f"{self.name} initialized")

    async def analyze(self, code: str, language: str = "python") -> Dict:
        """分析代码质量"""
        logger.info(f"Analyzing code in {language}")

        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"请审查以下 {language} 代码：\n\n```{language}\n{code}\n```",
            },
        ]

        model = llm_router.route("code_review")
        response = await llm_router.chat(messages, model=model)

        return {
            "agent": self.name,
            "model_used": model,
            "language": language,
            "issues": self._parse_response(response),
            "raw_response": response,
        }

    def _parse_response(self, response: str) -> List[Dict]:
        """解析响应结果"""
        issues = []

        # 简单解析，提取关键问题
        if "bug" in response.lower() or "error" in response.lower():
            issues.append({"severity": "high", "type": "potential_bug", "suggestion": "检查潜在错误"})

        if "security" in response.lower() or "safe" in response.lower():
            issues.append({"severity": "medium", "type": "security", "suggestion": "注意安全相关问题"})

        if "performance" in response.lower() or "optimize" in response.lower():
            issues.append({"severity": "low", "type": "performance", "suggestion": "考虑性能优化"})

        return issues if issues else [{"severity": "info", "type": "convention", "suggestion": "代码整体良好"}]

    async def batch_analyze(self, files: List[Dict[str, str]]) -> List[Dict]:
        """批量分析多个文件"""
        results = []
        for file in files:
            result = await self.analyze(
                code=file.get("content", ""),
                language=file.get("language", "python"),
            )
            result["file"] = file.get("path", "unknown")
            results.append(result)
        return results
