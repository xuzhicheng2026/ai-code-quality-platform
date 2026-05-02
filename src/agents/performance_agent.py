"""
性能优化 Agent - 提供代码性能改进建议
"""

from typing import Dict, List
from loguru import logger
from src.services.llm_router import llm_router


class PerformanceAgent:
    """性能优化 Agent"""

    SYSTEM_PROMPT = """你是一位性能优化专家，擅长发现代码中的性能瓶颈并提供优化建议。
请分析提供的代码，识别：
1. 算法复杂度问题（O(n²) 或更差的算法）
2. 不必要的循环或重复计算
3. 内存使用问题
4. I/O 瓶颈
5. 数据库查询优化建议
6. 缓存策略建议
7. 并发处理建议

请以结构化的 JSON 格式返回分析结果。"""

    PERFORMANCE_TIPS = {
        "python": [
            "使用列表推导式代替普通循环",
            "使用生成器处理大数据集",
            "避免在循环中重复创建对象",
            "使用局部变量缓存属性访问",
            "考虑使用 collections 模块优化数据结构",
        ],
        "javascript": [
            "避免在循环中操作 DOM",
            "使用事件委托代替多个事件监听器",
            "考虑使用 Web Workers 处理耗时任务",
            "使用虚拟滚动处理长列表",
        ],
    }

    def __init__(self):
        self.name = "PerformanceAgent"
        logger.info(f"{self.name} initialized")

    async def analyze(self, code: str, language: str = "python") -> Dict:
        """分析代码性能"""
        logger.info(f"Analyzing performance in {language} code")

        # 获取语言特定的优化建议
        tips = self.PERFORMANCE_TIPS.get(language.lower(), self.PERFORMANCE_TIPS["python"])

        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"请分析以下 {language} 代码的性能问题并提供优化建议：\n\n```{language}\n{code}\n```",
            },
        ]

        model = llm_router.route("performance_optimization")
        response = await llm_router.chat(messages, model=model)

        return {
            "agent": self.name,
            "model_used": model,
            "language": language,
            "analysis": response,
            "recommendations": self._extract_recommendations(response),
            "general_tips": tips,
        }

    def _extract_recommendations(self, response: str) -> List[Dict]:
        """提取优化建议"""
        recommendations = []

        keywords = {
            "algorithm": ["算法", "complexity", "O(n", "优化算法"],
            "loop": ["循环", "loop", "迭代", "优化"],
            "memory": ["内存", "memory", "垃圾回收", "清理"],
            "cache": ["缓存", "cache", "提升性能"],
            "async": ["异步", "async", "await", "并发"],
        }

        for category, words in keywords.items():
            if any(word in response.lower() for word in words):
                recommendations.append(
                    {
                        "category": category,
                        "suggestion": f"考虑优化{category}相关代码",
                    }
                )

        return recommendations if recommendations else [{"category": "general", "suggestion": "代码性能整体良好"}]

    async def suggest_alternatives(self, code: str, language: str = "python") -> str:
        """提供替代实现方案"""
        messages = [
            {"role": "system", "content": "请提供更优的代码实现方案。"},
            {
                "role": "user",
                "content": f"请优化以下 {language} 代码并提供替代实现：\n\n```{language}\n{code}\n```",
            },
        ]

        model = llm_router.route("performance_optimization")
        return await llm_router.chat(messages, model=model)
