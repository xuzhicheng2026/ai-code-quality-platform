"""
代码分析服务 - 整合多个 Agent 提供全面的代码分析
"""

from typing import Dict, List, Optional
from loguru import logger
from src.agents.code_review_agent import CodeReviewAgent
from src.agents.security_agent import SecurityAgent
from src.agents.performance_agent import PerformanceAgent


class CodeAnalyzer:
    """代码分析器 - 协调多个 Agent 提供全面的代码分析"""

    def __init__(self):
        self.code_review_agent = CodeReviewAgent()
        self.security_agent = SecurityAgent()
        self.performance_agent = PerformanceAgent()
        logger.info("CodeAnalyzer initialized with 3 agents")

    async def analyze_code(
        self,
        code: str,
        language: str = "python",
        analysis_types: Optional[List[str]] = None,
    ) -> Dict:
        """
        综合分析代码

        Args:
            code: 要分析的代码
            language: 编程语言
            analysis_types: 要执行的分析类型列表，默认包含所有类型

        Returns:
            综合分析结果
        """
        if analysis_types is None:
            analysis_types = ["review", "security", "performance"]

        results = {
            "language": language,
            "code_length": len(code),
            "analysis_results": {},
        }

        # 代码审查
        if "review" in analysis_types:
            logger.info("Running code review...")
            results["analysis_results"]["code_review"] = await self.code_review_agent.analyze(
                code, language
            )

        # 安全检测
        if "security" in analysis_types:
            logger.info("Running security scan...")
            results["analysis_results"]["security"] = await self.security_agent.analyze(
                code, language
            )

        # 性能分析
        if "performance" in analysis_types:
            logger.info("Running performance analysis...")
            results["analysis_results"]["performance"] = await self.performance_agent.analyze(
                code, language
            )

        # 生成汇总报告
        results["summary"] = self._generate_summary(results["analysis_results"])

        return results

    def _generate_summary(self, analysis_results: Dict) -> Dict:
        """生成分析汇总"""
        summary = {
            "total_issues": 0,
            "critical_issues": 0,
            "high_issues": 0,
            "medium_issues": 0,
            "low_issues": 0,
            "recommendations": [],
        }

        # 统计代码审查问题
        if "code_review" in analysis_results:
            for issue in analysis_results["code_review"].get("issues", []):
                summary["total_issues"] += 1
                severity = issue.get("severity", "low")
                if severity == "high":
                    summary["high_issues"] += 1
                elif severity == "medium":
                    summary["medium_issues"] += 1
                else:
                    summary["low_issues"] += 1

        # 统计安全问题
        if "security" in analysis_results:
            for vuln in analysis_results["security"].get("vulnerabilities", []):
                summary["total_issues"] += 1
                level = vuln.get("level", "low")
                if level == "critical":
                    summary["critical_issues"] += 1
                elif level == "high":
                    summary["high_issues"] += 1
                else:
                    summary["low_issues"] += 1

        # 收集建议
        if "performance" in analysis_results:
            for rec in analysis_results["performance"].get("recommendations", []):
                summary["recommendations"].append(rec.get("suggestion", ""))

        return summary

    async def analyze_batch(self, files: List[Dict[str, str]]) -> List[Dict]:
        """批量分析多个文件"""
        results = []
        for file in files:
            result = await self.analyze_code(
                code=file.get("content", ""),
                language=file.get("language", "python"),
            )
            result["file"] = file.get("path", "unknown")
            results.append(result)
        return results
