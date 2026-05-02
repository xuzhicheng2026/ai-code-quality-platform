"""
安全检测 Agent - 识别代码中的安全漏洞和风险
"""

from typing import Dict, List
from loguru import logger
from src.services.llm_router import llm_router


class SecurityAgent:
    """安全检测 Agent"""

    # 常见安全漏洞模式
    VULNERABILITY_PATTERNS = [
        ("SQL注入", ["execute(", "cursor.execute(", "raw(", ".format(", "f\"SELECT"]),
        ("XSS攻击", ["innerHTML", "document.write", "eval(", "dangerouslySetInnerHTML"]),
        ("命令注入", ["os.system(", "subprocess(", "exec(", "shell=True"]),
        ("敏感信息泄露", ["password", "api_key", "secret", "token", "credential"]),
        ("不安全的加密", ["md5(", "sha1(", "Crypto.Cipher", "Random"]),
    ]

    SYSTEM_PROMPT = """你是一位网络安全专家，擅长发现代码中的安全漏洞和潜在风险。
请分析提供的代码，识别：
1. SQL 注入风险
2. XSS 跨站脚本攻击风险
3. 命令注入风险
4. 敏感信息泄露
5. 不安全的加密或认证
6. 其他安全漏洞

请以结构化的 JSON 格式返回分析结果。"""

    def __init__(self):
        self.name = "SecurityAgent"
        logger.info(f"{self.name} initialized")

    async def analyze(self, code: str, language: str = "python") -> Dict:
        """分析代码安全性"""
        logger.info(f"Scanning security vulnerabilities in {language} code")

        # 先用模式匹配快速检测
        quick_scan = self._quick_scan(code)

        # 使用 LLM 进行深度分析
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"请分析以下 {language} 代码的安全漏洞：\n\n```{language}\n{code}\n```",
            },
        ]

        model = llm_router.route("security_analysis")
        llm_response = await llm_router.chat(messages, model=model)

        return {
            "agent": self.name,
            "model_used": model,
            "quick_scan_results": quick_scan,
            "llm_analysis": llm_response,
            "vulnerabilities": self._parse_vulnerabilities(llm_response),
        }

    def _quick_scan(self, code: str) -> List[Dict]:
        """快速模式匹配扫描"""
        findings = []
        code_lower = code.lower()

        for vuln_name, patterns in self.VULNERABILITY_PATTERNS:
            for pattern in patterns:
                if pattern.lower() in code_lower:
                    findings.append(
                        {
                            "type": vuln_name,
                            "pattern": pattern,
                            "severity": self._get_severity(vuln_name),
                        }
                    )

        return findings

    def _get_severity(self, vuln_type: str) -> str:
        """获取漏洞严重程度"""
        severity_map = {
            "SQL注入": "high",
            "XSS攻击": "high",
            "命令注入": "critical",
            "敏感信息泄露": "medium",
            "不安全的加密": "medium",
        }
        return severity_map.get(vuln_type, "low")

    def _parse_vulnerabilities(self, response: str) -> List[Dict]:
        """解析漏洞列表"""
        vulnerabilities = []

        critical_keywords = ["critical", "严重", "high"]
        high_keywords = ["high", "高危", "sql", "injection"]

        if any(kw in response.lower() for kw in critical_keywords):
            vulnerabilities.append(
                {"level": "critical", "description": "发现严重安全漏洞"}
            )
        if any(kw in response.lower() for kw in high_keywords):
            vulnerabilities.append(
                {"level": "high", "description": "发现高危安全漏洞"}
            )

        return vulnerabilities if vulnerabilities else [{"level": "low", "description": "未发现明显安全漏洞"}]
